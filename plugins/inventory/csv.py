# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Abhijeet Kasurde <akasurde@redhat.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = '''
    author: Abhijeet Kasurde (@Akasurde)
    name: csv
    short_description: Uses CSV file to create inventory
    description:
        - Uses a YAML configuration file with a valid YAML extension.
    extends_documentation_fragment:
      - constructed
      - inventory_cache
    options:
        plugin:
            description: token that ensures this is a source file for the 'csv' plugin.
            required: True
            choices: ['akasurde.demo.csv']
        filename:
            description: Absolute path of CSV file to read the inventory from.
            required: True
            type: str
'''
EXAMPLES = r'''
plugin: akasurde.demo.csv
strict: False
filename: /tmp/mycustominventory.csv
'''

import csv
import os

from ansible import constants as C
from ansible.errors import AnsibleParserError
from ansible.module_utils._text import to_native, to_text
from ansible.plugins.inventory import BaseInventoryPlugin

class InventoryModule(BaseInventoryPlugin):

    NAME = 'akasurde.demo.csv'

    def __init__(self):
        self._nmap = None
        super(InventoryModule, self).__init__()

    def _populate(self, hosts):
        for host in hosts:
            hostname = host['ip']
            self.inventory.add_host(hostname)
            for var, value in host.items():
                self.inventory.set_variable(hostname, var, value)

            self.inventory.set_variable(hostname, 'ansible_host', hostname)

    def verify_file(self, path):
        valid = False
        if super(InventoryModule, self).verify_file(path):
            file_name, ext = os.path.splitext(path)

            if not ext or ext in C.YAML_FILENAME_EXTENSIONS:
                valid = True

        return valid

    def parse(self, inventory, loader, path, cache=True):

        super(InventoryModule, self).parse(inventory, loader, path, cache=cache)

        self._read_config_data(path)
        csv_filename = self.get_option('filename')
        if not os.path.exists(csv_filename):
            raise AnsibleParserError("%s not found" % csv_filename)

        hosts = []
        with open(csv_filename) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for i in csv_reader:
                hosts.append(i)

        self._populate(hosts)
