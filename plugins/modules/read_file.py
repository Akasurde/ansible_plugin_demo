#!/usr/bin/python
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = ''' # '''
EXAMPLES = ''' # '''
RETURN = ''' # '''

from ansible.module_utils.basic import AnsibleModule

def main():
    module = AnsibleModule(
        argument_spec=dict(
            encrypted_file=dict(type='raw')
        ),
    )
    encrypted_content = module.params['encrypted_file']
    module.exit_json(msg=encrypted_content['user'])


if __name__ == '__main__':
    main()
