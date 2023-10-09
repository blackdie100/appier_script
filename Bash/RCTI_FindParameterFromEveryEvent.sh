#!/bin/bash

export APPID=$1
export FILEPATH=/mnt/devicedata4/event-store-disk/$1
export STORAGEPATH=/mnt/devicedata4/nick/RCTI
export PUREPARAMETER=$2
export PARAMETER=$2.txt

export FROMDATE=2020-02-01
export TODATE=2020-06-01

# rm -rf $STORAGEPATH/*

mkdir -p $STORAGEPATH/$1
mkdir $STORAGEPATH/$1/$PUREPARAMETER

cd $FILEPATH
curr="$FROMDATE"

while true; do
    cd $curr
    for ii in $(ls -d */ | cut -f1 -d'/');do
        cd $ii

        for iii in $(ls -d */ | cut -f1 -d'/');do
            if [ -f "$iii/$PARAMETER" ]; then
                sort $iii/$PARAMETER | awk '{print $2}' | uniq -c >> $STORAGEPATH/$1/$PUREPARAMETER/""$curr"".txt

            fi
        done
        cd ..
    done  

    [ "$curr" \< "$TODATE" ] || break
    curr=$( date +%Y-%m-%d --date "$curr +1 day" )
    cd ..
done

cd $STORAGEPATH/$1/$PUREPARAMETER

cat * > merged-txt.txt
sort merged-txt.txt | awk '{print $2}' | uniq -c | sort -k1,1nr -k2,2 > SortBySearch.txt

rm -rf merged-txt.txt