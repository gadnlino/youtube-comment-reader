import 'package:flutter/material.dart';
import 'package:frontend/app/common/api/bjj_api.dart';
import 'package:frontend/app/common/components/custom_button.dart';
import 'package:frontend/app/common/components/custom_cached_network_image.dart';
import 'package:frontend/app/common/components/custom_divider.dart';
import 'package:frontend/app/common/components/image_card.dart';
import 'package:frontend/app/common/controllers/academia_controller.dart';
import 'package:frontend/app/common/controllers/access_control_controller.dart';
import 'package:frontend/app/common/controllers/media_controller.dart';
import 'package:frontend/app/common/models/dto/pessoa_academia_dto.dart';
import 'package:frontend/app/common/models/midia.dart';
import 'package:frontend/app/common/themes/app_theme.dart';
import 'package:frontend/app/common/utils/navigation.dart';
import 'package:frontend/app/common/values/constants.dart';
import 'package:frontend/app/pages/gym_selection_page/gym_selection_page.dart';
import 'package:frontend/app/pages/profile_page/profile_page.dart';
import 'package:frontend/app/pages/teacher_history_page/teacher_history_page.dart';
import 'package:get/get.dart';
import 'package:intl/intl.dart';

const String gymHistoryPageRoute = "/gym-history";

class GymHistoryPageBinding implements Bindings {
  @override
  void dependencies() {
    Get.lazyPut(() => GymHistoryPageController());
  }
}

class GymHistoryPageController extends GetxController {
  final _bjjApi = BjjApi();
  final _accessControlController = Get.find<AccessControlController>();
  RxList<PessoaAcademiaDto> academiasPessoa = RxList();
  RxMap<int, Midia?> midiaAcademiasPessoa = RxMap();
  Rx<bool> loading = Rx(false);

  @override
  void onInit() {
    (() async {
      try {
        loading.value = true;
        await initialState();
      } finally {
        loading.value = false;
      }
    })();
    super.onInit();
  }

  Future initialState() async {
    await limparAcademiaEdicao();
    await fetchAcademiasPessoa();
  }

  Future limparAcademiaEdicao() async {
    var academiaController = Get.find<AcademiaController>();
    academiaController.academiaEdicao.value = null;
  }

  Future fetchAcademiasPessoa() async {
    var mediaController = Get.find<MediaController>();

    academiasPessoa.value = await _bjjApi.listarAcademiasPessoa(
        _accessControlController.pessoaLogada.value!.email!);

    for (var i = 0; i < academiasPessoa.length; i++) {
      midiaAcademiasPessoa[academiasPessoa.elementAt(i).idAcademia!] =
          await mediaController
              .storeMedia(academiasPessoa.elementAt(i).idLogo!);
    }
  }
}

class GymHistoryPage extends GetView<GymHistoryPageController> {
  Future removerAcademiaPessoa(PessoaAcademiaDto academia) async {
    Get.defaultDialog(
        title: "Remover academia",
        backgroundColor: Colors.white,
        content: Text(
          "Deseja remover ${academia.nmAcademia} do historico de academias?",
        ),
        textConfirm: "Remover academia",
        textCancel: "Cancelar",
        confirmTextColor: Colors.white,
        onConfirm: () async {
          var academiaController = Get.find<AcademiaController>();
          var accessControlController = Get.find<AccessControlController>();

          controller.loading.value = true;

          try {
            Navigation.goBack();
            await academiaController.deletarAcademiaPessoa(
                accessControlController.emailPessoaLogada.value,
                academia.idAcademia!);
            await controller.initialState();
          } finally {
            controller.loading.value = false;
          }
        });
  }

  Future finalizarMatriculaAcademiaPessoa(PessoaAcademiaDto academia) async {
    Get.defaultDialog(
        title: "Finalizar matrícula",
        backgroundColor: Colors.white,
        confirmTextColor: Colors.white,
        content: Text(
          "Deseja finalizar a matriícula na academia ${academia.nmAcademia}?",
        ),
        textConfirm: "Finalizar matrícula",
        textCancel: "Cancelar",
        onConfirm: () async {
          var academiaController = Get.find<AcademiaController>();
          var accessControlController = Get.find<AccessControlController>();

          try {
            Navigation.goBack();

            controller.loading.value = true;

            await academiaController.atualizarAcademiaPessoa(
                accessControlController.emailPessoaLogada.value,
                academia.idAcademia!,
                academia.dtInicio!,
                DateTime.now().toUtc());
            await controller.initialState();
          } finally {
            controller.loading.value = false;
          }
        });
  }

