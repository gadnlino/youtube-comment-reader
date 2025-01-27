import 'dart:convert';
import 'dart:ffi';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:frontend/app/common/api/bjj_api.dart';
import 'package:frontend/app/common/components/custom_cached_network_image.dart';
import 'package:frontend/app/common/components/image_card.dart';
import 'package:frontend/app/common/controllers/academia_controller.dart';
import 'package:frontend/app/common/controllers/access_control_controller.dart';
import 'package:frontend/app/common/controllers/federacao_controller.dart';
import 'package:frontend/app/common/controllers/media_controller.dart';
import 'package:frontend/app/common/models/academia.dart';
import 'package:frontend/app/common/models/dto/pessoa_academia_dto.dart';
import 'package:frontend/app/common/models/dto/pessoa_federacao_dto.dart';
import 'package:frontend/app/common/models/dto/professor_pessoa_dto.dart';
import 'package:frontend/app/common/models/federacao.dart';
import 'package:frontend/app/common/models/midia.dart';
import 'package:frontend/app/common/models/pessoa.dart';
import 'package:frontend/app/common/utils/navigation.dart';
import 'package:frontend/app/common/utils/utils.dart';
import 'package:frontend/app/pages/federation_selection_page/federation_selection_page.dart';
import 'package:frontend/app/pages/feed_page/feed_page.dart';
import 'package:frontend/app/pages/gym_history_page/gym_history_page.dart';
import 'package:frontend/app/pages/login_page/login_page.dart';
import 'package:frontend/app/pages/ranking_history_page/ranking_history_page.dart';
import 'package:frontend/app/pages/teacher_history_page/teacher_history_page.dart';
import 'package:frontend/app/pages/teacher_selection_page/teacher_selection_page.dart';
import 'package:frontend/app/pages/user_registration_page/user_registration_page.dart';
import 'package:get/get.dart';
import 'package:intl/intl.dart';

const String profilePageRoute = "/profile";

class ProfilePageBinding implements Bindings {
  @override
  void dependencies() {
    Get.lazyPut(() => ProfilePageController());
  }
}

class ProfilePageController extends GetxController {
  final _bjjApi = BjjApi();
  Rx<bool> loading = Rx(false);
  Rxn<ProfessorPessoaDto> professorPessoa = Rxn(null);
  RxList<PessoaAcademiaDto> academiasPessoa = RxList();
  RxList<PessoaFederacaoDto> federacoesPessoa = RxList();

  final _accessControlController = Get.find<AccessControlController>();
  final _mediaController = Get.find<MediaController>();

  @override
  void onInit() {
    (() async {
      try {
        loading.value = true;
        var futures = <Future>[];

        futures.add(_loadAcademiasPessoa());

        futures.add(_loadFederacoesPessoa());

        futures.add(_loadHistoricoProfessoresPessoa());

        await Future.wait(futures);
      } finally {
        loading.value = false;
      }
    })();
    super.onInit();
  }

  _loadAcademiasPessoa() async {
    academiasPessoa.value = await _bjjApi.listarAcademiasPessoa(
        _accessControlController.pessoaLogada.value!.email!);

    if (academiasPessoa.isNotEmpty) {
      await _mediaController.storeMedia(academiasPessoa.first.idLogo!);
    }
  }

  _loadFederacoesPessoa() async {
    federacoesPessoa.value = await _bjjApi.listarFederacoesPessoa(
        _accessControlController.pessoaLogada.value!.email!);

    if (federacoesPessoa.isNotEmpty && federacoesPessoa.first.idLogo != null) {
      await _mediaController.storeMedia(federacoesPessoa.first.idLogo!);
    }
  }

  _loadHistoricoProfessoresPessoa() async {
    var listaHistoricoProfessores =
        await _bjjApi.listarHistoricoProfessoresPessoa(
            _accessControlController.pessoaLogada.value!.email!);

    var professor = listaHistoricoProfessores.isNotEmpty
        ? listaHistoricoProfessores.first
        : null;

    if (professor != null) {
      professorPessoa.value = professor;

      if (professor.idFoto != null) {
        await _mediaController.storeMedia(professor.idFoto!);
      }
    }
  }
}

class ProfilePage extends GetView<ProfilePageController> {
  final _accessControlController = Get.find<AccessControlController>();
  final _mediaController = Get.find<MediaController>();
  final String pageTitle = "Perfil";

  Widget _buildAvatarWidget(Pessoa pessoa, Midia? fotoPessoa) {
    Widget? child;
    NetworkImage? backgroundImage;

    if (fotoPessoa == null || fotoPessoa.urlMidia == null) {
      child = Text(pessoa.nome != null
          ? Utils.getNameInitials(pessoa.nome as String)
          : "");
    } else {
      backgroundImage = NetworkImage(fotoPessoa.urlMidia as String);
    }

    return CircleAvatar(
      backgroundColor: Colors.white,
      backgroundImage: backgroundImage,
      radius: 40,
      child: child,
    );
  }

