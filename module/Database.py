"""
    Import this module if you need to make query to database
    Stores database object
"""

import config
import mysql.connector

myDatabase = mysql.connector.connect(**config.databaseConfig)