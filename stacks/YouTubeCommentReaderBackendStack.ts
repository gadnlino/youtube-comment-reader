import { IResource, LambdaIntegration, MockIntegration, PassthroughBehavior, RestApi } from 'aws-cdk-lib/aws-apigateway';
import { AttributeType, Table } from 'aws-cdk-lib/aws-dynamodb';
import { Architecture, DockerImageCode, DockerImageFunction, FunctionUrlAuthType, Runtime } from 'aws-cdk-lib/aws-lambda';
import { Secret } from 'aws-cdk-lib/aws-secretsmanager';
import { App, Stack, RemovalPolicy, Duration, CfnOutput } from 'aws-cdk-lib';
import { NodejsFunction, NodejsFunctionProps } from 'aws-cdk-lib/aws-lambda-nodejs';
import { join } from 'path';
import { Platform, DockerImageAsset } from 'aws-cdk-lib/aws-ecr-assets';
import { Rule, Schedule } from 'aws-cdk-lib/aws-events';
import { LambdaFunction } from 'aws-cdk-lib/aws-events-targets';
import * as uuid from "uuid";
import * as ecs from 'aws-cdk-lib/aws-ecs';
import { randomInt } from 'crypto';
import { Environment } from 'aws-cdk-lib';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as logs from 'aws-cdk-lib/aws-logs';
import * as elbv2 from 'aws-cdk-lib/aws-elasticloadbalancingv2';
import * as cdk from 'aws-cdk-lib';

const APP_NAME = 'YoutubeCommentReaderBackend';

const CUSTOM_API_KEY = generateCustomApiKey();

class SentimentAnalysisFargateStack extends Stack {
    public readonly serviceName: string;
    public readonly clusterName: string;
    public readonly logGroupName: string;
    public readonly loadBalancerURL: string;

    constructor(app: App, id: string, env: Environment) {
        super(app, id, {
            env
        });

        // Usa a VPC padrão
        const vpc = ec2.Vpc.fromLookup(this, `${APP_NAME}-Vpc`, { isDefault: true });

        // Create a security group for the ALB
        const albSecurityGroup = new ec2.SecurityGroup(this, APP_NAME + "-ALBSecurityGroup", {
            vpc,
            allowAllOutbound: true,
        });

        // Add ingress rule to allow HTTP traffic
        albSecurityGroup.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(80), "Allow HTTP traffic");

        // Create the Application Load Balancer
        const loadBalancer = new elbv2.ApplicationLoadBalancer(this, APP_NAME + "-ALB", {
            vpc,
            internetFacing: true,
            securityGroup: albSecurityGroup,
        });

        // Add a listener to the ALB
        const listener = loadBalancer.addListener(APP_NAME + "-Listener", {
            port: 80,
            open: true,
        });

        // Cria o cluster ECS
        const cluster = new ecs.Cluster(this, "Cluster", {
            vpc,
        });

        // Cria a imagem Docker a partir do Dockerfile local
        const dockerImageAsset = new DockerImageAsset(this, APP_NAME + "-DockerImage", {
            directory: join(__dirname, '../packages/containers/sentiment_analysis'),
        });

        // Cria um grupo de logs para a task Fargate
        const logGroup = new logs.LogGroup(this, APP_NAME + "-LogGroup", {
            retention: logs.RetentionDays.ONE_WEEK, // Retain logs for 1 week
        });

        // Cria a task definition
        const taskDefinition = new ecs.FargateTaskDefinition(this, APP_NAME + "-TaskDef", {
            cpu: 512, // 0.5 vCPU
            memoryLimitMiB: 1024 * 4, // 1 GB RAM
            ephemeralStorageGiB: 50, // 50 GB of ephemeral storage
            runtimePlatform: {
                cpuArchitecture: ecs.CpuArchitecture.ARM64,
                operatingSystemFamily: ecs.OperatingSystemFamily.LINUX,
            },
        });

        // Adiciona o container com configuração de logging
        const container = taskDefinition.addContainer(APP_NAME + "-Container", {
            image: ecs.ContainerImage.fromDockerImageAsset(dockerImageAsset),
            portMappings: [{ containerPort: 8080 }], // A porta que seu app escuta
            logging: ecs.LogDriver.awsLogs({
                streamPrefix: APP_NAME, // Prefixo para os streams de log
                logGroup, // Usa o grupo de logs criado
            }),
            environment: {
                SENTIMENT_ANALYSIS_API_KEY: CUSTOM_API_KEY,
            },
        });

