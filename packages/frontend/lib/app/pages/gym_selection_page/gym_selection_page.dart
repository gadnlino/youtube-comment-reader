import 'package:flutter/material.dart';
import 'package:frontend/app/common/api/bjj_api.dart';
import 'package:frontend/app/common/components/custom_button.dart';
import 'package:frontend/app/common/components/custom_cached_network_image.dart';
import 'package:frontend/app/common/components/custom_divider.dart';
import 'package:frontend/app/common/components/image_card.dart';
import 'package:frontend/app/common/controllers/academia_controller.dart';
import 'package:frontend/app/common/controllers/access_control_controller.dart';
import 'package:frontend/app/common/controllers/media_controller.dart';
import 'package:frontend/app/common/models/academia.dart';
import 'package:frontend/app/common/utils/navigation.dart';
import 'package:frontend/app/pages/gym_history_page/gym_history_page.dart';
import 'package:frontend/app/pages/profile_page/profile_page.dart';
import 'package:get/get.dart';
import 'package:get/get_rx/get_rx.dart';
import 'package:get/get_rx/src/rx_types/rx_types.dart';
import 'package:intl/intl.dart';

const String gymSelectionPageRoute = "/gym-selection";

class GymSelectionPageBinding implements Bindings {
  @override
  void dependencies() {
    Get.lazyPut(() => GymSelectionPageController());
  }
}

class GymSelectionPageController extends GetxController {
  final _bjjApi = BjjApi();
  final _accessControlController = Get.find<AccessControlController>();
  Rx<bool> loading = Rx(false);
  RxList<Academia?> academiasDisponiveis = RxList();

  @override
  void onInit() {
    (() async {
      var academiaController = Get.find<AcademiaController>();
      var mediaController = Get.find<MediaController>();

      loading.value = true;

      try {
        var todasAcademias = await _bjjApi.listarAcademias();

        var academiasPessoa = await _bjjApi.listarAcademiasPessoa(
            _accessControlController.pessoaLogada.value!.email!);

        academiasDisponiveis.value = todasAcademias
            .where((p0) => !academiasPessoa
                .any((element) => element.idAcademia == p0.idAcademia))
            .toList();

        await listarAcademias(academiaController, mediaController);
      } finally {
        loading.value = false;
      }
    })();
    super.onInit();
  }

  Future listarAcademias(AcademiaController academiaController,
      MediaController mediaController) async {
    var academias = await academiaController.listarAcademias();

    for (var i = 0; i < academias.length; i++) {
      var academia = academias.elementAt(i);
      if (academia.idLogo != null) {
        await mediaController.storeMedia(academia.idLogo!);
      }
    }
  }

  Future adicionarAcademiaPessoa(Academia academia) async {
    var accessControlController = Get.find<AccessControlController>();
    var academiaController = Get.find<AcademiaController>();
    var mediaController = Get.find<MediaController>();

    await academiaController.criarAcademiaPessoa(
        accessControlController.emailPessoaLogada.value,
        academia.idAcademia!,
        DateTime.now());
    await listarAcademias(academiaController, mediaController);
  }
}

class GymSelectionPage extends GetView<GymSelectionPageController> {
  Widget _gymSection(Academia academia) {
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
                  academia.nmAcademia,
                  style: const TextStyle(
                      color: Colors.white, fontWeight: FontWeight.bold),
                  textAlign: TextAlign.center,
                ),
                Text(
                  academia.endereco!,
                  style: const TextStyle(color: Colors.white),
                  textAlign: TextAlign.center,
                ),
                CustomButton(
                  text: "Adicionar",
                  type: ButtonType.primary,
                  onPressed: () async {
                    controller.loading.value = true;

                    try {
                      await controller.adicionarAcademiaPessoa(academia);
                      Navigation.popAndGoToPage(pageRoute: gymHistoryPageRoute);
                    } finally {
                      controller.loading.value = false;
                    }
                  },
                )
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
        title: const Text("Selecionar academia"),
        centerTitle: true,
        leading: IconButton(
            onPressed: () {
              Navigation.popAndGoToPage(pageRoute: gymHistoryPageRoute);
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

        if (controller.academiasDisponiveis.isEmpty) {
          return const Center(
            child: Text(
              "Sem mais academias disponiveis :(",
              style: TextStyle(color: Colors.white, fontSize: 20),
            ),
          );
        }

        controller.academiasDisponiveis
            .sort((a, b) => a!.nmAcademia.compareTo(b!.nmAcademia));
        controller.academiasDisponiveis
            .sort((a, b) => a!.nmAcademia.compareTo(b!.nmAcademia));

        return SingleChildScrollView(
          child: ListView.builder(
              itemCount: controller.academiasDisponiveis.length,
              physics: const ClampingScrollPhysics(),
              shrinkWrap: true,
              scrollDirection: Axis.vertical,
              itemBuilder: (BuildContext context, int index) => Column(
                    children: [
                      _gymSection(
                          controller.academiasDisponiveis.elementAt(index)!),
                      if (index < controller.academiasDisponiveis.length - 1)
                        const CustomDivider(),
                    ],
                  )),
        );
      }),
    );
  }
}
