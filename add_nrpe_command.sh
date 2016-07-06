#!/bin/bash -e

cat >>/usr/local/nagios/etc/objects/commands.cfg <<EOF

define command{
        command_name check_nrpe
        command_line \$USER1\$/check_nrpe -H \$HOSTADDRESS\$ -c \$ARG1\$ -a \$ARG2\$
        }
EOF
