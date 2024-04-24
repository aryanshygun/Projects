from init_db import *

class init_workplace:
    
    def __init__(self) -> None:
        self.active_user = None
        execute_db()
        
    ############################################    
    # HEADER - LOGIN - CHECK_LOGGER - LOGGGED OUT - EXITTING 
    ############################################  
    
    def header():
        print("\\\\//   \\\\//   \\\\//   \\\\//   \\\\//   \\\\//   \\\\//")
        print("   \\\\//   \\\\//   \\\\//   \\\\//   \\\\//   \\\\//   ")
        print("\\\\//   \\\\//   \\\\//   \\\\//   \\\\//   \\\\//   \\\\//") 
        
    def login(self):
        self.header()
        while True:
            log_status = input("Hello there! State your class:\n0 - Admin\n1 - Employee\n2 - Exit\n")
            if log_status == '0':
                self.check_logger(Recruiters)
                break
            elif log_status == '1':
                self.check_logger(Employees)
                break
            elif log_status == '2':
                print('Understandble, Have a great day!\n')
                self.exitting()
                os.remove('Projects/Company_database/Main Database.db')
                exit()
            print('Invalid answer! Try again:\n')  

    def check_logger(self, status):
        if status == Recruiters:
            person = 'admin'
        elif status == Employees:
            person = 'employee'
        print(f'Hello {person}! Please enter your username:')
        while True:
            username = input()
            if status.select().where(status.username == username).exists():
                self.active_user = status.select().where(status.username == username).get()
                print(f'Hi {self.active_user.first_name} {self.active_user.last_name}!\nplease enter your password:')
                while True:
                    active_user_password = input()
                    if active_user_password == self.active_user.password:
                        print('Congrats! You are now logged in.')
                        self.active_user.is_logged = True
                        self.active_user.save()
                        self.banner()
                        break
                    print('Incorrect password, Try again!')        
            print("Username Doesn't exist in our database, Try again:")
    
    def logged_out(self):
        self.active_user.is_logged = False
        self.active_user.save()
        self.active_user = None
        print('Logging out...')
        print('Have a good day!')
        self.header()
        self.login()
        return True
         
    def exitting(self):
        print('Bye!')
        self.header()
         
    ############################################    
    # REGISTRATION - TERMINATION - RESIGNATION
    ############################################  

    def registration(self, status):
        if status == Employees:
            while True:
                career_path = input("What's their profession?\nenginner\nteacher\nworker\n")
                careers = ['engineer', 'worker', 'teacher']
                if career_path not in careers:
                    print('Invalid response, try again.\n')
                else:
                    break
            profession = Careers.get(Careers.career == career_path)
            if profession.available_spots != 0:
                print("Luckily there are available spots!.")
                profession.available_spots -= 1
                profession.save()
            else:
                print('Unfortunately there are no available spots.\n')
                return True
            username = input("Enter the person's username:\n").lower()
            if Employees.select().where(Employees.username == username).exists():
                print('The user is already accepted!\n')
                return True
            yoe = int(input("How many years of experience do they have?\n"))
            if yoe < profession.experience_required:
                print("Unfortunately the person doesn't have the minimum amount of experience required.\n")
                return True
            Employees.create(
                username = username,
                first_name = username.title(),
                last_name = input("Enter the person's last name: \n").title(),
                password = input("Enter the person's desired password: \n"),
                profession = career_path,
                experience = yoe,
                is_logged = False)
            print('Successfully registered the Recruiter\n')
            return True
        elif status == Recruiters:
            username = input('Enter their username:\n').lower()
            if Recruiters.select().where(Recruiters.username == username).exists():
                print('The user is already accepted!\n')
                return True
            Recruiters.create(
                username = username,
                first_name = username.title(),
                password = input("Enter their password: \n"),
                last_name = input("Enter their last name: \n").title(),
                is_superadmin = False,
                is_logged = False )
            print('Successfully registered the Recruiter\n')
        
    def termination(self, status):
        empty_list = (status.select().count() == 0)
        if empty_list:
            print('No users to be found.\n')
            return True
        self.view_list(status)
        print("--------------------------------------------------")
        id = int(input("Enter the person's ID\n"))
        terminate = status.get(status.id == id)
        if isinstance(terminate, Employees):
            addone = Careers.get(Careers.career == terminate.profession)
            addone.available_spots += 1
            addone.save()
        if isinstance(terminate, Recruiters):
            if terminate.is_superadmin == True:
                print('You cant terminate another super admin.\n')
                return True
        terminate.delete_instance()
        print("--------------------------------------------------")
        print('User terminated.\n')
        return True
                    
    def resignation(self, status):
        resign = status.get(status.username == self.active_user.username)
        resign.delete_instance()
        if status == Employees:
            addone = Careers.get(Careers.career == self.active_user.profession)
            addone.available_spots += 1
            addone.save()
        self.active_user = None
        print('Good luck in your future endavours!\n')
        self.exitting() 
        self.login()
        return True
      
    ############################################    
    # VIEW LIST - VIEW SALARY
    ############################################         
          
    def view_list(self, status):
        if status == Employees:
            if Employees.select().count() == 0:
                print('No users to be found.\n')
                return True
            for i in Employees.select():
                print("--------------------------------------------------")
                employee = [f'{i.id}',
                    f'Username: {i.username}',
                    f'First name: {i.first_name}',
                    f'Last name: {i.last_name}',
                    f'profession: {i.profession}',
                    f'experience: {i.experience}',
                    f'Login status: {i.is_logged}']
                print('\n'.join(employee)) 
            return True
        elif status == Recruiters:
            for i in Recruiters.select():
                print("--------------------------------------------------")
                recruiter = [f'{i.id}',
                    f'Username: {i.username}',
                    f'First name: {i.first_name}',
                    f'Last name: {i.last_name}',
                    f'Super admin: {i.is_superadmin}',
                    f'Login status: {i.is_logged}']
                print('\n'.join(recruiter))
            return True
        elif status == Careers:
            for i in Careers.select():
                print("--------------------------------------------------")
                careers = [f'{i.id}',
                    f'career: {i.career}',
                    f'Salary per month: {i.salary_per_month}',
                    f'Available spots: {i.available_spots}',
                    f'Experience required: {i.experience_required}']
                print('\n'.join(careers))
            return True
                  
    def view_salary(self):
        career = Careers.get(Careers.career == self.active_user.profession)
        print(f"Your current monthly salary is {career.salary_per_month}!")
        return True
                    
    ############################################    
    # BANNER
    ############################################          
    
    def banner(self):
        self.header()
        if isinstance(self.active_user, Employees):
            employees_banner = [
                '-=-=-=-=-=-=-=-=-=-=-=-=-',
                f'Welcome to mission control, Employee {self.active_user.first_name}!',
                '',
                '1. View - Employees ',
                '2. View - Careers ',
                '3. View - Salary',
                '',
                '4. Resign',
                '5. Log out',
                '6. Exit',
                '-=-=-=-=-=-=-=-=-=-=-=-=-',
                '']  
            print('Navigate by entering the respective number:')
            while True:
                print('\n'.join(employees_banner))
                inp = int(input())
                if inp == 1:
                    self.view_list(Employees)
                elif inp == 2:
                    self.view_list(Careers)
                elif inp == 3:
                    self.view_salary()
                elif inp == 4:
                    self.resignation(Employees)
                elif inp == 5:
                    self.logged_out()
                elif inp == 6:
                    self.exitting()
                    os.remove('Projects/Company_database/Main Database.db')
                    exit()
        elif isinstance(self.active_user, Recruiters) and self.active_user.is_superadmin == False:
            recruiter_banner = [
                '-=-=-=-=-=-=-=-=-=-=-=-=-',
                f'Welcome to mission control, Recruiter {self.active_user.first_name}!',
                '',
                '1. View - Employees ',
                '2. View - Careers ',
                '3. View - Recruiters ',
                '',
                '4. Register  - Employee',
                '5. Terminate - Employee',
                '',
                '6. Resign',
                '7. Log out',
                '8. Exit',
                '-=-=-=-=-=-=-=-=-=-=-=-=-',
                '']  
            print('Navigate by entering the respective number:')
            while True:
                print('\n'.join(recruiter_banner))
                inp = int(input())
                if inp == 1:
                    self.view_list(Employees)
                elif inp == 2:
                    self.view_list(Careers)
                elif inp == 3:
                    self.view_list(Recruiters)
                elif inp == 4:
                    self.registration(Employees)
                elif inp == 5:
                    self.termination(Employees)
                elif inp == 6:
                    self.resignation(Recruiters)
                elif inp == 7:
                    self.logged_out()
                elif inp == 8:
                    self.exitting()
                    os.remove('Projects/Company_database/Main Database.db')
                    exit()                    
        elif isinstance(self.active_user, Recruiters) and self.active_user.is_superadmin == True:
            superadmin_banner = [
                '-=-=-=-=-=-=-=-=-=-=-=-=-',
                f'Welcome to mission control, Super-Admin {self.active_user.first_name}!',
                '',
                '1.  View - Employees ',
                '2.  View - Careers ',
                '3.  View - Recruiters ',
                '',
                '4.  Register  - Employee',
                '5.  Terminate - Employee',
                '',
                '6.  Register  - Recruiter',
                '7.  Terminate - Recruiter',
                '',
                '8.  View Monthly Cash out',
                '',
                '9.  Log out',
                '10. Exit',
                '-=-=-=-=-=-=-=-=-=-=-=-=-',
                '']  
            print('Navigate by entering the respective number:')
            while True:
                print('\n'.join(superadmin_banner))
                inp = int(input())
                if inp == 1:
                    self.view_list(Employees)
                elif inp == 2:
                    self.view_list(Careers)
                elif inp == 3:
                    self.view_list(Recruiters)
                elif inp == 4:
                    self.registration(Employees)
                elif inp == 5:
                    self.termination(Employees)
                elif inp == 6:
                    self.registration(Recruiters)
                elif inp == 7:
                    self.termination(Recruiters)
                elif inp == 8:
                    self.cashout()
                elif inp == 9:
                    self.logged_out()
                elif inp == 10:
                    self.exitting()
                    os.remove('Projects/Company_database/Main Database.db')
                    exit()
          
app = init_workplace()

if __name__=='__main__':
    app.login()