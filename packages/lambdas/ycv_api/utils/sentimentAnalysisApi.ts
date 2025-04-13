import axios from 'axios';

interface SentimentAnalysisResult {
    comment: string;
    sentiment: string;
    score: number;
}

const API_KEY = process.env.SENTIMENT_ANALYSIS_API_KEY;

const sentimentAnalysisApi = {
    analyzeSentiments: async (
        comments: string[],
    ): Promise<SentimentAnalysisResult[]> => {

        try {
            const response = await axios.post(
                process.env.SENTIMENT_ANALYSIS_API_URL!,
                { comments },
                {
                    headers: {
                        'Content-Type': 'application/json',
                        'x-api-key': API_KEY,
                    },
                }
            );

            return response.data.results;
        } catch (error) {
            throw error;
        }


    }
}

export default sentimentAnalysisApi;