"""
Test scheduler service
"""
import os
from unittest import TestCase

from yellowbot.schedulerservice import SchedulerService

TASKS_FILE_NAME = os.path.join(os.path.dirname(__file__), "yellowbot_tasks_test.json")


class TestSchedulerService(TestCase):
    def setUp(self):
        self._scheduler = SchedulerService(TASKS_FILE_NAME)
        pass

    def tearDown(self):
        pass

    def test_readTasks(self):
        tasks = self._scheduler.get_tasks()
        assert 3 == len(tasks)
        task = tasks[0]
        assert "test_task_name_1" == task.name
        assert "06:00 AM CET" == task.when
        assert "name_of_the_intent_1" == task.intent
        assert "param_value_1" == task.params['param_key_1']
        assert "param_value_2" == task.params['param_key_2']
        assert "surface_id_1" == task.surface.surface_id
        assert "surface_channel_id_1" == task.surface.channel_id
        assert "text_for_the_message_1" == task.surface.text
        task = tasks[1]
        assert "test_task_name_2" == task.name
        assert "08:00 PM CET" == task.when
        assert "name_of_the_intent_2" == task.intent
        assert "param_value_3" == task.params['param_key_3']
        assert "surface_id_2" == task.surface.surface_id
        assert "channel_id_2" == task.surface.channel_id
        assert None is task.surface.text
        task = tasks[2]
        assert "test_task_name_3" == task.name
        assert "03:00 PM CET" == task.when
        assert "name_of_the_intent_3" == task.intent
        assert None is task.params
        assert None is task.surface

