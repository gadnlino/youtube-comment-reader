import { IResource, LambdaIntegration, MockIntegration, PassthroughBehavior, RestApi } from 'aws-cdk-lib/aws-apigateway';
import { AttributeType, Table } from 'aws-cdk-lib/aws-dynamodb';
import { Runtime, Function, Code, Handler } from 'aws-cdk-lib/aws-lambda';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import { Secret } from 'aws-cdk-lib/aws-secretsmanager';
import { App, Stack, RemovalPolicy, Duration, CfnOutput } from 'aws-cdk-lib';
import { NodejsFunction, NodejsFunctionProps } from 'aws-cdk-lib/aws-lambda-nodejs';
import { join } from 'path';
import { Rule, Schedule } from 'aws-cdk-lib/aws-events';
import { LambdaFunction } from 'aws-cdk-lib/aws-events-targets';
import * as ecr from 'aws-cdk-lib/aws-ecr';
import * as uuid from "uuid";
import { randomInt } from 'crypto';
import { Environment } from 'aws-cdk-lib';

const APP_NAME = 'YoutubeCommentReaderBackend';

const CUSTOM_API_KEY = generateCustomApiKey();


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


        const youtubeApiKeySecretName = `${APP_NAME}-YoutubeApiKeySecret`;
        const youtubeApiKeySecret = new Secret(this, youtubeApiKeySecretName, {
            secretName: youtubeApiKeySecretName,
            removalPolicy: envName === 'prod' ? RemovalPolicy.RETAIN : RemovalPolicy.DESTROY,
        });

        // Reference existing ECR repository for sentiment analysis Lambda
        // The repository should be created manually or imported
        const ecrRepoName = `${APP_NAME.toLowerCase()}-sentiment-analysis`;
        const sentimentAnalysisEcrRepo = ecr.Repository.fromRepositoryName(
            this, 
            'SentimentAnalysisEcrRepo', 
            ecrRepoName
        );

        // Create Python Lambda function for sentiment analysis
        // NOTE: You must manually build and push the Docker image to ECR first:
        // 1. aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
        // 2. cd packages/lambdas/sentiment_analysis
        // 3. docker build --no-cache -t sentiment-analysis:latest .
        // 4. docker tag sentiment-analysis:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/<repo-name>:latest
        // 5. docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/<repo-name>:latest
        // 
        // To update: Change the IMAGE_DIGEST below to the new image digest after pushing
        const IMAGE_DIGEST = process.env.IMAGE_DIGEST || 'sha256:e1ed578a7fa46a0c2d345e077577623f5e02e49c3e178b9a2d0db8d1680d144d';
        
        const sentimentAnalysisLambdaFunctionName = `${APP_NAME}-sentimentAnalysis-v2`;
        const sentimentAnalysisLambdaFunction = new Function(this, sentimentAnalysisLambdaFunctionName, {
            functionName: sentimentAnalysisLambdaFunctionName,
            code: Code.fromEcrImage(sentimentAnalysisEcrRepo, {
                tagOrDigest: IMAGE_DIGEST
            }),
            handler: Handler.FROM_IMAGE,
            runtime: Runtime.FROM_IMAGE,
            timeout: Duration.minutes(2),
            memorySize: 1024, // Increased memory for ML workloads
            environment: {
                SENTIMENT_ANALYSIS_API_KEY: CUSTOM_API_KEY,
            },
        });

        // Add Lambda Function URL for direct HTTP access
        const sentimentAnalysisFunctionUrl = sentimentAnalysisLambdaFunction.addFunctionUrl({
            authType: lambda.FunctionUrlAuthType.NONE, // No authentication for simplicity
        });

        const apiName = `${APP_NAME}-RESTAPI`;
        // Create an API Gateway resource for each of the CRUD operations
        const api = new RestApi(this, apiName, {
            restApiName: apiName
            // In case you want to manage binary types, uncomment the following
            // binaryMediaTypes: ["*/*"],
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
                SENTIMENT_ANALYSIS_API_URL: sentimentAnalysisFunctionUrl.url,
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

        const listVideosLambdaFunctionName = `${APP_NAME}-listVideos`;
        const listVideosLambdaFunction = new NodejsFunction(this, listVideosLambdaFunctionName, {
            ...nodeJsFunctionProps,
            functionName: listVideosLambdaFunctionName,
            entry: join(__dirname, '..', lambdaFolder, 'listVideos.ts'),
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

        const listVideos = api.root.addResource('videos');
        listVideos.addMethod('GET', new LambdaIntegration(listVideosLambdaFunction));
        addCorsOptions(listVideos);

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

        // Output the Lambda Function URL for sentiment analysis
        new CfnOutput(this, 'SentimentAnalysisFunctionUrl', {
            value: sentimentAnalysisFunctionUrl.url,
            description: 'The URL of the sentiment analysis Lambda function',
        });

        // Output the ECR repository URI
        new CfnOutput(this, 'SentimentAnalysisEcrRepositoryUri', {
            value: sentimentAnalysisEcrRepo.repositoryUri,
            description: 'ECR repository URI for sentiment analysis Docker image',
        });
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