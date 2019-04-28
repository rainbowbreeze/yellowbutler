"""
Test scheduler service
"""
import os
from datetime import datetime
from unittest import TestCase

import arrow

from yellowbot.schedulerservice import SchedulerService, SchedulerTask

TASKS_FILE_NAME = os.path.join(os.path.dirname(__file__), "yellowbot_tasks_test.json")


class TestSchedulerService(TestCase):
    def setUp(self):
        self._scheduler = SchedulerService(TASKS_FILE_NAME)
        pass

    def tearDown(self):
        pass

    def test_noTasksFileExceptionRaised(self):
        with self.assertRaises(ValueError):
            SchedulerService("non_existing_file")

    def test_readTasks(self):
        tasks = self._scheduler.get_tasks()
        assert 4 == len(tasks)
        task = tasks[0]
        assert "test_task_name_1" == task.name
        assert "06:00" == task.when
        assert "UTC" == task.timezone
        assert "name_of_the_intent_1" == task.intent
        assert "param_value_1" == task.params['param_key_1']
        assert "param_value_2" == task.params['param_key_2']
        assert "surface_id_1" == task.surface.surface_id
        assert "surface_channel_id_1" == task.surface.channel_id
        assert None is task.surface.text
        assert "text_for_the_message_1" == task.default_message
        task = tasks[1]
        assert "test_task_name_2" == task.name
        assert "20:00" == task.when
        assert "Europe/Rome" == task.timezone
        assert "name_of_the_intent_2" == task.intent
        assert "param_value_3" == task.params['param_key_3']
        assert "surface_id_2" == task.surface.surface_id
        assert "channel_id_2" == task.surface.channel_id
        assert None is task.surface.text
        assert None is task.default_message
        task = tasks[2]
        assert "test_task_name_3" == task.name
        assert "15:00" == task.when
        assert "UTC" == task.timezone
        assert "name_of_the_intent_3" == task.intent
        assert None is task.params
        assert None is task.surface
        assert None is task.default_message
        task = tasks[3]
        assert "test_task_name_4" == task.name
        assert "17:00" == task.when
        assert "Europe/Rome" == task.timezone
        assert "name_of_the_intent_4" == task.intent
        assert None is task.params
        assert "test_surface_4" == task.surface.surface_id
        assert "123456" == task.surface.channel_id
        assert None is task.surface.text
        assert None is task.default_message

    def test_TimeComparison(self):
        """
        Tests different comparisons between times, without considering dates associated
        """
        a = arrow.get("13:00-00", "HH:mmZZ")
        assert a == arrow.get("13:00-00", "HH:mmZZ")
        assert a == arrow.get("14:00+01", "HH:mmZZ")
        assert a == arrow.get("14:00+01", "HH:mmZZ").to("UTC")
        assert a == arrow.get("10:30-02:30", "HH:mmZZ")

        # b = arrow.now("Europe/Rome")

        # Such date cannot exists in a UTC form, as it's before EPOC start
        #  moment
        with self.assertRaises(OverflowError):
            arrow.get("00:00+01", "HH:mmZZ").to("UTC")
        # Adding a day, this time no exception is raised
        try:
            print(arrow.get("00:00+01", "HH:mmZZ").shift(days=1).to("UTC"))
        except OverflowError:
            self.fail("Exception not raised!")
        print(arrow.get("00:00+00", "HH:mmZZ").shift(days=1).to("UTC"))

    def test_getTasksForInterval(self):
        tasks = self._scheduler.get_tasks()
        tasks.clear()

        assert 0 == len(self._scheduler.get_tasks())
        date_19_utc = arrow.get(datetime(2019, 5, 5, 19, 00, 00), 'UTC')
        res_tasks = self._scheduler.find_tasks_for_time(date_19_utc)
        assert 0 == len(res_tasks)

        tasks.append(SchedulerTask("task_19:00_utc", "19:00", "UTC", "test_intent_19:00+00"))
        res_tasks = self._scheduler.find_tasks_for_time(date_19_utc)
        assert 1 == len(res_tasks)
        assert "task_19:00_utc" == res_tasks[0].name

        res_tasks = self._scheduler.find_tasks_for_time(arrow.get(datetime(2019, 5, 5, 20, 00), 'UTC'))
        assert 0 == len(res_tasks)

        date_21_europe_rome = arrow.get(datetime(2019, 5, 5, 21, 00), "Europe/Rome")
        res_tasks = self._scheduler.find_tasks_for_time(date_21_europe_rome)
        assert 1 == len(res_tasks)
        assert "task_19:00_utc" == res_tasks[0].name

        tasks.append(SchedulerTask("task_08:00_us_pacific", "08:00", "US/Pacific", "test_intent_08:00-07"))
        res_tasks = self._scheduler.find_tasks_for_time(date_21_europe_rome)
        assert 1 == len(res_tasks)
        assert "task_19:00_utc" == res_tasks[0].name

        # GMT-8
        date_8_us_pacific = arrow.get(datetime(2019, 5, 5, 8, 00), "US/Pacific")
        res_tasks = self._scheduler.find_tasks_for_time(date_8_us_pacific)
        assert 1 == len(res_tasks)
        assert "task_08:00_us_pacific" == res_tasks[0].name
        # GMT-7
        res_tasks = self._scheduler.find_tasks_for_time(arrow.get(datetime(2019, 5, 5, 9, 00), "US/Mountain"))
        assert 1 == len(res_tasks)
        assert "task_08:00_us_pacific" == res_tasks[0].name
        tasks.append(SchedulerTask("task_10:00_us_central", "10:00", "US/Central", "test_intent_10:00-06"))
        res_tasks = self._scheduler.find_tasks_for_time(date_8_us_pacific)
        assert 2 == len(res_tasks)
        assert "task_08:00_us_pacific" == res_tasks[0].name
        assert "task_10:00_us_central" == res_tasks[1].name

        # Borderline tasks
        tasks.append(SchedulerTask("task_01:00_europe_rome", "01:00", "Europe/Rome", "test_intent_01:00+02"))
        res_tasks = self._scheduler.find_tasks_for_time(arrow.get(datetime(2019, 5, 5, 22, 00), "GMT"))
        assert 0 == len(res_tasks)
        res_tasks = self._scheduler.find_tasks_for_time(arrow.get(datetime(2019, 5, 5, 23, 00), "GMT"))
        # Day is not taken into account
        assert 1 == len(res_tasks)
        assert "task_01:00_europe_rome" == res_tasks[0].name



