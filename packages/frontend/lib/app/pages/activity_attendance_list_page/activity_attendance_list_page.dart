import 'package:flutter/material.dart';
import 'package:frontend/app/common/components/custom_app_bar.dart';
import 'package:frontend/app/common/components/custom_bottom_navigation_bar.dart';
import 'package:frontend/app/common/components/custom_button.dart';
import 'package:frontend/app/common/components/custom_cached_network_image.dart';
import 'package:frontend/app/common/utils/navigation.dart';
import 'package:frontend/app/pages/activity_details_page/activity_details_page.dart';

const String activityAttendanceListPageRoute = "/activity-attendance-list";

class ActivityAttendanceListPage extends StatelessWidget {
  const ActivityAttendanceListPage({super.key});

  Widget _studentSection(String name, {String? checkIn}) {
    return Row(
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
            if (checkIn != null)
              Text(checkIn,
                  style: TextStyle(
                    color: Colors.white,
                  ))
          ]),
        )
      ],
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
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      crossAxisAlignment: CrossAxisAlignment.center,
                      children: [
                        IconButton(
                            onPressed: () {
                              Navigation.popAndGoToPage(
                                  pageRoute: activityDetailsPageRoute);
                            },
                            icon: Icon(
                              Icons.arrow_back,
                              size: 25,
                              color: Colors.white,
                            )),
                        Text("Lista de presença",
                            style: TextStyle(
                                color: Colors.white,
                                fontSize: 20,
                                fontWeight: FontWeight.bold)),
                        Icon(
                          Icons.share,
                          size: 25,
                          color: Colors.white,
                        )
                      ],
                    ),
                    Row(mainAxisAlignment: MainAxisAlignment.center, children: [
                      Padding(
                        padding: const EdgeInsets.only(top: 20),
                        child: SizedBox(
                            height: 300,
                            width: 300,
                            child: Align(
                              alignment: Alignment.center,
                              child: CustomCachedNetworkImage(
                                url:
                                    "https://cdn.britannica.com/17/155017-050-9AC96FC8/Example-QR-code.jpg",
                              ),
                            )),
                      )
                    ]),
                    Padding(
                      padding: EdgeInsets.only(top: 20),
                      child: Text(
                          "Solicite que seus alunos atráves do app escaneiem o QR code acima para marcar presença no evento.",
                          style:
                              TextStyle(color: Colors.white, fontSize: 17.5)),
                    ),
                    Padding(
                      padding: EdgeInsets.only(top: 20),
                      child: Row(children: [
                        Text("Alunos presentes",
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
                      child: _studentSection("Guilherme Avelino",
                          checkIn: "Check-in em 17/02/2024 16:03"),
                    ),
                    Padding(
                      padding: EdgeInsets.only(top: 20),
                      child: Row(children: [
                        Text("Alunos inscritos",
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
                      child: _studentSection("Guilherme Avelino",
                          checkIn: "Check-in em 17/02/2024 16:03"),
                    ),
                    Padding(
                      padding: EdgeInsets.only(top: 10),
                      child: _studentSection("Antonio Vinicius"),
                    ),
                    Padding(
                      padding: EdgeInsets.only(top: 10),
                      child: _studentSection("Bruno Cruz"),
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
                                  text: "Confirmar presenças",
                                  type: ButtonType.primary,
                                  onPressed: () {
                                    Navigation.popAndGoToPage(
                                        pageRoute: activityDetailsPageRoute);
                                  },
                                ),
                              )),
                              Expanded(
                                  child: Padding(
                                padding: EdgeInsets.symmetric(
                                    horizontal: 10, vertical: 20),
                                child: CustomButton(
                                  text: "Finalizar atividade",
                                  type: ButtonType.cancel,
                                  onPressed: () {
                                    Navigation.popAndGoToPage(
                                        pageRoute: activityDetailsPageRoute);
                                  },
                                ),
                              ))
                            ],
                          )),
                    )
                  ]),
            ),
          ],
        ));
  }
}
