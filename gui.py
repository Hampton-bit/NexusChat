import tkinter as tk
from tkinter import ANCHOR, scrolledtext
import socket
import threading
from tkinter import ttk

from tkinter import messagebox
from tkinter import filedialog as fd

HOST = '10.7.93.134'
PORT = 65535

master = tk.Tk()
master.geometry('350x350+500+100')
master.resizable(True, True)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def connect():
    global username_button
    try:
        print("here")
        client.connect((HOST, PORT))
        print("Successfully connected to server")
    except:
        messagebox.showerror("Unable to connect to server", f"Unable to connect to server {HOST} {PORT}")

    username = username_textbox.get()
    password = password_textbox.get()
    if username != '' and password != '':
        data = f"{username},{password}"
        client.sendall(data.encode())
        # Sends username and password to the server as a single message
    else:
        messagebox.showerror("Invalid username or password", "Username and password cannot be empty")



    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)
    password_textbox.config(state=tk.DISABLED)
    


    

    users = tk.Tk()
    users.geometry("750x750+500+50")
    users.title("User List")
    users.resizable(True, True)

    title = tk.Label(users, text='Chat_Box', fg="black", bg='#34B7F1', font='Times 14 bold')
    title.pack()

    main = tk.Canvas(users, height=700, width=700, bg="#34B7F1")
    main.pack()

    frame = tk.Frame(main, bg="#66B2FF")
    # Create a modern-themed style
    
    frame.place(relx=0.25, rely=0.01, relheight=0.9, relwidth=0.7)

    message_box = scrolledtext.ScrolledText(frame, bg='#ECF7FA', fg='black', width=67, height=26.5)
    message_box.config(state=tk.DISABLED)
    message_box.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.8)

    def add_message(message): # Adds message to the messagebox
        message_box.config(state=tk.NORMAL)
        message_box.insert(tk.END, message + '\n')
        message_box.config(state=tk.DISABLED)

    def send_message(): # Sends message to the server with sender and person to be send
        message1 = "*****" + "&" + message_textbox.get("1.0","end")
        message2 = listbox.get(ANCHOR)
        message3 = username
        message = str(message1) + "&" + message2 + "&" + message3
        if message1 == '\n':
            messagebox.showerror("Blank Message", "You cannot send blank messages")
        elif message2 == '':
            messagebox.showerror("No User Selected", "Please select a user from the list to message")
        elif message3 == message2:
            messagebox.showerror("You Chose Yourself", "Please choose another user to message")
        else:
            client.sendall(message.encode())
            message_textbox.delete("1.0","end")
            disconnect_button.config(state=tk.NORMAL)

    message_textbox = tk.Text(frame, height=5, width=60)
    message_textbox.tag_configure('style',foreground="#bfbfbf", font='Times 10 italic')
    message_textbox.place(relx=0.01, rely=0.83)

    style.configure("Modern.TButton",
                foreground="black",
                background="#4CAF50",
                font=("Arial", 10, "bold"),
                padding=8)

    message_button = ttk.Button(frame, text="Send", command=send_message, style="Modern.TButton")
    message_button.place(relx=0.83, rely=0.84)

    disconnect_button = ttk.Button(frame, text='Disconnect', command=disconnect, style="Modern.TButton")
    disconnect_button.place(relx=0.83, rely=0.9)

    #message_button = tk.Button(frame, text="Send", command=send_message)
    #message_button.place(relx=0.88, rely=0.83)

    #disconnect_button = tk.Button(frame, text='Disconnect', command=disconnect)
    #disconnect_button.place(relx=0.83, rely=0.9)

    listbox = tk.Listbox(users,selectmode=tk.SINGLE)
    
    def add_list(user): # Adds users to the list
        if user not in listbox.get(0, "end"):
            listbox.insert("end", user)
        listbox.place(relx=0.05, rely=0.05, relwidth=0.2, relheight=0.9)
        
    def listen_for_lists_from_server(client):
        while 1 :
            first_message= client.recv(2048)
            print(first_message)
            if ("message_from_server" not in str(first_message)): # image
                file = open('indir.jpg', "wb")
                while first_message:
                    print("Image has arrived")
                    file.write(first_message)
                    first_message = client.recv(2048)
                    if len(first_message)<2048:
                        file.write(first_message)
                        file.close()
                        break
                    print("Image taken")
            else: # message and logged in users
                full_message = first_message.decode("utf-8")
                print("Message has arrived")
                message = full_message.split(",")[1]
                if (('~' not in message)): # Logged in users
                    chat_list = message.split(' ')
                    for user in chat_list:
                        add_list(f"{user}")
                else: # message
                    username = message.split("~")[0]
                    content = str(message.split("~")[1])
                    incoming_message = content.replace("\\n","")
                    person_to_be_send = message.split("~")[2]
                    add_message(f"[{username}] → [{person_to_be_send}] {incoming_message} ")

    threading.Thread(target=listen_for_lists_from_server, args=(client, )).start()

    def send_image(image_data): # Sends image bits to the server
        message = image_data
        client.send(message)

    def openfile():
        filetypes = (
            ('JPG', '*.jpg'),
            ('All files', '*.*')
        )

        file = fd.askopenfile(
            initialdir='/',
            filetypes=filetypes)

        image_name = str(file.name)
        image = open(image_name,"rb")
        image_data = image.read(2048)
        while image_data:
            send_image(image_data)
            image_data = image.read(2048)
        image.close()

    btn = tk.Button(users,text="Select File" ,command=openfile)
    btn.place(x=400,y=700)
    
    users.mainloop()
