import 'package:frontend/app/common/api/bjj_api.dart';
import 'package:frontend/app/common/models/dto/pessoa_federacao_dto.dart';
import 'package:frontend/app/common/models/federacao.dart';
import 'package:get/get.dart';

class FederacaoController extends GetxController {
  final _bjjApi = BjjApi();
  RxList<Federacao> federacoes = RxList();
  RxList<PessoaFederacaoDto> federacoesPessoa = RxList();
  Rx<bool> loading = Rx<bool>(false);
  Rx<int?> federacaoEdicao = Rx(null);

  Future<List<Federacao>> listarFederacoes() async {
    var listaFederacoes = await _bjjApi.listarFederacoes();

    federacoes.value = listaFederacoes;

    return federacoes;
  }

  Future<List<PessoaFederacaoDto>> listarFederacoesPessoa(String email) async {
    var listaFederacoesPessoa = await _bjjApi.listarFederacoesPessoa(email);

    federacoesPessoa.value = listaFederacoesPessoa;

    return listaFederacoesPessoa;
  }

  Future criarFederacaoPessoa(
      String email, int idFederacao, DateTime dtInicio) async {
    await _bjjApi.criarFederacaoPessoa(email, idFederacao, dtInicio);
  }

  Future atualizarFederacaoPessoa(
      String email, int idFederacao, DateTime dtInicio, DateTime dtFim) async {
    await _bjjApi.atualizarFederacaoPessoa(email, idFederacao, dtInicio,
        dtFim: dtFim);
  }

  Federacao? federacaoAtiva() {
    var federacaoAtiva = federacoesPessoa
        .where((p0) => p0.dtInicio != null && p0.dtFim == null)
        .firstOrNull;

    return federacaoAtiva != null ? Federacao.fromDto(federacaoAtiva) : null;
  }

  Future trocarFederacao(String email, Federacao novaFederacao) async {
    await _bjjApi.criarFederacaoPessoa(
        email, novaFederacao.idFederacao, DateTime.now().toUtc());

    var federacaoAtiva = federacoesPessoa
        .where((p0) => p0.dtInicio != null && p0.dtFim == null)
        .first;

    await _bjjApi.atualizarFederacaoPessoa(
        email, federacaoAtiva.idFederacao!, federacaoAtiva.dtInicio!,
        dtFim: DateTime.now().toUtc());
  }

  Future recarregarInformacoes(String email) async {
    await listarFederacoes();
    await listarFederacoesPessoa(email);
  }
}
