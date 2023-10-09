#!/bin/bash

export APPID=$1
export FILEPATH=/mnt/devicedata4/event-store-disk/$1
export STORAGEPATH=/mnt/devicedata4/nick/lafresh
export EVENTNAME=app_launched
export CUSTOMER=lafresh

export FROMDATE=2020-09-17
export TODATE=2020-10-05

export FILE=uid.txt

mkdir -p $STORAGEPATH
rm -rf $STORAGEPATH/*

cd $FILEPATH
curr="$FROMDATE"


while true; do
    if [ -d "$FILEPATH/$curr" ] ; then
        cd $FILEPATH/$curr
        for ii in $(ls -d */ | cut -f1 -d'/');do
            if [ -d "$ii/$EVENTNAME" ] ; then

                cat $ii/$EVENTNAME/$FILE >> ""$STORAGEPATH""/""$CUSTOMER"".txt
            fi
        done  

      else
        echo "No folder named $curr"
    fi
        [ "$curr" \< "$TODATE" ] || break
        curr=$( date +%Y-%m-%d --date "$curr +1 day" )

    cd ..
done

curr="$FROMDATE"

echo "Date || Count of unique user"

while true; do
    cat $STORAGEPATH/""$CUSTOMER"".txt | awk '$1 >= '$(date --date=""$curr" +8 hours" +"%s")' && $1 <= '$(date --date=""$( date +%Y-%m-%d --date "$curr +1 day" )" +8 hours" +"%s")'' >> ""$STORAGEPATH""/""$curr"".txt;

    NUMBER=$(cat $STORAGEPATH/$curr.txt | awk '{print $2}' | sort | uniq | wc -l)

    echo ""$curr" "$NUMBER""

    [ "$curr" \< "$TODATE" ] || break
    curr=$( date +%Y-%m-%d --date "$curr +1 day" )
done

sed 's/ \+/,/g' ""$STORAGEPATH""/""$CUSTOMER"".txt > ""$STORAGEPATH""/""$CUSTOMER"".csv

###### From Jason's code ######

# for i in {0..6}; do 
#   date=$(date -d "2020-08-09 -$i days" +'%Y-%m-%d');
#   echo $date;
#   cat $date/*/notification_received/uid.txt >> readmoo.txt;
# done

# cat readmoo.txt | awk '{print $2}' | sort | uniq | wc -l


# for i in {0..30};
#   do date=$(date -d "2020-08-09 -$i days" +'%Y-%m-%d');
#   echo $date;
#   cat $date/*/notification_received/uid.txt | awk '$1 > 15xxxxxxx && $1 < 15xxxxxxx' >> readmoo.txt;
# done
# cat readmoo.txt | awk '{print $2}' | sort | uniq | wc -l



