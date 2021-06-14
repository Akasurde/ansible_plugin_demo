# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Abhijeet Kasurde <akasurde@redhat.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = '''
    author: Abhijeet Kasurde (@Akasurde)
    name: timeit
    type: notification
    short_description: write playbook output in custom format
    description:
      - This callback writes playbook output in custom format
    requirements:
     - Whitelist in configuration
'''

import time

from ansible.module_utils._text import to_native
from ansible.plugins.callback import CallbackBase


class CallbackModule(CallbackBase):
    """
    logs playbook results
    """
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'akasurde.demo.timeit'
    CALLBACK_NEEDS_WHITELIST = True

    TIME_FORMAT = "%b %d %Y %H:%M:%S"
    MSG_FORMAT = "%(now)s - %(playbook)s - %(task_name)s - %(task_action)s - %(category)s"

    def __init__(self):

        super(CallbackModule, self).__init__()

    def set_options(self, task_keys=None, var_options=None, direct=None):
        super(CallbackModule, self).set_options(task_keys=task_keys, var_options=var_options, direct=direct)

    def log(self, result, category):
        now = time.strftime(self.TIME_FORMAT, time.localtime())

        msg = to_native(
            self.MSG_FORMAT
            % dict(
                now=now,
                playbook=self.playbook,
                task_name=result._task.name,
                task_action=result._task.action,
                category=category,
            )
        )
        self._display.display("%s" % msg)

    def v2_runner_on_failed(self, result, ignore_errors=False):
        self.log(result, 'FAILED')

    def v2_runner_on_ok(self, result):
        self.log(result, 'OK')

    def v2_runner_on_skipped(self, result):
        self.log(result, 'SKIPPED')

    def v2_runner_on_unreachable(self, result):
        self.log(result, 'UNREACHABLE')

    def v2_runner_on_async_failed(self, result):
        self.log(result, 'ASYNC_FAILED')

    def v2_playbook_on_start(self, playbook):
        self.playbook = playbook._file_name

