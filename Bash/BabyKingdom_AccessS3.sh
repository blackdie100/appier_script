#!/bin/bash

export FILEPATH=/home/ubuntu/nick/babyKingdom/data/
export S3PATH=s3://pd-bkmall-data-ex-appier/
export S3PROFILE=aiqua-vendor-baby-kingdom

export APPID=1259a6e5b3748c132a80
export SFTPPATH=ec2-54-254-145-132.ap-southeast-1.compute.amazonaws.com

export DatafeedFileName=$(/usr/local/bin/aws s3 ls $S3PATH --profile $S3PROFILE | sort | tail -n 1 | awk '{print $4}')


if /usr/local/bin/aws s3 cp $S3PATH$DatafeedFileName --profile $S3PROFILE $FILEPATH; then
  echo "download complete"
  mv $FILEPATH$DatafeedFileName $FILEPATH"babyKingdom.json"
  jq -r '(.data[0] | keys_unsorted), (.data[] | to_entries | map(.value))|@csv' $FILEPATH"babyKingdom.json" >> $FILEPATH"babyKingdom.csv"
else
  echo "fail"
fi

sshpass -p "123456" sftp $APPID"@"$SFTPPATH << SOMEDELIMITER 
  # rm qgraph/babyKingdom.json
  # rm qgraph/babyKingdom.csv
  put -p /home/ubuntu/nick/babyKingdom/data/babyKingdom.csv /home/1259a6e5b3748c132a80/qgraph/
  bye
SOMEDELIMITER

rm -rf $FILEPATH"babyKingdom.json"
rm -rf $FILEPATH"babyKingdom.csv"