from flask import Flask, request
import mysql.connector

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def employee():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        conn = mysql.connector.connect(
            host='34.56.155.20',
            user='new-user',
            password='12345678',
            database='employee-db'
        )
        cursor = conn.cursor()
        cursor.execute("INSERT INTO employees (name, email) VALUES (%s, %s)", (name, email))
        conn.commit()
        cursor.close()
        conn.close()
        return "Data inserted successfully!"

    return '''
        <form method="POST">
            Name: <input type="text" name="name"><br>
            Email: <input type="text" name="email"><br>
            <input type="submit" value="Submit">
        </form>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
