"""
    This module give you opportunity to make queries to database more easily more easily
    Please specify the function you need to use when you import this method.
"""


import mysql.connector

import datetime


def selectQuery(SQL_query : str, 
                query_inserting_values: list, 
                result_column_names : list[str], 
                databaseObject):
    
    if not databaseObject.is_connected():
        # connection corrupted reconnecting
        databaseObject.reconnect(attempts=5, delay=0.5)

    curr = databaseObject.cursor()
    curr.execute(SQL_query, query_inserting_values)
    dbResp = curr.fetchall()
    curr.close()

    # Checking if query has same number of columns as result_columns_names
    # if not throwing an error
    # Making it to prevent unexpected errors because mistakes of uncatched columns
    if len(dbResp) == 0:
        return []
    
    if len(dbResp[0]) != len(result_column_names):
        raise SyntaxError(f"DB query responce number of columns don't match number of provided names for them" \
                          f"QUERY: {SQL_query}" \
                          f"Provided columns: {result_column_names}")
    
    result = []
    for record in dbResp:
        row = {}
        for i in range(len(result_column_names)):
            if isinstance(record[i], datetime.datetime):
                # if there is a time object got from db
                # we tell interpreter that
                # time must be interpreted as utc time
                row[result_column_names[i]] = record[i].replace(tzinfo=datetime.timezone.utc)
            else:
                row[result_column_names[i]] = record[i]
        result.append(row)
    
    return result


def modifyQuery(SQL_query : str, 
                query_inserting_values: list,
                databaseObject,
                multi_q=False):
    
    if not databaseObject.is_connected():
        # connection corrupted reconnecting
        databaseObject.reconnect(attempts=5, delay=0.5)
        
    curr = databaseObject.cursor()
    queries = curr.execute(SQL_query, query_inserting_values, multi=multi_q)
    if multi_q:
        for _ in queries:
            pass
    databaseObject.commit()
    curr.close()