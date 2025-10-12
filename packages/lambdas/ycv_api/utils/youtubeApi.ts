import axios, { AxiosResponse } from 'axios';
import { YouTubeSearchResponse, 
    YouTubeCommentThreadsResponse, YouTubeSearchParams, YouTubeCommentThreadsParams, CommentsListParams, CommentsListResponse } from "../types/types";
import { SecretsManagerClient, GetSecretValueCommand } from "@aws-sdk/client-secrets-manager";

const YOUTUBE_API_URL = 'https://www.googleapis.com/youtube/v3';

// YouTube API endpoints
const SEARCH_API_URL = `${YOUTUBE_API_URL}/search`;
const LIST_VIDEOS_API_URL = `${YOUTUBE_API_URL}/videos`;
const COMMENT_THREADS_API_URL = `${YOUTUBE_API_URL}/commentThreads`;
const COMMENTS_API_URL = `${YOUTUBE_API_URL}/comments`;

let API_KEY: string| undefined;

const getSecret = async (): Promise<string | undefined> => {
    if (API_KEY) {
        return API_KEY;
    }

    const client = new SecretsManagerClient({ region: process.env.AWS_REGION }); // Replace with your AWS region

    try {
        const command = new GetSecretValueCommand({ SecretId: process.env.YOUTUBE_API_KEY_SECRET_NAME! });
        const response = await client.send(command);

        if (response.SecretString) {
            API_KEY = response.SecretString;
            return response.SecretString;
        }

    } catch (error) {
        console.error("Error retrieving secret:", error);
    }

    return undefined;
};


const youtubeApi =  {
    searchVideos : async (params: YouTubeSearchParams): Promise<AxiosResponse<YouTubeSearchResponse, any>> => {

        console.info(`executando ${SEARCH_API_URL}, parametros: ${JSON.stringify(params)}`);
    
        const response = await axios.get<YouTubeSearchResponse>(SEARCH_API_URL, {
            params: {
                ...params,
                key: await getSecret(),
            },
        });
    
        return response;
    },
    listVideos: async (params: YouTubeSearchParams): Promise<AxiosResponse<YouTubeSearchResponse, any>> => {
        console.info(`executando ${LIST_VIDEOS_API_URL}, parametros: ${JSON.stringify(params)}`);
    
        const response = await axios.get<YouTubeSearchResponse>(LIST_VIDEOS_API_URL, {
            params: {
                ...params,
                part: 'snippet',
                chart: 'mostPopular',
                key: await getSecret(),
            },
        });
    
        return response;
    },
    getVideoInformation: async (part: string, videoIds: string[]): Promise<AxiosResponse<YouTubeSearchResponse, any>> => {
        // Validate input parameters
        if (!part || part.trim() === '') {
            throw new Error('part parameter is required and cannot be empty');
        }
        
        if (!videoIds || videoIds.length === 0) {
            throw new Error('videoIds array is required and cannot be empty');
        }
        
        // Filter out any null, undefined, or empty video IDs
        const validVideoIds = videoIds.filter(id => id && id.trim() !== '');
        
        if (validVideoIds.length === 0) {
            throw new Error('No valid video IDs provided');
        }
        
        // Get API key and validate it
        const apiKey = await getSecret();
        if (!apiKey) {
            throw new Error('YouTube API key is not available');
        }
        
        const params = {
            part,
            id: validVideoIds.join(','),
        };
    
        console.info(`executando ${LIST_VIDEOS_API_URL}, parametros: ${JSON.stringify(params)}`);
    
        try {
            const response = await axios.get<YouTubeSearchResponse>(LIST_VIDEOS_API_URL, {
                params: {
                    ...params,
                    key: apiKey,
                },
            });
            
            return response;
        } catch (error: any) {
            console.error('YouTube API Error:', {
                url: LIST_VIDEOS_API_URL,
                params: params,
                status: error.response?.status,
                statusText: error.response?.statusText,
                data: error.response?.data,
                message: error.message
            });
            
            // Re-throw with more context
            throw new Error(`YouTube API request failed: ${error.response?.status} ${error.response?.statusText} - ${JSON.stringify(error.response?.data)}`);
        }
    },
    fetchComments: async (params: YouTubeCommentThreadsParams): Promise<AxiosResponse<YouTubeCommentThreadsResponse, any>> => {
        console.info(`executando ${COMMENT_THREADS_API_URL}, parametros: ${JSON.stringify(params)}`);
    
        const response: any = await axios.get<YouTubeCommentThreadsResponse>(COMMENT_THREADS_API_URL, {
            params: {
                ...params,
                key: await getSecret(),
            },
            validateStatus: status => (status >= 200 && status < 300) || status === 403
        });
    
        return response;
    },
    fetchCommentReplies: async (params: CommentsListParams): Promise<CommentsListResponse> => {
        console.info(`executando ${COMMENTS_API_URL}, parametros: ${JSON.stringify(params)}`);
    
        const response: any = await axios.get<CommentsListResponse>(COMMENTS_API_URL, {
            params: {
                ...params,
                key: await getSecret(),
            },
        });
    
        return response.data;
    }
};

export default youtubeApi;