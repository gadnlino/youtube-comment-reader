import 'package:flutter/material.dart';

class Midia {
  int? idMidia;
  int? idTipoMidia;
  String? urlMidia;
  String? nmArquivoMidia;
  String? pathMidia;

  Midia(
      {this.idMidia,
      this.idTipoMidia,
      this.nmArquivoMidia,
      this.pathMidia,
      this.urlMidia});

  Midia.fromJson(Map<String, dynamic> json) {
    idMidia = json.containsKey('id_midia') && json['id_midia'] != null
        ? json['id_midia']
        : null;
    idTipoMidia =
        json.containsKey('id_tipo_midia') && json['id_tipo_midia'] != null
            ? json['id_tipo_midia']
            : null;
    urlMidia = json.containsKey('url_midia') && json['url_midia'] != null
        ? json['url_midia']
        : null;
    nmArquivoMidia =
        json.containsKey('nm_arquivo_midia') && json['nm_arquivo_midia'] != null
            ? json['nm_arquivo_midia']
            : null;
    pathMidia = json.containsKey('path_midia') && json['path_midia'] != null
        ? json['path_midia']
        : null;
  }

  Map<String, dynamic> toJson() => {
        "id_midia": idMidia,
        "id_tipo_midia": idTipoMidia,
        "url_midia": urlMidia,
        "nm_arquivo_midia": nmArquivoMidia,
        "path_midia": pathMidia,
      };
}
