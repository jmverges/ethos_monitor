#!/bin/bash
#

if [ "$1" == "restart" ] || [ "$1" == "stop" ]
then
	pkill -ef '/home/ethos/ethos_utilities/daemon_remote_conf.php'
fi

proc=$(ps -aux | grep php | grep daemon_remote_conf)

if [ "$1" != "stop" ]
then
	if [ "$proc" == "" ]
	then
		/usr/bin/php /home/ethos/ethos_utilities/daemon_remote_conf.php &
		echo "Success!"
	else
		echo "Already launched!"
	fi
fi
