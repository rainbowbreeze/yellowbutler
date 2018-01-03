"""
Scheduler service, to run specific tasks at specific times
"""
import json
import os

from json_minify import json_minify

from yellowbot.surfaces.surfacemessage import SurfaceMessage


class SchedulerTask():
    """
    Define a task processed by the scheduler
    """
    def __init__(self, name, when, intent, params, surface_id, surface_channel_id, surface_text):
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

