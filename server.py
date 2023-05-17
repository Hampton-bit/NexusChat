import socket
import threading
import sqlite3


HOST = '10.7.93.134'
PORT = 65535
LISTENER_LIMIT = 5
DATABASE_NAME = r'E:\1. Courses\CCN\project\proj_orig\Python-SocketApp-master\my_database.db'

active_clients = []
active_users = []


def create_table():
    try:
      
      conn = sqlite3.connect(DATABASE_NAME)
      cursor = conn.cursor()

    # Create the users table with username and password columns
      cursor.execute('''CREATE TABLE IF NOT EXISTS users
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    ip_address TEXT NOT NULL,
                    port_no TEXT NOT NULL)''')

      conn.commit()
      conn.close()
      
    except:
      print('fail')

# Call the create_table function to create the table


def add_entry(username, password, ip_address, port_no):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        # Insert a new row into the users table with the provided values
        cursor.execute("INSERT INTO users (username, password, ip_address, port_no) VALUES (?, ?, ?, ?)",
                       (username, password, ip_address, port_no))

        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("Error inserting entry into the database:", e)
def read_entry():
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        # Select all rows from the users table
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()

        # Extract the username and password from each row and store them in separate lists
        username = [row[1] for row in rows]
        password = [row[2] for row in rows]
        

        conn.close()
        
        print(username,password)
        return username, password

    except sqlite3.Error as e:
        print("Error reading entries from the database:", e)


    
def replace_entry(id, username):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Replace an existing entry in the users table
    cursor.execute("REPLACE INTO users (id, username, password, email, age) VALUES (?, ?, ?, ?, ?)",
                   (id, username))

    conn.commit()
    conn.close()

def update_entry(id, new_data):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Update an existing entry in the users table
    cursor.execute("UPDATE users SET username = ? WHERE id = ?",
                   (*new_data, id))

    conn.commit()
    conn.close()
def delete_entry(id):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Delete an entry from the users table
    cursor.execute("DELETE FROM users WHERE id = ?", (id,))

    conn.commit()
    conn.close()
    
def listen_for_messages(client, username):
  while 1:
    message = client.recv(2048)
    if ((b'*****' not in message)):  # image
      while message:
        send_image_to_all(message)
        message = client.recv(2048)
        if len(message) < 2048:
          send_image_to_all(message)
          break
      print("while loop finished")

    else:  # message
      incoming_message = message.decode("utf-8")
      if incoming_message != '':
        chat = incoming_message.split("&")
        print(chat)
        message_to_be_send = chat[1]
        person_to_be_send = chat[2]
        sender = chat[3]
        final_message = "message_from_server," + username + '~' + message_to_be_send + '~' + person_to_be_send
        send_messages_to_one(final_message, person_to_be_send, sender)

      else:
        print(f"The message send from client {username} is empty")


def send_message_to_client(client, message):
  client.sendall(message.encode())


def send_image_to_client(client, message):
  client.send(message)


def send_messages_to_one(
    message, person_to_be_send,
    sender):  # Only sends message to the sender and person to be send

  for user in active_clients:
    if user[0] == person_to_be_send:
      send_message_to_client(user[1], message)

  for user2 in active_clients:
    if user2[0] == sender:
      send_message_to_client(user2[1], message)


def send_messages_to_all(message):  # Sends message to all users

  for user in active_clients:
    send_message_to_client(user[1], message)


def send_image_to_all(message):  # Sends image bits to the all users

  for user in active_clients:
    send_image_to_client(user[1], message)

def client_handler(client):
    while True:
        data = client.recv(2048).decode('utf-8')
        print(data)
        if data:
            username, password = data.split(',')
            ####
            username_list, password_list=read_entry()
            #if (username, password) in zip(username_list, password_list):
              #print("User exists!")
              #Connect the client or perform further actions
            #else:
             #   print("Invalid user")
                # Show appropriate message or take necessary actions
            
            add_entry(username,password,ip_address,port_no)
            active_clients.append((username, client))
            active_users.append(username)
            send_messages_to_all("message_from_server," + username)  # Sends logged in users to the client
            break
        else:
            print("Client data is empty")
    
    threading.Thread(target=listen_for_messages, args=(client, username)).start()



def main():
  create_table()
  
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  print("here")
  try:

    server.bind((HOST, PORT))
    print(f"Running the server on {HOST} {PORT}")
  except:
    print(f"Unable to bind to host {HOST} and port {PORT}")

  server.listen(LISTENER_LIMIT)
  username,password=read_entry()
  print(username,password)
  
  while 1:

    client, address = server.accept()
    print(f"Successfully connected to client {address[0]} {address[1]}")
    global ip_address
    ip_address=address[0]
    global  port_no
    port_no=address[1]
    threading.Thread(target=client_handler, args=(client, )).start()


if __name__ == '__main__':
  
  main()
  
  