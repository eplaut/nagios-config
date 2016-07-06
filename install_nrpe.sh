#!/bin/bash -e

if [ "$#" -ne 1 ]; then
    echo "usage: $0 NAGIOS_SERVER_IP" >&2
    exit 1
fi

apt-get install nagios-plugins nagios-nrpe-server

cat > /etc/nagios/nrpe_local.cfg <<EOF
allowed_hosts=$1 127.0.0.1
dont_blame_nrpe=1

command[check_users]=/usr/lib/nagios/plugins/check_users -w 5 -c 10
command[check_load]=/usr/lib/nagios/plugins/check_load -w 15,10,5 -c 30,25,20
command[check_all_disks]=/usr/lib/nagios/plugins/check_disk -w 20 -c 10
command[check_disk]=/usr/lib/nagios/plugins/check_disk -w 20 -c 10 -p \$ARG1\$
command[check_zombie_procs]=/usr/lib/nagios/plugins/check_procs -w 5 -c 10 -s Z
command[check_total_procs]=/usr/lib/nagios/plugins/check_procs -w 150 -c 200
command[check_swap]=/usr/lib/nagios/plugins/check_swap -w 20 -c 10
EOF

/etc/init.d/nagios-nrpe-server restart
