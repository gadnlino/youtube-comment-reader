import 'dart:convert';

import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:frontend/app/common/models/academia.dart';
import 'package:frontend/app/common/models/dto/pessoa_academia_dto.dart';
import 'package:frontend/app/common/models/dto/pessoa_federacao_dto.dart';
import 'package:frontend/app/common/models/dto/pessoa_graduacao_dto.dart';
import 'package:frontend/app/common/models/dto/professor_pessoa_dto.dart';
import 'package:frontend/app/common/models/federacao.dart';
import 'package:frontend/app/common/models/graduacao.dart';
import 'package:frontend/app/common/models/midia.dart';
import 'package:frontend/app/common/models/pessoa.dart';
import 'package:frontend/app/common/packages/client_http_package.dart';
import 'package:frontend/app/common/values/constants.dart';

class BjjApi {
  final ClientHttpPackage _clientHttp = ClientHttpPackage();

  Future criarPessoa(Pessoa pessoa) async {
    Response? response;

    try {
      response = await _clientHttp.post(
          url: "${Constants.apiUrl}/pessoa", data: pessoa.toJson());
    } catch (e) {
      if (response != null) {
        debugPrint('Response:');
        debugPrint(response.data as String);
      }
      debugPrint(e.toString());
      rethrow;
    }
  }

  Future<Pessoa?> buscarPessoa(String email) async {
    Response? response;

    try {
      response = await _clientHttp.get(
          url: "${Constants.apiUrl}/pessoa/$email",
          options: Options(
              validateStatus: (s) => (s! >= 200 && s <= 299) || s == 404,
              followRedirects: false));

      if (response.statusCode! >= 200 && response.statusCode! <= 299) {
        return Pessoa.fromJson(json.decode(response.data));
      }

      return null;
    } catch (e) {
      if (response != null) {
        debugPrint('Response:');
        debugPrint(response.data as String);
      }
      debugPrint(e.toString());
      rethrow;
    }
  }

  Future<bool> buscarPessoaExistente(String email) async {
    Response? response;

    try {
      response = await _clientHttp.get(
          url: "${Constants.apiUrl}/pessoa/existente/$email");

      if (response.statusCode! >= 200 && response.statusCode! <= 299) {
        return response.data == "true";
      }

      return false;
    } catch (e) {
      if (response != null) {
        debugPrint('Response:');
        debugPrint(response.data as String);
      }
      debugPrint(e.toString());
      rethrow;
    }
  }

  Future<Pessoa> buscarPessoaPorId(int idPessoa) async {
    Response? response;

    try {
      response =
          await _clientHttp.get(url: "${Constants.apiUrl}/pessoa/id/$idPessoa");

      return Pessoa.fromJson(json.decode(response.data));
    } catch (e) {
      if (response != null) {
        debugPrint('Response:');
        debugPrint(response.data as String);
      }
      debugPrint(e.toString());
      rethrow;
    }
  }

  Future<Midia> uploadMidia(Midia media) async {
    Response? response;

    try {
      response = await _clientHttp.post(
          url: "${Constants.apiUrl}/midia", data: media.toJson());

      return Midia.fromJson(json.decode(response.data));
    } catch (e) {
      if (response != null) {
        debugPrint('Response:');
        debugPrint(response.data as String);
      }
      debugPrint(e.toString());
      rethrow;
    }
  }

  Future<Midia?> downloadMidia(int idMidia) async {
    Response? response;

    try {
      response = await _clientHttp.get(
          url: "${Constants.apiUrl}/midia/${idMidia.toString()}",
          options: Options(
              validateStatus: (s) => (s! >= 200 && s <= 299) || s == 404,
              followRedirects: false));

      if (response.statusCode! >= 200 && response.statusCode! <= 299) {
        return Midia.fromJson(json.decode(response.data));
      }

      return null;
    } catch (e) {
      if (response != null) {
        debugPrint('Response:');
        debugPrint(response.data as String);
      }
      debugPrint(e.toString());
      rethrow;
    }
  }

  Future<List<Academia>> listarAcademias() async {
    Response? response;

    try {
      response =
          await _clientHttp.get(url: "${Constants.apiUrl}/academia/lista");

      return List<Academia>.from((json.decode(response.data) as List)
          .map((model) => Academia.fromJson(model)));
    } catch (e) {
      if (response != null) {
        debugPrint('Response:');
        debugPrint(response.data as String);
      }
      debugPrint(e.toString());
      rethrow;
    }
  }

