import 'package:frontend/app/common/models/models.dart';
import 'package:frontend/app/common/utils/favorite_manager.dart';
import 'package:get/get.dart';

class FavoritesController extends GetxController {
  final FavoriteManager _favoriteManager = FavoriteManager();

  Rx<bool> loading = Rx(false);

  final RxList<YouTubeSearchItem> _videoFavorites = RxList();
  final RxList<CommentFavorite> _commentFavorites = RxList();

  List<YouTubeSearchItem> get videoFavorites {
    (() async {
      var favorites = await _favoriteManager.getVideoFavorites();

      if (favorites != null) {
        _videoFavorites.value = favorites;
      }
    })();

    return _videoFavorites;
  }

  bool existVideoFavorite(String videoId) =>
      videoFavorites.any((v) => v.id == videoId);

  addVideoFavorite(YouTubeSearchItem video) async {
    _videoFavorites.value = [..._videoFavorites, video];

    await _favoriteManager.addVideoFavorite(video);
  }

  removeVideoFavorite(YouTubeSearchItem video) async {
    _videoFavorites.value =
        _videoFavorites.where((element) => element.id != video.id).toList();

    await _favoriteManager.removeVideoFavorite(video);
  }

  List<CommentFavorite> get commentFavorites {
    (() async {
      var favorites = await _favoriteManager.getCommentFavorites();

      if (favorites != null) {
        _commentFavorites.value = favorites;
      }
    })();

    return _commentFavorites;
  }

  bool existCommentFavorite(String commentId) =>
      commentFavorites.any((c) => c.comment?.id == commentId);

  addCommentFavorite(
      YouTubeComment comment,
      List<YouTubeComment>? replies,
      String? videoId,
      String? videoDescription,
      String? videoThumbnailUrl,
      String? videoTitle,
      String? channelTitle,
      String? videoPublishedAt) async {
    CommentFavorite favorite = CommentFavorite(
        comment: comment,
        replies: replies,
        videoId: videoId,
        videoDescription: videoDescription,
        videoThumbnailUrl: videoThumbnailUrl,
        videoTitle: videoTitle,
        channelTitle: channelTitle,
        videoPublishedAt: videoPublishedAt);

    _commentFavorites.value = [..._commentFavorites, favorite];

    await _favoriteManager.addCommentFavorite(favorite);
  }

  removeCommentFavorite(YouTubeComment comment) async {
    _commentFavorites.value = _commentFavorites
        .where((element) => element.comment?.id != comment.id)
        .toList();

    await _favoriteManager.removeCommentFavorite(comment);
  }
}
