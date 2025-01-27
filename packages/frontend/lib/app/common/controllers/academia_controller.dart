import 'package:frontend/app/common/api/bjj_api.dart';
import 'package:frontend/app/common/models/academia.dart';
import 'package:frontend/app/common/models/dto/pessoa_academia_dto.dart';
import 'package:get/get.dart';

class AcademiaController extends GetxController {
  final _bjjApi = BjjApi();
  RxList<Academia?> academias = RxList();
  RxList<PessoaAcademiaDto> academiasPessoa = RxList();
  Rx<int?> academiaEdicao = Rx(null);

  Future<List<Academia>> listarAcademias() async {
    var bjjApi = BjjApi();

    var listaAcademias = await bjjApi.listarAcademias();

    academias.value = listaAcademias;

    return listaAcademias;
  }

  // Future<List<PessoaAcademiaDto>?> listarAcademiasPessoa(String email) async {
  //   var listaAcademiasPessoa = await _bjjApi.listarAcademiasPessoa(email);

  //   listaAcademiasPessoa.sort((a, b) => -a.dtInicio!.compareTo(b.dtInicio!));

  //   academiasPessoa.value = listaAcademiasPessoa;

  //   return listaAcademiasPessoa;
  // }

  Future criarAcademiaPessoa(
      String email, int idAcademia, DateTime dtInicio) async {
    await _bjjApi.criarAcademiaPessoa(email, idAcademia, dtInicio);
  }

  Future atualizarAcademiaPessoa(
      String email, int idAcademia, DateTime dtInicio, DateTime dtFim) async {
    await _bjjApi.atualizarAcademiaPessoa(email, idAcademia, dtInicio,
        dtFim: dtFim);
  }

  Future deletarAcademiaPessoa(String email, int idAcademia) async {
    await _bjjApi.deletarAcademiaPessoa(email, idAcademia);
  }

  // List<Academia?> academiasDisponiveis() {
  //   return academias
  //       .where((p0) => !academiasPessoa
  //           .any((element) => element.idAcademia == p0?.idAcademia))
  //       .toList();
  // }
}
