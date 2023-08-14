from flask import Flask, request, session, redirect, url_for, render_template, flash
import psycopg2 #pip install psycopg2 
import psycopg2.extras
import re 
from werkzeug.security import generate_password_hash, check_password_hash

class CustomersHandler:
    """This class handles all database interactions related to the customers."""

    TABLE_NAME: str = "Customers"
    COLUMN_NAME: str = "name_surname"
    COLUMN_COMP: str = "company"
    COLUMN_EMAIL: str = "email"
    COLUMN_PASW: str = "password"


    def __init__(self) -> None:
        # Holds the database handler.
        self.db_handler = create_database_handler()

@app.route('/login/', methods=['GET', 'POST'])
def login():
    register_cursor=db_conn.acquire_cursor()
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email=request.form['email']
        password=request.form['password']
        print(password)
        #check if account exist
        register_cursor.execute('SELECT * FROM customers WHERE email=%s',(email,))
        account=register_cursor.fetchone()
        if account:
            password_rs = account['password']
            print(password_rs)
            # If account exists in users table in out database
            if check_password_hash(password_rs, password):
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account['id']
                session['email'] = account['email']
                # Redirect to home page
                return redirect(url_for('home'))
            else:
                # Account doesnt exist or username/password incorrect
                flash('Incorrect email/password')
        else:
            # Account doesnt exist or username/password incorrect
            flash('Incorrect email/password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    register_cursor=db_conn.acquire_cursor()

    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'name_surname' in request.form and 'company' in request.form and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        fullname = request.form['name_surname']
        username = request.form['company']
        password = request.form['email']
        email = request.form['password']
        _hashed_password = generate_password_hash(password)

        #Check if account exists using MySQL
        register_cursor.execute('SELECT * FROM customers WHERE email = %s', (email,))
        account = register_cursor.fetchone()
        print(account)
        # If account exists show error and validation checks
        if account:
            flash('Account already exists!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!')
        elif not username or not password or not email:
            flash('Please fill out the form!')
        else:
            # Account doesnt exists and the form data is valid, now insert new account into users table
            register_cursor.execute("INSERT INTO customers (name_surname, company, email, password) VALUES (%s,%s,%s,%s)", (name_surname, company, email, _hashed_password))
            db_conn.commit()
            flash('You have successfully registered!')
            
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('Please fill out the form!')
    # Show registration form with message (if any)
    return render_template('register.html')   

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('email', None)
   # Redirect to login page
   return redirect(url_for('login'))
   
@app.route('/profile')
def profile(): 
    register_cursor = db_conn.acquire_cursor()

    # Check if user is loggedin
    if 'loggedin' in session:
        register_cursor.execute('SELECT * FROM customers WHERE id = %s', [session['id']])
        account = register_cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login')) 