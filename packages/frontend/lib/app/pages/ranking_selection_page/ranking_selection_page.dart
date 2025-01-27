import 'package:flutter/material.dart';
import 'package:frontend/app/common/api/bjj_api.dart';
import 'package:frontend/app/common/components/custom_bottom_navigation_bar.dart';
import 'package:frontend/app/common/components/custom_button.dart';
import 'package:frontend/app/common/components/custom_divider.dart';
import 'package:frontend/app/common/components/image_card.dart';
import 'package:frontend/app/common/components/ranking_card.dart';
import 'package:frontend/app/common/controllers/access_control_controller.dart';
import 'package:frontend/app/common/models/dto/pessoa_graduacao_dto.dart';
import 'package:frontend/app/common/models/enums/graduacao_enum.dart';
import 'package:frontend/app/common/models/graduacao.dart';
import 'package:frontend/app/common/utils/navigation.dart';
import 'package:frontend/app/common/utils/utils.dart';
import 'package:frontend/app/pages/profile_page/profile_page.dart';
import 'package:frontend/app/pages/ranking_history_page/ranking_history_page.dart';
import 'package:get/get.dart';

const String rankingSelectionPageRoute = "/ranking-selection";

class RankingSelectionPageBinding implements Bindings {
  @override
  void dependencies() {
    Get.lazyPut(() => RankingSelectionPageController());
  }
}

class RankingSelectionPageController extends GetxController {
  final _accessControlController = Get.find<AccessControlController>();
  final _bjjApi = BjjApi();

  Rx<bool> loading = Rx(false);
  RxList<PessoaGraduacaoDto> graduacoesParaPessoa = RxList();

  @override
  void onInit() {
    (() async {
      try {
        loading.value = true;
        graduacoesParaPessoa.value = await _bjjApi.listarGraduacoesPessoa(
            _accessControlController.pessoaLogada.value!.email!);
        debugPrint("graduacoes do usuario obtidas");
      } finally {
        loading.value = false;
      }
    })();

    super.onInit();
  }

  Future criarGraduacaoPessoa(int idGraduacao) async {
    await _bjjApi.criarGraduacaoPessoa(
        _accessControlController.pessoaLogada.value!.email!, idGraduacao);
  }
}

class RankingSelectionPage extends GetView<RankingSelectionPageController> {
  Widget _rankingWidget(GraduacaoEnum ranking) {
    Widget component = Container();

    switch (ranking) {
      case GraduacaoEnum.branca:
        component = Column(children: [
          ImageCard(
            backgroundColor: Colors.white,
          )
        ]);
        break;
      case GraduacaoEnum.cinza_e_branca:
        component = Column(children: [
          ImageCard(
            backgroundColor: Colors.white,
          )
        ]);
        break;
      case GraduacaoEnum.azul:
        component = Column(children: [
          ImageCard(
            backgroundColor: const Color(0xff1d76bc),
          )
        ]);
        break;
      case GraduacaoEnum.roxa:
        component = Column(children: [
          ImageCard(
            backgroundColor: const Color(0xff9b00db),
          )
        ]);
        break;
      case GraduacaoEnum.marrom:
        component = Column(children: [
          ImageCard(
            backgroundColor: const Color(0xff5f3912),
          )
        ]);
        break;
      case GraduacaoEnum.preta:
        component = Column(children: [
          ImageCard(
            backgroundColor: const Color(0xff000000),
          )
        ]);
        break;
      case GraduacaoEnum.vermelha_e_preta:
        component = Column(children: [
          ImageCard(
            backgroundColor: const Color(0xff000000),
          )
        ]);
        break;
      case GraduacaoEnum.vermelha_e_branca:
        component = Column(children: [
          ImageCard(
            backgroundColor: const Color(0xff000000),
          )
        ]);
        break;
      case GraduacaoEnum.vermelha:
        component = Column(children: [
          ImageCard(
            backgroundColor: const Color(0xffff3200),
          )
        ]);
        break;
      default:
        break;
    }

    return component;
  }

  Widget _rankingSection(PessoaGraduacaoDto graduacao) {
    GraduacaoEnum ranking = GraduacaoEnum.values[graduacao.idGraduacao!];

    return Container(
      padding: const EdgeInsets.only(
        top: 20,
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          RankingCard(
            ranking: ranking,
          ),
          Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Text(
                graduacao.nmGraduacao!,
                style: const TextStyle(
                    color: Colors.white, fontWeight: FontWeight.bold),
              ),
              CustomButton(
                text: "Selecionar",
                type: ButtonType.primary,
                onPressed: () async {
                  try {
                    controller.loading.value = true;
                    await controller
                        .criarGraduacaoPessoa(graduacao.idGraduacao!);
                  } finally {
                    controller.loading.value = false;
                  }

                  Navigation.popAndGoToPage(pageRoute: rankingHistoryPageRoute);
                },
              )
            ],
          )
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    const pageTitle = "Selecione seu ranking";
    return Scaffold(
        appBar: AppBar(
          title: const Text(pageTitle),
          centerTitle: true,
          leading: IconButton(
              onPressed: () {
                Navigation.popAndGoToPage(pageRoute: rankingHistoryPageRoute);
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

            return ListView.builder(
                itemCount: controller.graduacoesParaPessoa.length,
                physics: const ClampingScrollPhysics(),
                shrinkWrap: true,
                scrollDirection: Axis.vertical,
                itemBuilder: (BuildContext context, int index) => Column(
                      children: [
                        _rankingSection(
                            controller.graduacoesParaPessoa.elementAt(index)),
                        if (index < controller.graduacoesParaPessoa.length - 1)
                          const CustomDivider(),
                      ],
                    ));
          },
        ));
  }
}
