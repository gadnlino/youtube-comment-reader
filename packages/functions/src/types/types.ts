export interface YouTubeSearchItem {
    kind: string; // Resource type, e.g., "youtube#searchResult"
    etag: string; // ETag for the item
    id: YouTubeSearchItemId; // Contains the ID of the video, channel, or playlist
    snippet: YouTubeSearchItemSnippet; // Contains video metadata (title, description, etc.)
}

export interface YouTubeSearchItemId {
    kind: string; // The type of resource, e.g., "youtube#video"
    videoId?: string; // Video ID (present if the resource is a video)
    channelId?: string; // Channel ID (present if the resource is a channel)
    playlistId?: string; // Playlist ID (present if the resource is a playlist)
}

export interface YouTubeSearchItemSnippet {
    publishedAt: string; // Date and time when the resource was published (ISO 8601 format)
    channelId: string; // ID of the channel that published the resource
    title: string; // Title of the video, channel, or playlist
    description: string; // Description of the resource
    thumbnails: YouTubeThumbnails; // Object containing thumbnail URLs and dimensions
    channelTitle: string; // Name of the channel that published the resource
    liveBroadcastContent: string; // Live broadcast state ("none", "upcoming", or "live")
}

export interface YouTubeThumbnails {
    default: YouTubeThumbnail; // Default thumbnail (smallest size)
    medium: YouTubeThumbnail; // Medium thumbnail
    high: YouTubeThumbnail; // High-resolution thumbnail
}

export interface YouTubeThumbnail {
    url: string; // URL of the thumbnail
    width: number; // Width of the thumbnail in pixels
    height: number; // Height of the thumbnail in pixels
}

export interface YouTubeSearchResponse {
    kind: string; // The type of API response, e.g., "youtube#searchListResponse"
    etag: string; // ETag of the response
    nextPageToken?: string; // Token for retrieving the next page of results (if available)
    regionCode?: string; // The region associated with the search results
    items: YouTubeSearchItem[]; // Array of search results
    pageInfo: YouTubePageInfo; // Object containing pagination details
}

// Pagination information for the search results
export interface YouTubePageInfo {
    totalResults: number;
    resultsPerPage: number;
}

// The response from the commentThreads endpoint
export interface YouTubeCommentThreadsResponse {
    kind: string; // e.g., "youtube#commentThreadListResponse"
    etag: string;
    nextPageToken: string | null;
    items: YouTubeCommentThread[];
    pageInfo: YouTubePageInfo;
}

// A single comment thread (may include replies)
export interface YouTubeCommentThread {
    kind: string; // e.g., "youtube#commentThread"
    etag: string;
    id: string; // The ID of the comment thread
    snippet: YouTubeCommentThreadSnippet;
    replies?: YouTubeCommentReplies; // Replies to the comment
}

// The snippet of the comment thread
export interface YouTubeCommentThreadSnippet {
    videoId: string; // The video ID for the video containing the comments
    topLevelComment: YouTubeComment; // The top-level (original) comment
    canReply: boolean; // Whether replies are allowed
    totalReplyCount: number; // The number of replies to the top-level comment
    isPublic: boolean; // Whether the comment is public
}

// A single comment
export interface YouTubeComment {
    kind: string; // e.g., "youtube#comment"
    etag: string;
    id: string; // The ID of the comment
    snippet: YouTubeCommentSnippet;
}

// The snippet of the comment
export interface YouTubeCommentSnippet {
    authorDisplayName: string; // The display name of the comment author
    authorProfileImageUrl: string; // URL of the author's profile image
    authorChannelUrl: string; // URL of the author's channel
    authorChannelId: {
        value: string; // The channel ID of the author
    };
    textDisplay: string; // The comment text (HTML formatted)
    textOriginal: string; // The raw comment text
    canRate: boolean; // Whether the current user can rate the comment
    viewerRating: 'none' | 'like' | 'dislike'; // The current viewer's rating of the comment
    likeCount: number; // The number of likes on the comment
    publishedAt: string; // ISO 8601 date format (when the comment was published)
    updatedAt: string; // ISO 8601 date format (when the comment was last updated)
}

// Replies to the comment (if available)
export interface YouTubeCommentReplies {
    comments: YouTubeComment[]; // Array of replies to the top-level comment
}

export interface YouTubeSearchParams {
    /**
     * Specifies which part of the resource to include in the response.
     * For `search.list`, the value must be `snippet`.
     */
    part: 'snippet';

    /**
     * Restricts the results to a specific type of resource.
     * Common values: 'video', 'channel', or 'playlist'.
     */
    type?: 'video' | 'channel' | 'playlist';

