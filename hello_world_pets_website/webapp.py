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

@webapp.route('/customers.html', methods=['GET', 'POST'])
def customers():
    db_connection = connect_to_database()
    
    # Query vet options to populate pet form drop-down menu
    query = 'SELECT vet_id, first_name, last_name, specialty FROM vets'
    vets_result = execute_query(db_connection, query)
    
    
    if request.method == 'POST':
        # They submitted a form
        if request.form['action'] == 'addCustomer':
            # They want to insert a new Customer record into the database
            
            # Get customer data from form fields
            customer_data = {
                    "First Name": request.form.get('first-name'),
                    "Last Name": request.form.get('last-name'),
                    "Email": request.form.get('email-address'),
                    "Phone Number": request.form.get('phone-number'),
                    "Street Address": request.form.get('street-address'),
                    "City": request.form.get('city'),
                    "State": request.form.get('state'),
                    "Zip Code": request.form.get('zip')
                    }

            # Check for any empty fields (all required in this form)
            missing_fields = []
            for field in customer_data.keys():
                if customer_data[field] == "":
                    missing_fields.append(field)

            if len(missing_fields) > 0:
                feedback = f"Correct missing information: {missing_fields}"
                return render_template('customers.html', customer_reg_result=feedback, vet_options=vets_result)

            # If no fields missing, do the insert
            query = 'INSERT INTO customers (first_name, last_name, email, phone, address, city, state, zip_code) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
            data = (customer_data["First Name"],
                    customer_data["Last Name"],
                    customer_data["Email"],
                    customer_data["Phone Number"],
                    customer_data["Street Address"], 
                    customer_data["City"], 
                    customer_data["State"],
                    customer_data["Zip Code"])
            
            try:
                result = execute_query(db_connection, query, data)
                if result:
                    feedback = f"Added Customer {customer_data['First Name']} {customer_data['Last Name']}"
                else:
                    feedback = "Add Customer Failed."
            except:
                feedback = "Add Customer Failed."
           
            # Render page with query execution feeback
            return render_template('customers.html', customer_reg_result=feedback, vet_options=vets_result)

        elif request.form['action'] == 'addPet':
            # They want to add a new Pet to an existing Customer
            
            # Get pet data from form fields
            pet_data = {
                    "Customer ID": request.form.get('customer-id'),
                    "Pet Name": request.form.get('pet-name'),
                    "Pet Species": request.form.get('pet-species'),
                    "Pet Breed": request.form.get('pet-breed'),
                    "Pet Age": request.form.get('pet-age'),
                    "Pet Gender": request.form.get('pet-gender'),
                    "Veterinarian Choice": request.form.get('vet'),
                    }

            # Check for any empty fields (all required in this form)
            missing_fields = []
            for field in pet_data.keys():
                if pet_data[field] == "":
                    missing_fields.append(field)

            if len(missing_fields) > 0:
                feedback = f"Correct missing information: {missing_fields}"
                return render_template('customers.html', pet_reg_result=feedback, vet_options=vets_result)

            # If no fields missing, do the insert
            query = 'INSERT INTO pets (pet_name, species, breed, age, gender, vet_id, customer_id) VALUES (%s,%s,%s,%s,%s,%s,%s)'
            data = (pet_data["Pet Name"],
                    pet_data["Pet Species"],
                    pet_data["Pet Breed"],
                    pet_data["Pet Age"],
                    pet_data["Pet Gender"], 
                    pet_data["Veterinarian Choice"], 
                    pet_data["Customer ID"])
            
            try:
                result = execute_query(db_connection, query, data)
                if result:
                    feedback = f"Added Pet {pet_data['Pet Name']}"
                else:
                    feedback = "Add Pet Failed."
            except:
                feedback = "Add Pet Failed."
           
            # Render page with query execution feeback
            return render_template('customers.html', pet_reg_result=feedback, vet_options=vets_result)
    
    # Just render the base webpage
    return render_template('customers.html', vet_options=vets_result)

@webapp.route('/pets.html', methods=['GET', 'POST'])
def pets():
    db_connection = connect_to_database()
   
    if request.method == 'POST':
        # They submitted the form
        if request.form['searchPets'] == 'customerName':
            customerName = request.form['petSearchText'].split()
            
            # One name provided - could be first or last
            if len(customerName) == 1:
                name = customerName[0]
                query = "SELECT * FROM pets where customer_id = (SELECT customer_id FROM customers WHERE first_name = '" + name + "' OR last_name = '" + name + "')"
            
            # Two names provided - first and last
            elif len(customerName) == 2:
                first = customerName[0]
                last = customerName[1]
                query = "SELECT * FROM pets where customer_id = (SELECT customer_id FROM customers WHERE first_name = '" + first + "' AND last_name = '" + last + "')"

            # Execute the query
            result = execute_query(db_connection, query).fetchall()

        elif request.form['searchPets'] == 'petName':
            petName = request.form['petSearchText']
            query = "SELECT * FROM pets where pet_name = '" + petName + "'"
            result = execute_query(db_connection, query).fetchall()

        elif request.form['searchPets'] == 'petType':
            petType = request.form['petSearchText']
            query = "SELECT * FROM pets WHERE species = '" + petType + "' OR breed = '" + petType + "'"
            result = execute_query(db_connection, query).fetchall()

        return render_template('pets.html', rows=result)
    else:
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

