from flask import Flask, render_template, request, redirect, url_for, session
import boto3
import json
from api import flights

def send_email_via_sns():
    sns = boto3.client('sns', region_name='us-east-1')
    topic_arn = 'arn:aws:sns:us-east-1:637423189033:new_user'
    
    response = sns.publish(
        TopicArn=topic_arn,
        Message='A new user has registered to your service',
        Subject='New registration'
    )
    print(response)

application = Flask(__name__)
application.secret_key = 'your_secret_key'

# Initialize a DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Users')

@application.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return render_template('date_entry.html')

@application.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        response = table.get_item(Key={'username': username})
        user = response.get('Item')
        if user and user['password'] == password:
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            return 'Invalid Credentials'
    return render_template('login.html')

@application.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check if user already exists
        existing_user = table.get_item(Key={'username': username}).get('Item')
        if not existing_user:
            table.put_item(Item={'username': username, 'password': password})
            send_email_via_sns()
            return redirect(url_for('login'))
        else:
            return 'Username already exists'
    return render_template('register.html')

@application.route('/flights', methods=['POST'])
def get_flights():
    origin = request.form['origin']
    destination = request.form['destination']
    date = request.form['date']
    
    flight_info = flights(origin, destination, date)
    #flight_info = fetch_flights_for_date(date)  # This should return a dictionary structured like your JSON
    return render_template('flights.html', date=date, flight_info=flight_info, origin=origin, destination=destination)


@application.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))

if __name__ == '__main__':
    application.run(debug=True)
