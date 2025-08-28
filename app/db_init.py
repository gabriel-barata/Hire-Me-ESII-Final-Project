import mysql.connector as sql
from modules.creds import user_pwd

from app.cv_schema_init import *

mycon = sql.connect(host="localhost", user="any_test", passwd=user_pwd)
cur = mycon.cursor()
cur.execute(CREATE_SCHEMA)
cur.execute(Create_users_Table)
cur.execute(Create_recruiter_Table)
cur.execute(Create_client_Table)
cur.execute(Create_Job_Table)
cur.execute(Create_Application_Table)
mycon.close()
