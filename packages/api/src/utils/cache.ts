import { DynamoDBClient, QueryCommand } from "@aws-sdk/client-dynamodb";
import { DynamoDBDocumentClient, GetCommand, GetCommandInput, PutCommand, QueryCommandInput, unmarshallOptions } from "@aws-sdk/lib-dynamodb";
import { unmarshall, marshall } from "@aws-sdk/util-dynamodb";

// Configure o cliente DynamoDB
const ddbDocClient = DynamoDBDocumentClient.from(new DynamoDBClient({ region: process.env.AWS_REGION }));
const expirationTimeMinutes = Number(process.env.EXPIRATION_TIME_MINUTES);

const cache = {
    getItem: async (pk: string) => {
        const params: QueryCommandInput = {
            TableName: process.env.SST_Table_tableName_CacheTable,
            KeyConditionExpression: "#key = :id", // Query by the primary key
            FilterExpression: "attribute_not_exists(expireAt) OR expireAt > :currentTime", // Check TTL
            ExpressionAttributeNames: {
                "#key": "key"
            },
            ExpressionAttributeValues: {
                ":id": marshall(pk),
                ":currentTime": marshall(new Date().getTime() / 1000), // Current UNIX timestamp in seconds
            },
        };

        try {
            const result = await ddbDocClient.send(new QueryCommand(params));

            if (result.Items && result.Items.length > 0) {
                const resultObj = unmarshall(result.Items[0]);

                console.log("Item found:", resultObj);

                return resultObj;
            } else {
                console.log("No valid item found");
                return null;
            }

        } catch (err) {
            console.error("Erro ao recuperar item:", err);
            throw err;
        }
    },
    putItem: async (pk: string, data: string) => {
        const now = new Date();
        const params = {
          TableName: process.env.SST_Table_tableName_CacheTable,
          Item: {
            key: pk, // Partition Key
            expireAt: new Date(now.getTime() + expirationTimeMinutes * 60000).getTime() / 1000,
            data: data, // Dados adicionais
          },
        };
      
        try {
          const result = await ddbDocClient.send(new PutCommand(params));
          console.log("Item inserido com sucesso:", result);
        } catch (err) {
          console.error("Erro ao inserir item:", err);
          throw err;
        }
    },
}

export default cache;