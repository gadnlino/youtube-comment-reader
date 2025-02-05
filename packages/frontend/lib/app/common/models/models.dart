class YouTubePageInfo {
  final int totalResults; // Total number of results
  final int resultsPerPage; // Number of results per page

  YouTubePageInfo({
    required this.totalResults,
    required this.resultsPerPage,
  });

  factory YouTubePageInfo.fromJson(Map<String, dynamic> json) {
    return YouTubePageInfo(
      totalResults: json['totalResults'],
      resultsPerPage: json['resultsPerPage'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'totalResults': totalResults,
      'resultsPerPage': resultsPerPage,
    };
  }
}

class YouTubeCommentThreadsResponse {
  final String kind;
  final String etag;
  final String? nextPageToken;
  final List<YouTubeCommentThread> items;
  final YouTubePageInfo pageInfo;

  YouTubeCommentThreadsResponse({
    required this.kind,
    required this.etag,
    this.nextPageToken,
    required this.items,
    required this.pageInfo,
  });

  factory YouTubeCommentThreadsResponse.fromJson(Map<String, dynamic> json) {
    return YouTubeCommentThreadsResponse(
      kind: json['kind'],
      etag: json['etag'],
      nextPageToken: json['nextPageToken'],
      items: (json['items'] as List)
          .map((item) => YouTubeCommentThread.fromJson(item))
          .toList(),
      pageInfo: YouTubePageInfo.fromJson(json['pageInfo']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'kind': kind,
      'etag': etag,
      'nextPageToken': nextPageToken,
      'items': items.map((item) => item.toJson()).toList(),
      'pageInfo': pageInfo.toJson(),
    };
  }
}

class YouTubeCommentThread {
  final String kind;
  final String etag;
  final String id;
  final YouTubeCommentThreadSnippet snippet;
  final YouTubeCommentReplies? replies;

  YouTubeCommentThread({
    required this.kind,
    required this.etag,
    required this.id,
    required this.snippet,
    this.replies,
  });

  factory YouTubeCommentThread.fromJson(Map<String, dynamic> json) {
    return YouTubeCommentThread(
      kind: json['kind'],
      etag: json['etag'],
      id: json['id'],
      snippet: YouTubeCommentThreadSnippet.fromJson(json['snippet']),
      replies: json['replies'] != null
          ? YouTubeCommentReplies.fromJson(json['replies'])
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'kind': kind,
      'etag': etag,
      'id': id,
      'snippet': snippet.toJson(),
      'replies': replies?.toJson(),
    };
  }
}

class YouTubeCommentThreadSnippet {
  final String videoId;
  final YouTubeComment topLevelComment;
  final bool canReply;
  final int totalReplyCount;
  final bool isPublic;

  YouTubeCommentThreadSnippet({
    required this.videoId,
    required this.topLevelComment,
    required this.canReply,
    required this.totalReplyCount,
    required this.isPublic,
  });

  factory YouTubeCommentThreadSnippet.fromJson(Map<String, dynamic> json) {
    return YouTubeCommentThreadSnippet(
      videoId: json['videoId'],
      topLevelComment: YouTubeComment.fromJson(json['topLevelComment']),
      canReply: json['canReply'],
      totalReplyCount: json['totalReplyCount'],
      isPublic: json['isPublic'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'videoId': videoId,
      'topLevelComment': topLevelComment.toJson(),
      'canReply': canReply,
      'totalReplyCount': totalReplyCount,
      'isPublic': isPublic,
    };
  }
}

class YouTubeComment {
  final String kind;
  final String etag;
  final String id;
  final YouTubeCommentSnippet snippet;

  YouTubeComment({
    required this.kind,
    required this.etag,
    required this.id,
    required this.snippet,
  });

  factory YouTubeComment.fromJson(Map<String, dynamic> json) {
    return YouTubeComment(
      kind: json['kind'],
      etag: json['etag'],
      id: json['id'],
      snippet: YouTubeCommentSnippet.fromJson(json['snippet']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'kind': kind,
      'etag': etag,
      'id': id,
      'snippet': snippet.toJson(),
    };
  }
}

class YouTubeCommentSnippet {
  final String authorDisplayName;
  final String authorProfileImageUrl;
  final String? authorChannelUrl;
  final String textDisplay;
  final String textOriginal;
  final bool canRate;
  final String viewerRating;
  final int likeCount;
  final String publishedAt;
  final String updatedAt;

  YouTubeCommentSnippet({
    required this.authorDisplayName,
    required this.authorProfileImageUrl,
    this.authorChannelUrl,
    required this.textDisplay,
    required this.textOriginal,
    required this.canRate,
    required this.viewerRating,
    required this.likeCount,
    required this.publishedAt,
    required this.updatedAt,
  });

  factory YouTubeCommentSnippet.fromJson(Map<String, dynamic> json) {
    return YouTubeCommentSnippet(
      authorDisplayName: json['authorDisplayName'],
      authorProfileImageUrl: json['authorProfileImageUrl'],
      authorChannelUrl: json['authorChannelUrl'],
      textDisplay: json['textDisplay'],
      textOriginal: json['textOriginal'],
      canRate: json['canRate'],
      viewerRating: json['viewerRating'],
      likeCount: json['likeCount'],
      publishedAt: json['publishedAt'],
      updatedAt: json['updatedAt'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'authorDisplayName': authorDisplayName,
      'authorProfileImageUrl': authorProfileImageUrl,
      'authorChannelUrl': authorChannelUrl,
      'textDisplay': textDisplay,
      'textOriginal': textOriginal,
      'canRate': canRate,
      'viewerRating': viewerRating,
      'likeCount': likeCount,
      'publishedAt': publishedAt,
      'updatedAt': updatedAt,
    };
  }
}

class YouTubeCommentReplies {
  final List<YouTubeComment> comments;

  YouTubeCommentReplies({
    required this.comments,
  });

  factory YouTubeCommentReplies.fromJson(Map<String, dynamic> json) {
    return YouTubeCommentReplies(
      comments: (json['comments'] as List)
          .map((comment) => YouTubeComment.fromJson(comment))
          .toList(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'comments': comments.map((comment) => comment.toJson()).toList(),
    };
  }
}

class YouTubeSearchParams {
  String part; // Always 'snippet'
  String? type; // 'video', 'channel', or 'playlist'
  String? order; // Sorting order
  int? maxResults; // Results limit (1-50)
  String? regionCode; // Region filter
  String? q; // Query term
  DateTime? publishedAfter; // Filter by start date (ISO 8601)
  DateTime? publishedBefore; // Filter by end date (ISO 8601)
  String? pageToken; // For paginated responses

  YouTubeSearchParams({
    this.part = 'snippet',
    this.type = 'video',
    this.order,
    this.maxResults = 500,
    this.regionCode = 'BR',
    this.q,
    this.publishedAfter,
    this.publishedBefore,
    this.pageToken,
  });

  factory YouTubeSearchParams.fromJson(Map<String, dynamic> json) {
    return YouTubeSearchParams(
      part: json['part'],
      type: json['type'],
      order: json['order'],
      maxResults: json['maxResults'],
      regionCode: json['regionCode'],
      q: json['q'],
      publishedAfter: DateTime.tryParse(json['publishedAfter']),
      publishedBefore: DateTime.tryParse(json['publishedBefore']),
      pageToken: json['pageToken'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      if (part.isNotEmpty) 'part': part,
      if (type != null && type!.isNotEmpty) 'type': type,
      if (order != null && order!.isNotEmpty) 'order': order,
      if (maxResults != null) 'maxResults': maxResults,
      if (regionCode != null && regionCode!.isNotEmpty)
        'regionCode': regionCode,
      if (q != null && q!.isNotEmpty) 'q': q,
      if (publishedAfter != null)
        'publishedAfter': publishedAfter?.toIso8601String(),
      if (publishedBefore != null)
        'publishedBefore': publishedBefore?.toIso8601String(),
      if (pageToken != null && pageToken!.isNotEmpty) 'pageToken': pageToken,
    };
  }
}

class YouTubeCommentThreadsParams {
  final String part; // Required, e.g., 'snippet,replies'
  final String? videoId; // Video ID filter
  final String? channelId; // Channel ID filter
  final String? pageToken; // For paginated responses
  final int? maxResults; // Results limit (1-100)
  final String? order; // Sorting order
  final String? searchTerms; // Search filter
  final String? textFormat; // 'html' or 'plainText'

  YouTubeCommentThreadsParams({
    required this.videoId,
    this.part = 'snippet',
    this.maxResults = 500,
    this.channelId,
    this.pageToken,
    this.order,
    this.searchTerms,
    this.textFormat,
  });

  factory YouTubeCommentThreadsParams.fromJson(Map<String, dynamic> json) {
    return YouTubeCommentThreadsParams(
      part: json['part'],
      videoId: json['videoId'],
      channelId: json['channelId'],
      pageToken: json['pageToken'],
      maxResults: json['maxResults'],
      order: json['order'],
      searchTerms: json['searchTerms'],
      textFormat: json['textFormat'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      if (part.isNotEmpty) 'part': part,
      if (videoId != null && videoId!.isNotEmpty) 'videoId': videoId,
      if (channelId != null && channelId!.isNotEmpty) 'channelId': channelId,
      if (pageToken != null && pageToken!.isNotEmpty) 'pageToken': pageToken,
      if (maxResults != null && maxResults! <= 0) 'maxResults': maxResults,
      if (order != null && order!.isNotEmpty) 'order': order,
      if (searchTerms != null && searchTerms!.isNotEmpty)
        'searchTerms': searchTerms,
      if (textFormat != null && textFormat!.isNotEmpty)
        'textFormat': textFormat,
    };
  }
}

class CommentsListParams {
  final String part; // 'id' or 'snippet'
  final String parentId; // Parent comment ID
  final String? pageToken; // For paginated responses
  final int? maxResults; // Results limit (1-100)
  final String key; // API key
  final String? textFormat; // 'html' or 'plainText'

  CommentsListParams({
    required this.part,
    required this.parentId,
    this.pageToken,
    this.maxResults,
    required this.key,
    this.textFormat,
  });

  factory CommentsListParams.fromJson(Map<String, dynamic> json) {
    return CommentsListParams(
      part: json['part'],
      parentId: json['parentId'],
      pageToken: json['pageToken'],
      maxResults: json['maxResults'],
      key: json['key'],
      textFormat: json['textFormat'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'part': part,
      'parentId': parentId,
      'pageToken': pageToken,
      'maxResults': maxResults,
      'key': key,
      'textFormat': textFormat,
    };
  }
}

class YouTubeSearchResponse {
  final String
      kind; // The type of API response, e.g., "youtube#searchListResponse"
  final String etag; // ETag of the response
  final String?
      nextPageToken; // Token for retrieving the next page of results (if available)
  final String? regionCode; // The region associated with the search results
  final List<YouTubeSearchItem> items; // Array of search results
  final YouTubePageInfo pageInfo; // Object containing pagination details

  YouTubeSearchResponse({
    required this.kind,
    required this.etag,
    this.nextPageToken,
    this.regionCode,
    required this.items,
    required this.pageInfo,
  });

  factory YouTubeSearchResponse.fromJson(Map<String, dynamic> json) {
    return YouTubeSearchResponse(
      kind: json['kind'],
      etag: json['etag'],
      nextPageToken: json['nextPageToken'],
      regionCode: json['regionCode'],
      items: (json['items'] as List)
          .map((item) => YouTubeSearchItem.fromJson(item))
          .toList(),
      pageInfo: YouTubePageInfo.fromJson(json['pageInfo']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'kind': kind,
      'etag': etag,
      'nextPageToken': nextPageToken,
      'regionCode': regionCode,
      'items': items.map((item) => item.toJson()).toList(),
      'pageInfo': pageInfo.toJson(),
    };
  }
}

class YouTubeSearchItem {
  final String kind; // Resource type, e.g., "youtube#searchResult"
  final String etag; // ETag for the item
  final YouTubeSearchItemId
      id; // Contains the ID of the video, channel, or playlist
  final YouTubeSearchItemSnippet
      snippet; // Contains video metadata (title, description, etc.)

  YouTubeSearchItem({
    required this.kind,
    required this.etag,
    required this.id,
    required this.snippet,
  });

  factory YouTubeSearchItem.fromJson(Map<String, dynamic> json) {
    return YouTubeSearchItem(
      kind: json['kind'],
      etag: json['etag'],
      id: YouTubeSearchItemId.fromJson(json['id']),
      snippet: YouTubeSearchItemSnippet.fromJson(json['snippet']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'kind': kind,
      'etag': etag,
      'id': id.toJson(),
      'snippet': snippet.toJson(),
    };
  }
}

class YouTubeSearchItemId {
  final String kind; // The type of resource, e.g., "youtube#video"
  final String? videoId; // Video ID (present if the resource is a video)
  final String? channelId; // Channel ID (present if the resource is a channel)
  final String?
      playlistId; // Playlist ID (present if the resource is a playlist)

  YouTubeSearchItemId({
    required this.kind,
    this.videoId,
    this.channelId,
    this.playlistId,
  });

  factory YouTubeSearchItemId.fromJson(Map<String, dynamic> json) {
    return YouTubeSearchItemId(
      kind: json['kind'],
      videoId: json['videoId'],
      channelId: json['channelId'],
      playlistId: json['playlistId'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'kind': kind,
      if (videoId != null) 'videoId': videoId,
      if (channelId != null) 'channelId': channelId,
      if (playlistId != null) 'playlistId': playlistId,
    };
  }
}

class YouTubeSearchItemSnippet {
  final String
      publishedAt; // Date and time when the resource was published (ISO 8601 format)
  final String channelId; // ID of the channel that published the resource
  final String title; // Title of the video, channel, or playlist
  final String description; // Description of the resource
  final YouTubeThumbnails
      thumbnails; // Object containing thumbnail URLs and dimensions
  final String channelTitle; // Name of the channel that published the resource
  final String
      liveBroadcastContent; // Live broadcast state ("none", "upcoming", or "live")

  YouTubeSearchItemSnippet({
    required this.publishedAt,
    required this.channelId,
    required this.title,
    required this.description,
    required this.thumbnails,
    required this.channelTitle,
    required this.liveBroadcastContent,
  });

  factory YouTubeSearchItemSnippet.fromJson(Map<String, dynamic> json) {
    return YouTubeSearchItemSnippet(
      publishedAt: json['publishedAt'],
      channelId: json['channelId'],
      title: json['title'],
      description: json['description'],
      thumbnails: YouTubeThumbnails.fromJson(json['thumbnails']),
      channelTitle: json['channelTitle'],
      liveBroadcastContent: json['liveBroadcastContent'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'publishedAt': publishedAt,
      'channelId': channelId,
      'title': title,
      'description': description,
      'thumbnails': thumbnails.toJson(),
      'channelTitle': channelTitle,
      'liveBroadcastContent': liveBroadcastContent,
    };
  }
}

class YouTubeThumbnails {
  final YouTubeThumbnail defaultThumbnail; // Default thumbnail (smallest size)
  final YouTubeThumbnail medium; // Medium thumbnail
  final YouTubeThumbnail high; // High-resolution thumbnail

  YouTubeThumbnails({
    required this.defaultThumbnail,
    required this.medium,
    required this.high,
  });

  factory YouTubeThumbnails.fromJson(Map<String, dynamic> json) {
    return YouTubeThumbnails(
      defaultThumbnail: YouTubeThumbnail.fromJson(json['default']),
      medium: YouTubeThumbnail.fromJson(json['medium']),
      high: YouTubeThumbnail.fromJson(json['high']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'default': defaultThumbnail.toJson(),
      'medium': medium.toJson(),
      'high': high.toJson(),
    };
  }
}

class YouTubeThumbnail {
  final String url; // URL of the thumbnail
  final int width; // Width of the thumbnail in pixels
  final int height; // Height of the thumbnail in pixels

  YouTubeThumbnail({
    required this.url,
    required this.width,
    required this.height,
  });

  factory YouTubeThumbnail.fromJson(Map<String, dynamic> json) {
    return YouTubeThumbnail(
      url: json['url'],
      width: json['width'],
      height: json['height'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'url': url,
      'width': width,
      'height': height,
    };
  }
}

class CommentsListResponse {
  final String kind; // Type of response, e.g., "youtube#commentListResponse"
  final String etag; // ETag of the response
  final String?
      nextPageToken; // Token for the next page of results (if available)
  final List<Comment> items; // List of comments

  CommentsListResponse({
    required this.kind,
    required this.etag,
    this.nextPageToken,
    required this.items,
  });

  factory CommentsListResponse.fromJson(Map<String, dynamic> json) {
    return CommentsListResponse(
      kind: json['kind'],
      etag: json['etag'],
      nextPageToken: json['nextPageToken'],
      items: (json['items'] as List)
          .map((item) => Comment.fromJson(item))
          .toList(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'kind': kind,
      'etag': etag,
      if (nextPageToken != null) 'nextPageToken': nextPageToken,
      'items': items.map((item) => item.toJson()).toList(),
    };
  }
}

class Comment {
  final String kind; // e.g., "youtube#comment"
  final String etag; // ETag of the comment
  final String id; // ID of the comment
  final CommentSnippet snippet; // Snippet containing comment details

  Comment({
    required this.kind,
    required this.etag,
    required this.id,
    required this.snippet,
  });

  factory Comment.fromJson(Map<String, dynamic> json) {
    return Comment(
      kind: json['kind'],
      etag: json['etag'],
      id: json['id'],
      snippet: CommentSnippet.fromJson(json['snippet']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'kind': kind,
      'etag': etag,
      'id': id,
      'snippet': snippet.toJson(),
    };
  }
}

class CommentSnippet {
  final String authorDisplayName; // Display name of the comment author
  final String authorProfileImageUrl; // URL of the author's profile image
  final String? authorChannelUrl; // URL of the author's channel (optional)
  final String textDisplay; // Comment text in HTML format
  final String textOriginal; // Comment text in plain format
  final String? parentId; // ID of the parent comment (if it's a reply)
  final String
      publishedAt; // ISO 8601 date format for when the comment was published
  final String
      updatedAt; // ISO 8601 date format for the last update to the comment
  final int likeCount; // Number of likes for the comment

  CommentSnippet({
    required this.authorDisplayName,
    required this.authorProfileImageUrl,
    this.authorChannelUrl,
    required this.textDisplay,
    required this.textOriginal,
    this.parentId,
    required this.publishedAt,
    required this.updatedAt,
    required this.likeCount,
  });

  factory CommentSnippet.fromJson(Map<String, dynamic> json) {
    return CommentSnippet(
      authorDisplayName: json['authorDisplayName'],
      authorProfileImageUrl: json['authorProfileImageUrl'],
      authorChannelUrl: json['authorChannelUrl'],
      textDisplay: json['textDisplay'],
      textOriginal: json['textOriginal'],
      parentId: json['parentId'],
      publishedAt: json['publishedAt'],
      updatedAt: json['updatedAt'],
      likeCount: json['likeCount'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'authorDisplayName': authorDisplayName,
      'authorProfileImageUrl': authorProfileImageUrl,
      'authorChannelUrl': authorChannelUrl,
      'textDisplay': textDisplay,
      'textOriginal': textOriginal,
      'parentId': parentId,
      'publishedAt': publishedAt,
      'updatedAt': updatedAt,
      'likeCount': likeCount,
    };
  }
}

class Favorites {
  late List<YouTubeSearchItem>? videos;
  late List<({YouTubeComment comment, List<YouTubeComment> replies})>? comments;

  Favorites({this.videos, this.comments}) {
    videos = <YouTubeSearchItem>[];
    comments = <({YouTubeComment comment, List<YouTubeComment> replies})>[];
  }

  Map<String, dynamic> toJson() {
    return {
      'videos': videos?.map((e) => e.toJson()),
      'comments': comments?.map((e) => {
            'comment': e.comment.toJson(),
            'replies': e.replies.map((r) => r.toJson())
          })
    };
  }

  factory Favorites.fromJson(Map<String, dynamic> json) {
    return Favorites(
      videos: (json['videos'] as List)
          .map((item) => YouTubeSearchItem.fromJson(item))
          .toList(),
      comments: (json['comments'] as List)
          .map((item) => (
                comment: YouTubeComment.fromJson(item['comment']),
                replies: (item['replies'] as List)
                    .map((e) => YouTubeComment.fromJson(e))
                    .toList()
              ))
          .toList(),
    );
  }
}
