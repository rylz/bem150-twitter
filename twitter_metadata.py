import json
import sqlite3
import time
import twitter

import config

api = twitter.Api(
        consumer_key=config.consumer_key,
        consumer_secret=config.consumer_secret,
        access_token_key=config.access_token_key,
        access_token_secret=config.access_token_secret)
db_conn = sqlite3.connect('metadata.db')

def get_user_names(uids):
    """Gets and saves twitter metadata for given uids.

    First tries the sqlite store for user metadata. Falls through to Twitter API for ground truth,
    and saves results to sqlite.

    Returns {uid: name} dictionary, with name falling back to the user's handle when not specified.

    """
    full_data = _get_twitter_metadata(uids)
    return {u: data[1] or data[0] for u, data in full_data.items()}


def get_twitter_handles(uids):
    """Gets and saves twitter metadata for given uids.

    First tries the sqlite store for user metadata. Falls through to Twitter API for ground truth,
    and saves results to sqlite.

    Returns {uid: handle} dictionary.

    """
    full_data = _get_twitter_metadata(uids)
    return {u: data[0] for u, data in full_data.items()}


def _get_twitter_metadata(uids):
    sql = """
        SELECT uid, handle, name, api_lookup_time, additional_metadata FROM twitter_user
        WHERE uid IN ({})
    """.format(','.join([str(uid) for uid in uids]))
    c = db_conn.cursor()
    c.execute(sql)

    results = {uid: (handle, name, lookup_time, metadata) for uid, handle, name, lookup_time, metadata in c.fetchall()}

    remaining_uids = list(set([int(uid) for uid in uids]).difference(set(results.keys())))
    if not remaining_uids:
        return results

    lookup_time = time.time()
    BATCH_SIZE = 100
    for i in range(0, len(remaining_uids), BATCH_SIZE):
        try:
            users = api.UsersLookup(user_id=list(remaining_uids[i:i+BATCH_SIZE]))
        except twitter.TwitterError as e:
            # for now, gracefully fail when the API fails (perhaps deleted accounts?)
            # note that this will allow one bad uid to fail for an entire batch...
            print("API failure for batch", e)
            for u in remaining_uids:
                results[u] = str(u)
            continue

        for u in users:
            # danger will robinson!! injecting data from public api into db. TODO sanitize
            insert_sql = """
                INSERT INTO twitter_user VALUES ({}, '{}', '{}', {}, '{}')
            """.format(u.id, u.screen_name, u.name.replace("'","''"), lookup_time, u.AsJsonString().replace("'","''"))
            c.execute(insert_sql)

            results[u.id] = (u.screen_name, u.name, lookup_time, u.AsJsonString())

    db_conn.commit()
    return results

