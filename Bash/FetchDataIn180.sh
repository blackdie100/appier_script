#!/bin/bash

export APPID=$1
export FILEPATH=/mnt/devicedata4/event-store-disk/$1
export EVENTNAME=$2

cd $FILEPATH
AllNum=0

for i in $(ls -d */ | cut -f1 -d'/');do
    cd $i
    for ii in $(ls -d */ | cut -f1 -d'/');do
        if [ -d "$ii/$EVENTNAME" ] ; then
            export UIDNUMBER=$(cat $ii/$EVENTNAME/uid.txt | wc -l)
            echo "There are "$UIDNUMBER" users at "$ii"~"$(($ii + 2))" o'clock on "$i""

            AllNum=$(($UIDNUMBER + $AllNum))
          else
          	echo "There is no user for "$EVENTNAME" event at "$ii"~"$(($ii + 2))" o'clock on "$i""
        fi
    done  
    cd ..
done

echo "Amount of all users is "$AllNum""


