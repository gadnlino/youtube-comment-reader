import { YouTubeCommentThreadsParams, YouTubeSearchParams } from "../types/types";
import cache from "../utils/cache";
import youtubeApi from "../utils/youtubeApi";

const cacheEnabled = process.env.CACHE_ENABLED === "true";

const youtubeApiRepository = {
    listVideos: async (part: string, videoIds: string[]) => {

        videoIds.sort();

        let searchVideoResults: any | null = null;

        const cacheKey = `listVideos:part=${part}&videoIds=${videoIds.join(',')}`;

        let cacheItem: Record<string, any> | null = null;

        if (cacheEnabled) {
            console.log('cacheKey', cacheKey);

            cacheItem = await cache.getItem(cacheKey);
        }

        if (cacheItem) {
            console.log('item encontrado no cache');

            console.log(cacheItem);

            searchVideoResults = JSON.parse(cacheItem.data);

            return [200, searchVideoResults];
        }
        else {
            console.log('NAO foi possivel encontrar nenhum item para essa busca no cache');
        }

        const response = await youtubeApi.listVideos(part, videoIds);

        if (response.status < 200 || response.status > 299)
            return [response.status, response.data];

        searchVideoResults = response.data;

        if (cacheEnabled) {
            await cache.putItem(cacheKey, JSON.stringify(searchVideoResults));
        }

        return [200, searchVideoResults];
    },

    searchVideos: async (parameters: YouTubeSearchParams) => {
        parameters.maxResults = Number(process.env.MAX_RESULTS);

        let searchVideoResults: any | null = null;

        const cacheKey = `searchVideos:part=${parameters.part}&regionCode=${parameters.regionCode}&type=${parameters.type}&q=${parameters.q}&pageToken=${parameters.pageToken}`;

        let cacheItem: Record<string, any> | null = null;

        if (cacheEnabled) {
            console.log('cacheKey', cacheKey);

            cacheItem = await cache.getItem(cacheKey);
        }

        if (cacheItem) {
            console.log('item encontrado no cache');

            console.log(cacheItem);

            searchVideoResults = JSON.parse(cacheItem.data);

            return [200, searchVideoResults];
        }
        else {
            console.log('NAO foi possivel encontrar nenhum item para essa busca no cache');
        }

        const response = await youtubeApi.searchVideos(parameters);

        if (response.status < 200 || response.status > 299)
            return [response.status, response.data];

        searchVideoResults = response.data;

        if (cacheEnabled) {
            await cache.putItem(cacheKey, JSON.stringify(searchVideoResults));
        }

        return [200, searchVideoResults];
    },

    fetchComments: async (parameters: YouTubeCommentThreadsParams) => {
        parameters.maxResults = Number(process.env.MAX_RESULTS);

        let videoCommentResults: any | null = null;

        const cacheKey = `fetchComments:part=${parameters.part}&videoId=${parameters.videoId}&searchTerms=${parameters.searchTerms}&order=${parameters.order}`;

        let cacheItem: Record<string, any> | null = null;

        if (cacheEnabled) {
            console.log('cacheKey', cacheKey);

            cacheItem = await cache.getItem(cacheKey);
        }

        if (cacheItem) {
            console.log('item encontrado no cache');

            console.log(cacheItem);

            videoCommentResults = JSON.parse(cacheItem.data);

            return [200, videoCommentResults];
        }
        else {
            console.log('NAO foi possivel encontrar nenhum item para essa busca no cache');
        }

        const response = await youtubeApi.fetchComments(parameters);

        if (response.status === 403) {
            return [403, response.data];
        }

        if (cacheEnabled) {
            console.log('cacheando objeto');
            await cache.putItem(cacheKey, JSON.stringify(response.data));
        }

        return [response.status, response.data];
    }
}

export default youtubeApiRepository;