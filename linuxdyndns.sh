#!/bin/bash
#You can start this script at startup by adding to crontab
#@reboot sh /path/to/linuxdyndns.sh
#Example Case - host in.ter.com
#HOST=in
#DOMAIN=ter.com
#PASSWORD=1234567890abcdef1234567890abcdef
#If you want to check
#every 01 minute: INTERVAL=1
#every 15 minute: INTERVAL=15

HOST=@
DOMAIN=ramsus.lat
PASSWORD=36234b88d3824206965336e97996cb40
INTERVAL=30

dns_ip=$(dig $HOST.$DOMAIN +short) #Check the registered IP in DNS
while true; do
        public_ip=$(dig TXT +short o-o.myaddr.l.google.com @ns1.google.com | awk -F'"' '{print $2}') #Check Public IP
        if [ "$public_ip" != "$dns_ip" ]; then
                python3 -c "from /home/ramsus/Programming/Daemons/bot.py import send_ip; force_send_ip()"
                curl "https://dynamicdns.park-your-domain.com/update?host=$HOST&domain=$DOMAIN&password=$PASSWORD&ip=$public_ip"
                sleep 300                          #Allow the DNS server to update
                dns_ip=$(dig $HOST.$DOMAIN +short) #Check the new IP and use new IP to compare to current IP
        fi
        sleep $(($INTERVAL * 60))
done
