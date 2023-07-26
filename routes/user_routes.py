# routes/user_routes.py
from flask import Blueprint, request, jsonify
import mysql.connector
from config import DB_CONFIG

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/submit', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']

        # Insert data into the database
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            cursor = connection.cursor()

            insert_query = "INSERT INTO MyUsers (firstname, lastname) VALUES (%s, %s)"
            data = (name, email)

            cursor.execute(insert_query, data)
            connection.commit()

            cursor.close()
            connection.close()

            return "Data inserted successfully!"
        except Exception as e:
            return f"An error occurred: {str(e)}"

@user_routes.route('/getdata', methods=['GET'])
def get_data():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        select_query = "SELECT * FROM MyUsers"
        cursor.execute(select_query)

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Convert rows to a list of dictionaries for JSON response
        data = []
        for row in rows:
            user = {
                'id': row[0],
                'firstname': row[1],
                'lastname': row[2]
            }
            data.append(user)

        cursor.close()
        connection.close()

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})

# routes/user_routes.py
from flask import Blueprint, request, jsonify
import mysql.connector
from config import DB_CONFIG

user_routes = Blueprint('user_routes', __name__)

# Existing routes for creating and retrieving users
# ...

@user_routes.route('/update', methods=['PUT'])
def update_user():
    if request.method == 'PUT':
        try:
            data = request.json
            user_id = data['id']
            new_name = data['name']
            new_email = data['email']

            connection = mysql.connector.connect(**DB_CONFIG)
            cursor = connection.cursor()

            update_query = "UPDATE MyUsers SET firstname = %s, lastname = %s WHERE id = %s"
            data = (new_name, new_email, user_id)

            cursor.execute(update_query, data)
            connection.commit()

            cursor.close()
            connection.close()

            return jsonify({"message": "User updated successfully!"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"error": "Method not allowed"}), 405

@user_routes.route('/delete', methods=['DELETE'])
def delete_user():
    if request.method == 'DELETE':
        try:
            data = request.json
            user_id = data['id']

            connection = mysql.connector.connect(**DB_CONFIG)
            cursor = connection.cursor()

            delete_query = "DELETE FROM MyUsers WHERE id = %s"
            data = (user_id,)

            cursor.execute(delete_query, data)
            connection.commit()

            cursor.close()
            connection.close()

            return jsonify({"message": "User deleted successfully!"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"error": "Method not allowed"}), 405
