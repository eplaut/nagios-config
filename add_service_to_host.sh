#!/bin/bash -e

if [ "$#" -ne 1 ]; then
    echo "usage: $0 HOST_NAME SERVICE_NAME COMMAND" >&2
    exit 1
fi

host_name=$1
service_name=$2
cmd=$3
test -f "/usr/local/nagios/etc/objects/${host_name}.cfg"
sed -e "s/HOSTNAME/$host_name/" -e "s/SERVICENAME/$service_name/" -e "s/COMMAND/$cmd/" templates/service.cfg >> "/usr/local/nagios/etc/objects/${host_name}.cfg"

