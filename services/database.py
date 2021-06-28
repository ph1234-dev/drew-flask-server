
import psycopg2
from psycopg2 import pool

# Reference
# https://pynative.com/psycopg2-python-postgresql-connection-pooling/
class DatabaseManager:

    def __init__(self):
        self.__HOST="localhost"
        self.__PORT="5432"
        self.__DATABASE="drew"
        self.__USER="postgres"
        self.__PASSWORD="1234"

        self.pool = None

        try:
            self.pool = pool.SimpleConnectionPool(
                    minconn=1,
                    maxconn=3,
                    user=self.__USER,
                    password=self.__PASSWORD,
                    host=self.__HOST,
                    database=self.__DATABASE,
                    )

            # if(self.__postgresql_pool):
            #     print("Pool connection created")

            self.connection = self.pool.getconn()

            # if (self.__connection):
            #     print("Initialization >> Received connection from pool")

        except(Exception, psycopg2.DatabaseError) as error:
            print("Error while connecting to postgres:: % % (error)s")
        # finally:
        #     if (self.__postgresql_pool):
        #         self.__postgresql_pool.closeall
        #         print("Postgresql connection closed")

    def get_connection(self):
        return self.connection

    def get_pool(self):
        return self.pool

    def return_connection(self):    
        print("Put away a PostgreSQL connection")
        return self.pool.putconn(self.connection)

    def is_alive(self):
        status = False
        try:
            cursor = self.connection.cursor() 
            cursor.execute("select 1")
            status = True
        except (Exception) as err:
            status = False
        
        return status
    # def return_pool(self,):
    #     self.pool.putconn(connection)

    # def closeConnection():
    #     self.__pool.closeall

    # def execute_query(self,query):

    #     result = None
    #     try:
            
    #         if (True):
    #             # print("Query [connection==none] >> Received connection from pool")
    #             self.__connection = self.__pool.getconn()
    #             self.__cursor = self.__connection.cursor()
    #             self.__cursor.execute(query)
    #             result = self.__cursor.fetchall()

    #             # for row in result:
    #             #     print(row)

    #             self.__connection.commit()
    #             self.__cursor.close()

    #             # Use this method to release the connection object and send back to connection pool
    #             self.__pool.putconn(self.__connection)


    #     except (Exception, psycopg2.DatabaseError) as error:
    #         print("Error:: " , error)
    #         result = error
    #     finally:
    #         self.__cursor.close()
    #         # Use this method to release the connection object and send back to connection pool
    #         self.__pool.putconn(self.__connection)

    #     return result


    #     """
    #     finally:
    #         # closing database connection.
    #         # use closeall() method to close all the active connection if you want to turn of the application
    #         if self.__postgreSQL_pool:
    #             self.__postgreSQL_pool.closeall
    #             print("PostgreSQL connection pool is closed")
    #     """

db = DatabaseManager()