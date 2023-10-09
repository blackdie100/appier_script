#!/bin/bash

export APPID=$1
export FILEPATH=/mnt/devicedata4/event-store-disk/$1
export EVENTNAME=app_launched
export CUSTOMERNAME=eTaskee

export FROMDATE=2019-09-20
export TODATE=2020-03-23

cd $FILEPATH
curr="$FROMDATE"

rm -rf /mnt/devicedata4/nick/""$CUSTOMERNAME""/*

# while true; do
for curr in $(ls -d */ | cut -f1 -d'/');do
    cd $curr

    for ii in $(ls -d */ | cut -f1 -d'/');do
        if [ -d "$ii/$EVENTNAME" ] ; then

            sort $ii/$EVENTNAME/uid.txt | awk '{print $2}' | uniq -c >> /mnt/devicedata4/nick/""$CUSTOMERNAME""/temp.txt  
        fi
    done  

    sort /mnt/devicedata4/nick/""$CUSTOMERNAME""/temp.txt | awk '{print $2}' | uniq -c > /mnt/devicedata4/nick/""$CUSTOMERNAME""/temp2.txt

    for i in $curr; do awk -v a=$i '{print a,$1,$2}' /mnt/devicedata4/nick/""$CUSTOMERNAME""/temp2.txt; echo "" ; done >> /mnt/devicedata4/nick/""$CUSTOMERNAME""/""$curr"".txt
    
    rm -rf /mnt/devicedata4/nick/""$CUSTOMERNAME""/temp.txt
    rm -rf /mnt/devicedata4/nick/""$CUSTOMERNAME""/temp2.txt

    # [ "$curr" \< "$TODATE" ] || break
    # curr=$( date +%Y-%m-%d --date "$curr +1 day" )

    cd ..
done

cd /mnt/devicedata4/nick/""$CUSTOMERNAME""
cat * > merged-txt.txt
