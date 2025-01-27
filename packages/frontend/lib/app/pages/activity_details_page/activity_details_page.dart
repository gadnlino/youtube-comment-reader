import 'package:flutter/material.dart';
import 'package:frontend/app/common/components/custom_app_bar.dart';
import 'package:frontend/app/common/components/custom_bottom_navigation_bar.dart';
import 'package:frontend/app/common/components/custom_button.dart';
import 'package:frontend/app/common/utils/navigation.dart';
import 'package:frontend/app/pages/activities_page/activities_page.dart';
import 'package:frontend/app/pages/activity_attendance_list_page/activity_attendance_list_page.dart';
import 'package:frontend/app/pages/feed_page/feed_page.dart';

const String activityDetailsPageRoute = "/activity-details";

class ActivityDetailsPage extends StatelessWidget {
  const ActivityDetailsPage({super.key});

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
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Stack(
                      children: [
                        Image.network(
                          "https://thefitnessphantom.com/wp-content/uploads/2023/02/Full-Body-Workout.jpg",
                          fit: BoxFit.cover,
                          height: 244,
                          width: double.infinity,
                        ),
                        Container(
                          padding:
                              EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              IconButton(
                                  onPressed: () {
                                    Navigation.popAndGoToPage(
                                        pageRoute: activitiesPageRoute);
                                  },
                                  icon: Icon(
                                    Icons.arrow_back,
                                    size: 30,
                                    color: Colors.white,
                                  )),
                              Icon(
                                Icons.share,
                                size: 30,
                                color: Colors.white,
                              )
                            ],
                          ),
                        )
                      ],
                    ),
                    Padding(
                      padding:
                          EdgeInsets.symmetric(horizontal: 10, vertical: 10),
                      child: Row(children: [
                        Text(
                          "Atiividade xyz",
                          style: TextStyle(
                              color: Colors.white,
                              fontSize: 25,
                              fontWeight: FontWeight.bold),
                        )
                      ]),
                    ),
                    Padding(
                      padding:
                          EdgeInsets.symmetric(horizontal: 10, vertical: 10),
                      child: Text(
                        "O Lorem Ipsum é um texto modelo da indústria tipográfica e de impressão. O Lorem Ipsum tem vindo a ser o texto padrão usado por estas indústrias desde o ano de 1500, quando uma misturou os caracteres de um texto para criar um espécime de livro. Este texto não só sobreviveu 5 séculos, mas também o salto para a tipografia electrónica, mantendo-se essencialmente inalterada. Foi popularizada nos anos 60 com a disponibilização.",
                        style: TextStyle(color: Colors.white, fontSize: 15),
                      ),
                    ),
                    Padding(
                      padding:
                          EdgeInsets.symmetric(horizontal: 10, vertical: 10),
                      child: Row(children: [
                        Icon(
                          Icons.schedule,
                          color: Colors.white,
                        ),
                        Text(
                          "25/11/2023 - 26/11/2023",
                          style: TextStyle(color: Colors.white, fontSize: 20),
                        )
                      ]),
                    ),
                    Padding(
                      padding:
                          EdgeInsets.symmetric(horizontal: 10, vertical: 10),
                      child: Row(children: [
                        Icon(
                          Icons.attach_money,
                          color: Colors.white,
                        ),
                        Text(
                          "Gratuito",
                          style: TextStyle(color: Colors.white, fontSize: 20),
                        )
                      ]),
                    ),
                    Padding(
                      padding:
                          EdgeInsets.symmetric(horizontal: 10, vertical: 10),
                      child: Row(children: [
                        Icon(
                          Icons.location_pin,
                          color: Colors.white,
                        ),
                        Text(
                          "Arena da Juventude (Arena de Deodoro)",
                          style: TextStyle(color: Colors.white, fontSize: 20),
                        )
                      ]),
                    ),
                    Expanded(
                      child: Align(
                          alignment: Alignment.bottomCenter,
                          child: Row(
                            children: [
                              Expanded(
                                  child: Padding(
                                padding: EdgeInsets.symmetric(
                                    horizontal: 10, vertical: 10),
                                child: CustomButton(
                                  text: "Confirmar",
                                  type: ButtonType.primary,
                                  onPressed: () {
                                    Navigation.popAndGoToPage(
                                        pageRoute: feedPageRoute);
                                  },
                                ),
                              )),
                              Expanded(
                                  child: Padding(
                                padding: EdgeInsets.symmetric(
                                    horizontal: 10, vertical: 10),
                                child: CustomButton(
                                  text: "Lista de presença",
                                  type: ButtonType.primary,
                                  onPressed: () {
                                    Navigation.popAndGoToPage(
                                        pageRoute:
                                            activityAttendanceListPageRoute);
                                  },
                                ),
                              ))
                            ],
                          )),
                    )
                  ],
                ))
          ],
        ));
  }
}
