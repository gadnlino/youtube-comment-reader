import 'dart:convert';
import 'dart:io';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:frontend/app/common/api/bjj_api.dart';
import 'package:frontend/app/common/components/custom_button.dart';
import 'package:frontend/app/common/components/custom_cached_network_image.dart';
import 'package:frontend/app/common/components/custom_divider.dart';
import 'package:frontend/app/common/components/image_card.dart';
import 'package:frontend/app/common/controllers/academia_controller.dart';
import 'package:frontend/app/common/controllers/access_control_controller.dart';
import 'package:frontend/app/common/controllers/federacao_controller.dart';
import 'package:frontend/app/common/controllers/media_controller.dart';
import 'package:frontend/app/common/models/academia.dart';
import 'package:frontend/app/common/models/enums/tipo_midia_enum.dart';
import 'package:frontend/app/common/models/federacao.dart';
import 'package:frontend/app/common/models/midia.dart';
import 'package:frontend/app/common/models/pessoa.dart';
import 'package:frontend/app/common/packages/image_picker_package.dart';
import 'package:frontend/app/common/utils/navigation.dart';
import 'package:frontend/app/common/utils/utils.dart';
import 'package:frontend/app/pages/federation_selection_page/federation_selection_page.dart';
import 'package:frontend/app/pages/feed_page/feed_page.dart';
import 'package:frontend/app/pages/gym_history_page/gym_history_page.dart';
import 'package:frontend/app/pages/login_page/login_page.dart';
import 'package:frontend/app/pages/profile_page/profile_page.dart';
import 'package:frontend/app/pages/ranking_history_page/ranking_history_page.dart';
import 'package:frontend/app/pages/teacher_selection_page/teacher_selection_page.dart';
import 'package:get/get.dart';
import 'package:intl/intl.dart';
import 'package:mime/mime.dart';

const String userRegistrationPageRoute = "/user-registration";

class UserRegistrationBinding implements Bindings {
  @override
  void dependencies() {
    Get.lazyPut(() => UserRegistrationPageController());
  }
}

class UserRegistrationPageController extends GetxController {
  final _bjjApi = BjjApi();
  final _accessControlController = Get.find<AccessControlController>();
  final _mediaController = Get.find<MediaController>();
  final _academiaController = Get.find<AcademiaController>();
  final loginFormKey = GlobalKey<FormState>();

  Rx<bool> editorMode = Rx<bool>(false);
  Rx<String> email = Rx<String>('');
  Rxn<String> emailErrorText = Rxn<String>(null);
  Rx<String> nome = Rx<String>('');
  Rxn<String> nomeErrorText = Rxn<String>(null);
  Rx<DateTime> dtNascimento = Rx<DateTime>(DateTime(1900));
  Rxn<String> dtNascimentoErrorText = Rxn<String>(null);
  Rxn<File> fotoPessoa = Rxn<File>(null);
  Rx<bool> souProfessor = Rx<bool>(false);
  Rx<bool> isValid = Rx<bool>(false);
  Rx<bool> loading = Rx<bool>(false);
  RxList<Academia> academiasDisponiveis = RxList();
  RxList<Academia> academiasSelecionadas = RxList();

  @override
  void onInit() {
    debounce<String>(nome, nomeValidations,
        time: const Duration(milliseconds: 500));
    debounce<DateTime>(dtNascimento, dtNascimentoValidations,
        time: const Duration(milliseconds: 500));

    ever(souProfessor, (newValue) {
      if (newValue) {
        (() async {
          try {
            loading.value = true;

            await listarAcademias();
          } finally {
            loading.value = false;
          }
        })();
      }
    });

    email.value = _accessControlController.emailPessoaLogada.value;
    nome.value = _accessControlController.nomePessoaLogada.value;
    dtNascimento.value =
        _accessControlController.pessoaLogada.value?.dtNascimento != null
            ? _accessControlController.pessoaLogada.value!.dtNascimento!
            : DateTime.now().toUtc();

    if (_accessControlController.urlFotoPessoaLogada.isNotEmpty &&
        _accessControlController.urlFotoPessoaLogada.value != '' &&
        _accessControlController.arquivoFotoPessoa.value == null) {
      (() async {
        File f = await downloadFotoPessoa(
            _accessControlController.urlFotoPessoaLogada.value);
        fotoPessoa.value = f;
      })();
    }

    super.onInit();
  }

  Future<File> downloadFotoPessoa(String url) async {
    await _mediaController.downloadAndStoreFileFromUrl(url);

    return await _mediaController.getDownloadedFileMedia(url);
  }

