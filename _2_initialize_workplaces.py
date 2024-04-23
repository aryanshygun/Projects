from _0_initialize_database import *
from Super_admins import superadmins

class init_workplace:
    def __init__(self) -> None:
        self.active_user = None
        execute_db()
        # db = SqliteDatabase('Main DataBase.db')
        # db.connect()
        
    def login(self):
        print("--------------------------------------------------")
        print("--------------------------------------------------")
        print("--------------------------------------------------")
        while True:
            log_status = input("Hello there, Are you an Admin(0) or an Employee(1)?\n(If neither, enter (2) to exit.)\n")
            if log_status == '0':
                if self.login_admin():
                    break
            elif log_status == '1':
                if self.login_employee():
                    break
            elif log_status == '2':
                print('Understandble, Have a great day!\n')
                exit()
            else:
                print('Invalid input! Please enter 0 for Admin, 1 for Employee, or 2 to exit.\n')
    
    def logged(self, status):
        activation =  status.get(status.username == self.active_user.username)
        activation.is_logged = True
        activation.save()
        
    def login_admin(self):
        active_user_username = input('Hello admin! Please enter your username:\n')
        check_active_user = Recruiters.select().where(Recruiters.username == active_user_username)
        if check_active_user.exists():
            self.active_user = check_active_user.get()
            active_user_password = input(f'Hi {self.active_user.first_name} {self.active_user.last_name}, please enter your password:\n')
            check_active_user_password = Recruiters.select().where(Recruiters.password == active_user_password)
            if check_active_user_password.exists():
                print('Congrats! You are now logged in.')
                self.logged(Recruiters)
                

                return True
            else:
                print('Invalid password! Please try again.\n')
        else:
            print('Invalid username! Please try again.\n')
        
    def login_employee(self):
        while True:
            active_user_username = input('Hello dear employee! Please enter your username:\n')
            check_active_user = Employees.select().where(Employees.username == active_user_username)
            if check_active_user.exists():
                self.active_user = check_active_user.get()
                active_user_password = input(f'Hi {self.active_user.first_name} {self.active_user.last_name}, please enter your password:\n')
                check_active_user_password = Employees.select().where(Employees.password == active_user_password)
                if check_active_user_password.exists():
                    print('Congrats! You are now logged in.')
                    # activate_status = Recruiters.get(Recruiters.username == 'amir')
                    # activate_status.is_logged = True
                    # activate_status.save()
                    
                    # self.banner()
                    return True
                else:
                    print('Invalid password! Please try again.\n')
            else:
                print('Invalid username! Please try again.\n')    
        
app = init_workplace()
app.login()