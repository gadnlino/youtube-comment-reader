import axios from 'axios';

export interface Comment {
    id: string;
    text: string;
    videoTitle?: string | null;
}

export interface CommentAnalysisRequest {
    comments: Comment[];
    model_name?: string;
}

export interface CommentAnalysisResult {
    request?: Comment;
    text?: string;
    label?: string;
    score?: number;
    sentiment?: string;
    total_processing_time?: number;
}

const API_KEY = process.env.SENTIMENT_ANALYSIS_API_KEY;

const sentimentAnalysisApi = {
    analyzeSentiments: async (
        requests: CommentAnalysisRequest,
    ): Promise<CommentAnalysisResult[]> => {

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