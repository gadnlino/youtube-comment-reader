class Pessoa {
  int? idPessoa;
  String? nome;
  String? email;
  DateTime? dtNascimento;
  int? idFoto;
  String? endereco;
  int? idProfessor;
  String? ehProfessor;

  Pessoa({
    this.idPessoa,
    this.nome,
    this.email,
    this.dtNascimento,
    this.idProfessor,
    this.idFoto,
    this.ehProfessor = 'N',
  });

  Pessoa.fromJson(Map<String, dynamic> json) {
    idPessoa = json.containsKey('id_pessoa') && json['id_pessoa'] != null
        ? json['id_pessoa']
        : null;
    nome =
        json.containsKey('nome') && json['nome'] != null ? json['nome'] : null;
    email = json.containsKey('email') && json['email'] != null
        ? json['email']
        : null;
    dtNascimento =
        json.containsKey('dt_nascimento') && json['dt_nascimento'] != null
            ? DateTime.parse(json['dt_nascimento'])
            : null;
    idFoto = json.containsKey('id_foto') && json['id_foto'] != null
        ? json['id_foto']
        : null;

    endereco = json.containsKey('endereco') && json['endereco'] != null
        ? json['endereco']
        : null;

    idProfessor =
        json.containsKey('id_professor') && json['id_professor'] != null
            ? json['id_professor']
            : null;

    ehProfessor =
        json.containsKey('eh_professor') && json['eh_professor'] != null
            ? json['eh_professor']
            : null;
  }

  Map<String, dynamic> toJson() => {
        "nome": nome,
        "email": email,
        "dt_nascimento": dtNascimento?.toIso8601String(),
        "eh_professor": ehProfessor,
        "id_foto": idFoto
      };
}