        const service = new ecs.FargateService(this, APP_NAME + "-Service", {
            cluster,
            taskDefinition,
            desiredCount: 1,
            assignPublicIp: true, // <- IP público para acessar diretamente
            vpcSubnets: { subnetType: ec2.SubnetType.PUBLIC },
        });

        // Attach the Fargate service to the ALB
        listener.addTargets(APP_NAME + "-ECS", {
            port: 8080, // The port your container listens on
            targets: [service],
        });
        // Grant the ALB permission to invoke the ECS service
        service.connections.allowFrom(listener, ec2.Port.tcp(8080), "Allow ALB to connect to ECS service");
        // Grant the ALB permission to connect to the ECS service
        loadBalancer.connections.allowFrom(service.connections, ec2.Port.tcp(8080), "Allow ECS service to connect to ALB");

        // Grant the ECS service permission to write logs to CloudWatch
        logGroup.grantWrite(service.taskDefinition.taskRole);

        this.serviceName = service.serviceName;
        this.clusterName = cluster.clusterName;
        this.logGroupName = logGroup.logGroupName;
        this.loadBalancerURL = 'http://' + loadBalancer.loadBalancerDnsName;

        new CfnOutput(this, APP_NAME + "-ServiceName", {
            value: this.serviceName,
            description: "The name of the Fargate service",
        });

        new CfnOutput(this, APP_NAME + "-ClusterName", {
            value: this.clusterName,
            description: "The name of the ECS cluster",
        });

        new CfnOutput(this, APP_NAME + "-LogGroupName", {
            value: this.logGroupName,
            description: "The name of the CloudWatch log group",
        });

        // Output the DNS name of the ALB
        new cdk.CfnOutput(this, APP_NAME + "-ALBDNS", {
            value: loadBalancer.loadBalancerDnsName,
            description: "The DNS name of the ALB",
        });
    }
}

