import 'package:flutter/material.dart';
import 'package:frontend/app/common/components/custom_app_bar.dart';
import 'package:frontend/app/common/components/custom_bottom_navigation_bar.dart';
import 'package:frontend/app/common/components/custom_cached_network_image.dart';

const String eventsPageRoute = "/events";

class EventsPage extends StatelessWidget {
  const EventsPage({super.key});

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
                crossAxisAlignment: CrossAxisAlignment.start,
                children: <Widget>[
                  Padding(
                    padding: EdgeInsets.only(top: 20, left: 10),
                    child: Text(
                      'Campeonatos',
                      style: TextStyle(
                          fontSize: 20,
                          color: Colors.white,
                          fontWeight: FontWeight.bold),
                    ),
                  ),
                  Padding(
                    padding: EdgeInsets.only(top: 10),
                    child: SizedBox(
                      height: 175.0,
                      child: ListView.builder(
                        physics: const ClampingScrollPhysics(),
                        shrinkWrap: true,
                        scrollDirection: Axis.horizontal,
                        itemCount: 15,
                        itemBuilder: (BuildContext context, int index) =>
                            Padding(
                          padding: EdgeInsets.symmetric(horizontal: 7.5),
                          child: InkWell(
                              child: Card(
                            elevation: 5.0,
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(10.0),
                            ),
                            child: Container(
                              padding: EdgeInsets.all(10.0),
                              child: ClipRRect(
                                borderRadius: BorderRadius.circular(10.0),
                                child: CustomCachedNetworkImage(
                                    url:
                                        'https://img.freepik.com/fotos-gratis/homem-de-vista-lateral-pulando-ao-ar-livre_23-2149557835.jpg'),
                              ),
                            ),
                          )),
                        ),
                      ),
                    ),
                  ),
                  Padding(
                    padding: EdgeInsets.only(top: 20, left: 10, right: 10),
                    child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text(
                            'Aulas',
                            style: TextStyle(
                                fontSize: 20,
                                color: Colors.white,
                                fontWeight: FontWeight.bold),
                          ),
                          Text(
                            'Ver mais',
                            style: TextStyle(
                              fontSize: 20,
                              color: Colors.white60,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ]),
                  ),
                  Padding(
                    padding: EdgeInsets.only(top: 10),
                    child: SizedBox(
                      height: 175.0,
                      child: ListView.builder(
                        physics: const ClampingScrollPhysics(),
                        shrinkWrap: true,
                        scrollDirection: Axis.horizontal,
                        itemCount: 15,
                        itemBuilder: (BuildContext context, int index) =>
                            Padding(
                          padding: EdgeInsets.symmetric(horizontal: 7.5),
                          child: Card(
                            elevation: 5.0,
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(10.0),
                            ),
                            child: Container(
                              padding: EdgeInsets.all(10.0),
                              child: ClipRRect(
                                borderRadius: BorderRadius.circular(10.0),
                                child: CustomCachedNetworkImage(
                                    url:
                                        'https://www.dmoose.com/cdn/shop/articles/Main_Image_c34524b2-86f3-4c60-92fa-2e9d67beccf5.jpg?v=1668438961'),
                              ),
                            ),
                          ),
                        ),
                      ),
                    ),
                  ),
                  Padding(
                    padding: EdgeInsets.only(top: 20, left: 10, right: 10),
                    child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text(
                            'Cursos',
                            style: TextStyle(
                                fontSize: 20,
                                color: Colors.white,
                                fontWeight: FontWeight.bold),
                          ),
                          Text(
                            'Ver mais',
                            style: TextStyle(
                              fontSize: 20,
                              color: Colors.white60,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ]),
                  ),
                  Padding(
                    padding: EdgeInsets.only(top: 10),
                    child: SizedBox(
                      height: 175.0,
                      child: ListView.builder(
                        physics: const ClampingScrollPhysics(),
                        shrinkWrap: true,
                        scrollDirection: Axis.horizontal,
                        itemCount: 15,
                        itemBuilder: (BuildContext context, int index) =>
                            Padding(
                          padding: EdgeInsets.symmetric(horizontal: 7.5),
                          child: Card(
                            elevation: 5.0,
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(10.0),
                            ),
                            child: Container(
                              padding: EdgeInsets.all(10.0),
                              child: ClipRRect(
                                borderRadius: BorderRadius.circular(10.0),
                                child: CustomCachedNetworkImage(
                                    url:
                                        'https://www.verywellfit.com/thmb/Xio5I7FgQh0GRwhS6qWAio3amOM=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/Pushups-5680bb925f9b586a9edf3927.jpg'),
                              ),
                            ),
                          ),
                        ),
                      ),
                    ),
                  ),
                  Padding(
                    padding: EdgeInsets.only(top: 20, left: 10, right: 10),
                    child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text(
                            'Descubra',
                            style: TextStyle(
                                fontSize: 20,
                                color: Colors.white,
                                fontWeight: FontWeight.bold),
                          ),
                          Text(
                            'Ver mais',
                            style: TextStyle(
                              fontSize: 20,
                              color: Colors.white60,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ]),
                  ),
                  Padding(
                    padding: EdgeInsets.only(top: 10),
                    child: SizedBox(
                      height: 175.0,
                      child: ListView.builder(
                        physics: const ClampingScrollPhysics(),
                        shrinkWrap: true,
                        scrollDirection: Axis.horizontal,
                        itemCount: 15,
                        itemBuilder: (BuildContext context, int index) =>
                            Padding(
                          padding: EdgeInsets.symmetric(horizontal: 7.5),
                          child: Card(
                            elevation: 5.0,
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(10.0),
                            ),
                            child: Container(
                              padding: EdgeInsets.all(10.0),
                              child: ClipRRect(
                                borderRadius: BorderRadius.circular(10.0),
                                child: CustomCachedNetworkImage(
                                    url:
                                        'https://imgix.bustle.com/uploads/getty/2023/2/13/f1af72e8-5e6b-45fc-86fd-878d06ea8efa-getty-1462488269.jpg?w=800&fit=crop&crop=focalpoint&auto=format%2Ccompress&fp-x=0.404&fp-y=0.458'),
                              ),
                            ),
                          ),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            )
          ],
        ));
  }
}
