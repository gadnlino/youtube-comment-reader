import 'package:flutter/material.dart';
import 'package:frontend/app/common/components/image_card.dart';
import 'package:frontend/app/common/models/enums/graduacao_enum.dart';
import 'package:frontend/app/common/models/graduacao.dart';

class RankingCard extends StatelessWidget {
  GraduacaoEnum ranking;
  final double _cardHeight = 200;
  final double _cardWidth = 130;

  RankingCard({super.key, required this.ranking});

  @override
  Widget build(BuildContext context) {
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
          Container(
            height: _cardHeight / 3,
            width: _cardWidth,
            decoration: const BoxDecoration(
                color: Color(0xff939599),
                borderRadius: BorderRadius.only(
                    topLeft: Radius.circular(10),
                    topRight: Radius.circular(10))),
          ),
          Container(
            height: _cardHeight / 3,
            width: _cardWidth,
            decoration: const BoxDecoration(color: Color(0xffffffff)),
          ),
          Container(
            height: _cardHeight / 3,
            width: _cardWidth,
            decoration: const BoxDecoration(
                color: Color(0xff939599),
                borderRadius: BorderRadius.only(
                    bottomLeft: Radius.circular(10),
                    bottomRight: Radius.circular(10))),
          ),
        ]);
        break;
      case GraduacaoEnum.cinza:
        component = Column(children: [
          Container(
            height: _cardHeight,
            width: _cardWidth,
            decoration: const BoxDecoration(
                color: Color(0xff939599),
                borderRadius: BorderRadius.all(
                  Radius.circular(10),
                )),
          ),
        ]);
        break;
      case GraduacaoEnum.cinza_e_preta:
        component = Column(children: [
          Container(
            height: _cardHeight / 3,
            width: _cardWidth,
            decoration: const BoxDecoration(
                color: Color(0xff939599),
                borderRadius: BorderRadius.only(
                    topLeft: Radius.circular(10),
                    topRight: Radius.circular(10))),
          ),
          Container(
            height: _cardHeight / 3,
            width: _cardWidth,
            decoration: const BoxDecoration(color: Color(0xff000000)),
          ),
          Container(
            height: _cardHeight / 3,
            width: _cardWidth,
            decoration: const BoxDecoration(
                color: Color(0xff939599),
                borderRadius: BorderRadius.only(
                    bottomLeft: Radius.circular(10),
                    bottomRight: Radius.circular(10))),
          ),
        ]);
        break;
      case GraduacaoEnum.amarela_e_branca:
        component = Column(children: [
          Container(
            height: _cardHeight / 3,
            width: _cardWidth,
            decoration: const BoxDecoration(
                color: Color(0xffffd300),
                borderRadius: BorderRadius.only(
                    topLeft: Radius.circular(10),
                    topRight: Radius.circular(10))),
          ),
          Container(
            height: _cardHeight / 3,
            width: _cardWidth,
            decoration: const BoxDecoration(color: Color(0xffffffff)),
          ),
          Container(
            height: _cardHeight / 3,
            width: _cardWidth,
            decoration: const BoxDecoration(
                color: Color(0xffffd300),
                borderRadius: BorderRadius.only(
                    bottomLeft: Radius.circular(10),
                    bottomRight: Radius.circular(10))),
          ),
        ]);
        break;
      case GraduacaoEnum.amarela:
        component = Column(children: [
          Container(
            height: _cardHeight,
            width: _cardWidth,
            decoration: const BoxDecoration(
                color: Color(0xffffd300),
                borderRadius: BorderRadius.all(
                  Radius.circular(10),
                )),
          ),
        ]);
        break;
      case GraduacaoEnum.amarela_e_preta:
        component = Column(children: [
          Container(
            height: _cardHeight / 3,
            width: _cardWidth,
            decoration: const BoxDecoration(
                color: Color(0xffffd300),
                borderRadius: BorderRadius.only(
                    topLeft: Radius.circular(10),
                    topRight: Radius.circular(10))),
          ),
          Container(
            height: _cardHeight / 3,
            width: _cardWidth,
            decoration: const BoxDecoration(color: Color(0xff000000)),
          ),
          Container(
            height: _cardHeight / 3,
            width: _cardWidth,
            decoration: const BoxDecoration(
                color: Color(0xffffd300),
                borderRadius: BorderRadius.only(
                    bottomLeft: Radius.circular(10),
                    bottomRight: Radius.circular(10))),
          ),
        ]);
        break;
      case GraduacaoEnum.laranja_e_branca:
        component = Column(children: [
          Container(
            height: _cardHeight / 3,
            width: _cardWidth,
            decoration: const BoxDecoration(
                color: Color(0xfff05b28),
                borderRadius: BorderRadius.only(
                    topLeft: Radius.circular(10),
                    topRight: Radius.circular(10))),
          ),
          Container(
            height: _cardHeight / 3,
            width: _cardWidth,
            decoration: const BoxDecoration(color: Color(0xffffffff)),
          ),
          Container(
            height: _cardHeight / 3,
            width: _cardWidth,
            decoration: const BoxDecoration(
                color: Color(0xfff05b28),
                borderRadius: BorderRadius.only(
                    bottomLeft: Radius.circular(10),
                    bottomRight: Radius.circular(10))),
          ),
        ]);
        break;
      case GraduacaoEnum.laranja:
        component = Column(children: [
          Container(
            height: _cardHeight,
            width: _cardWidth,
            decoration: const BoxDecoration(
                color: Color(0xfff05b28),
                borderRadius: BorderRadius.all(
                  Radius.circular(10),
                )),
          ),
        ]);
        break;
      case GraduacaoEnum.laranja_e_preta:
        component = Column(children: [
          Container(
            height: _cardHeight / 3,
            width: _cardWidth,
            decoration: const BoxDecoration(
                color: Color(0xfff05b28),
                borderRadius: BorderRadius.only(
                    topLeft: Radius.circular(10),
                    topRight: Radius.circular(10))),
          ),
          Container(
            height: _cardHeight / 3,
            width: _cardWidth,
            decoration: const BoxDecoration(color: Color(0xff000000)),
          ),
          Container(
            height: _cardHeight / 3,
            width: _cardWidth,
            decoration: const BoxDecoration(
                color: Color(0xfff05b28),
                borderRadius: BorderRadius.only(
                    bottomLeft: Radius.circular(10),
                    bottomRight: Radius.circular(10))),
          ),
        ]);
        break;
      case GraduacaoEnum.verde_e_branca:
        component = Column(children: [
          Container(
            height: _cardHeight / 3,
            width: _cardWidth,
            decoration: const BoxDecoration(
                color: Color(0xff006838),
                borderRadius: BorderRadius.only(
                    topLeft: Radius.circular(10),
                    topRight: Radius.circular(10))),
          ),
          Container(
            height: _cardHeight / 3,
            width: _cardWidth,
            decoration: const BoxDecoration(color: Color(0xffffffff)),
          ),
          Container(
            height: _cardHeight / 3,
            width: _cardWidth,
            decoration: const BoxDecoration(
                color: Color(0xff006838),
                borderRadius: BorderRadius.only(
                    bottomLeft: Radius.circular(10),
                    bottomRight: Radius.circular(10))),
          ),
        ]);
        break;
      case GraduacaoEnum.verde:
        component = Column(children: [
          Container(
            height: _cardHeight,
            width: _cardWidth,
            decoration: const BoxDecoration(
                color: Color(0xff006838),
                borderRadius: BorderRadius.all(
                  Radius.circular(10),
                )),
          ),
        ]);
        break;
      case GraduacaoEnum.verde_e_preta:
        component = Column(children: [
          Container(
            height: _cardHeight / 3,
            width: _cardWidth,
            decoration: const BoxDecoration(
                color: Color(0xff006838),
                borderRadius: BorderRadius.only(
                    topLeft: Radius.circular(10),
                    topRight: Radius.circular(10))),
          ),
          Container(
            height: _cardHeight / 3,
            width: _cardWidth,
            decoration: const BoxDecoration(color: Color(0xff000000)),
          ),
          Container(
            height: _cardHeight / 3,
            width: _cardWidth,
            decoration: const BoxDecoration(
                color: Color(0xff006838),
                borderRadius: BorderRadius.only(
                    bottomLeft: Radius.circular(10),
                    bottomRight: Radius.circular(10))),
          ),
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
        component = Row(children: [
          Container(
            height: 200,
            width: 65,
            decoration: const BoxDecoration(
                color: Color(0xff000000),
                borderRadius: BorderRadius.only(
                    topLeft: Radius.circular(10),
                    bottomLeft: Radius.circular(10))),
          ),
          Container(
            height: 200,
            width: 65,
            decoration: const BoxDecoration(
                color: Color(0xffff3200),
                borderRadius: BorderRadius.only(
                    topRight: Radius.circular(10),
                    bottomRight: Radius.circular(10))),
          ),
        ]);
        break;
      case GraduacaoEnum.vermelha_e_branca:
        component = Row(children: [
          Container(
            height: 200,
            width: 65,
            decoration: const BoxDecoration(
                color: Color(0xffff3200),
                borderRadius: BorderRadius.only(
                    topLeft: Radius.circular(10),
                    bottomLeft: Radius.circular(10))),
          ),
          Container(
            height: 200,
            width: 65,
            decoration: const BoxDecoration(
                color: Color(0xffffffff),
                borderRadius: BorderRadius.only(
                    topRight: Radius.circular(10),
                    bottomRight: Radius.circular(10))),
          ),
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
}
