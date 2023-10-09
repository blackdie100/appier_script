#!/bin/bash

export FILEPATH=/home/ubuntu/nick/Taipower
export S3PATH=s3://aiqua-prd-qgraph-backup-singapore/event-export
export APPIDS=("065d007a674da99ce51d" "065d007a674da99ce51d_ios" "476b897ae47d171fc971_web" "94d5bcf977440ea5fc57" "94d5bcf977440ea5fc57_ios" "b8f493cc6ea7f00f2cd7_web")
# export APPIDS=("476b897ae47d171fc971_web" "b8f493cc6ea7f00f2cd7_web")
export MONTHS=("01" "02" "03" "04")

cd $FILEPATH
rm -rf *

for APPID in ${APPIDS[@]};do

	mkdir -p $FILEPATH/$APPID
	cd $FILEPATH/$APPID

	for MONTH in ${MONTHS[@]};do

		mkdir -p $MONTH
		cd $MONTH

		/usr/local/bin/aws s3 sync $S3PATH/$APPID/2021/$MONTH . --profile aiqua
		gunzip */*

		cd ..
	done
done

for APPID in ${APPIDS[@]};do
	for MONTH in ${MONTHS[@]};do

		cd $FILEPATH/$APPID/$MONTH

		for NUMBER in ./*/;do

			cd $FILEPATH/$APPID/$MONTH/$NUMBER
			
			echo $APPID/$MONTH/$NUMBER

			if [[ $APPID == "476b897ae47d171fc971_web" ]]; then
                cat * | grep registion_completed | wc -l 

              else
              	cat * | grep registration_completed | wc -l 
            fi

			cd ..

		done
	done
done


