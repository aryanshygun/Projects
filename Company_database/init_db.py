# in this code we create the models and add to the database
import os
from peewee import *
from Super_admins import *

class Defaultmodel(Model):
    class Meta:
        database = SqliteDatabase('Main DataBase.db')

class Recruiters(Defaultmodel):
    username = CharField(unique = True, index = True)    
    first_name = CharField()
    last_name = CharField()
    password = CharField()
    is_superadmin = BooleanField()
    is_logged = BooleanField()
    
class Employees(Defaultmodel):
    username = CharField(unique = True, index = True)
    first_name = CharField()
    last_name = CharField()
    password = CharField()
    profession = CharField()
    experience = IntegerField()    
    is_logged = BooleanField()

class Careers(Defaultmodel):
    career = CharField(unique = True, index = True)
    salary_per_month = CharField()
    available_spots = IntegerField()
    experience_required = IntegerField()


db = SqliteDatabase('Main DataBase.db')

class Actions:
    @staticmethod
    def add_tables():
        db.connect()
        db.create_tables([Careers,Recruiters, Employees])

    @staticmethod
    def drop_tables():
        with db:
            db.drop_tables([Careers, Employees, Recruiters])
    
    @staticmethod
    def add_super_admins():
        for admin in superadmins:
            Recruiters.create(
                username = admin,
                first_name = superadmins[admin]['full_name'].split()[0],
                last_name = superadmins[admin]['full_name'].split()[1],
                password = superadmins[admin]['password'],
                is_superadmin = True,
                is_logged = False     
            )
    @staticmethod        
    def add_careers():
        for i in careers:
            Careers.create(
                career = careers[i]['career'],
                salary_per_month = careers[i]['salary_per_month'],
                available_spots = careers[i]['available_spots'],
                experience_required = careers[i]['experience_required']
            )
        
def execute_db():
    if not os.path.exists('Main DataBase.db'):
        Actions.add_tables()
        Actions.add_super_admins()
        Actions.add_careers()
