#!/bin/bash

export APPID=$1
export FILEPATH=/mnt/devicedata4/event-store-disk/$1
export EVENTNAME=register
export EVENTNAME2=register_success

cd $FILEPATH
AllNum=0
AllNum2=0

echo "Day || Count of register || Count of register_success "

for i in $(ls -d */ | cut -f1 -d'/');do
    cd $i
    for ii in $(ls -d */ | cut -f1 -d'/');do
        if [ -d "$ii/$EVENTNAME" ] ; then
            export UIDNUMBER=$(cat $ii/$EVENTNAME/uid.txt | wc -l)

        fi
        AllNum=$(($UIDNUMBER + $AllNum))
    done  

    for ii in $(ls -d */ | cut -f1 -d'/');do
        if [ -d "$ii/$EVENTNAME2" ] ; then
            export UIDNUMBER2=$(cat $ii/$EVENTNAME2/uid.txt | wc -l)

        fi
        AllNum2=$(($UIDNUMBER2 + $AllNum2))
    done  
    echo ""$i" "$AllNum" "$AllNum2""
    AllNum=0
    AllNum2=0
    cd ..
done



