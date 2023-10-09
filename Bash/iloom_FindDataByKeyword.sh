#!/bin/bash

export APPID=$1
export FILEPATH=/mnt/devicedata4/event-store-disk/$1
export EVENTNAME=book_list_shared

export FROMDATE=2020-03-24
export TODATE=2020-05-19

export FILE=uid.txt

cd $FILEPATH
curr="$FROMDATE"

while true; do
    cd $curr
    for ii in $(ls -d */ | cut -f1 -d'/');do
        if [ -d "$ii/$EVENTNAME" ] ; then

            sort $ii/$EVENTNAME/$FILE | awk '{print $2}' | uniq -c >> /mnt/devicedata4/nick/iloom/""$curr"".txt
        fi
    done  

    [ "$curr" \< "$TODATE" ] || break
    curr=$( date +%Y-%m-%d --date "$curr +1 day" )

    cd ..
done

cd /mnt/devicedata4/nick/iloom

cat * > merged-txt.txt
sort merged-txt.txt | awk '{print $2}' | uniq -c | sort -k1,1nr -k2,2 > SortBySearch.txt