import 'package:frontend/app/common/models/models.dart';
import 'package:frontend/app/common/utils/favorite_manager.dart';
import 'package:get/get.dart';

class FavoritesPageController extends GetxController {
  final FavoriteManager _favoriteManager = FavoriteManager();

  Rx<bool> loading = Rx(false);

  RxList<YouTubeSearchItem> videoFavorites = RxList();
  RxList<CommentFavorite> commentFavorites = RxList();

  @override
  void onInit() {
    (() async {
      try {
        loading.value = true;
        await loadVideoFavorites();
        await loadCommentFavorites();
      } finally {
        loading.value = false;
      }
    })();

    super.onInit();
  }

  loadVideoFavorites() async {
    var favorites = await _favoriteManager.getVideoFavorites();

    if (favorites != null) {
      videoFavorites.value = favorites;
    }
  }

  addVideoFavorite(YouTubeSearchItem video) async {
    videoFavorites.add(video);

    await _favoriteManager.addVideoFavorite(video);
  }

  removeVideoFavorite(YouTubeSearchItem video) async {
    videoFavorites.value =
        videoFavorites.where((element) => element.id != video.id).toList();

    await _favoriteManager.removeVideoFavorite(video);
  }

  loadCommentFavorites() async {
    var favorites = await _favoriteManager.getCommentFavorites();

    if (favorites != null) {
      commentFavorites.value = favorites;
    }
  }

  addCommentFavorite(
      YouTubeComment comment, List<YouTubeComment>? replies) async {
    CommentFavorite favorite = CommentFavorite(
      comment: comment,
      replies: replies,
    );

    commentFavorites.add(favorite);

    await _favoriteManager.addCommentFavorite(favorite);
  }

  removeCommentFavorite(YouTubeComment comment) async {
    commentFavorites.value = commentFavorites
        .where((element) => element.comment?.id != comment.id)
        .toList();

    await _favoriteManager.removeCommentFavorite(comment);
  }
}
