import { YouTubeCommentThreadsParams, YouTubeSearchParams } from "src/types/types";
import cache from "src/utils/cache";
import { fetchComments, searchVideos } from "src/utils/youtubeApi";

const cacheEnabled = process.env.CACHE_ENABLED === "true";

const youtubeApiRepository = {
    searchVideos: async (parameters: YouTubeSearchParams) => {
        parameters.maxResults = Number(process.env.MAX_RESULTS);

        let searchVideoResults: any | null = null;

        const cacheKey = `part=${parameters.part}&regionCode=${parameters.regionCode}&type=${parameters.type}&q=${parameters.q}&pageToken=${parameters.pageToken}`;

        let cacheItem = null;

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

        const response = await searchVideos(parameters);

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

        const cacheKey = `part=${parameters.part}&videoId=${parameters.videoId}`;

        let cacheItem = null;

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

        const response = await fetchComments(parameters);

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