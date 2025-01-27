import * as sst from "sst";
import { StackContext, Api, use, Auth, Table } from "sst/constructs";


export function DatabaseStack({ stack }: StackContext) {
  // Create a DynamoDB table
  const table = new Table(stack, "CacheTable", {
    fields: {
      key: "string", // Partition key
      expireAt: "number"
    },
    primaryIndex: { partitionKey: "key" },
    timeToLiveAttribute: "expireAt"
  });

  return {table};
}