from flask import Flask, render_template
from flask import request, redirect
from db_connector.db_connector import connect_to_database, execute_query
#create the web application
webapp = Flask(__name__)

'''
#provide a route where requests on the web application can be addressed
@webapp.route('/index')
#provide a view (fancy name for a function) which responds to any requests on this route
def hello():
    return render_template(index.html)
'''
@webapp.route('/')
def index():
    return render_template('index.html')

@webapp.route('/index.html')
def home():
    return render_template('index.html')

@webapp.route('/customers.html')
def customers():
    return render_template('customers.html')

@webapp.route('/pets.html')
def pets():
    return render_template('pets.html')

@webapp.route('/classes.html', methods=['GET', 'POST'])
def classes():
    db_connection = connect_to_database()
    if request.method == 'POST':
        # They submitted the form
        if request.form['searchClasses'] == 'className':
            className = request.form['classSearchText']
            query = "SELECT * from classes where class_name = '" + className + "'"
            result = execute_query(db_connection, query).fetchall()
        elif request.form['searchClasses'] == 'day':
            day = request.form['classSearchText']
            query = "SELECT * from classes where class_day = '" + day + "'"
            result = execute_query(db_connection, query).fetchall()
        elif request.form['searchClasses'] == 'time':
            time = request.form['classSearchText']
            query = "SELECT * from vets class_time = '" + time + "'"
            result = execute_query(db_connection, query).fetchall()
        elif request.form['searchClasses'] == 'price':
            price = request.form['classSearchText']
            query = "SELECT * from classes where class_price = " + str(price)
            result = execute_query(db_connection, query).fetchall()
        return render_template('classes.html', rows=result)
    else:
        # They're just visiting the page for the first time
        return render_template('classes.html')

@webapp.route('/vets.html', methods=['GET','POST'])
def vets():
    db_connection = connect_to_database()
    if request.method == 'POST':
        # They submitted the form
        if request.form['vetSearchType'] == 'vetFirstName':
            firstName = request.form['vetSearchText']
            query = "SELECT * from vets where first_name = '" + firstName + "'"
            result = execute_query(db_connection, query).fetchall()
        elif request.form['vetSearchType'] == 'vetLastName':
            lastName = request.form['vetSearchText']
            query = "SELECT * from vets where last_name = '" + lastName + "'"
            result = execute_query(db_connection, query).fetchall()
        elif request.form['vetSearchType'] == 'vetSpecialty':
            specialty = request.form['vetSearchText']
            query = "SELECT * from vets where specialty = '" + specialty + "'"
            result = execute_query(db_connection, query).fetchall()
        elif request.form['vetSearchType'] == 'petName':
            petName = request.form['vetSearchText']
            query = "SELECT * from vets where vet_id = (SELECT vet_id from pets where pet_name = '" + petName + "')"
            result = execute_query(db_connection, query).fetchall()
        return render_template('vets.html', rows=result)
    else:
        # They're just visiting the page for the first time
        return render_template('vets.html')

@webapp.route('/admin.html', methods=['GET', 'POST'])
def admin():
    db_connection = connect_to_database()
    
    # If the user is simply going to the admin page, display all info in all tables
    if request.method == 'GET':
        # Display customer table
        customer_query = 'SELECT * from customers'
        customer_result = execute_query(db_connection, customer_query).fetchall()
    
        # Display pets table
        pet_query = 'SELECT * from pets'
        pet_result = execute_query(db_connection, pet_query).fetchall()

        # Display classes table
        classes_query = 'SELECT * from classes'
        classes_result = execute_query(db_connection, classes_query).fetchall()
    
        # display enrollments table
        enroll_query = 'SELECT * from enrollments'
        enroll_result = execute_query(db_connection, enroll_query).fetchall()
    
        # Display vets table
        vet_query = 'SELECT * from vets'
        vet_result = execute_query(db_connection, vet_query).fetchall()
    
        # Return info from all tables
        return render_template('admin.html', rows=customer_result, pets=pet_result, classes = classes_result, enroll=enroll_result, vet=vet_result)

    # If users are inserting new information into the tables on the admin page
    if request.method == 'POST':
        # If they submitted a form to add a new customer
        if request.form['addCustomer']:
            customerFirstName = request.form.get('customerFirstName')
            customerLastName = request.form.get('customerLastName')
            customerEmail = request.form.get('customerEmail')
            customerPhone = request.form.get('customerPhone')
            customerAddress = request.form.get('customerAddress')
            customerCity = request.form.get('customerCity')
            customerState = request.form.get('customerState')
            customerZip = request.form.get('customerZip')
            query = 'INSERT INTO customers (first_name, last_name, email, phone, address, city, state, zip_code) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
            data = (customerFirstName, customerLastName, customerEmail, customerPhone, customerAddress, customerCity, customerState, customerZip)
            execute_query(db_connection, query, data)
            customer_updated_table = 'SELECT * FROM customers'
            customer_table = execute_query(db_connection, customer_updated_table).fetchall()
            return render_template('admin.html', customers=customer_table)



