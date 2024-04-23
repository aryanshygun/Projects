from _0_initialize_database import *
from Super_admins import superadmins

class init_workplace:
    def __init__(self) -> None:
        self.active_user = None
        execute_db()
        
    def logged(self, status):
        activation =  status.get(status.username == self.active_user.username)
        activation.is_logged = True
        activation.save()    
        
    def check_logger(self, status):
        if status == Recruiters:
            person = 'admin'
        elif status == Employees:
            person = 'employee'
        active_user_username = input(f'Hello {person}! Please enter your username:\n')
        check_active_user = status.select().where(status.username == active_user_username)
        if check_active_user.exists():
            self.active_user = check_active_user.get()
            active_user_password = input(f'Hi {self.active_user.first_name} {self.active_user.last_name}, please enter your password:\n')
            check_active_user_password = status.select().where(status.password == active_user_password)
            if check_active_user_password.exists():
                print('Congrats! You are now logged in.')
                self.logged(status)
                self.banner()
                    
    def login(self):
        print("--------------------------------------------------")
        print("--------------------------------------------------")
        print("--------------------------------------------------")
        while True:
            log_status = input("Hello there, Are you an Admin(0) or an Employee(1)?\n(If neither, enter (2) to exit.)\n")
            if log_status == '0':
                self.check_logger(Recruiters)
                break
            elif log_status == '1':
                self.check_logger(Employees)
                break
            elif log_status == '2':
                print('Understandble, Have a great day!\n')
                exit()
            else:
                print('Invalid input! Please enter 0 for Admin, 1 for Employee, or 2 to exit.\n')
                
    def banner(self):
        print("--------------------------------------------------")
        print("--------------------------------------------------")
        def print_banner():
            
            recruiter_banner = [
                '-=-=-=-=-=-=-=-=-=-=-=-=-',
                f'Welcome to mission control, {self.active_user.username}!',
                '1. View Profile',
                '2. View Recruiters List',
                '3. View Employees List',
                '4. View Monthly Cash out',
                '5. Register a new employee',
                '6. Fire a registered employee',
                '7. Log out',
                '8. Exit'
            ]
            
            superadmin_banner = recruiter_banner
            superadmin_banner.extend(['9. Register a new recruiter','10. Fire a registered recruiter'])
            
            employee_banner = [
                '-=-=-=-=-=-=-=-=-=-=-=-=-',
                f'Welcome to mission control, {self.active_user.username}!',
                '1. View Profile',
                '2. View salary',
                '3. View co workers List',
                '4. Contact HR in regards to a recruiter',
                '5. Resign from work',
                '7. Log out',
                '8. Exit'
            ]
            
            if isinstance(self.active_user, Employees) :
                print('\n\n'.join(employee_banner))
            elif isinstance(self.active_user, Recruiters):
                if self.active_user.is_superadmin == True:
                    print('\n\n'.join(superadmin_banner))
                else:
                    print('\n\n'.join(recruiter_banner))
        while True:
            print_banner()
            inp = input('Navigate by entering the respective value:\n')
            
            
            
        
        
        
        
        
app = init_workplace()
app.login()