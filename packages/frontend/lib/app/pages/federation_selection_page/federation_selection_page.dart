import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:frontend/app/common/components/custom_cached_network_image.dart';
import 'package:frontend/app/common/components/image_card.dart';
import 'package:frontend/app/common/controllers/access_control_controller.dart';
import 'package:frontend/app/common/controllers/federacao_controller.dart';
import 'package:frontend/app/common/controllers/media_controller.dart';
import 'package:frontend/app/common/models/federacao.dart';
import 'package:frontend/app/common/models/midia.dart';
import 'package:frontend/app/common/utils/navigation.dart';
import 'package:frontend/app/pages/profile_page/profile_page.dart';
import 'package:get/get.dart';

const String federationSelectionPageRoute = "/federation-selection";

class FederationSelectionPage extends StatelessWidget {
  FederationSelectionPage({super.key}) {
    (() async {
      var federacaoController = Get.find<FederacaoController>();
      var mediaController = Get.find<MediaController>();

      federacaoController.loading.value = true;

      try {
        await listarFederacoes(federacaoController, mediaController);
      } finally {
        federacaoController.loading.value = false;
      }
    })();
  }

  Future listarFederacoes(FederacaoController federacaoController,
      MediaController mediaController) async {
    var federacoes = await federacaoController.listarFederacoes();

    for (var i = 0; i < federacoes.length; i++) {
      var federacao = federacoes.elementAt(i);

      if (federacao.idLogo != null) {
        await mediaController.storeMedia(federacao.idLogo!);
      }
    }
  }

  Future trocarFederacao(Federacao novaFederacao) async {
    var accessControlController = Get.find<AccessControlController>();
    var federacaoController = Get.find<FederacaoController>();

    Get.defaultDialog(
        title: "Confirmar nova federação",
        backgroundColor: Colors.white,
        content: Text(
          "Deseja atribuir ${novaFederacao.nmFederacao} como sua nova federação?",
        ),
        textConfirm: "Sim",
        textCancel: "Cancelar",
        confirmTextColor: Colors.white,
        onConfirm: () async {
          federacaoController.loading.value = true;

          try {
            Navigation.goBack();
            await federacaoController.trocarFederacao(
                accessControlController.emailPessoaLogada.value, novaFederacao);
            await federacaoController.recarregarInformacoes(
                accessControlController.emailPessoaLogada.value);
          } finally {
            federacaoController.loading.value = false;
          }
        });
  }

  Widget _federationSection(Federacao federacao) {
    var mediaController = Get.find<MediaController>();
    var federacaoController = Get.find<FederacaoController>();

    Widget presentationWidget = Container();

    if (federacao.idLogo != null) {
      Midia logoFederacao = mediaController.getMedia(federacao.idLogo!)!;

      presentationWidget =
          CustomCachedNetworkImage(url: logoFederacao.urlMidia!);
    } else {
      presentationWidget = Center(
        child: Wrap(
          alignment: WrapAlignment.center,
          children: [
            Padding(
              padding: const EdgeInsets.all(5),
              child: Text(
                Federacao.nomeExibicaoFederacao(federacao),
                style: const TextStyle(color: Colors.white, fontSize: 17.5),
                textAlign: TextAlign.center,
              ),
            )
          ],
        ),
      );
    }

    bool ehFederacaoAtiva = federacaoController.federacaoAtiva()?.idFederacao ==
        federacao.idFederacao;

    return Column(
      children: [
        ImageCard(
          backgroundColor: Colors.grey,
          height: 170,
          onPressed: !ehFederacaoAtiva
              ? () async {
                  await trocarFederacao(federacao);
                }
              : null,
          child: presentationWidget,
        ),
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              federacao.nmFederacao.split('-').first.trim(),
              style: const TextStyle(color: Colors.white),
              overflow: TextOverflow.ellipsis,
            ),
            if (ehFederacaoAtiva)
              const Icon(
                Icons.check,
                color: Colors.white,
              )
          ],
        )
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Escolher federação"),
        centerTitle: true,
        leading: IconButton(
            onPressed: () {
              Navigation.popAndGoToPage(pageRoute: profilePageRoute);
            },
            icon: const Icon(Icons.arrow_back)),
      ),
      body: Obx(
        () {
          var federacaoController = Get.find<FederacaoController>();

          if (federacaoController.loading.value) {
            return const Center(
              child: CircularProgressIndicator(
                color: Colors.white,
              ),
            );
          }

          var federacoes = federacaoController.federacoes;

          federacoes.sort((a, b) {
            return Federacao.nomeExibicaoFederacao(a)
                .compareTo(Federacao.nomeExibicaoFederacao(b));
          });

          return SingleChildScrollView(
            child: GridView.count(
              physics: const ClampingScrollPhysics(),
              shrinkWrap: true,
              scrollDirection: Axis.vertical,
              crossAxisCount: 2,
              crossAxisSpacing: 30,
              childAspectRatio: 0.9,
              children: List.generate(
                  federacaoController.federacoes.length,
                  (index) => _federationSection(
                      federacaoController.federacoes.elementAt(index))),
            ),
          );
        },
      ),
    );
  }
}
