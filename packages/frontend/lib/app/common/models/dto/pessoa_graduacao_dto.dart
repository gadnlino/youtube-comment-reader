class PessoaGraduacaoDto {
  int? idPessoa;
  int? idGraduacao;
  String? nmGraduacao;
  String? ehSomenteInfantil;
  DateTime? dtGraduacao;
  int? idProfessor;
  String? aprovado;
  DateTime? dtAprovacao;
  String? comentario;

  PessoaGraduacaoDto(
      {this.idPessoa,
      this.idGraduacao,
      this.nmGraduacao,
      this.ehSomenteInfantil,
      this.dtGraduacao,
      this.idProfessor,
      this.aprovado,
      this.dtAprovacao,
      this.comentario});

  PessoaGraduacaoDto.fromJson(Map<String, dynamic> json) {
    idPessoa = json['id_pessoa'];
    idGraduacao = json['id_graduacao'];
    nmGraduacao = json['nm_graduacao'];
    ehSomenteInfantil = json['eh_somente_infantil'];
    dtGraduacao =
        json.containsKey('dt_graduacao') && json['dt_graduacao'] != null
            ? DateTime.parse(json['dt_graduacao'])
            : null;
    idProfessor =
        json.containsKey("id_professor") ? json['id_professor'] : null;
    aprovado = json.containsKey("aprovado") ? json['aprovado'] : null;
    dtAprovacao =
        json.containsKey('dt_aprovacao') && json['dt_aprovacao'] != null
            ? DateTime.parse(json['dt_aprovacao'])
            : null;
    comentario = json.containsKey("comentario") ? json['comentario'] : null;
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    data['id_pessoa'] = idPessoa;
    data['id_graduacao'] = idGraduacao;
    data['nm_graduacao'] = nmGraduacao;
    data['eh_somente_infantil'] = ehSomenteInfantil;
    data['id_professor'] = idProfessor;
    data['aprovado'] = aprovado;
    data['comentario'] = comentario;
    data['dt_graduacao'] = dtGraduacao?.toIso8601String();
    data['dt_aprovacao'] = dtAprovacao?.toIso8601String();

    return data;
  }
}