# Testing DB connection
@webapp.route('/db-test')
def test_database_connection():
    print("Executing a sample query on the database using the credentials from db_credentials.py")
    db_connection = connect_to_database()
    query = "SELECT * from customers;"
    result = execute_query(db_connection, query)
    return render_template('db_test.html', rows=result)

'''
@webapp.route('/browse_bsg_people')
#the name of this function is just a cosmetic thing
def browse_people():
    print("Fetching and rendering people web page")
    db_connection = connect_to_database()
    query = "SELECT fname, lname, homeworld, age, id from bsg_people;"
    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('people_browse.html', rows=result)

@webapp.route('/add_new_people', methods=['POST','GET'])
def add_new_people():
    db_connection = connect_to_database()
    if request.method == 'GET':
        query = 'SELECT id, name from bsg_planets'
        result = execute_query(db_connection, query).fetchall()
        print(result)

        return render_template('people_add_new.html', planets = result)
    elif request.method == 'POST':
        print("Add new people!")
        fname = request.form['fname']
        lname = request.form['lname']
        age = request.form['age']
        homeworld = request.form['homeworld']

        query = 'INSERT INTO bsg_people (fname, lname, age, homeworld) VALUES (%s,%s,%s,%s)'
        data = (fname, lname, age, homeworld)
        execute_query(db_connection, query, data)
        return ('Person added!')

@webapp.route('/')
def index():
    return "<p>Are you looking for /db_test or /hello or <a href='/browse_bsg_people'>/browse_bsg_people</a> or /add_new_people or /update_people/id or /delete_people/id </p>"

@webapp.route('/home')
def home():
    db_connection = connect_to_database()
    query = "DROP TABLE IF EXISTS diagnostic;"
    execute_query(db_connection, query)
    query = "CREATE TABLE diagnostic(id INT PRIMARY KEY, text VARCHAR(255) NOT NULL);"
    execute_query(db_connection, query)
    query = "INSERT INTO diagnostic (text) VALUES ('MySQL is working');"
    execute_query(db_connection, query)
    query = "SELECT * from diagnostic;"
    result = execute_query(db_connection, query)
    for r in result:
        print(f"{r[0]}, {r[1]}")
    return render_template('home.html', result = result)

@webapp.route('/db_test')
def test_database_connection():
    print("Executing a sample query on the database using the credentials from db_credentials.py")
    db_connection = connect_to_database()
    query = "SELECT * from bsg_people;"
    result = execute_query(db_connection, query)
    return render_template('db_test.html', rows=result)

#display update form and process any updates, using the same function
@webapp.route('/update_people/<int:id>', methods=['POST','GET'])
def update_people(id):
    print('In the function')
    db_connection = connect_to_database()
    #display existing data
    if request.method == 'GET':
        print('The GET request')
        people_query = 'SELECT id, fname, lname, homeworld, age from bsg_people WHERE id = %s'  % (id)
        people_result = execute_query(db_connection, people_query).fetchone()

        if people_result == None:
            return "No such person found!"

        planets_query = 'SELECT id, name from bsg_planets'
        planets_results = execute_query(db_connection, planets_query).fetchall()

        print('Returning')
        return render_template('people_update.html', planets = planets_results, person = people_result)
    elif request.method == 'POST':
        print('The POST request')
        character_id = request.form['character_id']
        fname = request.form['fname']
        lname = request.form['lname']
        age = request.form['age']
        homeworld = request.form['homeworld']

        query = "UPDATE bsg_people SET fname = %s, lname = %s, age = %s, homeworld = %s WHERE id = %s"
        data = (fname, lname, age, homeworld, character_id)
        result = execute_query(db_connection, query, data)
        print(str(result.rowcount) + " row(s) updated")

        return redirect('/browse_bsg_people')

@webapp.route('/delete_people/<int:id>')
def delete_people(id):
    # deletes a person with the given id
    db_connection = connect_to_database()
    query = "DELETE FROM bsg_people WHERE id = %s"
    data = (id,)

    result = execute_query(db_connection, query, data)
    return (str(result.rowcount) + "row deleted")
'''
