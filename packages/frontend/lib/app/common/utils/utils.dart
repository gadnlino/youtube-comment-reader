import 'package:intl/intl.dart';

class Utils {
  static String getNameInitials(String name) {
    return name.split(' ').map((e) => e.toUpperCase()[0]).take(2).join();
  }

  static String? formatDateOrNull(DateTime? dt, String format) {
    if (dt == null) {
      return null;
    }

    return DateFormat(format).format(dt);
  }
}
