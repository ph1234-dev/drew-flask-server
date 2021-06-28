from .database import db
import psycopg2
from functools import wraps

class Log_Service:

    def __init__(self):
      print ("Log service initiated")

    def log_conversation(self,user_id,user_message,bot_reply):
        result = {}
        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            sql = ("call log_conversation('%s','%s','%s')"%(user_id,user_message,bot_reply))
            cursor.execute(sql)
            conn.commit()
            cursor.close()

            result['success'] = True
        except (Exception, psycopg2.DatabaseError) as err:
            result['success'] = False
            result['error'] = err
            
        return result;        