def refresh_admin(feedback=None):
    db_connection = connect_to_database()
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
    if feedback:
        return render_template('admin.html', rows=customer_result, pets=pet_result, classes = classes_result, enroll=enroll_result, vet=vet_result, feedback=feedback)
    return render_template('admin.html', rows=customer_result, pets=pet_result, classes = classes_result, enroll=enroll_result, vet=vet_result)


@webapp.route('/admin.html', methods=['GET', 'POST'])
def admin():
    # If the user is simply going to the admin page, display all info in all tables
    if request.method == 'GET':
        return refresh_admin()

    # If users are inserting new information into the tables on the admin page
    if request.method == 'POST':
        
        # Set up feedback
        feedback = {"Customers": "",
                    "Pets": "",
                    "Classes": "",
                    "Enrollments": "",
                    "Vets": ""}

        db_connection = connect_to_database()
        
        # If they submitted to update a customer
        if request.form.get('customer-update'):
            return str(request.form.get('customer-update'))            

        # If they submitted to delete a customer
        elif request.form.get('customer-delete'):
            customer_id = request.form.get('customer-delete')
            query = "DELETE FROM customers WHERE customer_id = '" + customer_id + "'"
            execute_query(db_connection, query)
            return refresh_admin()
    
        # If they submitted to update a pet
        elif request.form.get('pet-update'):
            return str(request.form.get('pet-update'))            

        # If they submitted to delete a pet
        elif request.form.get('pet-delete'):
            pet_id = request.form.get('pet-delete')
            query = "DELETE FROM pets WHERE pet_id = '" + pet_id + "'"
            execute_query(db_connection, query)
            return refresh_admin()


        # If they submitted to add a new customer
        elif request.form.get('customer-insert'):
            # Get customer data from form fields
            customer_data = {
                    "First Name": request.form.get('customer_first_name'),
                    "Last Name": request.form.get('customer_last_name'),
                    "Email": request.form.get('customer_email'),
                    "Phone Number": request.form.get('customer_phone'),
                    "Street Address": request.form.get('customer_address'),
                    "City": request.form.get('customer_city'),
                    "State": request.form.get('customer_state'),
                    "Zip Code": request.form.get('customer_zip')
                    }

            # Check for any empty fields (all required in this form)
            missing_fields = []
            for field in customer_data.keys():
                if customer_data[field] == "":
                    missing_fields.append(field)

            if len(missing_fields) > 0:
                feedback["Customers"] = f"Correct missing information: {missing_fields}"

            # If no fields missing, do the insert
            else:
                query = 'INSERT INTO customers (first_name, last_name, email, phone, address, city, state, zip_code) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
                data = (customer_data["First Name"],
                        customer_data["Last Name"],
                        customer_data["Email"],
                        customer_data["Phone Number"],
                        customer_data["Street Address"], 
                        customer_data["City"], 
                        customer_data["State"],
                        customer_data["Zip Code"])
                
                try:
                    result = execute_query(db_connection, query, data)
                    if result:
                        feedback["Customers"] = f"Added Customer {customer_data['First Name']} {customer_data['Last Name']}"
                    else:
                        feedback["Customers"] = "Add Customer Failed."
                except:
                    feedback["Customers"] = "Add Customer Failed."
                
            return refresh_admin(feedback)
        
        # If they submitted a new pet
        elif request.form.get('pet-insert'):
            
            # Get pet data from form fields
            pet_data = {
                    "Pet Name": request.form.get('pet_name'),
                    "Species": request.form.get('pet_species'),
                    "Breed": request.form.get('pet_breed'),
                    "Age": request.form.get('pet_age'),
                    "Gender": request.form.get('pet_gender'),
                    "Vet ID": request.form.get('vet_id'),
                    "Customer ID": request.form.get('customer_id')
                    }

            # Check for any empty fields (all required in this form)
            missing_fields = [] 
            for field in pet_data.keys():
                if pet_data[field] == "":
                    missing_fields.append(field)

            if len(missing_fields) > 0:
                feedback["Pets"] = f"Correct missing information: {missing_fields}"

            # If no fields missing, do the insert
            else:
                query = 'INSERT INTO pets (pet_name, species, breed, age, gender, vet_id, customer_id) VALUES (%s,%s,%s,%s,%s,%s,%s)'
                data = (pet_data["Pet Name"],
                        pet_data["Species"],
                        pet_data["Breed"],
                        pet_data["Age"],
                        pet_data["Gender"], 
                        pet_data["Vet ID"], 
                        pet_data["Customer ID"])
                
                try:
                    result = execute_query(db_connection, query, data)
                    if result:
                        feedback["Pets"] = f"Added Pet {pet_data['Pet Name']}"
                    else:
                        feedback["Pets"] = "Add Pet Failed."
                except:
                    feedback["Pets"] = "Add Pet Failed."
           
            return refresh_admin(feedback)


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
