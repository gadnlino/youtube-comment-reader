import 'package:flutter/material.dart';
import 'package:frontend/app/common/api/bjj_api.dart';
import 'package:frontend/app/common/components/custom_button.dart';
import 'package:frontend/app/common/components/image_card.dart';
import 'package:frontend/app/common/components/ranking_card.dart';
import 'package:frontend/app/common/controllers/access_control_controller.dart';
import 'package:frontend/app/common/models/dto/pessoa_graduacao_dto.dart';
import 'package:frontend/app/common/models/enums/graduacao_enum.dart';
import 'package:frontend/app/common/models/graduacao.dart';
import 'package:frontend/app/common/utils/navigation.dart';
import 'package:frontend/app/pages/feed_page/feed_page.dart';
import 'package:frontend/app/pages/ranking_history_page/ranking_history_page.dart';
import 'package:frontend/app/pages/ranking_selection_page/ranking_selection_page.dart';
import 'package:get/get.dart';
import 'package:get/get_core/src/get_main.dart';
import 'package:get/get_instance/src/bindings_interface.dart';

const String advanceRankingPageRoute = "/advance-ranking";

class AdvanceRankingPageBinding implements Bindings {
  @override
  void dependencies() {
    Get.lazyPut(() => AdvanceRankingPageController());
  }
}

class AdvanceRankingPageController extends GetxController {
  final _accessControlController = Get.find<AccessControlController>();
  final BjjApi _bjjApi = BjjApi();

  Rx<bool> loading = Rx(false);
  RxList<PessoaGraduacaoDto> graduacoesDaPessoa = RxList();
  RxList<Graduacao> graduacoesParaPessoa = RxList();

  @override
  void onInit() {
    (() async {
      try {
        loading.value = true;

        graduacoesDaPessoa.value = await _bjjApi.listarGraduacoesPessoa(
            _accessControlController.pessoaLogada.value!.email!);
        graduacoesParaPessoa.value = await _bjjApi.listarGraduacoesParaPessoa(
            _accessControlController.pessoaLogada.value!.email!);
        debugPrint("graduacoes do usuario obtidas");
      } finally {
        loading.value = false;
      }
    })();

    super.onInit();
  }

  Future avancarRanking(int idProximaGraduacao) async {
    try {
      loading.value = true;

      await _bjjApi.criarGraduacaoPessoa(
          _accessControlController.pessoaLogada.value!.email!,
          idProximaGraduacao);

      Navigation.popAndGoToPage(pageRoute: rankingHistoryPageRoute);
    } finally {
      loading.value = false;
    }
  }
}

class AdvanceRankingPage extends GetView<AdvanceRankingPageController> {
  const AdvanceRankingPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: const Text("Avançar ranking"),
          centerTitle: true,
          leading: IconButton(
              onPressed: () {
                Navigation.popAndGoToPage(pageRoute: rankingHistoryPageRoute);
              },
              icon: const Icon(Icons.arrow_back)),
        ),
        body: CustomScrollView(
          slivers: [
            SliverFillRemaining(
              hasScrollBody: false,
              child: Obx(() {
                if (controller.loading.value) {
                  return const Center(
                    child: CircularProgressIndicator(
                      color: Colors.white,
                    ),
                  );
                }

                controller.graduacoesDaPessoa
                    .sort((a, b) => a.idGraduacao! - b.idGraduacao!);

                controller.graduacoesParaPessoa
                    .sort((a, b) => a.idGraduacao! - b.idGraduacao!);

                int idGraduacaoPessoa =
                    controller.graduacoesDaPessoa.last.idGraduacao!;

                Graduacao proximaGraduacao = controller.graduacoesParaPessoa
                    .elementAt(controller.graduacoesDaPessoa.indexWhere(
                            (p0) => p0.idGraduacao! == idGraduacaoPessoa) +
                        1);

                GraduacaoEnum rankingEnum =
                    GraduacaoEnum.values[proximaGraduacao.idGraduacao!];

                return Column(
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    const Padding(
                      padding: EdgeInsets.only(top: 40),
                      child: Text("Próximo ranking:",
                          style: TextStyle(
                              color: Colors.white,
                              fontWeight: FontWeight.bold,
                              fontSize: 20)),
                    ),
                    RankingCard(ranking: rankingEnum),
                    Padding(
                      padding: EdgeInsets.only(top: 20),
                      child: Text(proximaGraduacao.nmGraduacao!,
                          style: TextStyle(color: Colors.white, fontSize: 20)),
                    ),
                    const Padding(
                      padding: EdgeInsets.only(top: 20),
                      child: Text("O professor irá aprovar o seu novo ranking.",
                          style:
                              TextStyle(color: Colors.white, fontSize: 17.5)),
                    ),
                    Expanded(
                      child: Align(
                          alignment: Alignment.bottomCenter,
                          child: Row(
                            children: [
                              Expanded(
                                  child: Padding(
                                padding: const EdgeInsets.symmetric(
                                    horizontal: 10, vertical: 10),
                                child: CustomButton(
                                  text: "Confirmar",
                                  type: ButtonType.primary,
                                  onPressed: () => controller.avancarRanking(
                                      proximaGraduacao.idGraduacao!),
                                ),
                              ))
                            ],
                          )),
                    )
                  ],
                );
              }),
            )
          ],
        ));
  }
}