  Future<List<PessoaAcademiaDto>> listarAcademiasPessoa(String email) async {
    Response? response;

    try {
      response = await _clientHttp.get(
          url: "${Constants.apiUrl}/pessoa/$email/academia/lista");

      return List<PessoaAcademiaDto>.from((json.decode(response.data) as List)
          .map((model) => PessoaAcademiaDto.fromJson(model)));
    } catch (e) {
      if (response != null) {
        debugPrint('Response:');
        debugPrint(response.data as String);
      }
      debugPrint(e.toString());
      rethrow;
    }
  }

  Future criarAcademiaPessoa(String email, int idAcademia, DateTime dtInicio,
      {DateTime? dtFim, String? ehProfessor}) async {
    Response? response;

    try {
      response = await _clientHttp.post(
          url: "${Constants.apiUrl}/pessoa/$email/academia/$idAcademia",
          data: {
            'dt_inicio': dtInicio.toIso8601String(),
            'dt_fim': dtFim?.toIso8601String(),
            'eh_professor': ehProfessor
          });
    } catch (e) {
      if (response != null) {
        debugPrint('Response:');
        debugPrint(response.data as String);
      }
      debugPrint(e.toString());
      rethrow;
    }
  }

  Future atualizarAcademiaPessoa(
      String email, int idAcademia, DateTime dtInicio,
      {DateTime? dtFim}) async {
    Response? response;

    try {
      response = await _clientHttp.put(
          url: "${Constants.apiUrl}/pessoa/$email/academia/$idAcademia",
          data: {
            'dt_inicio': dtInicio.toIso8601String(),
            'dt_fim': dtFim?.toIso8601String()
          });
    } catch (e) {
      if (response != null) {
        debugPrint('Response:');
        debugPrint(response.data as String);
      }
      debugPrint(e.toString());
      rethrow;
    }
  }

  Future deletarAcademiaPessoa(String email, int idAcademia) async {
    Response? response;

    try {
      response = await _clientHttp.delete(
          url: "${Constants.apiUrl}/pessoa/$email/academia/$idAcademia");
    } catch (e) {
      if (response != null) {
        debugPrint('Response:');
        debugPrint(response.data as String);
      }
      debugPrint(e.toString());
      rethrow;
    }
  }

  Future<List<PessoaGraduacaoDto>> listarGraduacoesPessoa(String email) async {
    Response? response;

    try {
      response = await _clientHttp.get(
          url: "${Constants.apiUrl}/pessoa/$email/graduacao/lista");

      return List<PessoaGraduacaoDto>.from((json.decode(response.data) as List)
          .map((model) => PessoaGraduacaoDto.fromJson(model)));
    } catch (e) {
      if (response != null) {
        debugPrint('Response:');
        debugPrint(response.data as String);
      }
      debugPrint(e.toString());
      rethrow;
    }
  }

  Future<List<Graduacao>> listarGraduacoesParaPessoa(String email) async {
    Response? response;

    try {
      response = await _clientHttp.get(
          url: "${Constants.apiUrl}/graduacao/$email/lista");

      return List<Graduacao>.from((json.decode(response.data) as List)
          .map((model) => Graduacao.fromJson(model)));
    } catch (e) {
      if (response != null) {
        debugPrint('Response:');
        debugPrint(response.data as String);
      }
      debugPrint(e.toString());
      rethrow;
    }
  }

  Future<List<Federacao>> listarFederacoes() async {
    Response? response;

    try {
      response =
          await _clientHttp.get(url: "${Constants.apiUrl}/federacao/lista");

      return List<Federacao>.from((json.decode(response.data) as List)
          .map((model) => Federacao.fromJson(model)));
    } catch (e) {
      if (response != null) {
        debugPrint('Response:');
        debugPrint(response.data as String);
      }
      debugPrint(e.toString());
      rethrow;
    }
  }

  Future<List<PessoaFederacaoDto>> listarFederacoesPessoa(String email) async {
    Response? response;

    try {
      response = await _clientHttp.get(
          url: "${Constants.apiUrl}/pessoa/$email/federacao/lista");

      return List<PessoaFederacaoDto>.from((json.decode(response.data) as List)
          .map((model) => PessoaFederacaoDto.fromJson(model)));
    } catch (e) {
      if (response != null) {
        debugPrint('Response:');
        debugPrint(response.data as String);
      }
      debugPrint(e.toString());
      rethrow;
    }
  }

