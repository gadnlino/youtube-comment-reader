import 'package:frontend/app/common/models/dto/pessoa_federacao_dto.dart';

class Federacao {
  late int idFederacao;
  late String nmFederacao;
  late int? idLogo;

  Federacao({
    required this.idFederacao,
    required this.nmFederacao,
    required this.idLogo,
  });

  static String nomeExibicaoFederacao(Federacao federacao) {
    return federacao.nmFederacao.split('-').last.trim().toUpperCase();
  }

  static String siglaFederacao(Federacao federacao) {
    return federacao.nmFederacao.split('-').first.trim().toUpperCase();
  }

  Federacao.fromJson(Map<String, dynamic> json) {
    idFederacao = json['id_federacao'];
    nmFederacao = json['nm_federacao'];
    idLogo = json['id_logo'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    data['id_federacao'] = idFederacao;
    data['nm_federacao'] = nmFederacao;
    data['id_logo'] = idLogo;
    return data;
  }

  Federacao.fromDto(PessoaFederacaoDto dto) {
    idFederacao = dto.idFederacao!;
    nmFederacao = dto.nmFederacao!;
    idLogo = dto.idLogo!;
  }
}
