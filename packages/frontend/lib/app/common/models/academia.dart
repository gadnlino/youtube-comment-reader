class Academia {
  int? idAcademia;
  int? idEquipe;
  int? idResponsavel;
  late String nmAcademia;
  String? endereco;
  int? idLogo;

  Academia(
      {this.idAcademia,
      this.idEquipe,
      this.idResponsavel,
      required this.nmAcademia,
      this.endereco,
      this.idLogo});

  Academia.fromJson(Map<String, dynamic> json) {
    idAcademia = json['id_academia'];
    idEquipe = json['id_equipe'];
    idResponsavel = json['id_responsavel'];
    nmAcademia = json['nm_academia'];
    endereco = json['endereco'];
    idLogo = json['id_logo'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    data['id_academia'] = idAcademia;
    data['id_equipe'] = idEquipe;
    data['id_responsavel'] = idResponsavel;
    data['nm_academia'] = nmAcademia;
    data['endereco'] = endereco;
    data['id_logo'] = idLogo;
    return data;
  }
}
