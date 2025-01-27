class CommentsDisabledException implements Exception {
  String cause;
  CommentsDisabledException(this.cause);
}
