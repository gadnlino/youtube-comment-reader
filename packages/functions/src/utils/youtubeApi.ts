import axios, { AxiosResponse } from 'axios';
import { YouTubeSearchItem, YouTubeSearchResponse, YouTubeComment, YouTubeCommentThreadsResponse, YouTubeSearchParams, YouTubeCommentThreadsParams, CommentsListParams, CommentsListResponse } from "../types/types"

// Replace with your API Key


// YouTube API endpoints
const SEARCH_API_URL = 'https://www.googleapis.com/youtube/v3/search';
const COMMENT_THREADS_API_URL = 'https://www.googleapis.com/youtube/v3/commentThreads';
const COMMENTS_API_URL = 'https://www.googleapis.com/youtube/v3/comments';

export async function searchVideos(params: YouTubeSearchParams): Promise<AxiosResponse<YouTubeSearchResponse, any>> {

    console.info(`executando ${SEARCH_API_URL}, parametros: ${JSON.stringify(params)}`);

    const response = await axios.get<YouTubeSearchResponse>(SEARCH_API_URL, {
        params: {
            ...params,
            key: API_KEY
        },
    });

    return response;
}

export async function fetchComments(params: YouTubeCommentThreadsParams): Promise<AxiosResponse<YouTubeCommentThreadsResponse, any>> {
    console.info(`executando ${COMMENT_THREADS_API_URL}, parametros: ${JSON.stringify(params)}`);

    const response: any = await axios.get<YouTubeCommentThreadsResponse>(COMMENT_THREADS_API_URL, {
        params: {
            ...params,
            key: API_KEY,
        },
        validateStatus: status => (status >= 200 && status < 300) || status === 403
    });

    return response;
}

export async function fetchCommentReplies(params: CommentsListParams): Promise<CommentsListResponse> {
    console.info(`executando ${COMMENTS_API_URL}, parametros: ${JSON.stringify(params)}`);

    const response: any = await axios.get<CommentsListResponse>(COMMENTS_API_URL, {
        params: {
            ...params,
            key: API_KEY,
        },
    });

    return response.data;
}