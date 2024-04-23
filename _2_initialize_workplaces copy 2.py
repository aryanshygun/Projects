from _0_initialize_database import *

class init_workplace:
    def __init__(self) -> None:
        self.active_user = None
        execute_db()
        
    def logged(self, status):
        activation =  status.get(status.username == self.active_user.username)
        activation.is_logged = True
        activation.save()    
    
    def logged_out(self, status):
        deactivation = status.get(status.username == self.active_user.username)
        deactivation.is_logged = False
        deactivation.save()
        self.active_user = None
        print('Logging out...')
        print('Have a good day!')
    
    def exitting():
        print('Bye!')
        print("--------------------------------------------------")
        print("--------------------------------------------------")
        exit()
        
    def check_logger(self, status):
        if status == Recruiters:
            person = 'admin'
        elif status == Employees:
            person = 'employee'
        
        while True:
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
                    break
            else:
                print("Username Doesn't exist in our database, Try again\n")
                print("--------------------------------------------------")
            
                    
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
                
    def view_profile(self):
        
        if isinstance(self.active_user, Recruiters):
            stats = Recruiters.get(Recruiters.username == self.active_user.username)
            print("--------------------------------------------------")
            print('Here is your profile!\n')
            print('Username: ', stats.username)
            print('First name: ', stats.first_name)
            print('Last name: ', stats.last_name)
            print('Password: ', stats.password)
            print('Superadmin: ', stats.is_superadmin)
            print("--------------------------------------------------")
            
        elif isinstance(self.active_user, Employees):
            stats = Employees.get(Employees.username == self.active_user.username)
            print("--------------------------------------------------")
            print('Here is your profile!\n')
            print('Username: ', stats.username)
            print('First name: ', stats.first_name)
            print('Last name: ', stats.last_name)
            print('Password: ', stats.password)
            print('Profession: ', stats.profession)
            print('Age: ', stats.age)
            print('Experience: ', stats.experience)
            print("--------------------------------------------------")
                    
    def banner(self):
        print("--------------------------------------------------")
        print("--------------------------------------------------")
        if isinstance(self.active_user, Employees):
            employee_banner = [
                '-=-=-=-=-=-=-=-=-=-=-=-=-',
                f'Welcome to mission control, {self.active_user.first_name}!',
                '1. View Profile',
                '2. View salary',
                '3. View co workers List',
                '4. Contact HR in regards to a recruiter',
                '5. Resign from work',
                '6. Log out',
                '7. Exit']
            print('\n'.join(employee_banner))
            while True:
                inp = input('Navigate by entering the respective value:\n')
                if inp == '1':
                    self.view_profile()
                elif inp == '2':
                    self.view_salary()
                elif inp == '3':
                    self.view_coworker_employees()
                elif inp == '4':
                    self.complaint()
                elif inp == '5':
                    self.resignation()
                elif inp == '6':
                    self.logged_out(Employees)
                    app.login()
                    return
                elif inp == '7':
                    self.exitting()

        elif isinstance(self.active_user, Recruiters) and self.active_user.is_superadmin == False:
            recruiter_banner = [
                '-=-=-=-=-=-=-=-=-=-=-=-=-',
                f'Welcome to mission control, {self.active_user.first_name}!',
                '1. View Profile',
                '2. View Recruiters List',
                '3. View Employees List',
                '4. View Monthly Cash out',
                '5. Register a new employee',
                '6. Fire a registered employee',
                '7. Resign from work',
                '8. Log out',
                '9. Exit']            
            print('\n'.join(recruiter_banner))
            while True:
                inp = input('Navigate by entering the respective value:\n')
                if inp == '1':
                    self.view_profile()
                elif inp == '2':
                    self.view_recruiters()
                elif inp == '3':
                    self.view_employees()
                elif inp == '4':
                    self.cashout()
                elif inp == '5':
                    self.register_employee()
                elif inp == '6':
                    self.fire_employee()
                elif inp == '7':
                    self.resignation()
                elif inp == '8':
                    self.logged_out(Recruiters)
                    app.login()
                    return
                elif inp == '9':
                    self.exitting()
                    
        elif isinstance(self.active_user, Recruiters) and self.active_user.is_superadmin == True:
            superadmin_banner = [
                '-=-=-=-=-=-=-=-=-=-=-=-=-',
                f'Welcome to mission control, {self.active_user.first_name}!',
                '1. View Profile',
                '2. View Recruiters List',
                '3. View Employees List',
                '4. View Monthly Cash out',
                '5. Register a new employee',
                '6. Fire a registered employee',
                '7. Log out',
                '8. Exit',
                '9. Register a new recruiter',
                '10. Fire a registered recruiter']  
            
            print('\n'.join(superadmin_banner))
            while True:
                inp = input('Navigate by entering the respective value:\n')
                if inp == '1':
                    self.view_profile()
                elif inp == '2':
                    self.view_recruiters()
                elif inp == '3':
                    self.view_employees()
                elif inp == '4':
                    self.cashout()
                elif inp == '5':
                    self.register_employee()
                elif inp == '6':
                    self.fire_employee()
                elif inp == '7':
                    self.logged_out(Recruiters)
                    app.login()
                    return
                elif inp == '8':
                    self.exitting()
                elif inp == '9':
                    self.register_recruiter()
                elif inp == '10':
                    self.fire_recruiter()
        
            
        
        
        
        
        
app = init_workplace()
app.login()