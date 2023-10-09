from argparse import ArgumentParser
from bson import ObjectId
import logging
import os
import json


from pymongo import MongoClient, ASCENDING

from dotenv import load_dotenv


load_dotenv()

# config logger
logging.basicConfig(

    format='%(asctime)s %(levelname)s:%(name)s: %(message)s',

    level=logging.DEBUG,

    datefmt='%Y-%m-%d %H:%M:%S'

)


logger = logging.getLogger('areq')
logging.getLogger('chardet.charsetprober').disabled = True


if __name__ == '__main__':


    scriptDirectory = os.path.dirname(os.path.realpath(__file__))

    result_file = scriptDirectory + '/update_status.json'

    parser = ArgumentParser(

        usage='python replicate_data_across_db.py --source <db> --destination <db>',

        description='This program replicates all of the data from one db to another db.')

    parser.add_argument('--source', dest='source', help='the source db', required=True)

    parser.add_argument('--destination', dest='destination', help='the destinated db', required=True)


    args = parser.parse_args()


    source = args.source

    destination = args.destination


    print(result_file)

    with open(result_file, 'r') as f:

        update_status = json.loads(f.read())


    file_obj = open(result_file, 'w')

    client = MongoClient(os.getenv('MONGO_HOST'))


    # replicate profiles

    logger.info(f'replicate profiles table from {source} to {destination}')


    succ_count = 0

    fail_count = 0

    source_collection = client[source]['profiles']

    dest_collection = client[destination]['profiles']


    if 'profiles' in update_status:

        query = {'mTime': {'$gte': update_status['profiles']}}

    else:

        query = {}


    for record in source_collection.find(query).sort('mTime', ASCENDING):

        userId = record.pop('userId')

        try:

            dest_collection.update_one({'userId': userId}, {'$set': record}, upsert=True)

            succ_count += 1

        except Exception as e:

            logger.error(f'upsert error: {e}')

            fail_count += 1

        update_status['profiles'] = record['mTime']


    logger.info(f'replicate {succ_count} profiles entries successfully, {fail_count} failed.')


    # replicate user_details

    logger.info(f'replicate user_details table from {source} to {destination}')


    succ_count = 0

    fail_count = 0

    source_collection = client[source]['user_details']

    dest_collection = client[destination]['user_details']


    if 'user_details' in update_status:

        query = {'mTime': {'$gte': update_status['user_details']}}

    else:

        query = {}

    

    for record in source_collection.find(query).sort('mTime', ASCENDING):

        userId = record.pop('userId')

        try:

            dest_collection.update_one({'userId': userId}, {'$set': record}, upsert=True)

            succ_count += 1

        except Exception as e:

            logger.error(f'upsert error: {e}')

            fail_count += 1

        update_status['user_details'] = record['mTime']


    logger.info(f'replicate {succ_count} user_details entries successfully, {fail_count} failed.')


    # replicate user_details

    logger.info(f'replicate events table from {source} to {destination}')


    succ_count = 0

    fail_count = 0

    source_collection = client[source]['events']

    dest_collection = client[destination]['events']


    if 'events' in update_status:

        query = {'_id': {'$gt': ObjectId(update_status['events'])}}

    else:

        query = {}

    

    for record in source_collection.find(query).sort('_id', ASCENDING):

        try:

            dest_collection.insert_one(record)

            succ_count += 1

        except Exception as e:

            logger.error(f'insert error: {e}')

            fail_count += 1

        update_status['events'] = str(record['_id'])


    logger.info(f'replicate {succ_count} events entries successfully, {fail_count} failed.')


    file_obj.write(json.dumps(update_status))

    file_obj.close()