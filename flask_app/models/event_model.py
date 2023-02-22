from datetime import date
from flask_app.config.mysqlconnections import connectToMySQL
from flask import flash
import imp
from flask_app.models.user_model import User





class Event:
    def __init__ (self,data):
        self.title = data['title']
        self.location = data['location']
        self.activity = data['activity']
        self.user_id= data["user_id"]
        self.image_url = data["image_url"]


    @classmethod
    def save_event(cls, data ):
        query = "INSERT INTO event(title,location,activity,image_url,user_id) VALUES (%(title)s,%(location)s,%(activity)s,%(image_url)s,%(user_id)s);"
        results=connectToMySQL('meetup').query_db( query, data )
        return results

    @classmethod
    def get_all(cls,data):
        query = "SELECT * FROM meetup.event;"
        results=connectToMySQL('meetup').query_db( query, data )
        return results


    @staticmethod
    def validate_event(event):
        is_valid = True # we assume this is true

        if len(event['title']) == 0 :
            flash("title name can not be empty")
            is_valid = False

        if len(event['title'])  < 5 :
            flash("title name can not be less than 5 characters")
            is_valid = False

        if len(event['location']) == 0 :
            flash("location name can not be empty")
            is_valid = False

        if len(event['location'])  < 5 :
            flash("location name can not be less than 5 characters")
            is_valid = False

        if len(event['activity']) == 0 :
            flash("activity can not be empty")
            is_valid = False
            
        if len(event['image_url']) == 0 :
            flash("activity can not be empty")
            is_valid = False

        if len(event['activity']) < 5 :
            flash("activity name can not be less than 5 characters")
            is_valid = False

        return is_valid


    @classmethod
    def get_event(cls,data):
        query = "SELECT * FROM event JOIN user ON event.user_id = user.id"
        results = connectToMySQL('meetup').query_db(query,data)
        return results

    @classmethod
    def get_both_by_event_id(cls,data):
        query = "SELECT * FROM event JOIN user ON user.id = event.user_id WHERE event.id =%(id)s"
        results = connectToMySQL('meetup').query_db(query,data)
        return results

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM event WHERE id = %(id)s;"
        result = connectToMySQL('meetup').query_db(query,data)
        return result

    @classmethod
    def edit(cls, data):
        query = "UPDATE event SET title=%(title)s, location=%(location)s, activity=%(activity)s where id = %(id)s;"
        connectToMySQL('meetup').query_db(query, data)
        return


    @classmethod
    def delete (cls,data):
        query = "DELETE FROM event WHERE id = %(id)s"
        connectToMySQL('meetup').query_db(query,data)