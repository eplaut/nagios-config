#!/bin/bash -e

if [ "$#" -ne 2 ]; then
    echo "usage: $0 HOST_NAME HOST_ADDRESS" >&2
    exit 1
fi

host_name=$1
host_address=$2
sed -e "s/HOSTNAME/$host_name/" -e "s/HOSTADDRESS/$host_address/" templates/host.cfg > "/usr/local/nagios/etc/objects/${host_name}.cfg"
echo "cfg_file=/usr/local/nagios/etc/objects/${host_name}.cfg" >> "/usr/local/nagios/etc/nagios.cfg"


