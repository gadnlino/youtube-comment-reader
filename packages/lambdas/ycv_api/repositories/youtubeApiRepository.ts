import { YouTubeCommentThreadsParams, YouTubeCommentThreadsResponse, YouTubeSearchParams } from "../types/types";
import cache from "../utils/cache";
import youtubeApi from "../utils/youtubeApi";
import sentimentAnalysisApi from "../utils/sentimentAnalysisApi";

const cacheEnabled = process.env.CACHE_ENABLED === "true";

const addSentimentInformation = async (response: YouTubeCommentThreadsResponse): Promise<YouTubeCommentThreadsResponse> => {
    console.log('adicionando informacoes de sentimento');

    if (!response.items || response.items.length === 0) {
        return response;
    }

    const comments = response.items.map((item: any) => item.snippet.topLevelComment.snippet.textDisplay);

    const sentiments = await sentimentAnalysisApi.analyzeSentiments(comments);

    response.items.forEach((item: any, index: number) => {
        item.sentiment = sentiments[index].sentiment;
        item.score = sentiments[index].score;
    });

    return response;
}

const filterBySentiment = (response: YouTubeCommentThreadsResponse, parameters: YouTubeCommentThreadsParams): YouTubeCommentThreadsResponse => {

    console.log('filtrando comentarios');

    if (!response.items || response.items.length === 0) {
        return response;
    }

    const sentiments: string[] = [];

    if (parameters.showPositives) {
        sentiments.push('positive');
    }

    if (parameters.showNegatives) {
        sentiments.push('negative');
    }

    if (parameters.showNeutral) {
        sentiments.push('neutral');
    }

    response.items = response.items.filter((item: any) => sentiments.includes(item.sentiment));

    return response;
}

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

        const hasSentimentFilter = parameters.showNegatives || parameters.showPositives || parameters.showNeutral;

        const cacheKey = `fetchComments:part=${parameters.part}&videoId=${parameters.videoId}&searchTerms=${parameters.searchTerms}&order=${parameters.order}`;

        let cacheItem: Record<string, any> | null = null;

        if (cacheEnabled) {
            //console.log('cacheKey', cacheKey);

            cacheItem = await cache.getItem(cacheKey);
        }

        if (cacheItem) {
            // console.log('item encontrado no cache');

            // console.log(cacheItem);

            videoCommentResults = JSON.parse(cacheItem.data);

            return [200, hasSentimentFilter ? await addSentimentInformation(videoCommentResults).then(r=>filterBySentiment(r, parameters)) : videoCommentResults];
        }
        else {
            console.log('NAO foi possivel encontrar nenhum item para essa busca no cache');
        }

        const response = await youtubeApi.fetchComments(parameters);

        if (response.status === 403) {
            return [403, response.data];
        }

        let responseVideos = response.data;

        if (hasSentimentFilter) {
            responseVideos = await addSentimentInformation(responseVideos).then(r => filterBySentiment(r, parameters));
        }

        if (cacheEnabled) {
            console.log('cacheando objeto');
            await cache.putItem(cacheKey, JSON.stringify(responseVideos));
        }

        return [response.status, responseVideos];
    }
}

export default youtubeApiRepository;