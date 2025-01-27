import 'package:flutter/material.dart';
import 'package:frontend/app/common/components/custom_app_bar.dart';
import 'package:frontend/app/common/components/custom_bottom_navigation_bar.dart';
import 'package:frontend/app/common/components/custom_cached_network_image.dart';
import 'package:frontend/app/common/components/custom_divider.dart';

const String feedPageRoute = "/feed";

class FeedPage extends StatelessWidget {
  const FeedPage({super.key});

  Widget _getPostSectionWidget() {
    return Column(
      children: [
        SizedBox(
          child: Stack(children: [
            CustomCachedNetworkImage(
              url:
                  "https://hips.hearstapps.com/hmg-prod/images/gym-workout-weight-training-bodybuilding-muscular-royalty-free-image-1703160802.jpg?crop=1.00xw:1.00xh;0,0&resize=2048:*",
              fit: BoxFit.cover,
              height: 244,
              width: double.infinity,
            ),
            Container(
              margin: const EdgeInsets.all(10),
              child: Row(
                children: [
                  CircleAvatar(
                    radius: 15,
                    backgroundColor: Colors.white,
                    child: Text("GA"),
                  ),
                  Text(
                    "Julia",
                    style: TextStyle(
                        color: Colors.white,
                        fontWeight: FontWeight.bold,
                        fontSize: 15),
                  )
                ],
              ),
            )
          ]),
        ),
        Container(
          padding: EdgeInsetsDirectional.symmetric(horizontal: 5, vertical: 5),
          child: Row(children: [
            const Icon(
              Icons.favorite,
              color: Colors.white,
            ),
            const Icon(
              Icons.comment,
              color: Colors.white,
            ),
            const Icon(
              Icons.share,
              color: Colors.white,
            ),
            Spacer(),
            const Icon(
              Icons.bookmark,
              color: Colors.white,
            )
          ]),
        ),
        Container(
          padding: EdgeInsetsDirectional.symmetric(horizontal: 5, vertical: 5),
          child: Row(children: [
            Text(
              "+999 likes",
              style: TextStyle(color: Color(0xffFFF50A)),
            )
          ]),
        ),
        Container(
          padding:
              const EdgeInsetsDirectional.symmetric(horizontal: 5, vertical: 5),
          child: const Row(
            children: [
              Flexible(
                  child: Text(
                "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the lea",
                style: TextStyle(color: Colors.white),
              ))
            ],
          ),
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: CustomAppBar(),
      bottomNavigationBar: const CustomBottomNavigationBar(),
      body: SingleChildScrollView(
        child: Container(
            padding: EdgeInsets.symmetric(vertical: 5.0),
            child: Column(
              children: [
                _getPostSectionWidget(),
                CustomDivider(),
                _getPostSectionWidget(),
                CustomDivider(),
                _getPostSectionWidget()
              ],
            )),
      ),
    );
  }
}
