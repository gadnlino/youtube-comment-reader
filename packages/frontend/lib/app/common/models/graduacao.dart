class Graduacao {
  int? idGraduacao;
  String? nmGraduacao;
  String? ehProfessor;
  String? ehSomenteInfantil;

  Graduacao(
      {required this.idGraduacao,
      required this.nmGraduacao,
      required this.ehProfessor});

  Graduacao.fromJson(Map<String, dynamic> json) {
    idGraduacao =
        json.containsKey('id_graduacao') && json['id_graduacao'] != null
            ? json['id_graduacao']
            : null;
    nmGraduacao =
        json.containsKey('nm_graduacao') && json['nm_graduacao'] != null
            ? json['nm_graduacao']
            : null;
    ehProfessor =
        json.containsKey('eh_professor') && json['eh_professor'] != null
            ? json['eh_professor']
            : null;

    ehSomenteInfantil = json.containsKey('eh_somente_infantil') &&
            json['eh_somente_infantil'] != null
        ? json['eh_somente_infantil']
        : null;
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    data['id_graduacao'] = idGraduacao;
    data['nm_graduacao'] = nmGraduacao;
    data['eh_professor'] = ehProfessor;
    data["eh_somente_infantil"] = ehSomenteInfantil;
    return data;
  }
}
