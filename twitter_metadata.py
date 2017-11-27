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
    sql = """
        SELECT uid, handle, name FROM twitter_user
        WHERE uid IN ({})
    """.format(','.join([str(uid) for uid in uids]))
    c = db_conn.cursor()
    c.execute(sql)

    results = {uid: name or handle for uid, handle, name in c.fetchall()}

    remaining_uids = set([int(uid) for uid in uids]).difference(set(results.keys()))
    if not remaining_uids:
        return results

    # TODO make this work for more than 100 uids
    lookup_time = time.time()
    users = api.UsersLookup(user_id=list(remaining_uids))
    for u in users:
        # danger will robinson!! injecting data from public api into db. TODO sanitize
        insert_sql = """
            INSERT INTO twitter_user VALUES ({}, '{}', '{}', {}, '{}')
        """.format(u.id, u.screen_name, u.name.replace("'","''"), lookup_time, u.AsJsonString().replace("'","''"))
        print(insert_sql)
        c.execute(insert_sql)

        results[u.id] = u.name or u.screen_name

    db_conn.commit()
    return results

