from flask import Flask, render_template, redirect, url_for, request, flash, send_file, Response
from flask_mysqldb import MySQL
import bcrypt
import record
import pyodbc

app = Flask(__name__)
app.secret_key = "super secret key"
server = 'tcp:resourceiam.database.windows.net'
database = 'resourcedb'
username = 'admintomlin'
password = 'Tomlin@WF'
#driver = "com.mysql.cj.jdbc.XADataSource"
driver= '{ODBC Driver 18 for SQL Server}'

connection_string = f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}'
cnxn = pyodbc.connect(connection_string)



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        cur = cnxn.cursor()
        #cur.execute("CREATE table users (id INT IDENTITY PRIMARY KEY, username VARCHAR(255), email VARCHAR(255),password VARCHAR(255)) ")
        cur.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
        cnxn.commit()
        cur.close()

        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = cnxn.cursor() 
        cur.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cur.fetchone()
        cur.close()

        if user and user[3]==password:
            print(user[0])
            print(user[1])
            print(user[2])
            print(user[3])
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Please check your email and password.', 'danger')

    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/record_audio', methods=['POST'])
def record_audio():
    record.record_audio()
    return send_file('recorded_audio.wav', as_attachment=True)
# Other routes and functions...

if __name__ == '__main__':
    app.run(debug=True)