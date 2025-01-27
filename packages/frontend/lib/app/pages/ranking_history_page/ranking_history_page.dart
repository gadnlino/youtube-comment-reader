import 'package:flutter/material.dart';
import 'package:frontend/app/common/api/bjj_api.dart';
import 'package:frontend/app/common/components/custom_bottom_navigation_bar.dart';
import 'package:frontend/app/common/components/custom_button.dart';
import 'package:frontend/app/common/components/custom_divider.dart';
import 'package:frontend/app/common/components/image_card.dart';
import 'package:frontend/app/common/components/ranking_card.dart';
import 'package:frontend/app/common/controllers/access_control_controller.dart';
import 'package:frontend/app/common/models/academia.dart';
import 'package:frontend/app/common/models/dto/pessoa_graduacao_dto.dart';
import 'package:frontend/app/common/models/enums/graduacao_enum.dart';
import 'package:frontend/app/common/models/graduacao.dart';
import 'package:frontend/app/common/utils/navigation.dart';
import 'package:frontend/app/common/utils/utils.dart';
import 'package:frontend/app/pages/advance_ranking_page/advance_ranking_page.dart';
import 'package:frontend/app/pages/profile_page/profile_page.dart';
import 'package:frontend/app/pages/ranking_selection_page/ranking_selection_page.dart';
import 'package:get/get.dart';

const String rankingHistoryPageRoute = "/ranking-history";

class RankingHistoryPageBinding implements Bindings {
  @override
  void dependencies() {
    Get.lazyPut(() => RankingHistoryPageController());
  }
}

class RankingHistoryPageController extends GetxController {
  final _bjjApi = BjjApi();
  final _accessControlController = Get.find<AccessControlController>();

  Rx<bool> loading = Rx(false);
  RxList<PessoaGraduacaoDto> graduacoesPessoa = RxList();

  @override
  void onInit() {
    (() async {
      try {
        loading.value = true;

        var result = await _bjjApi.listarGraduacoesPessoa(
            _accessControlController.pessoaLogada.value!.email!);
        result.sort((a, b) => -a.dtGraduacao!.compareTo(b.dtGraduacao!));
        graduacoesPessoa.value = result;

        debugPrint("graduacoes do usuario obtidas");
      } finally {
        loading.value = false;
      }
    })();

    super.onInit();
  }
}

class RankingHistoryPage extends GetView<RankingHistoryPageController> {
  const RankingHistoryPage({super.key});

  Widget _rankingSection(PessoaGraduacaoDto ranking) {
    String? dtGraduacao =
        Utils.formatDateOrNull(ranking.dtGraduacao, "dd/MM/yyyy");

    String? dtAprovacao =
        Utils.formatDateOrNull(ranking.dtAprovacao, "dd/MM/yyyy");

    return Container(
      padding: const EdgeInsets.only(
        top: 20,
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          RankingCard(ranking: GraduacaoEnum.values[ranking.idGraduacao!]),
          Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Text(
                ranking.nmGraduacao!,
                style: const TextStyle(
                    color: Colors.white, fontWeight: FontWeight.bold),
              ),
              if (dtGraduacao != null)
                Text(
                  dtGraduacao,
                  style: const TextStyle(color: Colors.white),
                ),
              if (dtAprovacao != null)
                Row(
                  children: [
                    const Icon(
                      Icons.check,
                      color: Colors.white,
                    ),
                    Text(
                      "Aprovada em $dtAprovacao",
                      style: const TextStyle(color: Colors.white),
                    ),
                  ],
                )
              else
                const Text(
                  "Não aprovada",
                  style: TextStyle(color: Colors.white),
                )
            ],
          )
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    const pageTitle = "Histórico de rankings";
    return Scaffold(
        appBar: AppBar(
          title: const Text(pageTitle),
          centerTitle: true,
          leading: IconButton(
              onPressed: () {
                Navigation.popAndGoToPage(pageRoute: profilePageRoute);
              },
              icon: const Icon(Icons.arrow_back)),
        ),
        bottomNavigationBar: const CustomBottomNavigationBar(),
        body: Obx(
          () {
            if (controller.loading.value) {
              return const Center(
                child: CircularProgressIndicator(
                  color: Colors.white,
                ),
              );
            }

            if (controller.graduacoesPessoa.isEmpty) {
              return Center(
                child: CustomButton(
                  text: "Selecionar ranking",
                  type: ButtonType.primary,
                  onPressed: () {
                    Navigation.popAndGoToPage(
                        pageRoute: rankingSelectionPageRoute);
                  },
                ),
              );
            }

            return Column(
              children: [
                Expanded(
                  child: ListView.builder(
                      itemCount: controller.graduacoesPessoa.length,
                      physics: const ClampingScrollPhysics(),
                      shrinkWrap: true,
                      scrollDirection: Axis.vertical,
                      itemBuilder: (BuildContext context, int index) => Column(
                            children: [
                              _rankingSection(
                                  controller.graduacoesPessoa.elementAt(index)),
                              if (index <
                                  controller.graduacoesPessoa.length - 1)
                                const CustomDivider(),
                            ],
                          )),
                ),
                Align(
                    alignment: Alignment.bottomCenter,
                    child: Row(
                      children: [
                        Expanded(
                            child: Padding(
                          padding: const EdgeInsets.symmetric(
                              horizontal: 10, vertical: 20),
                          child: CustomButton(
                            text: "Avançar ranking",
                            type: ButtonType.primary,
                            onPressed: () {
                              Navigation.popAndGoToPage(
                                  pageRoute: advanceRankingPageRoute);
                            },
                          ),
                        )),
                      ],
                    ))
              ],
            );
          },
        ));
  }
}
