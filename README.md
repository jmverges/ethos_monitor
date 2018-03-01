#This is a utils package for ethOS distro

git clone https://github.com/jmverges/ethos_utilities.git

crontab -e

add the following line at the end

@reboot /home/ethos/ethos_utilities/check_crash.py

close crontab

if you want push notifications you can use pushsafer.com

create a file /etc/ethos/pushsafer which only contains you apikey

create a file /etc/ethos/remote.url which only contains you public config url with HTTP, NOT HTTPS

Add this line /home/ethos/ethos_utilities/autoupdate.sh in your custom.sh 

r for reboot