  Widget _profileInfosSection() {
    return Obx(
      () {
        return Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            _buildAvatarWidget(
                _accessControlController.pessoaLogada.value!,
                _accessControlController.pessoaLogada.value!.idFoto != null
                    ? _mediaController.midias[
                        _accessControlController.pessoaLogada.value!.idFoto]
                    : null),
            Flexible(
                child: Wrap(
              alignment: WrapAlignment.center,
              children: [
                Column(
                  children: [
                    Text(
                      _accessControlController.pessoaLogada.value!.nome ?? "",
                      style:
                          const TextStyle(color: Colors.white, fontSize: 17.5),
                      textAlign: TextAlign.center,
                    ),
                    Builder(
                      builder: (_) {
                        Widget result = Container();

                        if (_accessControlController
                                .pessoaLogada.value!.dtNascimento !=
                            null) {
                          result = Text(
                            DateFormat("dd/MM/yyyy").format(
                                _accessControlController.pessoaLogada.value!
                                    .dtNascimento as DateTime),
                            style: const TextStyle(
                                color: Colors.white, fontSize: 17.5),
                            textAlign: TextAlign.center,
                          );
                        }
                        return result;
                      },
                    ),
                    Builder(
                      builder: (_) {
                        Widget result = Container();

                        if (_accessControlController
                                .pessoaLogada.value!.endereco !=
                            null) {
                          result = Text(
                            _accessControlController
                                    .pessoaLogada.value!.endereco ??
                                "",
                            style: const TextStyle(
                              color: Colors.white,
                            ),
                            textAlign: TextAlign.center,
                          );
                        }

                        return result;
                      },
                    )
                  ],
                ),
              ],
            )),
            InkWell(
              child: const Icon(
                Icons.edit,
                color: Colors.white,
              ),
              onTap: () {
                Navigation.popAndGoToPage(
                    pageRoute: userRegistrationPageRoute,
                    parameters: {
                      'mode': 'editor',
                    });
              },
            )
          ],
        );
      },
    );
  }

  Widget _gymSection() {
    Widget presentationWidget = Container();

    presentationWidget = Column(
      children: [
        const Text(
          "Academia",
          style: TextStyle(color: Colors.white, fontSize: 17.5),
        ),
        Obx(() {
          var academiaPessoa = controller.academiasPessoa.firstOrNull;
          var urlLogoAcademia = academiaPessoa != null &&
                  academiaPessoa.idLogo != null &&
                  _mediaController.getMedia(academiaPessoa.idLogo) != null
              ? _mediaController.getMedia(academiaPessoa.idLogo)?.urlMidia
              : null;

          return ImageCard(
            backgroundColor: Colors.grey,
            onPressed: () {
              Navigation.popAndGoToPage(pageRoute: gymHistoryPageRoute);
            },
            child: urlLogoAcademia != null
                ? CustomCachedNetworkImage(url: urlLogoAcademia)
                : const Center(
                    child: Wrap(
                      alignment: WrapAlignment.center,
                      children: [
                        Padding(
                          padding: EdgeInsets.all(5),
                          child: Text(
                            "Escolha uma academia",
                            style:
                                TextStyle(color: Colors.white, fontSize: 17.5),
                            textAlign: TextAlign.center,
                          ),
                        )
                      ],
                    ),
                  ),
          );
        })
      ],
    );

    return presentationWidget;
  }

  Widget _rankingSection() {
    Widget presentationWidget = Container();

    presentationWidget = Column(
      children: [
        const Text(
          "Ranking",
          style: TextStyle(color: Colors.white, fontSize: 17.5),
        ),
        ImageCard(
          backgroundColor: Colors.blueGrey,
          onPressed: () {
            Navigation.popAndGoToPage(pageRoute: rankingHistoryPageRoute);
          },
          child: const Center(
            child: Wrap(
              alignment: WrapAlignment.center,
              children: [
                Padding(
                  padding: EdgeInsets.all(5),
                  child: Text(
                    "Clique para visualizar",
                    style: TextStyle(color: Colors.white, fontSize: 17.5),
                    textAlign: TextAlign.center,
                  ),
                )
              ],
            ),
          ),
        )
      ],
    );

    return presentationWidget;
  }

  Widget _teacherSection() {
    Widget presentationWidget = Container();

    presentationWidget = Column(
      children: [
        const Text(
          "Professor",
          style: TextStyle(color: Colors.white, fontSize: 17.5),
        ),
        Obx(
          () {
            Widget? innerWidget;

            if (_accessControlController.pessoaLogada.value!.idProfessor ==
                null) {
              innerWidget = const Center(
                child: Wrap(
                  alignment: WrapAlignment.center,
                  children: [
                    Padding(
                      padding: EdgeInsets.all(5),
                      child: Text(
                        "Selecione um professor",
                        style: TextStyle(color: Colors.white, fontSize: 17.5),
                        textAlign: TextAlign.center,
                      ),
                    )
                  ],
                ),
              );
            } else {
              Widget? child;
              NetworkImage? backgroundImage;

              Midia? fotoProfessor =
                  controller.professorPessoa.value!.idFoto != null
                      ? _mediaController
                          .getMedia(controller.professorPessoa.value!.idFoto)
                      : null;

              if (fotoProfessor != null) {
                backgroundImage = NetworkImage(fotoProfessor.urlMidia!);
              } else {
                child = Text(controller.professorPessoa.value!.nome != null
                    ? controller.professorPessoa.value!.nome!
                    : "");
              }

              innerWidget = CircleAvatar(
                backgroundColor: Colors.white,
                backgroundImage: backgroundImage,
                radius: 30,
                child: child,
              );
            }

            return ImageCard(
              backgroundColor: Colors.blueGrey,
              onPressed: () {
                Navigation.popAndGoToPage(pageRoute: teacherHistoryPageRoute);
              },
              child: innerWidget,
            );
          },
        )
      ],
    );

    return presentationWidget;
  }

  Widget _federationSection() {
    Widget presentationWidget = Container();

    presentationWidget = Column(
      children: [
        const Text(
          "Federação",
          style: TextStyle(color: Colors.white, fontSize: 17.5),
        ),
        Obx(
          () {
            Widget? innerWidget;

            var federacao = controller.federacoesPessoa
                .where((p0) => p0.dtInicio != null && p0.dtFim == null)
                .firstOrNull;

            var federacaoAtiva =
                federacao != null ? Federacao.fromDto(federacao) : null;

            if (federacaoAtiva == null) {
              innerWidget = const Center(
                child: Wrap(
                  alignment: WrapAlignment.center,
                  children: [
                    Padding(
                      padding: EdgeInsets.all(5),
                      child: Text(
                        "Escolha uma federação",
                        style: TextStyle(color: Colors.white, fontSize: 17.5),
                        textAlign: TextAlign.center,
                      ),
                    )
                  ],
                ),
              );
            } else if (federacaoAtiva.idLogo != null &&
                _mediaController.getMedia(federacaoAtiva.idLogo) != null) {
              var urlLogoFederacao =
                  _mediaController.getMedia(federacaoAtiva.idLogo)?.urlMidia;

              innerWidget = CustomCachedNetworkImage(url: urlLogoFederacao!);
            } else {
              innerWidget = Center(
                child: Wrap(
                  alignment: WrapAlignment.center,
                  children: [
                    Padding(
                      padding: const EdgeInsets.all(5),
                      child: Text(
                        Federacao.nomeExibicaoFederacao(federacaoAtiva),
                        style: const TextStyle(
                            color: Colors.white, fontSize: 17.5),
                        textAlign: TextAlign.center,
                      ),
                    )
                  ],
                ),
              );
            }

            return ImageCard(
              backgroundColor: Colors.blueGrey,
              onPressed: () {
                Navigation.popAndGoToPage(
                    pageRoute: federationSelectionPageRoute);
              },
              child: innerWidget,
            );
          },
        )
      ],
    );

    return presentationWidget;
  }

  void _logout() async {
    var accessControlController = Get.find<AccessControlController>();

    Get.defaultDialog(
        title: "",
        backgroundColor: Colors.white,
        content: const Text(
          "Deseja mesmo sair do app?",
        ),
        textConfirm: "Sim",
        textCancel: "Não, voltar",
        confirmTextColor: Colors.white,
        onConfirm: () async {
          await accessControlController.doLogout();
        });
  }

  @override
  Widget build(BuildContext context) {
    var menus = [
      _gymSection(),
      _federationSection(),
      _rankingSection(),
      _teacherSection()
    ];

    return Scaffold(
      appBar: AppBar(
        title: Text(pageTitle),
        centerTitle: true,
        leading: IconButton(
            onPressed: () {
              Navigation.popAndGoToPage(pageRoute: feedPageRoute);
            },
            icon: const Icon(Icons.arrow_back)),
        actions: [
          InkWell(
            onTap: _logout,
            child: const Icon(Icons.logout),
          )
        ],
      ),
      body: SingleChildScrollView(
          child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 20),
              child: Column(
                children: [
                  Container(
                    padding: const EdgeInsets.only(
                      top: 20,
                    ),
                    child: _profileInfosSection(),
                  ),
                  Container(
                    padding: const EdgeInsets.only(
                      top: 20,
                    ),
                    child: GridView.count(
                      physics: const ClampingScrollPhysics(),
                      shrinkWrap: true,
                      scrollDirection: Axis.vertical,
                      crossAxisCount: 2,
                      childAspectRatio: 0.75,
                      children: menus,
                    ),
                  ),
                ],
              ))),
    );
  }
}
