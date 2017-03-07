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
import baker
from string import Template
try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser

CONF_DIR = '/usr/local/nagios/etc/objects'
MAIN_CONF = '/usr/local/nagios/etc/nagios.cfg'

def _load_template(filename, **kwargs):
    with open(filename) as fh:
        template = Template(fh.read())
    return template.substitute(kwargs)


def _host_cfg_file(host_name):
    return '{}/{}.cfg'.format(CONF_DIR, host_name)


@baker.command(default=True)
def load_config(config_file):
    parser = ConfigParser()
    parser.read(config_file)
    parser.sections()
    for section in parser.sections():
        add_host(section, parser.get(section, 'ip'))
        # os.system('./add_host.sh {} {}'.format(section, parser.get(section, 'ip')))
        parser.remove_option(section, 'ip')
        for service, command in parser.items(section):
            add_service_to_host(section, service, command)
            # os.system('./add_service_to_host.sh {} {} {}'.format(section, service, command.replace('/', r'\/')))


@baker.command
def add_host(host_name, host_address):
    host_cfg_file = _host_cfg_file(host_name)
    text = _load_template(os.path.join('templates', 'host.cfg'),
                          hostname=host_name, hostaddress=host_address)

    with open(host_cfg_file, 'w') as fh:
        fh.write(text)
    with open(MAIN_CONF, 'a') as fh:
        fh.write('cfg_file={}\n'.format(host_cfg_file))


@baker.command
def add_service_to_host(host_name, service_name, command):
    text = _load_template(os.path.join('templates', 'service.cfg'),
                          hostname=host_name, servicename=service_name, command=command)

    with open(_host_cfg_file(host_name), 'a') as fh:
        fh.write(text)


@baker.command
def add_command(command_name):
    with open('templates/{}.cfg'.format(command_name), 'r') as fh:
        text = fh.read()

    with open(os.path.join(CONF_DIR, 'command.cfg'), 'a') as fh:
        fh.write(text)


if __name__ == '__main__':
    baker.run()
