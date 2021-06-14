# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Abhijeet Kasurde <akasurde@redhat.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


def to_dict(sequence, key_name='name'):
    '''Convert a list to a dictionary.
    '''
    ret = []
    for i in sequence:
        ret.append({key_name: i})
    return ret


class FilterModule(object):
    '''Ansible Demo filters'''

    def filters(self):
        return {
            'to_dict': to_dict,
        }
