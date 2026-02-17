#neccesary imports for the flask server, password generation, finding file paths, database management and random number generation
from flask import request, redirect
from flask import Flask
import re 
from werkzeug.security import generate_password_hash, check_password_hash 
import sqlite3 
import os 
import random 


app = Flask(__name__, static_folder="Resources") 
def check_login(name, password):
    try:
        FileDirectory = os.path.dirname(os.path.abspath(__file__)) #finds the file directory
        DatabasePath = os.path.join(FileDirectory, "Resources", "Database", "Inventory.db") #Understands the path to the database
        
        #SQL commands
        conn = sqlite3.connect(DatabasePath) #connects to the database file based on directory
        cursor = conn.cursor() #creates a cursor object to execute SQL commands
        cursor.execute("SELECT Password FROM Accounts WHERE Username = ?",(name,)) #sql command to select password where username matches input

        #translates the hashed password and checks it against the input password
        for (stored_hash,) in cursor:
            if check_password_hash(stored_hash, password):
                conn.close()
                return True

        conn.close()
        return False
    except:
        return False

#function to create a new account in the database
def create_account(name, password):
    hashed_password = generate_password_hash(password) #hashes the password

    FileDirectorR = os.path.dirname(os.path.abspath(__file__)) #connects to the database file based on directory
    DatabasePath = os.path.join(FileDirectorR, "Resources", "Database", "Inventory.db") #creates a cursor object to execute SQL commands

    conn = sqlite3.connect(DatabasePath) #connects to the database file based on directory
    conn.execute('CREATE TABLE IF NOT EXISTS Accounts (ProductID INTEGER PRIMARY KEY AUTOINCREMENT, UserName Text NOT NULL, Password Text NOT NULL)') #creates the Accounts table if it doesn't exist
    conn.execute('INSERT INTO Accounts (UserName, Password) VALUES (?, ?)', (name, hashed_password)) #inserts the new account into the Accounts table
    conn.commit() 
    conn.close() 


#function to verify password strength using regex
def verify_password(password):
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{6,20}$' #rensures the password has a lowercase, uppercase, number, special character and is 6-20 characters long
    return re.match(pattern, password) #returns true if the password matches



@app.route("/") #sets default route to login page
def index(): 
    return redirect("/Resources/HTML/LogInPage.html") #sends user to login page



@app.route("/login", methods=["POST"]) #login on flask end
def login(): #sub program for login
    name = request.form.get("name").strip() #recieves username from form and strips whitespace
    password = request.form.get("password") #recieves password from form
    if check_login(name, password): #
        return redirect(f"/Resources/HTML/MainPage.html?name={name}") #redirects user to the main page if login is successful
    else:
        return "<script>alert('Wrong username or password'); window.location.href='/';</script>" 



@app.route("/create", methods=["POST"]) #account creation on flask end
def create(): #sub program for account creation
    name = request.form.get("name").strip() #recieves username from form and strips whitespace
    password = request.form.get("password") #recieves password from form
    
    if verify_password(password):
        create_account(name, password)  
        return f"<script>alert('Account {name} created successfully!'); window.location.href='/';</script>"
    else:
        return "<script>alert('Password invalid. Must have uppercase, lowercase, number, special char, 6-20 chars.');</script>" 
    


@app.route("/pay", methods=["POST"]) #payment processing on flask end
def pay(): #sub program for payment processing

    card = request.form["card"] #recieves card number from form
    if len(card) != 16 or not card.isdigit(): #checks if card number is valid
        return "<script>alert('Invalid card number. Must be 16 digits.'); window.location.href='/Resources/HTML/BrowseStock.html';</script>" 
    
    else: #if card number is valid, check expiry date
        expiry = request.form["expiry"] #recieves expiry date from form
        if len(expiry) != 5 or not re.match(r'^\d{2}/\d{2}$', expiry):
            return "<script>alert('Invalid expiry date. Must be in MM/YY format.'); window.location.href='/Resources/HTML/BrowseStock.html';</script>" 
        
        else: #if expiry date is valid, check CVC
            cvc = request.form["cvc"] #recieves CVC from form
            if len(cvc) != 3 or not cvc.isdigit(): 
                return "<script>alert('Invalid CVC. Must be 3 digits.'); window.location.href='/Resources/HTML/BrowseStock.html';</script>" 
            else: #if all payment details are valid, process payment
                code = random.randint(1000000000, 9999999999)  #generates transaction code
                return f"<script>alert('Payment successful! Your transaction code is {code}, please pick up at your local branch.'); window.location.href='/Resources/HTML/MainPage.html';</script>" 


@app.route("/BookInstallation", methods=["POST"]) #installation booking on flask end
def BookInstallation(): 
    #gets all the data from the html file
    name = request.form.get("fullName")
    email = request.form.get("email")
    phone = request.form.get("phone")
    date = request.form.get("appointmentDate")
    time = request.form.get("appointmentTime")
    service_type = request.form.get("serviceType")

    #checks to make sure are all are not blank
    if not all([name, email, phone, date, time, service_type]):
        return "<script>alert('All fields are required.'); window.location.href='/Resources/HTML/ScheduleInstillations.html';</script>"

    FileDirectory = os.path.dirname(os.path.abspath(__file__)) #connects to the database file based on directory
    DatabasePath = os.path.join(FileDirectory, "Resources", "Database", "Inventory.db") #creates a cursor object to execute SQL commands

    #SQL operations similar to above (login and account creation)
    conn = sqlite3.connect(DatabasePath)
    cursor = conn.cursor()
    conn.execute('CREATE TABLE IF NOT EXISTS Installations (Name Text NOT NULL, Email Text NOT NULL, Phone Text NOT NULL, Date Text NOT NULL, Time Text NOT NULL, ServiceType Text NOT NULL)')
    cursor.execute('INSERT INTO Installations (Name, Email, Phone, Date, Time, ServiceType) VALUES (?, ?, ?, ?, ?, ?)', (name, email, phone, date, time, service_type))
    conn.commit()
    conn.close()

    return f"<script>alert('Installation booked successfully for {name}!'); window.location.href='/Resources/HTML/MainPage.html';</script>" 


@app.route("/BookAppointment", methods=["POST"]) #appointment booking on flask end
def BookAppointment(): 
    #gets all the data from the html file
    name = request.form.get("fullName")
    email = request.form.get("email")
    phone = request.form.get("phone")
    date = request.form.get("appointmentDate")
    time = request.form.get("appointmentTime")
    #checks to make sure are all are not blank
    if not all([name, email, phone, date, time]):
        return "<script>alert('All fields are required.'); window.location.href='/Resources/HTML/ScheduleApointments.html';</script>"

    FileDirectory = os.path.dirname(os.path.abspath(__file__)) #connects to the database file based on directory
    DatabasePath = os.path.join(FileDirectory, "Resources", "Database", "Inventory.db") #creates a cursor object to execute SQL commands

    #SQL operations similar to above (login and account creation)
    conn = sqlite3.connect(DatabasePath)
    cursor = conn.cursor()
    conn.execute('CREATE TABLE IF NOT EXISTS Appointments (Name Text NOT NULL, Email Text NOT NULL, Phone Text NOT NULL, Date Text NOT NULL, Time Text NOT NULL)')
    cursor.execute('INSERT INTO Appointments (Name, Email, Phone, Date, Time) VALUES (?, ?, ?, ?, ?)', (name, email, phone, date, time))
    conn.commit()
    conn.close()

    return f"<script>alert('Appointment booked successfully for {name}!'); window.location.href='/Resources/HTML/MainPage.html';</script>" 






if __name__ == "__main__": 
    app.run(debug=True) 