  void nomeValidations(String val) async {
    debugPrint('Validando nome');
    nomeErrorText.value = null;
    isValid.value = false;
    if (val.isNotEmpty) {
      if (val.length < 2) {
        nomeErrorText.value = 'O nome digitado é muito curto';
      } else {
        nomeErrorText.value = null;
        isValid.value = true;
      }
    } else {
      nomeErrorText.value = 'O nome deve ser preenchido';
    }
  }

  void dtNascimentoValidations(DateTime val) async {
    debugPrint('Validando dtNascimento');
    dtNascimentoErrorText.value = null;
    isValid.value = false;

    final today = DateTime.now();
    if (!(val.compareTo(DateTime(1900)) > 0 && val.compareTo(today) < 0)) {
      dtNascimentoErrorText.value = 'A data de nascimento é inválida';
    } else {
      dtNascimentoErrorText.value = null;
      isValid.value = true;
    }
  }

  Future<bool> criarPessoa() async {
    debugPrint('Criando pessoa');

    bool result = false;
    loading.value = true;

    try {
      final mediaController = Get.find<MediaController>();
      final accessControlController = Get.find<AccessControlController>();

      int? idFoto;

      if (fotoPessoa.value != null) {
        Midia media = Midia();
        media.idTipoMidia = TipoMidiaEnum.ARQUIVO.index;
        media.nmArquivoMidia = fotoPessoa.value?.uri.pathSegments.last;
        media = await mediaController.uploadMedia(media, fotoPessoa.value!);

        idFoto = media.idMidia;
      }

      Pessoa pessoa = Pessoa(
          nome: nome.value,
          email: email.value,
          dtNascimento: dtNascimento.value,
          idFoto: idFoto);

      await _bjjApi.criarPessoa(pessoa);

      if (academiasSelecionadas.isNotEmpty) {
        for (Academia academia in academiasSelecionadas) {
          await _bjjApi.criarAcademiaPessoa(
              pessoa.email!, academia.idAcademia!, DateTime.now().toUtc(),
              ehProfessor: 'S');
        }
      }

      accessControlController.pessoaLogada.value = pessoa;

      debugPrint('Pessoa criada');

      result = true;
    } finally {
      loading.value = false;
    }

    return result;
  }

  Future adicionarAcademiaPessoa(Academia academia) async {
    await _academiaController.criarAcademiaPessoa(
        _accessControlController.emailPessoaLogada.value,
        academia.idAcademia!,
        DateTime.now());
    await listarAcademias();
  }

  Future listarAcademias() async {
    academiasDisponiveis.value = await _academiaController.listarAcademias();

    for (var i = 0; i < academiasDisponiveis.length; i++) {
      var academia = academiasDisponiveis.elementAt(i);
      if (academia.idLogo != null) {
        await _mediaController.storeMedia(academia.idLogo!);
      }
    }
  }
}

class UserRegistrationPage extends GetView<UserRegistrationPageController> {
  final String pageTitle = "Suas informações";
  final ImagePickerPackage _imagePickerPackage = ImagePickerPackage();
  final AccessControlController _accessControlController =
      Get.find<AccessControlController>();

  UserRegistrationPage({super.key}) {
    String? mode =
        Get.parameters.containsKey('mode') ? Get.parameters['mode'] : null;

    if (mode != null && mode.isNotEmpty && mode == "editor") {
      controller.editorMode.value = true;
      controller.fotoPessoa.value =
          _accessControlController.arquivoFotoPessoa.value;
    }
  }

  Widget _buildSelectedImageWidget(String? nomePessoa, File? fotoPessoa) {
    Widget? child;
    dynamic backgroundImage;
    double radius = 80;

    if (fotoPessoa == null) {
      child = Text(
        nomePessoa != null ? Utils.getNameInitials(nomePessoa) : "",
        style: const TextStyle(fontSize: 40),
      );
    } else {
      backgroundImage = Image.file(
        fotoPessoa,
        fit: BoxFit.cover,
      ).image;
    }

    return CircleAvatar(
      radius: radius,
      backgroundColor: Colors.white,
      child: CircleAvatar(
        radius: radius,
        backgroundColor: Colors.white,
        backgroundImage: backgroundImage,
        child: child,
      ),
    );
  }

