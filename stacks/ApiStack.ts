import { StackContext, Api, use, Auth } from "sst/constructs";
import { DatabaseStack } from "./DatabaseStack";

export function ApiStack({ stack }: StackContext) {
    const { table } = use(DatabaseStack);

    // Create the HTTP API
    const api = new Api(stack, "Api-" + process.env.SST_STAGE, {
        defaults: {
            function: {
                // Bind the table name to our API
                bind: [table],
                permissions: ["secretsmanager", "dynamodb"],
                environment: {
                    "MAX_RESULTS": "500",
                    "EXPIRATION_TIME_MINUTES": "5"
                }
            },
        },
        routes: {
            "GET /search": {
                function: {
                    environment:{
                        CACHE_ENABLED: "true"
                    },
                    functionName: "lbd-ycv-search-videos-" + process.env.SST_STAGE,
                    handler: "packages/functions/src/searchVideos.main"
                },

            },
            "GET /video/comments": {
                function: {
                    functionName: "lbd-ycv-fetch-video-comments-" + process.env.SST_STAGE,
                    handler: "packages/functions/src/fetchComments.main"
                },

            },
            "GET /video/comment/replies": {
                function: {
                    functionName: "lbd-ycv-fetch-video-comment-replies-" + process.env.SST_STAGE,
                    handler: "packages/functions/src/fetchCommentReplies.main"
                },
            },
        },
    });

    // Show the URLs in the output
    stack.addOutputs({
        ApiEndpoint: api.url,
    });

    return { api };
}