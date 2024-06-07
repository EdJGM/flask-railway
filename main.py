from flask import Flask, render_template, request, redirect, url_for, flash
from pymysql.cursors import DictCursor
from dotenv import load_dotenv
import os
import pymysql

app = Flask(__name__)

# Load environment variables
load_dotenv()

# MySQL Connection
connection = pymysql.connect(
    host=os.getenv('MYSQL_HOST', 'localhost'),
    user=os.getenv('MYSQL_USER', 'root'),
    password=os.getenv('MYSQL_PASSWORD', ''),
    db=os.getenv('MYSQL_DB', 'flaskcontacts'),
    cursorclass=DictCursor,
    port=int(os.getenv('MYSQL_PORT', 35139))
)

# Settings
app.secret_key = 'mysecret'

@app.route('/')
def index():
    cur = connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    return render_template('index.html' , contacts = data)

@app.route('/add_contact', methods=['GET','POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = connection.cursor()
        cur.execute('INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s)', (fullname, phone, email))
        connection.commit()
        flash('Contact added successfully!')
        return redirect(url_for('index'))

@app.route('/edit/<id>')
def get_contact(id):
    cur = connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = {0}'.format(id))
    data = cur.fetchall()
    return render_template('edit_contact.html', contact = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = connection.cursor()
        cur.execute("""
            UPDATE contacts
            SET fullname = %s,
                phone = %s,
                email = %s
            WHERE id = %s
        """, (fullname, phone, email, id))
        connection.commit()
        flash('Contact updated successfully!')
        return redirect(url_for('index'))

@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    connection.commit()
    flash('Contact removed successfully!')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))