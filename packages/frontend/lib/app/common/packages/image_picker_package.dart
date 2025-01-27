import 'package:image_picker/image_picker.dart';

class ImagePickerPackage {
  final ImagePicker _picker = ImagePicker();

  Future<String?> pickImage({ImageSource source = ImageSource.gallery}) async {
    final pickedFile = await _picker.pickImage(source: source);

    if (pickedFile == null) return null;

    return pickedFile.path;
  }
}
