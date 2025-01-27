class PessoaAcademiaDto {
  int? idAcademia;
  int? idEquipe;
  int? idResponsavel;
  String? nmAcademia;
  String? endereco;
  DateTime? dtInicio;
  DateTime? dtFim;
  int? idLogo;

  PessoaAcademiaDto(
      {this.idAcademia,
      this.idEquipe,
      this.idResponsavel,
      this.nmAcademia,
      this.endereco,
      this.idLogo});

  PessoaAcademiaDto.fromJson(Map<String, dynamic> json) {
    idAcademia = json['id_academia'];
    idEquipe = json['id_equipe'];
    idResponsavel = json['id_responsavel'];
    nmAcademia = json['nm_academia'];
    endereco = json['endereco'];
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
    data['id_academia'] = idAcademia;
    data['id_equipe'] = idEquipe;
    data['id_responsavel'] = idResponsavel;
    data['nm_academia'] = nmAcademia;
    data['endereco'] = endereco;
    data['id_logo'] = idLogo;
    data['dt_inicio'] = dtInicio?.toIso8601String();
    data['dt_fim'] = dtFim?.toIso8601String();

    return data;
  }
}
