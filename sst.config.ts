import { SSTConfig } from "sst";
import { ApiStack } from "./stacks/ApiStack";
import { DatabaseStack } from "./stacks/DatabaseStack";
import { SentimentAnalysisFunctionStack } from "./stacks/SentimentAnalysisFunctionStack";

export default {
  config(_input) {
    return {
      name: "youtube-comment-viewer",
      region: "us-east-1",
    };
  },
  stacks(app) {
    if (app.stage !== "prod") {
      app.setDefaultRemovalPolicy("destroy");
    }

    app
    .stack(DatabaseStack)
    .stack(ApiStack)
    .stack(SentimentAnalysisFunctionStack);
  }
} satisfies SSTConfig;
