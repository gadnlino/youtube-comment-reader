import { StackContext, Function } from "sst/constructs";

export function SentimentAnalysisFunctionStack({ stack }: StackContext) {
  const analyzeSentiment = new Function(stack, "analyze-sentiment-function-" + process.env.SST_STAGE, {
    runtime: "python3.12",
    handler: "packages/functions/sentiment_analysis/main.lambda_handler",
    timeout: 60,
    memorySize: 1024,
    url: {
        authorizer: "none",
    },
    // copyFiles:[{from: "packages/functions/sentiment_analysis", to:"."}],
    // environment: {
    //   EXPECTED_KEY: "chave-super-secreta", // defina como quiser
    // },
    python: {
        noDocker: true,
        // installCommands: [
        //     "pip install -r packages/functions/sentiment_analysis/requirements.txt -t packages/functions/sentiment_analysis"
        // ]
    }
    },
  );

  stack.addOutputs({
    SentimentURL: analyzeSentiment.url!,
  });
}