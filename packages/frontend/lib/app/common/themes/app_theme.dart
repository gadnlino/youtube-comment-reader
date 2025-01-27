import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

const Color appBackgroungColorDarkTheme = Color(0xff062029);

//https://docs.flutter.dev/cookbook/design/themes
ThemeData appThemeData = ThemeData(
    colorScheme: ColorScheme.fromSwatch(primarySwatch: Colors.orange),
    textTheme:
        GoogleFonts.poppinsTextTheme().copyWith(displayMedium: TextStyle()),
    scaffoldBackgroundColor: appBackgroungColorDarkTheme,
    appBarTheme: const AppBarTheme(
        backgroundColor: appBackgroungColorDarkTheme,
        titleTextStyle: TextStyle(
            color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold),
        iconTheme: IconThemeData(color: Colors.white)),
    bottomNavigationBarTheme: const BottomNavigationBarThemeData(
      backgroundColor: appBackgroungColorDarkTheme,
    ));
