# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Abhijeet Kasurde <akasurde@redhat.com>
# Copyright: (c) 2018, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
    name: random_uuid
    author:
      - Abhijeet Kasurde (@Akasurde)
    short_description: Generates random UUID
    version_added: '1.0.0'
    description:
      - Generates random UUID.
    options:
      upper:
        description:
        - Include uppercase letters in the string.
        default: false
        type: bool
"""

EXAMPLES = r"""
- name: Generate random UUID
  ansible.builtin.debug:
    var: lookup('community.general.random_uuid')
  # Example result: ['9b8df1f8-5f0b-43c7-a498-03c7217e3a01']

- name: Generate random UUID in uppercase
  ansible.builtin.debug:
    var: lookup('community.general.random_uuid', upper=True)
  # Example result: ['08CE3F2E-C9E7-4828-8940-01A19DC52CF6']
"""

RETURN = r"""
  _raw:
    description: A one-element list containing a random UUID
    type: list
    elements: str
"""

import uuid

from ansible.plugins.lookup import LookupBase
from ansible.module_utils._text import to_native


class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)

        upper = self.get_option("upper")

        uuid_value = to_native(uuid.uuid4())

        if upper:
            uuid_value = uuid_value.upper()

        return [uuid_value]
