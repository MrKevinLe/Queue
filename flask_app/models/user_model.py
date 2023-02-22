from flask_app import app
from flask_app.config.mysqlconnections import connectToMySQL
from flask import flash
import re
import imp
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__ (self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.phone_number = data['phone_number']
        self.about = data['about']
        self.age = data['age']
        self.gamer_tag = data['gamer_tag']



    # Create a user 
    @classmethod
    def save(cls,data):
        query = "INSERT INTO user (first_name,last_name,email,password,phone_number,about,age,gamer_tag) VALUES ( %(first_name)s ,%(last_name)s,%(email)s,%(password)s,%(phone_number)s,%(about)s,%(age)s,%(gamer_tag)s);"
        results=connectToMySQL('meetup').query_db( query, data )
        return results

    # validate the user creation
    @staticmethod
    def validate_user(user):
        is_valid = True # we assume this is true
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters.")
            is_valid = False
        if len(user['first_name']) == 0 :
            flash("First name can not be empty")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 character")
            is_valid = False
        if len(user['password']) <  3:
            flash("Password must have at least 3 characters")
            is_valid = False
        if len(user['password']) == 0:
            flash("Password can not be empty")
            is_valid = False
        if len(user['confirm_password']) == 0:
            flash("Password can not be empty")
            is_valid = False
        if len(user['email']) == 0:
            flash("email can not be empty")
            is_valid = False
        if len(user['gamer_tag']) == 0:
            flash("gamer_tag can not be empty")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash('Passwords must match')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False

        return is_valid

    # validate the login
    @staticmethod
    def validate_login(user):
        is_valid = True # we assume this is true

        if len(user['email']) == 0 :
            flash("email name can not be empty")

        if len(user['password']) == 0 :
            flash("password name can not be empty")

        if user['password'] != user['password']:
            flash('wrong')
            is_valid = False


        return is_valid


    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM user WHERE email = %(email)s;"
        result = connectToMySQL("meetup").query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])



    @classmethod
    def get_by_id(cls,data ):
        query = "SELECT * FROM user WHERE id = %(ids)s;"
        result = connectToMySQL("meetup").query_db(query,data)

        return result

    @classmethod
    def get_by_user_id(cls,data ):
        query = "SELECT * FROM user WHERE id = user_id;"
        result = connectToMySQL("meetup").query_db(query,data)
        return result



    @classmethod
    def get_both_user_id(cls,data):
        query = 'SELECT * FROM user JOIN event ON user.id = event.user_id WHERE user.id =%(id)s' 
        results = connectToMySQL("meetup").query_db(query,data)
        return results

    @classmethod
    def get_both_other_id(cls,data):
        query = 'SELECT * FROM user JOIN event ON user.id = event.user_id WHERE event.id =%(id)s'  
        results = connectToMySQL("meetup").query_db(query,data)
        return results

    @classmethod
    def get_all(cls,data):
        query = "SELECT * FROM meetup.user;"
        results = connectToMySQL("meetup").query_db(query,data)
        return results
