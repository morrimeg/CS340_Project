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
    
    # Query customer options to populate pet form drop-down menu
    query = 'SELECT customer_id, first_name, last_name FROM customers'
    customers_result = execute_query(db_connection, query)
    
    
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
                return render_template('customers.html', customer_reg_result=feedback, vet_options=vets_result, customer_options=customers_result)

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
            return render_template('customers.html', customer_reg_result=feedback, vet_options=vets_result, customer_options=customers_result)

        elif request.form['action'] == 'addPet':
            # They want to add a new Pet to an existing Customer
            
            # Get pet data from form fields
            pet_data = {
                    "Customer ID": request.form.get('customer-select'),
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
                return render_template('customers.html', customer_reg_result=feedback, vet_options=vets_result, customer_options=customers_result)

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
            return render_template('customers.html', customer_reg_result=feedback, vet_options=vets_result, customer_options=customers_result)
    
    # Just render the base webpage
    return render_template('customers.html', vet_options=vets_result, customer_options=customers_result)

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

    # Get all existing data from Classes table for dropdowns
    # get data for selecting by class name
    class_name_query = "SELECT class_name FROM classes"
    class_tuple = execute_query(db_connection, class_name_query).fetchall()
    # turn class_day_list into a list instead of a tuple
    # https://www.geeksforgeeks.org/python-convert-list-of-tuples-into-list/
    class_list = [item for x in class_tuple for item in x]

    class_day_query = "SELECT DISTINCT DAYNAME(class_day) FROM classes"
    class_day_tuple = execute_query(db_connection, class_day_query).fetchall()
    # turn class_day_list into a list instead of a tuple
    # https://www.geeksforgeeks.org/python-convert-list-of-tuples-into-list/
    class_day_list = [item for t in class_day_tuple for item in t] 

    class_time_query = "SELECT DISTINCT HOUR(class_time) as time FROM classes ORDER BY time ASC"
    class_time_tuple = execute_query(db_connection, class_time_query).fetchall()
    class_time_list = [item for t in class_time_tuple for item in t]

    # If the user does a search on the classes table...
    if request.method == 'POST':

        # They submitted the form
        if request.form['searchClasses'] == 'className':
            className = request.form.get('select-class-name')
            query = "SELECT * FROM classes WHERE class_name = '" + className + "'"
            result = execute_query(db_connection, query).fetchall()
        
        elif request.form['searchClasses'] == 'day':
            day = request.form.get('select-class-day')
            query = "SELECT * FROM classes WHERE DAYNAME(class_day) = '" + day + "'"
            result = execute_query(db_connection, query).fetchall()
        
        elif request.form['searchClasses'] == 'time':
            time = request.form.get('select-class-time')
            query = "SELECT * FROM classes WHERE HOUR(class_time) = '" + time + "'"
            result = execute_query(db_connection, query).fetchall()
        
        elif request.form['searchClasses'] == 'price':
            price = request.form.get('price-range') #['classSearchText']
            query = "SELECT * FROM classes WHERE class_price <= " + str(price)
            result = execute_query(db_connection, query).fetchall()

            if result is None:
                result = "No prices at or bwlow" + str(price)
            
        return render_template('classes.html', rows=result, class_list=class_list, class_day=class_day_list, class_time=class_time_list)
    
    else:
        # They're just visiting the page for the first time
        #return render_template('classes.html')
        return render_template("classes.html", class_list=class_list, class_day=class_day_list, class_time=class_time_list)


    

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
            query = "SELECT * FROM vets WHERE specialty LIKE '%%" + specialty + "%%'"
            print("query", query)
            result = execute_query(db_connection, query).fetchall()
        elif request.form['vetSearchType'] == 'petName':
            petName = request.form['vetSearchText']
            query = "SELECT * FROM vets WHERE vet_id = (SELECT vet_id FROM pets WHERE pet_name = '" + petName + "')"
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
    
    # Display teachers table
    teacher_query = 'SELECT * from teachers'
    teacher_result = execute_query(db_connection, teacher_query).fetchall()

    # Display vets table
    vet_query = 'SELECT * from vets'
    vet_result = execute_query(db_connection, vet_query).fetchall()

    # Return info from all tables
    if feedback:
        return render_template('admin.html', rows=customer_result, pets=pet_result, classes = classes_result, enroll=enroll_result, vet=vet_result, teacher=teacher_result, feedback=feedback)
    return render_template('admin.html', rows=customer_result, pets=pet_result, classes = classes_result, enroll=enroll_result, vet=vet_result, teacher=teacher_result)


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
                    "Teachers": "",
                    "Vets": ""}

        db_connection = connect_to_database()

        # They submitted a form to update a customer
        if request.form.get('customer-update'): # == 'updateCustomer':
            
            # Get customer data from form fields
            customer_data = {
                    "First Name": request.form.get('customer-first-name'),
                    "Last Name": request.form.get('customer-last-name'),
                    "Email": request.form.get('customer-email'),
                    "Phone Number": request.form.get('customer-phone'),
                    "Street Address": request.form.get('customer-address'),
                    "City": request.form.get('customer-city'),
                    "State": request.form.get('customer-state'),
                    "Zip Code": request.form.get('customer-zip-code'),
                    "Customer ID": request.form.get('customer-id')
                    }
            print(request.form.get('customer-update'))
            print()
            print(customer_data) #TAKE OUT
            
            # If no fields missing, do the insert
            query = 'UPDATE customers SET first_name = %s, last_name = %s, email = %s, phone = %s, address = %s, city = %s, state = %s, zip_code = %s WHERE customer_id = %s'
            data = (customer_data["First Name"],
                    customer_data["Last Name"],
                    customer_data["Email"],
                    customer_data["Phone Number"],
                    customer_data["Street Address"], 
                    customer_data["City"], 
                    customer_data["State"],
                    customer_data["Zip Code"],
                    customer_data["Customer ID"])
            
            try:
                result = execute_query(db_connection, query, data)
                
                if result:
                    feedback = f"Updated Customer {customer_data['First Name']} {customer_data['Last Name']}"
                else:
                    feedback = "Update Customer Failed."
            except:
                feedback = "Update Customer Failed."
            
            return refresh_admin(feedback)

        # If they request to update a Pet
        elif request.form.get('pet-update'):
            
            # Get pet data from form fields
            pet_data = {
                    "Pet Name": request.form.get('pet-name'),
                    "Pet Species": request.form.get('pet-species'),
                    "Pet Breed": request.form.get('pet-breed'),
                    "Pet Age": request.form.get('pet-age'),
                    "Pet Gender": request.form.get('pet-gender'),
                    "Vet First Name": request.form.get('vet-first-name'),
                    "Vet Last Name": request.form.get('vet-last-name'),
                    "Customer First Name": request.form.get('customer-first-name'),
                    "Customer Last Name": request.form.get('customer-last-name'),
                    "Pet ID": request.form.get('pet-id')
                    }
            

            # Do the update
            query = 'UPDATE pets SET pet_name = %s, species = %s, breed = %s, age = %s, gender = %s, vet_id = (SELECT vet_id from vets where first_name = %s and last_name = %s), customer_id = (SELECT customer_id from customers where first_name = %s and last_name = %s) WHERE pet_id = %s'
            data = (pet_data["Pet Name"],
                    pet_data["Pet Species"],
                    pet_data["Pet Breed"],
                    pet_data["Pet Age"],
                    pet_data["Pet Gender"],
                    pet_data["Vet First Name"],
                    pet_data["Vet Last Name"], 
                    pet_data["Customer First Name"], 
                    pet_data["Customer Last Name"],
                    pet_data["Pet ID"])
            
            try:
                result = execute_query(db_connection, query, data)
                
                if result:
                    feedback = f"Updated Pet {pet_data['Pet Name']}"
                else:
                    feedback = "Update Pets Failed."
            except:
                feedback = "Update Pets Failed."
            
            return refresh_admin(feedback)


        # If they submitted to update a Class
        elif request.form.get('class-update'):
            
            # Get class data from form fields
            class_data = {
                    "Class Name": request.form.get('class-name'),
                    "Class Description": request.form.get('class-description'),
                    "Class Day": request.form.get('class-day'),
                    "Class Time": request.form.get('class-time'),
                    "Class Price": request.form.get('class-price'),
                    "Class Seats": request.form.get('class-seats'),
                    "Teacher First Name": request.form.get('teacher-first-name'),
                    "Teacher Last Name": request.form.get('teacher-last-name'),
                    "Class ID": request.form.get('class-id')
                    }
            

            # Do the update
            query = 'UPDATE classes SET class_name = %s, class_description = %s, class_day = %s, class_time = %s, class_price = %s, class_seats = %s, teacher_id = (SELECT teacher_id from teachers where first_name = %s and last_name = %s) WHERE class_id = %s'
            data = (class_data["Class Name"],
                    class_data["Class Description"],
                    class_data["Class Day"],
                    class_data["Class Time"],
                    class_data["Class Price"],
                    class_data["Class Seats"],
                    class_data["Teacher First Name"], 
                    class_data["Teacher Last Name"],
                    class_data["Class ID"])
            
            try:
                result = execute_query(db_connection, query, data)
                
                if result:
                    feedback = f"Updated Class {class_data['Class Name']}"
                else:
                    feedback = "Update Class Failed."
            except:
                feedback = "Update Class Failed."
            
            return refresh_admin(feedback)

        # If they requested to upate an enrollment
        elif request.form.get('enrollment-update'):
            
            # Get enrollment data from form fields
            enrollment_data = {
                    "Pet Name": request.form.get('pet-name'),
                    "Class Name": request.form.get('class-name'),
                    "Enrollment ID": request.form.get('enroll-id')
                    }
            

            # Do the update
            query = 'UPDATE enrollments SET pet_id = (SELECT pet_id from pets where pet_name = %s), class_id = (SELECT class_id from classes where class_name = %s) WHERE enrollment_id = %s'
            data = (enrollment_data["Pet Name"],
                    enrollment_data["Class Name"],
                    enrollment_data["Enrollment ID"])
            
            try:
                result = execute_query(db_connection, query, data)
                
                if result:
                    feedback = f"Updated Enrollment {class_data['Enrollment Name']}"
                else:
                    feedback = "Update Enrollment Failed."
            except:
                feedback = "Update Enrollment Failed."
            
            return refresh_admin(feedback)


        # If they submitted to update a teacher
        elif request.form.get('teacher-update'):
            
            # Get teacher data from form fields
            teacher_data = {
                    "Teacher First Name": request.form.get('teacher-first-name'),
                    "Teacher Last Name": request.form.get('teacher-last-name'),
                    "Teacher Email": request.form.get('teacher-email'),
                    "Teacher Phone": request.form.get('teacher-phone'),
                    "Teacher ID": request.form.get('teacher-id')
                    }
            
            # Do the update
            query = 'UPDATE teachers SET first_name = %s, last_name = %s, email = %s, phone = %s WHERE teacher_id = %s'
            data = (teacher_data["Teacher First Name"],
                    teacher_data["Teacher Last Name"],
                    teacher_data["Teacher Email"],
                    teacher_data["Teacher Phone"],
                    teacher_data["Teacher ID"])
            
            try:
                result = execute_query(db_connection, query, data)
                
                if result:
                    feedback = f"Updated Teacher {teacher_data['Teacher First Name']} {teacher_data['Teacher Last Name']}"
                else:
                    feedback = "Update Teacher Failed."
            except:
                feedback = "Update Teacher Failed."
            
            return refresh_admin(feedback)

        # If they submitted to update a vet
        elif request.form.get('vet-update'):
            
            # Get vet data from form fields
            vet_data = {
                    "Vet First Name": request.form.get('vet-first-name'),
                    "Vet Last Name": request.form.get('vet-last-name'),
                    "Vet Email": request.form.get('vet-email'),
                    "Vet Phone": request.form.get('vet-phone'),
                    "Vet Specialty": request.form.get('vet-specialty'),
                    "Vet ID": request.form.get('vet-id')
                    }
            
            # Do the update
            query = 'UPDATE vets SET first_name = %s, last_name = %s, email = %s, phone = %s, specialty = %s WHERE vet_id = %s'
            data = (vet_data["Vet First Name"],
                    vet_data["Vet Last Name"],
                    vet_data["Vet Email"],
                    vet_data["Vet Phone"],
                    vet_data["Vet Specialty"],
                    vet_data["Vet ID"])
            
            try:
                result = execute_query(db_connection, query, data)
                
                if result:
                    feedback = f"Updated Vet {vet_data['Vet First Name']} {vet_data['Vet Last Name']}"
                else:
                    feedback = "Update Vet Failed."
            except:
                feedback = "Update Vet Failed."
            
            return refresh_admin(feedback)

        # If they submitted to delete a customer
        elif request.form.get('customer-delete'):
            customer_id = request.form.get('customer-delete')
            query = "DELETE FROM customers WHERE customer_id = '" + customer_id + "'"
            execute_query(db_connection, query)
            return refresh_admin()          

        # If they submitted to delete a pet
        elif request.form.get('pet-delete'):
            pet_id = request.form.get('pet-delete')
            query = "DELETE FROM pets WHERE pet_id = '" + pet_id + "'"
            execute_query(db_connection, query)
            return refresh_admin()        

        # If they submitted to delete a class
        elif request.form.get('class-delete'):
            class_id = request.form.get('class-delete')
            query = "DELETE FROM classes WHERE class_id = '" + class_id + "'"
            execute_query(db_connection, query)
            return refresh_admin()      

        # If they submitted to delete an enrollment
        elif request.form.get('enroll-delete'):
            enrollment_id = request.form.get('enroll-delete')
            query = "DELETE FROM enrollments WHERE enrollment_id = '" + enrollment_id + "'"
            execute_query(db_connection, query)
            return refresh_admin()         

        # If they submitted to delete a teacher
        elif request.form.get('teacher-delete'):
            teacher_id = request.form.get('teacher-delete')
            query = "DELETE FROM teachers WHERE teacher_id = '" + teacher_id + "'"
            execute_query(db_connection, query)
            return refresh_admin()           

        # If they submitted to delete a vet
        elif request.form.get('vet-delete'):
            vet_id = request.form.get('vet-delete')
            query = "DELETE FROM vets WHERE vet_id = '" + vet_id + "'"
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
                    "Vet First Name": request.form.get('vet_first_name'),
                    "Vet Last Name": request.form.get('vet_last_name'),
                    "Customer First Name": request.form.get('customer_first_name'),
                    "Customer Last Name": request.form.get('customer_last_name')
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
                query = 'INSERT INTO pets (pet_name, species, breed, age, gender, vet_id, customer_id) VALUES (%s,%s,%s,%s,%s, (SELECT vet_id from vets where first_name = %s and last_name = %s),(SELECT customer_id from customers where first_name = %s and last_name = %s))'
                data = (pet_data["Pet Name"],
                        pet_data["Species"],
                        pet_data["Breed"],
                        pet_data["Age"],
                        pet_data["Gender"], 
                        pet_data["Vet First Name"],
                        pet_data["Vet Last Name"],
                        pet_data["Customer First Name"],
                        pet_data["Customer Last Name"])
                
                try:
                    result = execute_query(db_connection, query, data)
                    if result:
                        feedback["Pets"] = f"Added Pet {pet_data['Pet Name']}"
                    else:
                        feedback["Pets"] = "Add Pet Failed."
                except:
                    feedback["Pets"] = "Add Pet Failed."
           
            return refresh_admin(feedback)

        # If they submitted a new class
        elif request.form.get('class-insert'):
            
            # Get class data from form fields
            class_data = {
                    "Class Name": request.form.get('class_name'),
                    "Class Description": request.form.get('class_description'),
                    "Class Day": request.form.get('class_day'),
                    "Class Time": request.form.get('class_time'),
                    "Class Price": request.form.get('class_price'),
                    "Class Enrollments": request.form.get('class_enrollments'),
                    "Class Seats": request.form.get('class_seats')
                    }

            # Check for any empty fields (all required in this form)
            missing_fields = [] 
            for field in class_data.keys():
                if class_data[field] == "":
                    missing_fields.append(field)

            if len(missing_fields) > 0:
                feedback["Classes"] = f"Correct missing information: {missing_fields}"

            # If no fields missing, do the insert
            else:
                query = 'INSERT INTO classes (class_name, class_description, class_day, class_time, class_price, class_enrollments, class_seats) VALUES (%s, %s, %s, %s, %s,%s, %s)'
                data = (class_data["Class Name"],
                        class_data["Class Description"],
                        class_data["Class Day"],
                        class_data["Class Time"],
                        class_data["Class Price"], 
                        class_data["Class Enrollments"], 
                        class_data["Class Seats"])
                
                try:
                    result = execute_query(db_connection, query, data)
                    if result:
                        feedback["Classes"] = f"Added Class {class_data['Class Name']}"
                    else:
                        feedback["Classes"] = "Add Class Failed."
                except:
                    feedback["Classes"] = "Add Class Failed."
           
            return refresh_admin(feedback)

        # If they submitted a new enrollment
        elif request.form.get('enroll-insert'):
            
            # Get class data from form fields
            enroll_data = {
                    "Pet Name": request.form.get('pet_name'),
                    "Class Name": request.form.get('class_name')
                    }

            # Check for any empty fields (all required in this form)
            missing_fields = [] 
            for field in enroll_data.keys():
                if enroll_data[field] == "":
                    missing_fields.append(field)

            if len(missing_fields) > 0:
                feedback["Enrollments"] = f"Correct missing information: {missing_fields}"

            # If no fields missing, do the insert
            else:
                query = 'INSERT INTO enrollments (pet_id, class_id) VALUES ((SELECT pet_id FROM pets WHERE pet_name = %s), (SELECT class_id FROM classes WHERE class_name = %s))'
                data = (enroll_data["Pet Name"],
                        enroll_data["Class Name"])
                
                try:
                    result = execute_query(db_connection, query, data)
                    if result:
                        feedback["Enrollments"] = f"Added Enrollment {enroll_data['Pet Name']} {enroll_data['Class Name']}"
                    else:
                        feedback["Enrollments"] = "Add Enrollment Failed."
                except:
                    feedback["Enrollments"] = "Add Enrollment Failed."
           
            return refresh_admin(feedback)
        
        # If they submitted a new teacher
        elif request.form.get('teacher-insert'):
            
            # Get class data from form fields
            teacher_data = {
                    "Teacher First Name": request.form.get('teacher_first_name'),
                    "Teacher Last Name": request.form.get('teacher_last_name'),
                    "Teacher Email": request.form.get('teacher_email'),
                    "Teacher Phone": request.form.get('teacher_phone'),
                    }

            # Check for any empty fields (all required in this form)
            missing_fields = [] 
            for field in teacher_data.keys():
                if teacher_data[field] == "":
                    missing_fields.append(field)

            if len(missing_fields) > 0:
                feedback["Teachers"] = f"Correct missing information: {missing_fields}"

            # If no fields missing, do the insert
            else:
                query = 'INSERT INTO teachers (first_name, last_name, email, phone) VALUES (%s, %s, %s, %s)'
                data = (teacher_data["Teacher First Name"],
                        teacher_data["Teacher Last Name"],
                        teacher_data["Teacher Email"],
                        teacher_data["Teacher Phone"])
              
                try:
                    result = execute_query(db_connection, query, data)
                    if result:
                        feedback["Teachers"] = f"Added Teacher {teacher_data['Teacher First Name']} {teacher_data['Teacher Last Name']}"
                    else:
                        feedback["Teachers"] = "Add Teacher Failed."
                except:
                    feedback["Teachers"] = "Add Teacher Failed."
           
            return refresh_admin(feedback)


        # If they submitted a new vet
        elif request.form.get('vet-insert'):
            
            # Get class data from form fields
            vet_data = {
                    "Vet First Name": request.form.get('vet_first_name'),
                    "Vet Last Name": request.form.get('vet_last_name'),
                    "Vet Email": request.form.get('vet_email'),
                    "Vet Phone": request.form.get('vet_phone'),
                    "Vet Specialty": request.form.get('vet_specialty')
                    }

            # Check for any empty fields (all required in this form)
            missing_fields = [] 
            for field in vet_data.keys():
                if vet_data[field] == "":
                    missing_fields.append(field)

            if len(missing_fields) > 0:
                feedback["Vets"] = f"Correct missing information: {missing_fields}"

            # If no fields missing, do the insert
            else:
                query = 'INSERT INTO vets (first_name, last_name, email, phone, specialty) VALUES (%s, %s, %s, %s, %s)'
                data = (vet_data["Vet First Name"],
                        vet_data["Vet Last Name"],
                        vet_data["Vet Email"],
                        vet_data["Vet Phone"],
                        vet_data["Vet Specialty"])
              
                try:
                    result = execute_query(db_connection, query, data)
                    if result:
                        feedback["Vets"] = f"Added Vet {vet_data['Vet First Name']} {vet_data['Vet Last Name']}"
                    else:
                        feedback["Vets"] = "Add Vet Failed."
                except:
                    feedback["Vets"] = "Add Vet Failed."
           
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