  Widget _gymSection(PessoaAcademiaDto academia) {
    final DateFormat formatter = DateFormat('dd/MM/yyyy');
    final String dtInicioStr = formatter.format(academia.dtInicio!);
    final String dtFimStr = academia.dtFim != null
        ? formatter.format(academia.dtFim!)
        : 'Atualmente';

    return Container(
      padding: const EdgeInsets.only(top: 20, bottom: 20),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          Column(children: [
            Obx(() {
              var mediaController = Get.find<MediaController>();
              var midiaLogoAcademia = mediaController.getMedia(academia.idLogo);
              return ImageCard(
                backgroundColor: Colors.grey,
                child: midiaLogoAcademia != null
                    ? CustomCachedNetworkImage(url: midiaLogoAcademia.urlMidia!)
                    : null,
              );
            })
          ]),
          Flexible(
            child: Wrap(
              alignment: WrapAlignment.center,
              children: [
                Text(
                  academia.nmAcademia!,
                  style: const TextStyle(
                      color: Colors.white, fontWeight: FontWeight.bold),
                  textAlign: TextAlign.center,
                ),
                Text(
                  academia.endereco!,
                  style: const TextStyle(color: Colors.white),
                  textAlign: TextAlign.center,
                ),
                Text(
                  "$dtInicioStr - $dtFimStr",
                  style: const TextStyle(color: Colors.white),
                  textAlign: TextAlign.center,
                ),
                Obx(() {
                  var academiaController = Get.find<AcademiaController>();

                  if (academiaController.academiaEdicao.value !=
                      academia.idAcademia) {
                    return InkWell(
                      onTap: () {
                        academiaController.academiaEdicao.value =
                            academia.idAcademia!;
                      },
                      child: const Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(
                            Icons.edit,
                            color: Colors.white,
                          ),
                          Text(
                            "Editar",
                            style: TextStyle(color: Colors.white),
                          )
                        ],
                      ),
                    );
                  }

                  return Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    crossAxisAlignment: CrossAxisAlignment.center,
                    children: [
                      if (academia.dtFim == null)
                        Expanded(
                            child: InkWell(
                          onTap: () async {
                            await finalizarMatriculaAcademiaPessoa(academia);
                          },
                          child: const Column(
                            children: [
                              Icon(
                                Icons.check_circle,
                                color: Colors.white,
                              ),
                              Wrap(
                                alignment: WrapAlignment.center,
                                children: [
                                  Text(
                                    "Finalizar matrícula",
                                    textAlign: TextAlign.center,
                                    style: TextStyle(
                                        color: Colors.white, fontSize: 12),
                                  )
                                ],
                              )
                            ],
                          ),
                        )),
                      Expanded(
                          child: InkWell(
                        onTap: () async {
                          await removerAcademiaPessoa(academia);
                        },
                        child: const Column(
                          children: [
                            Icon(
                              Icons.delete,
                              color: Colors.white,
                            ),
                            Wrap(
                              alignment: WrapAlignment.center,
                              children: [
                                Text(
                                  "Remover da lista",
                                  textAlign: TextAlign.center,
                                  style: TextStyle(
                                      color: Colors.white, fontSize: 12),
                                )
                              ],
                            )
                          ],
                        ),
                      )),
                      Expanded(
                          child: InkWell(
                        onTap: () async {
                          await controller.limparAcademiaEdicao();
                        },
                        child: const Column(
                          children: [
                            Icon(
                              Icons.cancel,
                              color: Color.fromRGBO(255, 255, 255, 1),
                            ),
                            Text(
                              "Cancelar",
                              style:
                                  TextStyle(color: Colors.white, fontSize: 12),
                            )
                          ],
                        ),
                      ))
                    ],
                  );
                })
              ],
            ),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Histórico de academias"),
        centerTitle: true,
        leading: IconButton(
            onPressed: () {
              Navigation.popAndGoToPage(pageRoute: profilePageRoute);
            },
            icon: const Icon(Icons.arrow_back)),
      ),
      body: Obx(() {
        if (controller.loading.value) {
          return const Center(
            child: CircularProgressIndicator(
              color: Colors.white,
            ),
          );
        }

        if (controller.academiasPessoa.isEmpty) {
          return Center(
            child: CustomButton(
              text: "Selecionar academia",
              type: ButtonType.primary,
              onPressed: () {
                Navigation.popAndGoToPage(pageRoute: gymSelectionPageRoute);
              },
            ),
          );
        }

        return Column(
          children: [
            Expanded(
                child: SingleChildScrollView(
                    child: Container(
                        padding: const EdgeInsets.symmetric(horizontal: 20),
                        child: ListView.builder(
                            itemCount: controller.academiasPessoa.length,
                            physics: const ClampingScrollPhysics(),
                            shrinkWrap: true,
                            scrollDirection: Axis.vertical,
                            itemBuilder: (BuildContext context, int index) =>
                                Column(
                                  children: [
                                    _gymSection(controller.academiasPessoa
                                        .elementAt(index)),
                                    if (index <
                                        controller.academiasPessoa.length - 1)
                                      const CustomDivider(),
                                  ],
                                ))))),
            Align(
                alignment: Alignment.bottomCenter,
                child: Row(
                  children: [
                    Expanded(
                        child: Padding(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 10, vertical: 20),
                      child: CustomButton(
                        text: "Selecionar nova academia",
                        type: ButtonType.primary,
                        onPressed: () {
                          Navigation.popAndGoToPage(
                              pageRoute: gymSelectionPageRoute);
                        },
                      ),
                    )),
                  ],
                ))
          ],
        );
      }),
    );
  }
}
