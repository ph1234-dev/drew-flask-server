from .database import db
import psycopg2


class User_Service:

    def __init__(self):
        print("user service created")

    def check_username_exist(self,username):
        result = {}
        
        try:

            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("select username from users u where u.username='%s'" %(username))
            
            result_set = cursor.fetchone()
            if ( result_set is not None):
                result['username'] = result_set[0]
                # result['status'] = "exist"
                result['exist'] = True
            else:
                result['exist'] = False
                pass
                # result['status'] = "username does not exist"
            cursor.close()
            conn.commit()
            
        except (Exception,psycopg2.DatabaseError) as err:
            result['check username'] ="check username"
            result['error'] = err

        
        return result


    def check_userid_exist(self,id):
        # print("checking if user: [%s] exist" %(id) )
        result = {}
        
        try:

            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("select id from users where id=%s" %(id))
            
            result_set = cursor.fetchone()
            if ( result_set is not None):
                result['user_id'] = result_set[0]
                result['status'] = "exist"
            else:
                result['status'] = "user does not exist"
            cursor.close()
            conn.commit()
            
        except (Exception,psycopg2.DatabaseError) as err:
            result['check user id'] ="check user id"
            result['error'] = err

        
        return result

    def login_user(self,username,password):
        print("logging user: " + username)

        result = {}
        try:
            conn = None
            conn = db.get_connection()
            cursor = conn.cursor()
            sql = ("select id,name from users where username='%s' and password='%s'" % (username,password))
            cursor.execute(sql)
            conn.commit()
            
            result_set = cursor.fetchone()
            # returns a row

            if (result_set is not None):
                result['id'] = result_set[0]
                result['name'] = result_set[0]
                result['success'] = True
            else:
                result['success'] = False
            
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as err:
            # print ("create user error:: %s" % (err))
            result['success'] = False
            result['error'] = err
            # conn.rollback()

        return result

    def create_user(self,username,password,name):
        print("Creating new user:: " + username)
        
        result = {}

        try:
            conn = db.get_connection()
            cursor = conn.cursor()
            sql = ("call create_user('%s','%s','%s')" % (username,password,name))
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            result['status'] = "ok"
        except (Exception, psycopg2.DatabaseError) as err:
            # print ("create user error:: %s" % (err))
            result['error'] = err
            conn.rollback()

        return result