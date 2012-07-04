# Copyright 2012 Locaweb.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
# @author: Francisco Freire, Locaweb.
# @author: Thiago Morello (morellon), Locaweb.
# @author: Willian Molinari (PotHix), Locaweb.
# @author: Juliano Martinez (ncode), Locaweb.

import os
import socket
import ConfigParser

import logging
import logging.config
import logging.handlers

config = ConfigParser.ConfigParser()
config_file = "/etc/simplestack/simplestack.cfg"

if os.path.isfile(config_file):
    config.read(config_file)


def set_logger():
    root_logger = logging.root
    root_logger.setLevel(logging.DEBUG)

    log_format = "[%(name)s] %(levelname)s - %(message)s"
    log_date_format = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(log_format, log_date_format)

    SysLogHandler = logging.handlers.SysLogHandler
    try:
        handler = SysLogHandler(address='/dev/log',
                                facility=SysLogHandler.LOG_SYSLOG)
    except socket.error:
        handler = SysLogHandler(address='/var/run/syslog',
                                facility=SysLogHandler.LOG_SYSLOG)

    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
