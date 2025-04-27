import { YouTubeCommentThread, YouTubeCommentThreadsParams, YouTubeCommentThreadsResponse, YouTubeSearchParams } from "../types/types";
import cache from "../utils/cache";
import youtubeApi from "../utils/youtubeApi";
import sentimentAnalysisApi, { SentimentAnalysisRequest, SentimentAnalysisResult } from "../utils/sentimentAnalysisApi";
import pLimit from "p-limit";

const cacheEnabled = process.env.CACHE_ENABLED === "true";
const FETCH_SENTIMENT_BATCH_SIZE = 10;
const maxParallelRequests = 5;

function batchify(list: any[], batchSize: number) {
    const batches: any[] = [];
    for (let i = 0; i < list.length; i += batchSize) {
        batches.push(list.slice(i, i + batchSize));
    }
    return batches;
}

const addSentimentInformation = async (response: YouTubeCommentThreadsResponse): Promise<YouTubeCommentThreadsResponse> => {
    console.log('adicionando informacoes de sentimento');

    if (!response.items || response.items.length === 0) {
        return response;
    }

    const comments: SentimentAnalysisRequest[] = response.items.map((item: YouTubeCommentThread) => ({ text: item.snippet.topLevelComment.snippet.textDisplay, id: item.id }));

    const batches = batchify(comments, FETCH_SENTIMENT_BATCH_SIZE); // Dividindo em lotes de 10

    const limit = pLimit(maxParallelRequests);

    const analysisPromises = batches.map(batch => limit(async () => {
        return await sentimentAnalysisApi.analyzeSentiments(batch);
    }));

    const responses = await Promise.all(analysisPromises);

    const allResults = responses.flatMap(res => res);

    response.items.forEach((item: any, index: number) => {
        const sentiment: SentimentAnalysisResult | undefined = allResults.find((result: any) => result.request.id === item.id);

        item.sentiment = sentiment?.sentiment;
        item.score = sentiment?.score;
    });

    return response;
}

const filterBySentiment = (response: YouTubeCommentThreadsResponse, parameters: any): YouTubeCommentThreadsResponse => {

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

    console.log('filtrando comentarios com sentimento', sentiments, parameters);

    const filteredComments = response.items.filter((item: any) => sentiments.includes(item.sentiment));

    console.log('filteredComments', filteredComments.map((item: any) => ({ textDisplay: item.snippet.topLevelComment.snippet.textDisplay, sentiment: item.sentiment })));

    response.items = filteredComments;

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

        const showPositives = parameters.showPositives && String(parameters.showPositives) === 'true';
        const showNegatives = parameters.showNegatives && String(parameters.showNegatives) === 'true';
        const showNeutral = parameters.showNeutral && String(parameters.showNeutral) === 'true';

        console.log('sentimentFilters', { showPositives, showNegatives, showNeutral });

        const hasSentimentFilter = showPositives || showNegatives || showNeutral;

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

            return [200, hasSentimentFilter ? await addSentimentInformation(videoCommentResults).then(r => filterBySentiment(r, { showPositives, showNegatives, showNeutral })) : videoCommentResults];
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
            responseVideos = await addSentimentInformation(responseVideos).then(r => filterBySentiment(r, { showPositives, showNegatives, showNeutral }));
        }

        if (cacheEnabled) {
            console.log('cacheando objeto');
            await cache.putItem(cacheKey, JSON.stringify(responseVideos));
        }

        return [response.status, responseVideos];
    }
}

export default youtubeApiRepository;