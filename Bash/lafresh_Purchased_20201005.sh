# !/bin/bash

export APPID=$1
export FILEPATH=/mnt/devicedata4/event-store-disk/$1
export STORAGEPATH=/mnt/devicedata4/nick/lafresh
export EVENTNAMES=("app_launched" "product_viewed" "product_purchased")
export CUSTOMER=lafresh

export FROMDATE=2020-09-01
export TODATE=2020-10-07

export FILE=uid.txt

### For product_viewed and product_purchased ###
export PARAMETER1=category_name.txt
export PARAMETER2=product_name.txt
export PARAMETER3=id.txt
export PARAMETER4=product_link.txt
export PARAMETER5=product_image.txt
export PARAMETER6=product_price.txt


mkdir -p $STORAGEPATH
rm -rf $STORAGEPATH/*

cd $FILEPATH
curr="$FROMDATE"


for EVENTNAME in ${EVENTNAMES[@]};do
    while true; do
        if [ -d "$FILEPATH/$curr" ]; then
            cd $FILEPATH/$curr
            for ii in $(ls -d */ | cut -f1 -d'/');do
                
                if [ -d "$ii/$EVENTNAME" ]; then

                    if [[ $EVENTNAME == "app_launched" ]]; then

                        awk '$1 = $1 FS "app_launched"' $ii/$EVENTNAME/$FILE >> ""$STORAGEPATH""/dummy.txt

                    elif [[ $EVENTNAME == "product_viewed" ]]; then

                        if [[ $APPID == *_ios ]]; then
                            export PARAMETER3=product_id.txt
                        fi

                        paste \
                        $ii/$EVENTNAME/$FILE $ii/$EVENTNAME/$PARAMETER1 $ii/$EVENTNAME/$PARAMETER2 $ii/$EVENTNAME/$PARAMETER3 \
                        $ii/$EVENTNAME/$PARAMETER4 $ii/$EVENTNAME/$PARAMETER5 $ii/$EVENTNAME/$PARAMETER6 \
                        |awk -v OFS='\t' '{print $1, $2, $5, $8, $11, $14, $17, $20}' | awk '$1 = $1 FS "product_viewed"' >> ""$STORAGEPATH""/dummy.txt

                    elif [[ $EVENTNAME == "product_purchased" ]]; then
                        export PARAMETER3=uid.txt
                        paste \
                        $ii/$EVENTNAME/$FILE $ii/$EVENTNAME/$PARAMETER1 $ii/$EVENTNAME/$PARAMETER2 $ii/$EVENTNAME/$PARAMETER3 \
                        $ii/$EVENTNAME/$PARAMETER4 $ii/$EVENTNAME/$PARAMETER5 $ii/$EVENTNAME/$PARAMETER6 \
                        |awk -v OFS='\t' '{print $1, $2, $5, $8, $11, $14, $17, $20}'| awk '$1 = $1 FS "product_purchased"' >> ""$STORAGEPATH""/dummy.txt

                    fi
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
done

printf '%(%F %H:%M:%S)T\n' $(awk -F' ' '{print $1}' ""$STORAGEPATH""/dummy.txt) >> ""$STORAGEPATH""/date.txt
pr -mts' ' ""$STORAGEPATH""/date.txt ""$STORAGEPATH""/dummy.txt >> ""$STORAGEPATH""/""$CUSTOMER"".txt

sed 's/ \+/,/g' ""$STORAGEPATH""/""$CUSTOMER"".txt > ""$STORAGEPATH""/""$CUSTOMER"".csv

rm -rf ""$STORAGEPATH""/product_viewed.txt ""$STORAGEPATH""/product_purchased.txt ""$STORAGEPATH""/dummy.txt ""$STORAGEPATH""/date.txt ""$STORAGEPATH""/dummy2.txt


