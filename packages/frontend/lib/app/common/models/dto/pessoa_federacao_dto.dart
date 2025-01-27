class PessoaFederacaoDto {
  int? idFederacao;
  String? nmFederacao;
  DateTime? dtInicio;
  DateTime? dtFim;
  int? idLogo;

  PessoaFederacaoDto(
      {this.idFederacao,
      this.nmFederacao,
      this.dtInicio,
      this.dtFim,
      this.idLogo});

  PessoaFederacaoDto.fromJson(Map<String, dynamic> json) {
    idFederacao = json['id_federacao'];
    nmFederacao = json['nm_federacao'];
    idLogo = json['id_logo'];
    dtInicio = json.containsKey('dt_inicio') && json['dt_inicio'] != null
        ? DateTime.parse(json['dt_inicio'])
        : null;

    dtFim = json.containsKey('dt_fim') && json['dt_fim'] != null
        ? DateTime.parse(json['dt_fim'])
        : null;
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    data['id_federacao'] = idFederacao;
    data['nm_federacao'] = nmFederacao;
    data['id_logo'] = idLogo;
    data['dt_inicio'] = dtInicio?.toIso8601String();
    data['dt_fim'] = dtFim?.toIso8601String();

    return data;
  }
}
