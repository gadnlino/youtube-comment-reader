import 'package:flutter/material.dart';
import 'package:frontend/app/common/components/custom_app_bar.dart';
import 'package:frontend/app/common/components/custom_bottom_navigation_bar.dart';
import 'package:frontend/app/common/components/custom_cached_network_image.dart';
import 'package:frontend/app/common/utils/navigation.dart';
import 'package:frontend/app/pages/activity_details_page/activity_details_page.dart';
import 'package:frontend/app/pages/gym_selection_page/gym_selection_page.dart';
import 'package:get/get.dart';
import 'package:get/get_instance/src/bindings_interface.dart';
import 'package:get/get_state_manager/src/simple/get_controllers.dart';
import 'package:table_calendar/table_calendar.dart';

const String activitiesPageRoute = "/activities";

class ActivitiesPageBinding implements Bindings {
  @override
  void dependencies() {
    Get.lazyPut(() => ActivitiesPageController());
  }
}

class ActivitiesPageController extends GetxController {
  Rx<DateTime> focusedDay = Rx(DateTime.now().toUtc());
  Rx<DateTime> currentDay = Rx(DateTime.now().toUtc());
  Rx<CalendarFormat> calendarFormat = Rx(CalendarFormat.week);
}

class ActivitiesPage extends GetView<ActivitiesPageController> {
  const ActivitiesPage({super.key});

  Widget build(BuildContext context) {
    return Scaffold(
      appBar: CustomAppBar(),
      bottomNavigationBar: const CustomBottomNavigationBar(),
      body: SingleChildScrollView(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Obx(() {
              return TableCalendar(
                calendarFormat: controller.calendarFormat.value,
                daysOfWeekStyle: const DaysOfWeekStyle(
                    weekdayStyle: TextStyle(color: Colors.white)),
                headerStyle: const HeaderStyle(
                    titleCentered: true,
                    formatButtonVisible: true,
                    formatButtonTextStyle: TextStyle(color: Colors.white),
                    titleTextStyle: TextStyle(color: Colors.white)),
                calendarStyle: const CalendarStyle(
                    outsideDaysVisible: false,
                    defaultTextStyle: TextStyle(color: Colors.white)),
                currentDay: controller.currentDay.value,
                focusedDay: controller.focusedDay.value,
                firstDay: DateTime.now(),
                lastDay: DateTime.now().add(const Duration(days: 365 * 2)),
                startingDayOfWeek: StartingDayOfWeek.sunday,
                onFormatChanged: (format) {
                  if (controller.calendarFormat.value != format) {
                    controller.calendarFormat.value = format;
                  }
                },
                selectedDayPredicate: (day) {
                  return isSameDay(controller.focusedDay.value, day);
                },
                onDaySelected: (selectedDay, focusedDay) {
                  controller.currentDay.value = selectedDay;
                  controller.focusedDay.value = focusedDay;
                },
                onPageChanged: (focusedDay) {
                  controller.focusedDay.value = focusedDay;
                },
              );
            })
          ],
        ),
      ),
    );
  }
}
