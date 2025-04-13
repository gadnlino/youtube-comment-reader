import { App, Environment } from 'aws-cdk-lib';
import { YouTubeCommentReaderBackendStack } from './stacks/YouTubeCommentReaderBackendStack';

const ENV_NAME = 'dev';

const environments = {
    dev: {
        account: "626536433438",
        region: "us-east-1"
    }
}

const app = new App();

new YouTubeCommentReaderBackendStack(app, 'YouTubeCommentReaderBackendStack', environments[ENV_NAME]);

app.synth();