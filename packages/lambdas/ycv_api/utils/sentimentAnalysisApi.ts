import axios from 'axios';

export interface SentimentAnalysisRequest{
    text: string;
    id: string;
}

export interface SentimentAnalysisResult {
    request: SentimentAnalysisRequest;
    sentiment: string;
    score: number;
}

const API_KEY = process.env.SENTIMENT_ANALYSIS_API_KEY;

const sentimentAnalysisApi = {
    analyzeSentiments: async (
        requests: SentimentAnalysisRequest[],
    ): Promise<SentimentAnalysisResult[]> => {

        try {
            const response = await axios.post(
                process.env.SENTIMENT_ANALYSIS_API_URL! + '/analyze',
                { comments: requests },
                {
                    headers: {
                        'Content-Type': 'application/json',
                        'x-api-key': API_KEY,
                    },
                }
            );

            return response.data;
        } catch (error) {
            throw error;
        }


    }
}

export default sentimentAnalysisApi;