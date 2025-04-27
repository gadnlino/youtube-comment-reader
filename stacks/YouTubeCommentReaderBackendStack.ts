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
import { AwsCustomResource, AwsCustomResourcePolicy, PhysicalResourceId } from 'aws-cdk-lib/custom-resources';
import * as ec2 from 'aws-cdk-lib/aws-ec2';

const APP_NAME = 'YoutubeCommentReaderBackend';

export class YouTubeCommentReaderBackendStack extends Stack {
    constructor(app: App, id: string, envName: string, env: Environment) {
        super(app, id, {
            env
        });

        // Usa a VPC padrão
        // const vpc = ec2.Vpc.fromLookup(this, `${APP_NAME}-Vpc`, { isDefault: true });

        // // Cria o cluster ECS
        // const cluster = new ecs.Cluster(this, "Cluster", {
        //     vpc,
        // });

        // // Cria a imagem Docker a partir do Dockerfile local
        // const dockerImageAsset = new DockerImageAsset(this, "DockerImage", {
        //     directory: "./caminho/para/seu/projeto", // <- coloca o caminho onde está seu Dockerfile
        // });


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

        const customApiKey = generateCustomApiKey();

        const sentimentAnalysisLambdaFunctionName = `${APP_NAME}-SentimentAnalysisLambdaFunction`;

        const sentimentAnalysisLambdaFunction = new DockerImageFunction(
            this,
            sentimentAnalysisLambdaFunctionName,
            {
                functionName: sentimentAnalysisLambdaFunctionName,
                architecture: Architecture.ARM_64,
                code: DockerImageCode.fromImageAsset(join(__dirname, '..', 'packages/lambdas/sentiment_analysis'), { platform: Platform.LINUX_ARM64 }),
                memorySize: 3008,
                timeout: Duration.minutes(15),
                environment: {
                    SENTIMENT_ANALYSIS_API_KEY: customApiKey
                }
            }
        );

        const functionUrl = sentimentAnalysisLambdaFunction.addFunctionUrl({
            authType: FunctionUrlAuthType.NONE,
        });

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
                SENTIMENT_ANALYSIS_API_URL: functionUrl.url,
                SENTIMENT_ANALYSIS_API_KEY: customApiKey,
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

        new CfnOutput(this, "SentimentAnalysisLambdaFunctionUrl", {
            value: functionUrl.url || "",
        });

        youtubeApiKeySecret.grantRead(searchVideoLambdaFunction);
        youtubeApiKeySecret.grantRead(fetchVideoCommentsLambdaFunction);
        youtubeApiKeySecret.grantRead(fetchVideoCommentRepliesLambdaFunction);

        const prewarmCustomResource = new AwsCustomResource(this, "InvokeWarmUpOnDeploy", {
            onCreate: {
                service: "Lambda",
                action: "invoke",
                parameters: {
                    FunctionName: warmUpLambdaFunction.functionName,
                    InvocationType: "Event", // Async
                    Payload: JSON.stringify({
                        comments: ["prewarm_create"]
                    }),
                },
                physicalResourceId: PhysicalResourceId.of("WarmUpInvokeOnceCreate"),
            },
            onUpdate: {
                service: "Lambda",
                action: "invoke",
                parameters: {
                    FunctionName: warmUpLambdaFunction.functionName,
                    InvocationType: "Event", // Async
                    Payload: JSON.stringify({
                        comments: ["prewarm_update"]
                    }),
                },
                physicalResourceId: PhysicalResourceId.of("WarmUpInvokeOnceUpdate"),
            },
            policy: AwsCustomResourcePolicy.fromSdkCalls({
                resources: [warmUpLambdaFunction.functionArn],
            }),
        });

        warmUpLambdaFunction.grantInvoke(prewarmCustomResource);
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