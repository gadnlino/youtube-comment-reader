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
import 'package:frontend/app/common/models/dto/professor_pessoa_dto.dart';
import 'package:frontend/app/common/models/midia.dart';
import 'package:frontend/app/common/utils/navigation.dart';
import 'package:frontend/app/pages/gym_history_page/gym_history_page.dart';
import 'package:frontend/app/pages/profile_page/profile_page.dart';
import 'package:frontend/app/pages/teacher_history_page/teacher_history_page.dart';
import 'package:get/get.dart';
import 'package:intl/intl.dart';

const String teacherSelectionPageRoute = "/teacher-selection";

class TeacherSelectionPageBinding implements Bindings {
  @override
  void dependencies() {
    Get.lazyPut(() => TeacherSelectionPageController());
  }
}

class TeacherSelectionPageController extends GetxController {
  RxList<ProfessorPessoaDto> professoresDisponiveis = RxList();
  Rx<bool> loading = Rx(false);
  final _bjjApi = BjjApi();
  final _accessControlController = Get.find<AccessControlController>();

  @override
  void onInit() {
    (() async {
      loading.value = true;

      try {
        var professoresPessoa = await _bjjApi.listarProfessoresPessoa(
            _accessControlController.pessoaLogada.value!.email!);

        var historicoProfessores =
            await _bjjApi.listarHistoricoProfessoresPessoa(
                _accessControlController.pessoaLogada.value!.email!);

        professoresDisponiveis.value = professoresPessoa
            .where((element) =>
                !historicoProfessores
                    .any((pp) => pp.idPessoa == element.idPessoa) ||
                historicoProfessores.any((pp) =>
                    pp.idPessoa == element.idPessoa && pp.dtFim == null))
            .toList();
      } finally {
        loading.value = false;
      }
    })();
    super.onInit();
  }

  Future criarProfessorPessoa(ProfessorPessoaDto professor) async {
    try {
      loading.value = true;

      await _bjjApi.criarProfessorPessoa(
          _accessControlController.pessoaLogada.value!.email!,
          professor.idPessoa!,
          professor.idAcademia!);
    } finally {
      loading.value = false;
    }
  }
}

class TeacherSelectionPage extends GetView<TeacherSelectionPageController> {
  Widget _teacherSection(ProfessorPessoaDto professor, Midia? fotoProfessor) {
    Widget? presentationWidget;

    if (fotoProfessor == null) {
      presentationWidget = CircleAvatar(
        backgroundColor: Colors.white,
        radius: 20,
        child: Center(
          child: Wrap(
            alignment: WrapAlignment.center,
            children: [
              Padding(
                padding: const EdgeInsets.all(5),
                child: Text(
                  professor.nome!,
                  style: const TextStyle(fontSize: 17.5),
                  textAlign: TextAlign.center,
                ),
              )
            ],
          ),
        ),
      );
    } else {
      presentationWidget =
          CustomCachedNetworkImage(url: fotoProfessor.urlMidia!);
    }

    return Container(
      padding: const EdgeInsets.only(top: 20, bottom: 20),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          Column(children: [
            ImageCard(
              backgroundColor: Colors.grey,
              child: presentationWidget,
            )
          ]),
          Flexible(
            child: Wrap(
              alignment: WrapAlignment.center,
              children: [
                Text(
                  professor.nome!,
                  style: const TextStyle(
                      color: Colors.white, fontWeight: FontWeight.bold),
                  textAlign: TextAlign.center,
                ),
                Text(
                  professor.nmAcademia!,
                  style: const TextStyle(color: Colors.white),
                  textAlign: TextAlign.center,
                ),
                CustomButton(
                  text: "Selecionar",
                  type: ButtonType.primary,
                  onPressed: () async {
                    await controller.criarProfessorPessoa(professor);
                    Navigation.popAndGoToPage(
                        pageRoute: teacherHistoryPageRoute);
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
        title: const Text("Selecionar professor"),
        centerTitle: true,
        leading: IconButton(
            onPressed: () {
              Navigation.popAndGoToPage(pageRoute: teacherHistoryPageRoute);
            },
            icon: const Icon(Icons.arrow_back)),
      ),
      body: Obx(() {
        var mediaController = Get.find<MediaController>();

        if (controller.loading.value) {
          return const Center(
            child: CircularProgressIndicator(
              color: Colors.white,
            ),
          );
        }

        if (controller.professoresDisponiveis.isEmpty) {
          return const Center(
            child: Text(
              "Sem professores disponiveis :(",
              style: TextStyle(color: Colors.white, fontSize: 20),
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
                    itemCount: controller.professoresDisponiveis.length,
                    physics: const ClampingScrollPhysics(),
                    shrinkWrap: true,
                    scrollDirection: Axis.vertical,
                    itemBuilder: (BuildContext context, int index) {
                      var professor =
                          controller.professoresDisponiveis.elementAt(index);

                      var fotoProfessor = professor.idFoto != null
                          ? mediaController.getMedia(professor.idFoto!)
                          : null;

                      return Column(
                        children: [
                          _teacherSection(professor, fotoProfessor),
                          if (index <
                              controller.professoresDisponiveis.length - 1)
                            const CustomDivider(),
                        ],
                      );
                    }),
              ),
            ))
          ],
        );
      }),
    );
  }
}