    /**
     * Specifies the order in which results should be returned.
     * Options:
     * - 'date' for newest first
     * - 'rating' for highest rated
     * - 'relevance' (default) for most relevant
     * - 'title' for alphabetical
     * - 'videoCount' for highest video count
     * - 'viewCount' for most viewed
     */
    order?: 'date' | 'rating' | 'relevance' | 'title' | 'videoCount' | 'viewCount';

    /**
     * Limits the number of results returned in a single request.
     * Must be an integer between 1 and 50. Default is 5.
     */
    maxResults?: number;

    /**
     * Restricts results to videos from a specific region.
     * Use a two-letter ISO 3166-1 alpha-2 country code (e.g., 'US', 'BR').
     */
    regionCode?: string;

    /**
     * Specifies a query term to search for.
     * Leave undefined or empty for broad searches.
     */
    q?: string;

    /**
     * Filters results to include only resources published after a specific date.
     * Use ISO 8601 format (e.g., '2024-01-01T00:00:00Z').
     */
    publishedAfter?: string;

    /**
     * Filters results to include only resources published before a specific date.
     * Use ISO 8601 format (e.g., '2024-01-01T00:00:00Z').
     */
    publishedBefore?: string;

    /**
     * Token to retrieve the next page of results in paginated requests.
     */
    pageToken?: string;

    /**
     * Your API key for authenticating the request.
     */
    key: string;
}

export interface YouTubeCommentThreadsParams {
    /**
     * Specifies which part of the resource to include in the response.
     * Options:
     * - 'id': Only includes the thread ID.
     * - 'snippet': Includes the top-level comment and basic metadata.
     * - 'replies': Includes replies to the top-level comment.
     * Multiple values can be combined with commas (e.g., 'snippet,replies').
     */
    part: 'id' | 'snippet' | 'replies' | 'snippet,replies';

    /**
     * Specifies the ID of the video for which to retrieve comments.
     * Either `videoId` or `channelId` must be provided.
     */
    videoId?: string;

    /**
     * Specifies the ID of the channel for which to retrieve comment threads.
     * Either `channelId` or `videoId` must be provided.
     */
    channelId?: string;

    /**
     * Token to retrieve the next page of results in a paginated response.
     */
    pageToken?: string;

    /**
     * Limits the number of results returned in a single request.
     * Must be an integer between 1 and 100. Default is 20.
     */
    maxResults?: number;

    /**
     * Specifies the order of the comments in the response.
     * Options:
     * - 'time': Newest comments first.
     * - 'relevance': Most relevant comments first.
     */
    order?: 'time' | 'relevance';

    /**
     * Filters results to include only comments containing the specified search term.
     */
    searchTerms?: string;

    /**
     * Your API key for authenticating the request.
     */
    key: string;

    /**
     * Indicates whether the API should return comments with ratings.
     * This parameter is currently ignored by the API.
     */
    textFormat?: 'html' | 'plainText';
}

export interface CommentThreadsListResponse {
    kind: 'youtube#commentThreadListResponse';
    etag: string;
    nextPageToken?: string;
    items: CommentThread[];
}

export interface CommentThread {
    kind: 'youtube#commentThread';
    etag: string;
    id: string;
    snippet: CommentThreadSnippet;
    replies?: {
        comments: Comment[];
    };
}

export interface CommentThreadSnippet {
    videoId: string;
    topLevelComment: Comment;
    canReply: boolean;
    totalReplyCount: number;
    isPublic: boolean;
}

export interface Comment {
    kind: 'youtube#comment';
    etag: string;
    id: string;
    snippet: CommentSnippet;
}

export interface CommentSnippet {
    authorDisplayName: string;
    authorProfileImageUrl: string;
    authorChannelUrl?: string;
    textDisplay: string;
    textOriginal: string;
    parentId?: string;
    publishedAt: string;
    updatedAt: string;
    likeCount: number;
}

export interface CommentsListParams {
    /**
     * Specifies which parts of the resource to include in the response.
     * Options: 'id', 'snippet'.
     */
    part: 'id' | 'snippet';

    /**
     * ID of the parent comment for which to retrieve replies.
     */
    parentId: string;

    /**
     * Token to retrieve the next page of results in a paginated response.
     */
    pageToken?: string;

    /**
     * Maximum number of replies to return (1–100).
     * Default: 20.
     */
    maxResults?: number;

    /**
     * Your API key for authentication.
     */
    key: string;

    /**
     * Specifies whether the API should return replies in HTML or plain text format.
     */
    textFormat?: 'html' | 'plainText';
}

export interface CommentsListResponse {
    kind: 'youtube#commentListResponse';
    etag: string;
    nextPageToken?: string;
    items: Comment[];
}
