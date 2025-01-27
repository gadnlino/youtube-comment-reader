import 'package:flutter/material.dart';
import 'package:frontend/app/common/components/custom_app_bar.dart';
import 'package:frontend/app/common/components/custom_bottom_navigation_bar.dart';
import 'package:frontend/app/common/components/custom_button.dart';

const String pendenciesPageRoute = "/pendencies";

class PendenciesPage extends StatelessWidget {
  const PendenciesPage({super.key});

  Widget _studentSection(
      {required String name,
      required String oldRaking,
      required String newRanking,
      required String date,
      bool selected = false}) {
    return Container(
      decoration: selected ? BoxDecoration(color: Color(0xff215A6F)) : null,
      child: Row(
        children: [
          CircleAvatar(
            radius: 15,
            backgroundColor: Colors.white,
            child: Text("GA"),
          ),
          Padding(
            padding: EdgeInsets.only(left: 10),
            child:
                Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text(name,
                  style: TextStyle(
                      color: Colors.white, fontWeight: FontWeight.bold)),
              Row(
                children: [
                  Text(oldRaking,
                      style: TextStyle(
                        color: Colors.white,
                      )),
                  Icon(
                    Icons.arrow_forward,
                    color: Colors.white,
                    size: 15,
                  ),
                  Text(newRanking,
                      style: TextStyle(
                        color: Colors.white,
                      )),
                ],
              ),
            ]),
          ),
          const Spacer(),
          Padding(
            padding: EdgeInsets.only(right: 10),
            child:
                Text(date, style: TextStyle(color: Colors.white, fontSize: 15)),
          )
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: CustomAppBar(),
        bottomNavigationBar: CustomBottomNavigationBar(),
        body: CustomScrollView(
          slivers: [
            SliverFillRemaining(
              hasScrollBody: false,
              child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Padding(
                      padding: EdgeInsets.only(top: 20),
                      child: Row(children: [
                        Text("Avançar ranking",
                            style: TextStyle(
                                color: Colors.white,
                                fontSize: 20,
                                fontWeight: FontWeight.bold)),
                        Icon(
                          Icons.expand_less,
                          color: Colors.white,
                        )
                      ]),
                    ),
                    Padding(
                      padding: EdgeInsets.only(top: 10),
                      child: _studentSection(
                          name: "Guilherme Avelino",
                          oldRaking: "AZUL",
                          newRanking: "ROXA",
                          date: "16/02/2024"),
                    ),
                    Padding(
                      padding: EdgeInsets.only(top: 10),
                      child: _studentSection(
                          name: "Guilherme Avelino",
                          oldRaking: "AZUL",
                          newRanking: "ROXA",
                          date: "16/02/2024",
                          selected: true),
                    ),
                    Expanded(
                      child: Align(
                          alignment: Alignment.bottomCenter,
                          child: Row(
                            children: [
                              Expanded(
                                  child: Padding(
                                padding: EdgeInsets.symmetric(
                                    horizontal: 10, vertical: 20),
                                child: CustomButton(
                                  text: "Aprovar selecionados",
                                  type: ButtonType.primary,
                                  onPressed: () {},
                                ),
                              )),
                              Expanded(
                                  child: Padding(
                                padding: EdgeInsets.symmetric(
                                    horizontal: 10, vertical: 20),
                                child: CustomButton(
                                  text: "Reprovar selecionados",
                                  type: ButtonType.cancel,
                                  onPressed: () {},
                                ),
                              ))
                            ],
                          )),
                    )
                  ]),
            )
          ],
        ));
  }
}