  Future criarFederacaoPessoa(String email, int idFederacao, DateTime dtInicio,
      {DateTime? dtFim}) async {
    Response? response;

    try {
      response = await _clientHttp.post(
          url: "${Constants.apiUrl}/pessoa/$email/federacao/$idFederacao",
          data: {
            'dt_inicio': dtInicio.toIso8601String(),
            'dt_fim': dtFim?.toIso8601String()
          });
    } catch (e) {
      if (response != null) {
        debugPrint('Response:');
        debugPrint(response.data as String);
      }
      debugPrint(e.toString());
      rethrow;
    }
  }

  Future criarGraduacaoPessoa(String email, int idGraduacao) async {
    Response? response;

    try {
      response = await _clientHttp.post(
          url: "${Constants.apiUrl}/pessoa/$email/graduacao/$idGraduacao",
          data: null);
    } catch (e) {
      if (response != null) {
        debugPrint('Response:');
        debugPrint(response.data as String);
      }
      debugPrint(e.toString());
      rethrow;
    }
  }

  Future atualizarFederacaoPessoa(
      String email, int idFederacao, DateTime dtInicio,
      {DateTime? dtFim}) async {
    Response? response;

    try {
      response = await _clientHttp.put(
          url: "${Constants.apiUrl}/pessoa/$email/federacao/$idFederacao",
          data: {
            'dt_inicio': dtInicio.toIso8601String(),
            'dt_fim': dtFim?.toIso8601String()
          });
    } catch (e) {
      if (response != null) {
        debugPrint('Response:');
        debugPrint(response.data as String);
      }
      debugPrint(e.toString());
      rethrow;
    }
  }

  Future<List<ProfessorPessoaDto>> listarProfessoresPessoa(String email) async {
    Response? response;

    try {
      response = await _clientHttp.get(
          url: "${Constants.apiUrl}/pessoa/$email/professores/lista");

      return List<ProfessorPessoaDto>.from((json.decode(response.data) as List)
          .map((model) => ProfessorPessoaDto.fromJson(model)));
    } catch (e) {
      if (response != null) {
        debugPrint('Response:');
        debugPrint(response.data as String);
      }
      debugPrint(e.toString());
      rethrow;
    }
  }

  Future<List<ProfessorPessoaDto>> listarHistoricoProfessoresPessoa(
      String email) async {
    Response? response;

    try {
      response = await _clientHttp.get(
          url: "${Constants.apiUrl}/pessoa/$email/professores/historico/lista");

      return List<ProfessorPessoaDto>.from((json.decode(response.data) as List)
          .map((model) => ProfessorPessoaDto.fromJson(model)));
    } catch (e) {
      if (response != null) {
        debugPrint('Response:');
        debugPrint(response.data as String);
      }
      debugPrint(e.toString());
      rethrow;
    }
  }

  Future criarProfessorPessoa(
      String emailPessoa, int idProfessor, int idAcademia) async {
    Response? response;

    try {
      response = await _clientHttp.post(
          url:
              "${Constants.apiUrl}/pessoa/$emailPessoa/professor/$idProfessor/$idAcademia",
          data: null);
    } catch (e) {
      if (response != null) {
        debugPrint('Response:');
        debugPrint(response.data as String);
      }
      debugPrint(e.toString());
      rethrow;
    }
  }

  Future atualizarProfessorPessoa(
      String emailPessoa, int idProfessorPessoa, DateTime dtFim) async {
    Response? response;

    try {
      response = await _clientHttp.put(
          url:
              "${Constants.apiUrl}/pessoa/$emailPessoa/professor/$idProfessorPessoa",
          data: {'dt_fim': dtFim.toIso8601String()});
    } catch (e) {
      if (response != null) {
        debugPrint('Response:');
        debugPrint(response.data as String);
      }
      debugPrint(e.toString());
      rethrow;
    }
  }

  Future deletarProfessorPessoa(
      String emailPessoa, int idProfessorPessoa) async {
    Response? response;

    try {
      response = await _clientHttp.delete(
          url:
              "${Constants.apiUrl}/pessoa/$emailPessoa/professor/$idProfessorPessoa",
          data: null);
    } catch (e) {
      if (response != null) {
        debugPrint('Response:');
        debugPrint(response.data as String);
      }
      debugPrint(e.toString());
      rethrow;
    }
  }

  Future<bool> pessoaEhProfessor(String emailPessoa) async {
    Response? response;

    try {
      String url = "${Constants.apiUrl}/pessoa/$emailPessoa/ehProfessor";
      response = await _clientHttp.get(url: url);

      return response.data == "true";
    } catch (e) {
      if (response != null) {
        debugPrint('Response:');
        debugPrint(response.data as String);
      }
      debugPrint(e.toString());
      rethrow;
    }
  }
}
