# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Abhijeet Kasurde <akasurde@redhat.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


import copy
import json
import traceback

from ansible.errors import AnsibleError
from ansible.module_utils._text import to_text
from ansible.plugins.action import ActionBase


class ActionModule(ActionBase):

    TRANSFERS_FILES = True
    DEFAULT_NEWLINE_SEQUENCE = "\n"

    def _ensure_invocation(self, result):
        # NOTE: adding invocation arguments here needs to be kept in sync with
        # any no_log specified in the argument_spec in the module.
        if 'invocation' not in result:
            if self._play_context.no_log:
                result['invocation'] = "CENSORED: no_log is set"
            else:
                result['invocation'] = self._task.args.copy()
                result['invocation']['module_args'] = self._task.args.copy()

        return result


    def run(self, tmp=None, task_vars=None):
        ''' handler for k8s options '''
        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)
        del tmp  # tmp no longer has any effect

        # Check current transport connection and depending upon
        # look for config and src
        # 'local' => look files on Ansible Controller
        # Transport other than 'local' => look files on remote node
        remote_transport = self._connection.transport != 'local'

        new_module_args = copy.deepcopy(self._task.args)

        config = self._task.args.get('encrypted_file', None)
        # find the config in the expected search path
        if config and not remote_transport:
            # config is local
            try:
                # find in expected paths
                config = self._find_needle('files', config)
            except AnsibleError as e:
                result['failed'] = True
                result['msg'] = to_text(e)
                result['exception'] = traceback.format_exc()
                return result

            # decrypt config found
            actual_file = self._loader.get_real_file(config, decrypt=True)

            ret = {}
            try:
                ret = json.load(open(actual_file))
            except Exception as e:
                pass
            new_module_args['encrypted_file'] = ret

        # Execute module which called this action plugin
        module_return = self._execute_module(module_name=self._task.action, module_args=new_module_args, task_vars=task_vars)

        # Delete tmp path
        self._remove_tmp_path(self._connection._shell.tmpdir)

        result.update(module_return)

        return self._ensure_invocation(result)
