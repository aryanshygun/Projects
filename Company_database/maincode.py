from init_db import *

class init_workplace:
    
    def __init__(self) -> None:
        self.active_user = None
        execute_db()
        
    ############################################    
    # LOGIN SECTION - RESIGNATION - REGISTRATION - EXPLESION
    ############################################  
    
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
                user = status.get(status.username == self.active_user.username)
                
                while True:
                    active_user_password = input(f'Hi {user.first_name} {user.last_name}, please enter your password:\n')
                    
                    if active_user_password == user.password:
                        print('Congrats! You are now logged in.')
                        self.logged(status)
                        self.banner()
                        break
                    
                    else:
                        
                        print('Incorrect password, Try again!\n')
                        
            else:
                
                print("Username Doesn't exist in our database, Try again\n")
                print("--------------------------------------------------")
        
                
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
       
       
    def exitting(self):
        
        print('Bye!')
        print("--------------------------------------------------")
        print("--------------------------------------------------")
        # exit()  
         
    ############################################    
    # REGISTRATION - TERMINATION - RESIGNATION
    ############################################  
    
    def register_recruiter(self):
        
        # while True:
            
        User_username = input("Enter the person's User name:\n")
        
        while True:
            
            super_admin = input("Is the registeree a Super Admin or just a Recruiter? Y/N\n")
            
            if super_admin == 'Y':
                
                a_admin = True
                break
            
            elif super_admin == 'N':
                
                a_admin = False
                break
            
            else:
                
                print('Invalid answer, Try again!\n')
                
        if not Recruiters.select().where(Recruiters.username == User_username).exists():
            
            Recruiters.create(
                username = User_username,
                password = input("Enter the person's desired password: \n"),
                first_name = User_username.title(),
                last_name = input("Enter the person's last name: \n"),
                is_superadmin = a_admin,
                is_logged = False )
            print("--------------------------------------------------")
            print('Successfully registered the Recruiter\n')
            # self.banner()
            # break
        
        else:
            
            print('this username is exist. pleas enter an other one.')
           
                
    def fire_recruiter(self):
        
        self.view_recruiters()
        print("--------------------------------------------------")
        number = int(input('Select the number of the Recruiter you want to terminate.\n'))
        terminate = Recruiters.get(Recruiters.id == number)
        
        if terminate.is_superadmin == True:
            
            print('You cant terminate a Super admin!\n')
            
        else:
            
            terminate.delete_instance()
            print("--------------------------------------------------")
            print(f"Recruiter number {number} has been terminated.\n")
     
    def register_employee(self):
        
        career_path = input("Enter the potential employee's profession:\n")           
        spots_left = Careers.get(Careers.career == career_path)
        
        if spots_left.available_spots != 0:
            
            print('Luckily there are available spots!')
            spots_left.available_spots -= 1
            spots_left.save()
            username = input("Enter the person's username:\n")
            
            if not Employees.select().where(Employees.username == username).exists():
                
                Employees.create(
                    username = username,
                    password = input("Enter the person's desired password: \n"),
                    first_name = username.title(),
                    last_name = input("Enter the person's last name: \n"),
                    profession = career_path,
                    experience = int(input('How many years of experience?\n')),
                    is_logged = False
                    )
                print("--------------------------------------------------")
                print('Successfully registered the Recruiter\n')
                # self.banner()
                # break
            
            else:
                
                print('this username is exist. pleas enter an other one.')
        else:
            print('Sorry, No available spots!\n')
    
    def fire_employee(self):
        is_empty = (Employees.select().count() == 0)
        if is_empty:
            print('There are no employees to terminate!\n')
        
        
                    
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
      
    ############################################    
    # VIEWING
    ############################################         
          
    def view_profile(self):
        
        if isinstance(self.active_user, Recruiters):
            
            stats = Recruiters.get(Recruiters.username == self.active_user.username)
            print("--------------------------------------------------")
            print('Here is your personal profile!\n')
            print('Username:', stats.username)
            print('First name:', stats.first_name)
            print('Last name:', stats.last_name)
            print('Password:', stats.password)
            print('Superadmin:', stats.is_superadmin)
            print("--------------------------------------------------")
            
        elif isinstance(self.active_user, Employees):
            
            stats = Employees.get(Employees.username == self.active_user.username)
            print("--------------------------------------------------")
            print('Here is your personal profile!\n')
            print('Username:', stats.username)
            print('First name:', stats.first_name)
            print('Last name:', stats.last_name)
            print('Password:', stats.password)
            print('Profession:', stats.profession)
            print('Experience:', stats.experience)
            print("--------------------------------------------------")
              
                        
    def view_recruiters(self):
        
        for i in Recruiters.select():
            
            print("--------------------------------------------------")
            recruiter = [f'{i.id}',
                f'Username: {i.username}',
                f'First name: {i.first_name}',
                f'Last name: {i.last_name}',
                f'Super admin: {i.is_superadmin}',
                f'Login status: {i.is_logged}']
            print('\n'.join(recruiter))
    
    
    def view_careers(self):
        
        for i in Careers.select():
            
            print("--------------------------------------------------")
            careers = [f'{i.id}',
                f'career: {i.career}',
                f'Salary per month: {i.salary_per_month}',
                f'Available spots: {i.available_spots}',
                f'Experience required: {i.experience_required}']
            print('\n'.join(careers))
    
    def view_employees(self):
        
        is_empty = (Employees.select().count() == 0)
        
        if is_empty:
            
            print('There are no employees to terminate!\n')
            
        else:
            
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
                
    ############################################    
    # BANNER
    ############################################          
    
    
    def banner(self):
        
        print("--------------------------------------------------")
        
        if isinstance(self.active_user, Employees):
            
            employee_banner = [
                '-=-=-=-=-=-=-=-=-=-=-=-=-',
                f'Welcome to mission control, {self.active_user.first_name}!',
                '',
                '1. View Personal Profile',
                '2. View Employees list',
                '3. View your salary',
                '4. Resign from the work',
                '5. Log out',
                '6. Exit',
                '-=-=-=-=-=-=-=-=-=-=-=-=-']  
            

            while True:
                
                print('\n'.join(employee_banner))
                inp = input('Navigate by entering the respective value:\n')
                
                if inp == '1':
                    self.view_profile()
                    
                elif inp == '2':
                    self.view_employees()
                    
                elif inp == '3':
                    print("--------------------------------------------------")
                    career = Careers.get(Careers.career == self.active_user.profession)
                    print(f"Your current salary is: {career.salary_per_month}")
                    
                elif inp == '4':
                    self.resignation(Employees)
                    
                elif inp == '5':
                    self.logged_out(Employees)
                    app.login()
                    return
                
                elif inp == '6':
                    self.exitting()


        elif isinstance(self.active_user, Recruiters) and self.active_user.is_superadmin == False:
            
            recruiter_banner = [
                '-=-=-=-=-=-=-=-=-=-=-=-=-',
                f'Welcome to mission control, {self.active_user.first_name}!',
                '',
                '1. View Personal Profile',
                '2. View Employees list',
                '3. View Recruiters list',
                '4. Register an Employee',
                '5. Terminate an Employee',
                '6. Resign from the work',
                '7. Log out',
                '8. Exit',
                '-=-=-=-=-=-=-=-=-=-=-=-=-']          
            
            while True:
                
                print('\n'.join(recruiter_banner))
                inp = input('Navigate by entering the respective value:\n')
                if inp == '1':
                    self.view_profile()
                    
                elif inp == '2':
                    self.view_employees()
                    
                elif inp == '3':
                    self.view_recruiters()
                    
                elif inp == '4':
                    self.register_employee()
                    
                elif inp == '5':
                    self.fire_employee()
                    
                elif inp == '6':
                    self.resignation(Recruiters)
                    
                elif inp == '7':
                    self.logged_out(Recruiters)
                    app.login()
                    return
                
                elif inp == '8':
                    self.exitting()
                    
                    
        elif isinstance(self.active_user, Recruiters) and self.active_user.is_superadmin == True:
            
            superadmin_banner = [
                '-=-=-=-=-=-=-=-=-=-=-=-=-',
                f'Welcome to mission control, {self.active_user.first_name}!',
                '',
                '1. View Personal Profile',
                '2. View Employees list',
                '3. View Careers list',
                '4. View Recruiters list',
                '5. Register an Employee',
                '6. Register a  Recruiter',
                '7. Terminate an Employee',
                '8. Terminate a  Recruiter',
                '9. View Monthly Cash out',
                '10. Log out',
                '11. Exit',
                '-=-=-=-=-=-=-=-=-=-=-=-=-']  
            
            while True:
                
                print('\n'.join(superadmin_banner))
                inp = input('Navigate by entering the respective value:\n')
                
                if inp == '1':
                    self.view_profile()
                    
                elif inp == '2':
                    self.view_employees()
   
                elif inp == '3':
                    self.view_careers()
                    
                elif inp == '4':
                    self.view_recruiters()
                    
                elif inp == '5':
                    self.register_employee()
                    
                elif inp == '6':
                    self.register_recruiter()
                    
                elif inp == '7':
                    self.fire_employee()
                    
                elif inp == '8':
                    self.fire_recruiter()

                elif inp == '9':
                    self.cashout()
                    
                elif inp == '10':
                    self.logged_out(Recruiters)
                    app.login()
                    return
                   
                elif inp == '11':
                    self.exitting()
                
                      
app = init_workplace()
app.login()