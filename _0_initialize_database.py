# in this code we create the models and add to the database
import os
from peewee import *
from Super_admins import superadmins

class Defaultmodel(Model):
    class Meta:
        database = SqliteDatabase('Main DataBase.db')

class Workplaces(Defaultmodel):
    career_path = CharField(unique = True, index = True)
    salary_per_month = CharField()
    max_employee = IntegerField()
    experience_required = IntegerField()
    age_limit = IntegerField()

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
    age = IntegerField()
    experience = IntegerField()    
    is_logged = BooleanField()

db = SqliteDatabase('Main DataBase.db')

class Actions:
    @staticmethod
    def add_tables():
        db.connect()
        db.create_tables([Workplaces,Recruiters, Employees])

    @staticmethod
    def drop_tables():
        with db:
            db.drop_tables([Workplaces, Employees, Recruiters])
    
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
    
def execute_db():
    if not os.path.exists('Main DataBase.db'):
        Actions.add_tables()
        Actions.add_super_admins()
    else:
        Actions.drop_tables()
        Actions.add_tables()
        Actions.add_super_admins()
    # Actions.add_tables()
    # Actions.add_super_admins()

# def drop_db():
#     Actions.drop_tables()

if __name__ == '__main__':
    execute_db()
    
# execute_db()
# x = 'aaamir'
# user_to_change = Recruiters.get(Recruiters.username == 'amir')  # Change condition to match user ID
# user_to_change.username = x
# user_to_change.save()

# user = Recruiters.get(Recruiters.username == 'amir')
# user.is_logged = True
# user.save()
# print(user.is_logged)