  Widget _buildImageSelectionWidget() {
    List<Widget> children = [];

    if (controller.fotoPessoa.value == null) {
      children = [
        const Icon(
          Icons.camera_alt,
          color: Colors.white,
        ),
        InkWell(
          onTap: () async {
            debugPrint("clicou em selecionar imagem");

            final imagePath = await _imagePickerPackage.pickImage();

            if (imagePath != null) {
              controller.fotoPessoa.value = File(imagePath);
            }
          },
          child: const Text(
            "Selecionar imagem",
            style: TextStyle(color: Colors.white),
          ),
        )
      ];
    } else {
      children = [
        const Icon(
          Icons.cancel,
          color: Colors.white,
        ),
        InkWell(
          onTap: () {
            controller.fotoPessoa.value = null;
          },
          child: const Text(
            "Remover imagem",
            style: TextStyle(color: Colors.white),
          ),
        )
      ];
    }

    return Row(mainAxisAlignment: MainAxisAlignment.center, children: children);
  }

  void _cadastrarPessoa() async {
    var result = await controller.criarPessoa();

    if (result == true) {
      Navigation.popAndGoToPage(pageRoute: feedPageRoute);
    }
  }

  Future _goBack() async {
    if (controller.editorMode.value) {
      Navigation.popAndGoToPage(pageRoute: profilePageRoute);
    } else {
      await _accessControlController.doLogout();
      Navigation.popAndGoToPage(pageRoute: loginPageRoute);
    }
  }