def disconnect():
    client.sendall("disconnect".encode())
    client.close()  
title = tk.Label(master, text='CHAT BINGO', fg="black", bg="#34B7F1", font='Times 14 bold')
title.pack()

area = tk.Canvas(master, height=200, width=400)
area.pack()

master.title('ChatApp')

frame = tk.Frame(master, bg="#34B7F1")
frame.place(relx=0.001, rely=0.081, relheight=1, relwidth=1)


username_label = tk.Label(frame,text="Username:",font="Times 10 bold")
username_label.place(x=20,y=70)

name = tk.StringVar()
username_textbox = tk.Entry(frame, textvariable=name)
username_textbox.place(x=110,y=70)

password_label = tk.Label(frame,text="Password :",font="Times 10 bold")
password_label.place(x=20,y=90)

password = tk.StringVar()
password_textbox = tk.Entry(frame, textvariable=password, show='*')
password_textbox.place(x=110,y=90)
style = ttk.Style()
# Configure the style for the labels
#####

# Configure the custom style for the labels
style.configure("Custom.TLabel", font=("Arial", 12), foreground="black", background="#F1F1F1", padding=5)

# Create the labels using ttk.Label with the custom style
username_label = ttk.Label(frame, text="Username :", style="Custom.TLabel")
username_label.place(x=17, y=70)

password_label = ttk.Label(frame, text="Password : ", style="Custom.TLabel")
password_label.place(x=17, y=95)

# Create the labels using ttk.Label
#username_label = ttk.Label(frame, text="Username:", style="TLabe1")
#username_label.place(x=20, y=70)

#password_label = ttk.Label(frame, text="Password:", style="TLabe1")
#password_label.place(x=20, y=98)
#style.configure("TLabel", font=("Helvetica", 10, "bold"))
#username_label = ttk.Label(frame, text="Username:", style="TLabel")
#username_label.place(x=20, y=70)

#password_label = ttk.Label(frame, text="Password:", style="TLabel")
#password_label.place(x=20, y=90)
style.configure("TEntry", padding=5)
username_textbox = ttk.Entry(frame, textvariable=name, style="TEntry")
username_textbox.place(x=110, y=70)

password_textbox = ttk.Entry(frame, textvariable=password, show='*', style="TEntry")
password_textbox.place(x=110, y=98)


#username_button = tk.Button(frame, text="Login", command=connect)
#username_button.place(x=194,y=120)

style.configure("TButton",
                foreground="black",
                background="#4CAF50",
                font=("Helvetica", 8),
                padding=10)
username_button = ttk.Button(frame, text="Login", command=connect, style="TButton")
username_button.place(x=198, y=130)



def main():
    master.mainloop()
    
if __name__ == '__main__':
    main()
