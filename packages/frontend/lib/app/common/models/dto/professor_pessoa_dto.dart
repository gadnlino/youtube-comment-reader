class ProfessorPessoaDto {
  late int? idProfessorPessoa;
  late int? idPessoa;
  late String? nome;
  late int? idFoto;
  late int? idAcademia;
  late int? idEquipe;
  late int? idResponsavel;
  late String? nmAcademia;
  late String? endereco;
  late int? idLogo;
  late DateTime? dtInicio;
  late DateTime? dtFim;
  late String? ehProfessor;

  ProfessorPessoaDto(
      {this.idPessoa,
      this.nome,
      this.idFoto,
      this.idAcademia,
      this.idEquipe,
      this.idResponsavel,
      this.nmAcademia,
      this.endereco,
      this.idLogo});

  ProfessorPessoaDto.fromJson(Map<String, dynamic> json) {
    idProfessorPessoa = json.containsKey("id_professor_pessoa") &&
            json['id_professor_pessoa'] != null
        ? json['id_professor_pessoa']
        : null;
    idPessoa = json.containsKey("id_pessoa") && json['id_pessoa'] != null
        ? json['id_pessoa']
        : null;
    nome =
        json.containsKey("nome") && json['nome'] != null ? json['nome'] : null;
    idFoto = json.containsKey("idFoto") && json['idFoto'] != null
        ? json['idFoto']
        : null;
    idAcademia = json.containsKey('id_academia') && json['id_academia'] != null
        ? json['id_academia']
        : null;
    idEquipe = json.containsKey('id_equipe') && json['id_equipe'] != null
        ? json['id_equipe']
        : null;
    idResponsavel =
        json.containsKey('id_responsavel') && json['id_responsavel'] != null
            ? json['id_responsavel']
            : null;
    nmAcademia = json.containsKey('nm_academia') && json['nm_academia'] != null
        ? json['nm_academia']
        : null;
    endereco = json.containsKey('endereco') && json['endereco'] != null
        ? json['endereco']
        : null;
    idLogo = json.containsKey('id_logo') && json['id_logo'] != null
        ? json['id_logo']
        : null;
    dtInicio = (json.containsKey('dt_inicio') && json['dt_inicio'] != null
        ? DateTime.parse(json['dt_inicio'])
        : null);

    dtFim = (json.containsKey('dt_fim') && json['dt_fim'] != null
        ? DateTime.parse(json['dt_fim'])
        : null);
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    data['id_professor_pessoa'] = idProfessorPessoa;
    data['id_pessoa'] = idPessoa;
    data['nome'] = nome;
    data['id_foto'] = idFoto;
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
