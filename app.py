import mysql.connector
from mysql.connector import Error
from flask import Flask, request, jsonify
import json
app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'passwd': 'saransh',
    'database': 'db'
}
#connection = mysql.connector.connect(**db_config)


# we have created this function because the connection was getting lost every time we added or did something to the database,
# now we call this function and make a connection everytime any other function is called so that we dont have to do it manually everytime
# we have added error handling in every function so that we get to know if there is any error over there, we also close the connection we have made
# in everu other function so that it doesnt create two connections at one time
def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            return connection
    except Error as e:
        app.logger.error(f"Error connecting to MySQL: {e}")
        return None
    
connection = get_db_connection()
if connection.is_connected():
    print("Database connected")
    db_info = connection.get_server_info()
    print("Connected to MySQL Server version ", db_info)
connection.close()

@app.route('/')
def home():
    return "Book Management System API"

@app.route('/api/book', methods=['POST'])
def add_book():
    connection=get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            data = request.get_json()
            title = data['title']
            author = data['author']
            published_date = data['published_date']
            cursor.execute("INSERT INTO books (title, author, published_date) VALUES (%s, %s, %s)",
                        (title, author, published_date))
            connection.commit()
            
            return jsonify({'message': 'Book added successfully!'}), 201
        except Exception as e:
            app.logger.error(f"Error deleting book: {e}")
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            connection.close()
    else:
        return jsonify({'message': 'Failed to connect to the database'}), 500


@app.route('/api/books', methods=['GET'])
def get_books():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM books")
            books = cursor.fetchall()
           
            return jsonify(books)
        except Exception as e:
            app.logger.error(f"Error deleting book: {e}")
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            connection.close()
    else :
        return jsonify({'message': 'Failed to connect to the database'}), 500

@app.route('/api/book/<int:book_id>', methods=['GET'])
def get_book(book_id):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM books WHERE id=%s", (book_id,))
            book = cursor.fetchone()
           
            return jsonify(book)
        except Exception as e:
            app.logger.error(f"Error deleting book: {e}")
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            connection.close()
    else:
        return jsonify({'message': 'Failed to connect to the database'}), 500
    
@app.route('/api/book/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    connection=get_db_connection()
    if connection:
        try:

            updated_book = request.get_json()
            title = updated_book['title']
            author = updated_book['author']
            published_date = updated_book['published_date']
            cursor = connection.cursor()
            cursor.execute("UPDATE books SET title=%s, author=%s, published_date=%s WHERE id=%s",
                        (title, author, published_date, book_id))
            connection.commit()
            
            return jsonify(updated_book)
        except Exception as e:
            app.logger.error(f"Error deleting book: {e}")
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            connection.close()
    else:
        return jsonify({'message': 'Failed to connect to the database'}), 500

@app.route('/api/book/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    connection= get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM books WHERE id=%s", (book_id,))
            connection.commit()
            
            return '', 204
        except Exception as e:
            app.logger.error(f"Error deleting book: {e}")
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            connection.close()
    else:
        return jsonify({'message': 'Failed to connect to the database'}), 500


if __name__ == "__main__":
    app.run(debug=True)


