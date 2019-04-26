"""
Test scheduler service
"""
import os
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
        assert 3 == len(tasks)
        task = tasks[0]
        assert "test_task_name_1" == task.name
        # assert time.strptime("06:00 CET", "%H:%M %Z") == task.when
        assert "06:00+00" == task.when
        assert "name_of_the_intent_1" == task.intent
        assert "param_value_1" == task.params['param_key_1']
        assert "param_value_2" == task.params['param_key_2']
        assert "surface_id_1" == task.surface.surface_id
        assert "surface_channel_id_1" == task.surface.channel_id
        assert "text_for_the_message_1" == task.surface.text
        task = tasks[1]
        assert "test_task_name_2" == task.name
        assert "20:00+04" == task.when
        assert "name_of_the_intent_2" == task.intent
        assert "param_value_3" == task.params['param_key_3']
        assert "surface_id_2" == task.surface.surface_id
        assert "channel_id_2" == task.surface.channel_id
        assert None is task.surface.text
        task = tasks[2]
        assert "test_task_name_3" == task.name
        assert "15:00+03:30" == task.when
        assert "name_of_the_intent_3" == task.intent
        assert None is task.params
        assert None is task.surface

    def test_TimeComparison(self):
        """
        Tests different comparisons between times, without considering dates associated
        """
        a = arrow.get("13:00-00", "HH:mmZZ")
        assert a == arrow.get("13:00-00", "HH:mmZZ")
        assert a == arrow.get("14:00+01", "HH:mmZZ")
        assert a == arrow.get("14:00+01", "HH:mmZZ").to("UTC")
        assert a == arrow.get("10:30-02:30", "HH:mmZZ")

        # Such date cannot exists in a UTC form, as it's before EPOC start
        #  moment
        with self.assertRaises(OverflowError):
            arrow.get("00:00+01", "HH:mmZZ").to("UTC")
        # Adding a day, this time no exception is raised
        try:
            print(arrow.get("00:00+01", "HH:mmZZ").replace(days=1).to("UTC"))
        except OverflowError:
            self.fail("Exception not raised!")
        print(arrow.get("00:00+00", "HH:mmZZ").replace(days=1).to("UTC"))

    def test_getTasksForInterval(self):
        # print(arrow.utcnow())
        tasks = self._scheduler.get_tasks()
        tasks.clear()

        assert 0 == len(self._scheduler.get_tasks())
        res_tasks = self._scheduler.find_tasks_for_time("19:00+00")
        assert 0 == len(res_tasks)

        tasks.append(SchedulerTask("task_19:00+00", "19:00+00", "test_intent_19:00+00"))
        res_tasks = self._scheduler.find_tasks_for_time("19:00+00")
        assert 1 == len(res_tasks)
        assert "task_19:00+00" == res_tasks[0].name
        res_tasks = self._scheduler.find_tasks_for_time("20:00+01")
        assert 1 == len(res_tasks)
        assert "task_19:00+00" == res_tasks[0].name
        tasks.append(SchedulerTask("task_08:00+00", "08:00+00", "test_intent_08:00+00"))
        res_tasks = self._scheduler.find_tasks_for_time("20:00+01")
        assert 1 == len(res_tasks)
        assert "task_19:00+00" == res_tasks[0].name

        tasks.append(SchedulerTask("task_01:00-07", "01:00-07", "test_intent_01:00-07"))
        res_tasks = self._scheduler.find_tasks_for_time("08:00+00")
        assert 2 == len(res_tasks)
        assert "task_08:00+00" == res_tasks[0].name
        assert "task_01:00-07" == res_tasks[1].name

        # Borderline tasks
        tasks.append(SchedulerTask("task_23:00-02", "23:00-02", "test_intent_23:00-02"))
        res_tasks = self._scheduler.find_tasks_for_time("00:00+00")
        assert 0 == len(res_tasks)
        res_tasks = self._scheduler.find_tasks_for_time("01:00+00")
        assert 1 == len(res_tasks)
        assert "task_23:00-02" == res_tasks[0].name

        tasks.append(SchedulerTask("task_01:30+02:30", "01:30+02:30", "test_intent_01:30+02_30"))
        res_tasks = self._scheduler.find_tasks_for_time("00:00+00")
        assert 0 == len(res_tasks)
        res_tasks = self._scheduler.find_tasks_for_time("23:00+00")
        assert 1 == len(res_tasks)
        assert "task_01:30+02:30" == res_tasks[0].name

    def test_getCurrentHour(self):
        #print(self._scheduler.get_current_hour())
        pass



