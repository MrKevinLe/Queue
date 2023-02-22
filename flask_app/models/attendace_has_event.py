from flask_app.config.mysqlconnections import connectToMySQL
from flask import flash
import imp





class Attendance_has_event:
    def __init__ (self,data):
        self.attendance_id= data["attendance_id"]
        self.event_id= data["event_id"]


    @classmethod
    def save_manytomany(cls, data ):
        query = "INSERT INTO attendance_has_event(attendance_id,event_id) VALUES (%(attendance_id)s,%(event_id)s);"
        results=connectToMySQL('meetup').query_db( query, data )
        return results

    @classmethod
    def delete_many (cls,data):
        query = "DELETE FROM attendance_has_event WHERE event_id = %(id)s AND attendance_id = %(ids)s "
        connectToMySQL('meetup').query_db(query,data)

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM attendance_has_event WHERE event_id = %(id)s;"
        result = connectToMySQL('meetup').query_db(query,data)
        return result
    @classmethod
    def get_all(cls, data):
        query ="SELECT * FROM meetup.attendance_has_event;"
        result = connectToMySQL('meetup').query_db(query,data)
        return result