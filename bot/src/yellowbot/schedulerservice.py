"""
Scheduler service, to run specific tasks at specific times
"""
import json
import os

import time

import arrow
from json_minify import json_minify

from yellowbot.surfaces.surfacemessage import SurfaceMessage


class SchedulerTask():
    """
    Define a task processed by the scheduler.

    All the time are in the format HH:mmZZ, ISO_8601, https://en.wikipedia.org/wiki/ISO_8601#Times
     Examples:
      19:30+00
      01:34+02:00
      23:32-09
      etc
    """
    def __init__(self,
                 name,
                 when,
                 intent,
                 params = None,
                 surface_id = None,
                 surface_channel_id = None,
                 surface_text = None):
        """
        Create a new task for the scheduler service
        :param name: name of the task
        :type name: str
        :param when: when the task is executed
        :type when: str
        :param intent: intent to launch
        :type intent: str
        :param params: optional parameters for the intent
        :type params: dict
        :param surface_id: surface id to use for communication
        :type surface_id: str
        :param surface_channel_id: surface channel id to use for communication
        :type surface_channel_id: str
        :param surface_text: text to use for communication
        :type surface_text: str
        """
        self.name = name
        self.when = when
        self.intent = intent
        self.params = params
        if None is surface_id and None is surface_channel_id and None is surface_text:
            self.surface = None
        else:
            self.surface = SurfaceMessage(surface_id, surface_channel_id, surface_text)


class SchedulerService():
    """
    Tasks are defined in a json file, please see examples at yellowbot_tasks_template.json

    Each tasks specifies
    * The name of the task
    * When the task needs to be executed
    * Intent and parameters to launch
    * Interaction surface details to output task results
    """

    def __init__(self, tasks_file):
        """

        :param tasks_file:
        :type tasks_file: str
        """
        self._load_tasks(tasks_file)

    def get_tasks(self):
        """
        Gets the list of tasks

        :return: list of tasks
        :rtype: list
        """
        return self._tasks

    def _load_tasks(self, tasks_file):
        """
        Load config key/value pairs from a file
        :param config_file: name of the file. Can be full path or, otherwise,
        same folder of this class is considered
        :type config_file: str

        :return:
        """
        self._tasks = []
        if not os.path.isfile(tasks_file):
            # Folder where this file is, can work also without the abspath,
            #  but better for debug so full path is traced in the error
            base_folder = os.path.abspath(os.path.dirname(__file__))
            full_tasks_path = os.path.join(base_folder, tasks_file)  # combine with the config file name
        else:
            full_tasks_path = tasks_file
        # Now if has the file and full path with configurations
        if os.path.isfile(full_tasks_path):
            with open(full_tasks_path, 'r') as f:
                json_with_comment = open(full_tasks_path).read()
                tasks = json.loads(json_minify(json_with_comment))

                # Converts into object
                for task_dict in tasks:
                    task = SchedulerTask(
                        task_dict['name'],
                        #time.strptime(task_dict['when'], "%H:%M %Z"),
                        task_dict['when'],
                        task_dict['intent'],
                        task_dict['params'] if 'params' in task_dict else None,
                        task_dict['surface_id'] if 'surface_id' in task_dict else None,
                        task_dict['surface_channel_id'] if 'surface_channel_id' in task_dict else None,
                        task_dict['surface_text'] if 'surface_text' in task_dict else None,
                    )
                    self._tasks.append(task)

        else:
            raise ValueError("Cannot find tasks file {}".format(full_tasks_path))

    def get_current_hour(self):
        """
        Returns current UTC time, where minutes are always 00
        :return:
        """
        current_time = arrow.utcnow().format("HH:mmZZ")
        return "{}00{}".format(
            current_time[:3],
            current_time[5:])

    def find_tasks_for_time(self, execution_time):
        """
        Finds tasks scheduled for the given time
        :param execution_time: time when the task should be executed
        :type execution_time: time
        :return: list of tasks that match the criteria
        :rtype: list
        """
        tasks = []

        # In order to compare time, also date has to be added
        # For example 10:00 in Berlin in July is 08:00 UTC, but in December, it would be 09:00 UTC
        # There are several issues with struct_time and conversion to a
        #  datetime. For example, mktime, suggested to convert a struct_time
        #  in local time to a datetime in python doc (see https://docs.python.org/3/library/time.html),
        #  fails miserably on my dev pc because of the underling C
        #  implementation of mktime (more at https://stackoverflow.com/a/2518828)
        # So, in order to overcome this complexity, I'm using Arrow library
        #
        # By default, the EPOC time is used by arrow when converting a
        #  simple time, and everything starts on 1970/01/01 UTC
        # When comparing times near the midnight, with different timezones,
        #  it could happen the time converted in UTC is before the EPOC
        #  start, so Arrow generates a OverflowError. 01:00+03 is an example.
        # To avoid this problem, I always add one day to the original time,
        #  so the corresponding UTC time is always valid

        refer_date = arrow.get(execution_time, "HH:mmZZ").replace(days=1).to("UTC")
        # Drops the date part, keeping only a time converted to UTC, finally
        # a common base for comparisons of all kind
        execution_utc_time_only = refer_date.format("HH:mm ZZ")

        for task in self._tasks:
            check_time = arrow.get(task.when, "HH:mmZZ").replace(days=1).to("UTC")
            # "normalize" the task time in the same way
            if execution_utc_time_only == check_time.format("HH:mm ZZ"):
                tasks.append(task)
        return tasks