  Widget _gymSection(Academia academia) {
    var mediaController = Get.find<MediaController>();
    var midiaLogoAcademia = mediaController.getMedia(academia.idLogo);
    bool academiaSelecionada = controller.academiasSelecionadas
        .any((element) => element.idAcademia == academia.idAcademia);
    return Container(
      padding: const EdgeInsets.only(top: 20, bottom: 20),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          Column(children: [
            ImageCard(
              backgroundColor: Colors.grey,
              child: midiaLogoAcademia != null
                  ? CustomCachedNetworkImage(url: midiaLogoAcademia.urlMidia!)
                  : null,
            )
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
                  text: academiaSelecionada ? "Selecionado!" : "Selecionar",
                  type: academiaSelecionada
                      ? ButtonType.success
                      : ButtonType.primary,
                  onPressed: () {
                    if (academiaSelecionada) {
                      controller.academiasSelecionadas.value = controller
                          .academiasSelecionadas
                          .where((p0) => p0.idAcademia != academia.idAcademia)
                          .toList();
                    } else {
                      controller.academiasSelecionadas.add(academia);
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
        title: Text(pageTitle),
        centerTitle: true,
        leading:
            IconButton(onPressed: _goBack, icon: const Icon(Icons.arrow_back)),
      ),
      body: Obx(() {
        if (controller.loading.value) {
          return const Center(
            child: CircularProgressIndicator(
              color: Colors.white,
            ),
          );
        }

        return SingleChildScrollView(
            child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 20),
                child: Column(
                  children: [
                    Obx(() {
                      return Container(
                        padding: const EdgeInsets.only(
                          top: 20,
                        ),
                        child: _buildSelectedImageWidget(
                            controller.nome.value, controller.fotoPessoa.value),
                      );
                    }),
                    Container(
                      padding: const EdgeInsets.only(
                        top: 10,
                      ),
                      child: Obx(() => _buildImageSelectionWidget()),
                    ),
                    Container(
                      padding: const EdgeInsets.only(
                        top: 20,
                      ),
                      child: Form(
                        child: Column(
                          children: [
                            Padding(
                              padding: const EdgeInsets.symmetric(vertical: 15),
                              child: Obx(() {
                                return TextFormField(
                                  initialValue: controller.email.value,
                                  readOnly: true,
                                  enabled: false,
                                  style: const TextStyle(
                                      fontSize: 18.0, color: Colors.black),
                                  decoration: InputDecoration(
                                    errorText: controller.emailErrorText.value,
                                    contentPadding: const EdgeInsets.only(
                                        left: 14.0, bottom: 8.0, top: 8.0),
                                    fillColor: Colors.grey,
                                    filled: true,
                                    hintText: 'Seu e-mail',
                                    focusedBorder: OutlineInputBorder(
                                      borderSide:
                                          const BorderSide(color: Colors.white),
                                      borderRadius: BorderRadius.circular(5),
                                    ),
                                    enabledBorder: UnderlineInputBorder(
                                      borderSide:
                                          const BorderSide(color: Colors.white),
                                      borderRadius: BorderRadius.circular(5),
                                    ),
                                  ),
                                );
                              }),
                            ),
                            Padding(
                              padding: const EdgeInsets.symmetric(vertical: 15),
                              child: Obx(() {
                                return TextFormField(
                                  onChanged: (value) =>
                                      controller.nome.value = value,
                                  initialValue: controller.nome.value,
                                  readOnly: false,
                                  style: const TextStyle(
                                      fontSize: 18.0, color: Colors.black),
                                  decoration: InputDecoration(
                                    errorText: controller.nomeErrorText.value,
                                    contentPadding: const EdgeInsets.only(
                                        left: 14.0, bottom: 8.0, top: 8.0),
                                    fillColor: Colors.white,
                                    filled: true,
                                    hintText: 'Seu nome',
                                    focusedBorder: OutlineInputBorder(
                                      borderSide:
                                          const BorderSide(color: Colors.white),
                                      borderRadius: BorderRadius.circular(5),
                                    ),
                                    enabledBorder: UnderlineInputBorder(
                                      borderSide:
                                          const BorderSide(color: Colors.white),
                                      borderRadius: BorderRadius.circular(5),
                                    ),
                                  ),
                                );
                              }),
                            ),
                            Padding(
                              padding: const EdgeInsets.symmetric(vertical: 15),
                              child: Obx(() => TextFormField(
                                    controller: TextEditingController(
                                        text: Utils.formatDateOrNull(
                                            controller.dtNascimento.value,
                                            'dd/MM/yyyy')),
                                    keyboardType: TextInputType.none,
                                    onTap: () async {
                                      final DateTime? dtNascimento =
                                          await showDatePicker(
                                        context: context,
                                        firstDate: DateTime(1900),
                                        lastDate: DateTime.now(),
                                        initialDate:
                                            controller.dtNascimento.value,
                                      );

                                      if (dtNascimento != null) {
                                        controller.dtNascimento.value =
                                            dtNascimento;
                                      }
                                    },
                                    readOnly: false,
                                    style: const TextStyle(
                                        fontSize: 18.0, color: Colors.black),
                                    decoration: InputDecoration(
                                      errorText: controller
                                          .dtNascimentoErrorText.value,
                                      contentPadding: const EdgeInsets.only(
                                          left: 14.0, bottom: 8.0, top: 8.0),
                                      fillColor: Colors.white,
                                      filled: true,
                                      hintText: 'Data de nascimento',
                                      focusedBorder: OutlineInputBorder(
                                        borderSide: const BorderSide(
                                            color: Colors.white),
                                        borderRadius: BorderRadius.circular(5),
                                      ),
                                      enabledBorder: UnderlineInputBorder(
                                        borderSide: const BorderSide(
                                            color: Colors.white),
                                        borderRadius: BorderRadius.circular(5),
                                      ),
                                    ),
                                  )),
                            ),
                            Obx(() => Padding(
                                  padding:
                                      const EdgeInsets.symmetric(vertical: 15),
                                  child: SwitchListTile(
                                    title: const Text(
                                      "Sou professor",
                                      style: TextStyle(color: Colors.white),
                                    ),
                                    value: controller.souProfessor.value,
                                    onChanged: (newValue) {
                                      controller.souProfessor.value = newValue;
                                    },
                                  ),
                                )),
                            Obx(() {
                              if (controller.souProfessor.value) {
                                return Column(
                                  children: [
                                    const Align(
                                      alignment: Alignment.center,
                                      child: Text(
                                        "Selecionar academias",
                                        style: TextStyle(
                                            color: Colors.white,
                                            fontSize: 17.5),
                                      ),
                                    ),
                                    ListView.builder(
                                        itemCount: controller
                                            .academiasDisponiveis.length,
                                        physics: const ClampingScrollPhysics(),
                                        shrinkWrap: true,
                                        scrollDirection: Axis.vertical,
                                        itemBuilder: (BuildContext context,
                                                int index) =>
                                            Column(
                                              children: [
                                                Obx(() => _gymSection(controller
                                                    .academiasDisponiveis
                                                    .elementAt(index))),
                                                if (index <
                                                    controller
                                                            .academiasDisponiveis
                                                            .length -
                                                        1)
                                                  const CustomDivider(),
                                              ],
                                            ))
                                  ],
                                );
                              }

                              return Container();
                            }),
                            Obx(() {
                              return CustomButton(
                                text: controller.editorMode.value
                                    ? "Salvar informações"
                                    : "Cadastrar",
                                type: !controller.loading.value &&
                                        controller.isValid.value
                                    ? ButtonType.primary
                                    : ButtonType.neutral,
                                onPressed: !controller.loading.value &&
                                        controller.isValid.value
                                    ? _cadastrarPessoa
                                    : () {},
                              );
                            })
                          ],
                        ),
                      ),
                    ),
                  ],
                )));
      }),
    );
  }
}
