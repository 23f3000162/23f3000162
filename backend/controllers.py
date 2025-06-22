# here i am writing all the routes which directs us to web pages
from flask import current_app as app
from flask import Flask, render_template,request,redirect,url_for,session
from backend.models import * # to check the database and match the username and password and other things
# you can name your app as 
# from flask import current_app as ticket_app,,so now you need to write app as ticket app wherever used..
# like ticket_app= Flask(_name_, template_folder="../templates")
# app = Flask(_name_, template_folder="../templates")  # Fix path issue,,sir ne ye line nahi likhi hai
from sqlalchemy import func
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password match
        user = User.query.filter_by(username=username, password=password).first()
        if user and user.role == 1:
            session['user_id'] = user.id
            return redirect(url_for('user_dashboard', user=user))
        elif user and user.role == 0:
            session['user_id'] = user.id
            return redirect(url_for('admin_dashboard', user=user))
        else:
            return "Invalid username or password. Please try again."
        

    # If the request method is GET, render the login page

    return render_template('login.html')

@app.route('/login_user', methods=['POST','GET'])
def login_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password match
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            return render_template('user_dashboard.html', user=user)
        else:
            return "Invalid username or password. Please try again."
        
    return render_template('signup.html')  

@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        fullname = request.form['fullname']
        password = request.form['password']
        username = request.form['username']
        phone = request.form['phone']
        address = request.form['address']
        pincode = request.form['pincode']

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Username already exists. Please choose a different one."

        # Create a new user
        new_user = User(fullname=fullname, password=password, username=username, phone=phone, address=address, pincode=pincode)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('signup.html') 

@app.route('/admin_dashboard')
def admin_dashboard():
    parking_lots = ParkingLot.query.all()
    return render_template('admin_dashboard.html' , parking_lots=parking_lots)

@app.route('/admin_users')
def admin_users():
    users = User.query.filter_by(role=1).all()
    return render_template('admin_users.html', users=users)


    
@app.route('/admin_search')
def admin_search():
    return render_template('admin_search.html')

@app.route('/edit_parkinglot/<int:parkinglot_id>', methods=['GET', 'POST'])
def edit_parkinglot():

    return render_template('edit_parkinglot.html')

@app.route('/admin_summery')
def admin_summery():
    return render_template('admin_summery.html')

@app.route('/edit_delite')
def edit_delite():
    return render_template('edit_delite.html')

@app.route('/new_parking_lot', methods=['GET', 'POST'])
def new_parking_lot():
    if request.method == 'POST':
        location = request.form['location']
        address = request.form['address']
        pincode = request.form['pincode']
        price = request.form['price']
        
        avilable_spots = request.form['available_spots']

        # Create a new parking lot
        new_parking_lot = ParkingLot(prime_location_name=location, price_per_hour=price, address=address, pin_code=pincode, number_of_spots=avilable_spots)
        db.session.add(new_parking_lot)
        db.session.commit()

        return redirect(url_for('admin_dashboard'))
    return render_template('new_parking_lot.html')

@app.route('/user_dashboard')
def user_dashboard():
    parking_lots = ParkingLot.query.all()
    return render_template('user_dashboard.html', parking_lots=parking_lots)

@app.route('/user_summery')
def user_summery():
    return render_template('user_summery.html')

@app.route('/relase_the_parking_spot', methods=['GET', 'POST'])
def relase_the_parking_spot():
    if request.method == 'POST':
        spot_id = request.form['spot_id']
        vechicle_number = request.form['vehicle_number']
        releasing_time = request.form['releasing_time']
        total_cost = request.form['total_cost']
        parkin_timestamp = request.form['parking_time']

        # Find the reservation by spot_id
        reservation = Reservation.query.filter_by(spot_id=spot_id).first()
        if reservation:
            reservation.leaving_timestamp = releasing_time
            reservation.total_cost = total_cost
            reservation.parking_timestamp = parkin_timestamp
            reservation.status = 'Completed'
            reservation.vechicle_number = vechicle_number
            db.session.commit()
            return render_template('relase_the_parking_spot.html', message="Parking spot released successfully.")
        else:
            return "No reservation found for the given spot ID."
    return render_template('relase_the_parking_spot.html')
    

    
        


        # Find the reservation by spot_id
        

    return render_template('relase_the_parking_spot.html')


@app.route('/book_the_parking_spot', methods=['GET', 'POST'])
def book_the_parking_spot():
    if request.method == 'POST':
        spot_id = request.form['spot_id']
        lot_id = request.form['lot_id']
        user_id = request.form['user_id']
        vechicle_number = request.form['vehicle_number']

        # Create a new reservation
        new_reservation = Reservation(spot_id=spot_id, lot_id=lot_id, user_id=user_id, vechicle_number=vechicle_number, status='Booked')
        db.session.add(new_reservation)
        db.session.commit()

        return render_template('book_the_parking_spot.html', message="Parking spot booked successfully.")
    return render_template('book_the_parking_spot.html')

@app.route('/edit_delete_parking_spot')
def edit_delete_parking_spot():
    return render_template('edit_delete_parking_spot.html')

@app.route('/accuied')
def accuied():
    return render_template('accuied.html')

# @app.route('/delete_parking_lots')
# def delete_parking_lots():
#     return render_template('delete_parking_lots.html')
 
    


# app.run(debug=True)
