#!/usr/bin/env python
"""
conf file example

[elk-server]
ip = elk.server.ip
kibana = check_http
elasticsearch = check_http!-p 9200
logstash-3333 = check_tcp!3333
logstash-3334 = check_tcp!3334
load = check_nrpe!check_load
"""

import os, sys
try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser

parser = ConfigParser()
parser.read(sys.argv[1])
parser.sections()
for section in parser.sections():
    os.system('./add_host.sh {} {}'.format(section, parser.get(section, 'ip')))
    parser.remove_option(section, 'ip')
    for service, command in parser.items(section):
        os.system('./add_service_to_host.sh {} {} {}'.format(section, service, command.replace('/', r'\/')))