export class YouTubeCommentReaderBackendStack extends Stack {
    constructor(app: App, id: string, envName: string, env: Environment) {
        super(app, id, {
            env
        });

        const tableName = `${APP_NAME}-CacheDynamoDBTable`;

        const dynamoTable = new Table(this, tableName, {
            partitionKey: {
                name: 'key',
                type: AttributeType.STRING
            },
            tableName,
            timeToLiveAttribute: 'expireAt',
            removalPolicy: envName === 'prod' ? RemovalPolicy.RETAIN : RemovalPolicy.DESTROY,
        });

        const sentimentAnalysisFargateStack = new SentimentAnalysisFargateStack(app, `${APP_NAME}-SentimentAnalysisFargateStack`, env);

        const youtubeApiKeySecretName = `${APP_NAME}-YoutubeApiKeySecret`;
        const youtubeApiKeySecret = new Secret(this, youtubeApiKeySecretName, {
            secretName: youtubeApiKeySecretName,
            removalPolicy: envName === 'prod' ? RemovalPolicy.RETAIN : RemovalPolicy.DESTROY,
        });

        const nodeJsFunctionProps: NodejsFunctionProps = {
            timeout: Duration.seconds(30),
            bundling: {
                externalModules: [
                    'aws-sdk', // Use the 'aws-sdk' available in the Lambda runtime
                ],

            },
            environment: {
                DYNAMODB_TABLE_NAME: dynamoTable.tableName,
                SENTIMENT_ANALYSIS_API_URL: sentimentAnalysisFargateStack.loadBalancerURL,
                SENTIMENT_ANALYSIS_API_KEY: CUSTOM_API_KEY,
                MAX_RESULTS: "500",
                CACHE_ENABLED: "true",
                EXPIRATION_TIME_MINUTES: "10",
                YOUTUBE_API_KEY_SECRET_NAME: youtubeApiKeySecret.secretName
            },
            runtime: Runtime.NODEJS_LATEST,
        }

        // Create a Lambda function for each of the CRUD operations
        const searchVideoLambdaFunctionName = `${APP_NAME}-searchVideos`;
        const lambdaFolder = 'packages/lambdas/ycv_api';

        const searchVideoLambdaFunction = new NodejsFunction(this, searchVideoLambdaFunctionName, {
            ...nodeJsFunctionProps,
            functionName: searchVideoLambdaFunctionName,
            entry: join(__dirname, '..', lambdaFolder, 'searchVideos.ts'),
            handler: 'main',
        });

        const fetchVideoCommentsLambdaFunctionName = `${APP_NAME}-fetchVideoComments`;

        const fetchVideoCommentsLambdaFunction = new NodejsFunction(this, fetchVideoCommentsLambdaFunctionName, {
            ...nodeJsFunctionProps,
            functionName: fetchVideoCommentsLambdaFunctionName,
            entry: join(__dirname, '..', lambdaFolder, 'fetchComments.ts'),
            handler: 'main',
            timeout: Duration.minutes(2),
        });

        const fetchVideoCommentRepliesLambdaFunctionName = `${APP_NAME}-fetchVideoCommentReplies`;

        const fetchVideoCommentRepliesLambdaFunction = new NodejsFunction(this, fetchVideoCommentRepliesLambdaFunctionName, {
            ...nodeJsFunctionProps,
            functionName: fetchVideoCommentRepliesLambdaFunctionName,
            entry: join(__dirname, '..', lambdaFolder, 'fetchCommentReplies.ts'),
            handler: 'main',
        });

        // Grant the Lambda function read access to the DynamoDB table
        dynamoTable.grantReadWriteData(searchVideoLambdaFunction);
        dynamoTable.grantReadWriteData(fetchVideoCommentsLambdaFunction);
        dynamoTable.grantReadWriteData(fetchVideoCommentRepliesLambdaFunction);

        const apiName = `${APP_NAME}-RESTAPI`;
        // Create an API Gateway resource for each of the CRUD operations
        const api = new RestApi(this, apiName, {
            restApiName: apiName
            // In case you want to manage binary types, uncomment the following
            // binaryMediaTypes: ["*/*"],
        });

        const searchVideos = api.root.addResource('search');
        searchVideos.addMethod('GET', new LambdaIntegration(searchVideoLambdaFunction));
        addCorsOptions(searchVideos);

        const videoComments = api.root.addResource('video').addResource('comments');
        videoComments.addMethod('GET', new LambdaIntegration(fetchVideoCommentsLambdaFunction));
        addCorsOptions(videoComments);

        const videoCommentReplies = searchVideos.addResource('video').addResource('comment').addResource('replies');
        videoCommentReplies.addMethod('GET', new LambdaIntegration(fetchVideoCommentRepliesLambdaFunction));
        addCorsOptions(videoCommentReplies);

        const warmUpLambdaFunctionName = `${APP_NAME}-WarmUpLambdaFunction`;

        const warmUpLambdaFunction = new NodejsFunction(this, warmUpLambdaFunctionName, {
            functionName: warmUpLambdaFunctionName,
            entry: join(__dirname, '..', 'packages/lambdas/warmup', 'warmup_lambda.ts'),
            timeout: Duration.minutes(10),
            ...nodeJsFunctionProps,
        });

        const ruleName = `${APP_NAME}-WarmUpScheduleRule`;

        // Regra que chama a Lambda a cada 5 minutos
        new Rule(this, ruleName, {
            ruleName,
            schedule: Schedule.rate(Duration.minutes(5)),
            targets: [new LambdaFunction(warmUpLambdaFunction)]
        });

        youtubeApiKeySecret.grantRead(searchVideoLambdaFunction);
        youtubeApiKeySecret.grantRead(fetchVideoCommentsLambdaFunction);
        youtubeApiKeySecret.grantRead(fetchVideoCommentRepliesLambdaFunction);
    }
}

function addCorsOptions(apiResource: IResource) {
    apiResource.addMethod('OPTIONS', new MockIntegration({
        // In case you want to use binary media types, uncomment the following line
        // contentHandling: ContentHandling.CONVERT_TO_TEXT,
        integrationResponses: [{
            statusCode: '200',
            responseParameters: {
                'method.response.header.Access-Control-Allow-Headers': "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Amz-User-Agent'",
                'method.response.header.Access-Control-Allow-Origin': "'*'",
                'method.response.header.Access-Control-Allow-Credentials': "'false'",
                'method.response.header.Access-Control-Allow-Methods': "'OPTIONS,GET,PUT,POST,DELETE'",
            },
        }],
        // In case you want to use binary media types, comment out the following line
        passthroughBehavior: PassthroughBehavior.NEVER,
        requestTemplates: {
            "application/json": "{\"statusCode\": 200}"
        },
    }), {
        methodResponses: [{
            statusCode: '200',
            responseParameters: {
                'method.response.header.Access-Control-Allow-Headers': true,
                'method.response.header.Access-Control-Allow-Methods': true,
                'method.response.header.Access-Control-Allow-Credentials': true,
                'method.response.header.Access-Control-Allow-Origin': true,
            },
        }]
    })
}

function generateCustomApiKey() {
    const t = randomInt(5, 10)

    let key = '';

    for (let i = 0; i < t; i++) {
        key += uuid.v4();
    }

    return key;
}