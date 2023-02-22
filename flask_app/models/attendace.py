from flask_app.config.mysqlconnections import connectToMySQL
from flask import flash
import imp





class Attendance:
    def __init__ (self,data):
        self.name = data['name']

    @classmethod
    def save_attend(cls, data ):
        query = "INSERT INTO attendance(name) VALUES (%(name)s);"
        results=connectToMySQL('meetup').query_db( query, data )
        return results

    @classmethod
    def get_all(cls,data):
        query = "SELECT * FROM meetup.attendance;"
        results = connectToMySQL('meetup').query_db(query,data)
        return results

    @classmethod
    def delete (cls,data):
        query = "DELETE FROM meetup.attendance WHERE id = %(id)s"

        connectToMySQL('meetup').query_db(query,data)