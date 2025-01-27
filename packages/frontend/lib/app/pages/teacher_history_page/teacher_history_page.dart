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
import 'package:frontend/app/common/models/pessoa.dart';
import 'package:frontend/app/common/utils/navigation.dart';
import 'package:frontend/app/pages/gym_history_page/gym_history_page.dart';
import 'package:frontend/app/pages/profile_page/profile_page.dart';
import 'package:frontend/app/pages/teacher_selection_page/teacher_selection_page.dart';
import 'package:get/get.dart';
import 'package:intl/intl.dart';

const String teacherHistoryPageRoute = "/teacher-history";

class TeacherHistoryPageBinding implements Bindings {
  @override
  void dependencies() {
    Get.lazyPut(() => TeacherHistoryPageController());
  }
}

class TeacherHistoryPageController extends GetxController {
  final _bjjApi = BjjApi();
  final _accessControlController = Get.find<AccessControlController>();
  Rx<bool> loading = Rx(false);
  Rxn<ProfessorPessoaDto> professorEdicao = Rxn(null);
  RxList<ProfessorPessoaDto> historicoProfessores = RxList();
  RxList<Academia?> academiasDisponiveis = RxList();

  @override
  void onInit() {
    (() async {
      loading.value = true;

      try {
        await clearState();
        await initialState();
      } finally {
        loading.value = false;
      }
    })();
    super.onInit();
  }

  Future clearState() async {
    professorEdicao.value = null;
    historicoProfessores.value = [];
  }

  Future initialState() async {
    historicoProfessores.value = await _bjjApi.listarHistoricoProfessoresPessoa(
        _accessControlController.pessoaLogada.value!.email!);
  }

  Future terminarAula(ProfessorPessoaDto professor) async {
    await _bjjApi.atualizarProfessorPessoa(
        _accessControlController.pessoaLogada.value!.email!,
        professor.idProfessorPessoa!,
        DateTime.now().toUtc());
  }

  Future deletarProfessorPessoa(ProfessorPessoaDto professor) async {
    await _bjjApi.deletarProfessorPessoa(
        _accessControlController.pessoaLogada.value!.email!,
        professor.idProfessorPessoa!);
  }
}

class TeacherHistoryPage extends GetView<TeacherHistoryPageController> {
  Future terminarAulas(ProfessorPessoaDto professor) async {
    Get.defaultDialog(
        title: "Terminar aulas",
        backgroundColor: Colors.white,
        content: Text(
          "Deseja indicar o termino das aulas com o professor ${professor.nome}, na academia ${professor.nmAcademia}?",
        ),
        textConfirm: "Terminar aulas",
        textCancel: "Cancelar",
        confirmTextColor: Colors.white,
        onConfirm: () async {
          controller.loading.value = true;

          try {
            Navigation.goBack();
            await controller.terminarAula(professor);
            await controller.clearState();
            await controller.initialState();
          } finally {
            controller.loading.value = false;
          }
        });
  }

  Future deletar(ProfessorPessoaDto professor) async {
    Get.defaultDialog(
        title: "Remover da lista",
        backgroundColor: Colors.white,
        content: Text(
          "Deseja remover o professor ${professor.nome} da lista?",
        ),
        textConfirm: "Remover",
        textCancel: "Cancelar",
        confirmTextColor: Colors.white,
        onConfirm: () async {
          controller.loading.value = true;

          try {
            Navigation.goBack();
            await controller.deletarProfessorPessoa(professor);
            await controller.clearState();
            await controller.initialState();
          } finally {
            controller.loading.value = false;
          }
        });
  }

  Widget _teacherSection(ProfessorPessoaDto professor, Midia? fotoProfessor) {
    final DateFormat formatter = DateFormat('dd/MM/yyyy');
    final String dtInicioStr = formatter.format(professor.dtInicio!);
    final String dtFimStr = professor.dtFim != null
        ? formatter.format(professor.dtFim!)
        : 'Atualmente';
    return Container(
      padding: const EdgeInsets.only(top: 20, bottom: 20),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          Column(children: [
            Builder(builder: (_) {
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

              return ImageCard(
                backgroundColor: Colors.grey,
                child: presentationWidget,
              );
            }),
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
                Text(
                  "$dtInicioStr - $dtFimStr",
                  style: const TextStyle(color: Colors.white),
                  textAlign: TextAlign.center,
                ),
                Obx(
                  () {
                    if (controller.professorEdicao.value == null) {
                      return InkWell(
                        onTap: () {
                          controller.professorEdicao.value = professor;
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
                        if (professor.dtFim == null)
                          Expanded(
                              child: InkWell(
                            onTap: () async {
                              await terminarAulas(professor);
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
                                      "Terminar aulas",
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
                            await deletar(professor);
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
                          onTap: () {
                            controller.professorEdicao.value = null;
                          },
                          child: const Column(
                            children: [
                              Icon(
                                Icons.cancel,
                                color: Color.fromRGBO(255, 255, 255, 1),
                              ),
                              Text(
                                "Cancelar",
                                style: TextStyle(
                                    color: Colors.white, fontSize: 12),
                              )
                            ],
                          ),
                        ))
                      ],
                    );
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
        title: const Text("Histórico de professores"),
        centerTitle: true,
        leading: IconButton(
            onPressed: () {
              Navigation.popAndGoToPage(pageRoute: profilePageRoute);
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

        if (controller.historicoProfessores.isEmpty) {
          return Center(
            child: CustomButton(
              text: "Selecionar professor",
              type: ButtonType.primary,
              onPressed: () {
                Navigation.popAndGoToPage(pageRoute: teacherSelectionPageRoute);
              },
            ),
          );
        }

        controller.historicoProfessores
            .sort((a, b) => -a.dtInicio!.compareTo(b.dtFim!));

        return Column(
          children: [
            Expanded(
                child: SingleChildScrollView(
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 20),
                child: ListView.builder(
                    itemCount: controller.historicoProfessores.length,
                    physics: const ClampingScrollPhysics(),
                    shrinkWrap: true,
                    scrollDirection: Axis.vertical,
                    itemBuilder: (BuildContext context, int index) {
                      var professor =
                          controller.historicoProfessores.elementAt(index);

                      var fotoProfessor = professor.idFoto != null
                          ? mediaController.getMedia(professor.idFoto!)
                          : null;

                      return Column(
                        children: [
                          _teacherSection(professor, fotoProfessor),
                          if (index <
                              controller.historicoProfessores.length - 1)
                            const CustomDivider(),
                        ],
                      );
                    }),
              ),
            )),
            Align(
                alignment: Alignment.bottomCenter,
                child: Row(
                  children: [
                    Expanded(
                        child: Padding(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 10, vertical: 20),
                      child: CustomButton(
                        text: "Selecionar novo professor",
                        type: ButtonType.primary,
                        onPressed: () {
                          Navigation.popAndGoToPage(
                              pageRoute: teacherSelectionPageRoute);
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
