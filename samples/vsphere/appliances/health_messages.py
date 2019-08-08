#!/usr/bin/env python
"""
* *******************************************************
* Copyright (c) VMware, Inc. 2017. All Rights Reserved.
* SPDX-License-Identifier: MIT
* *******************************************************
*
* DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
* WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
* EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
* WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
* NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.
"""

__author__ = 'VMware, Inc.'
__copyright__ = 'Copyright 2017 VMware, Inc. All rights reserved.'
__vcenter_version__ = '6.7+'

from samples.vsphere.common import sample_cli
from samples.vsphere.common import sample_util
from samples.vsphere.common import vapiconnect
from com.vmware.appliance_client import Health 
from com.vmware.vapi.std_client import LocalizableMessage

class HealthMessages(object) :
    """
    Demonstrates getting Health messages for various health items

    Retrieves Health messages details from vCenter and prints the data

    """


    def __init__(self):
        self.item = None
        self.stub_config = None

    def setup(self):
        parser = sample_cli.build_arg_parser()
        parser.add_argument(
            '--item',
            required=True,
            action='store',
            choices=['memory', 'cpu' , 'storage'],
            help='Specify the name of health item to view the messages')
        args = sample_util.process_cli_args(parser.parse_args())
        self.item = args.item

    # Connect to vAPI services
        self.stub_config = vapiconnect.connect(
            host=args.server,
            user=args.username,
            pwd=args.password,
            skip_verification=args.skipverification)

        self.health_client = Health(self.stub_config)

    def run(self):
        message_list = self.health_client.messages(self.item)
        print(" Health Alarams")
        print("-------------------\n")
        if not message_list:
            print("No health alarms for : " + self.item)
        else:
            for message in message_list :
                print("Alert time : " + message.getTime())
                print("Alert message Id: " + message.getId())
                msg = message.getMessage()
                def_message = LocalizableMessage(msg.default_message)
                print("Alert message : "+ def_message)


def main():
    health_sample = HealthMessages()
    health_sample.setup()
    health_sample.run()

if __name__ == '__main__':
    main()
