import { SecretsManager } from "aws-sdk";

let dbSecretValue: string | undefined;

const secretsManager = new SecretsManager({ region: process.env.AWS_REGION });

export const getDbSecret = async () => {
    if (!dbSecretValue) {
        console.log("Obtendo a secret de banco de dados");

        const getSecretValueResponse = await secretsManager
            .getSecretValue({ SecretId: process.env.DB_CREDENTIALS_SECRET as string })
            .promise();

        console.log("Secret de banco de dados obtida");

        dbSecretValue = getSecretValueResponse.SecretString;
    }

    return dbSecretValue;
}
