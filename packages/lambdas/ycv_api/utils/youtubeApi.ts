import axios, { AxiosResponse } from 'axios';
import { YouTubeSearchItem, YouTubeSearchResponse, YouTubeComment, 
    YouTubeCommentThreadsResponse, YouTubeSearchParams, YouTubeCommentThreadsParams, CommentsListParams, CommentsListResponse } from "../types/types";
import { SecretsManagerClient, GetSecretValueCommand } from "@aws-sdk/client-secrets-manager";
import { get } from 'http';

// YouTube API endpoints
const SEARCH_API_URL = 'https://www.googleapis.com/youtube/v3/search';
const LIST_VIDEOS_API_URL = 'https://www.googleapis.com/youtube/v3/videos';
const COMMENT_THREADS_API_URL = 'https://www.googleapis.com/youtube/v3/commentThreads';
const COMMENTS_API_URL = 'https://www.googleapis.com/youtube/v3/comments';

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
    listVideos: async (part: string, videoIds: string[]): Promise<AxiosResponse<YouTubeSearchResponse, any>> => {
        const params = {
            part,
            id: videoIds.join(',')
        };
    
        console.info(`executando ${LIST_VIDEOS_API_URL}, parametros: ${JSON.stringify(params)}`);
    
        const response = await axios.get<YouTubeSearchResponse>(LIST_VIDEOS_API_URL, {
            params: {
                ...params,
                key: await getSecret(),
            },
        });
    
        return response;
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