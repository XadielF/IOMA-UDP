from tkinter import *
import socket
import threading
import random
from server import *

def root_window(name):
    login_window.destroy()
    root = Tk()
    root.title("Inter-Office Messaging Application")
    root.geometry("700x700")

    # Insert the peers text box
    peers_label = Label(root, text="Peers:", bg="pink", font=("Arial", 12))
    peers_label.grid(row=0, column=0)
    peers_textbox = Text(root, width=25, height=30, highlightbackground="black", highlightthickness=1, font=("Arial", 10))
    peers_textbox.grid(row=1, column=0)
    peers_textbox.insert(END, name)
    peers_textbox.grid_propagate(0)


    # Message List frame
    message_list_label = Label(root, text="Message List:", bg="pink", font=("Arial", 12))
    message_list_label.grid(row=0, column=1)
    message_list_textbox = Text(root, width=50, height=30, highlightbackground="black", highlightthickness=1, font=("Arial", 10))
    message_list_textbox.grid(row=1, column=1)
    message_list_textbox.grid_propagate(0)

    message_label = Label(root, text="Message:", bg="pink", font=("Arial", 15))
    message_label.grid(row=2, column=0, pady=15, padx=10, sticky=W)

    text_box = Text(root, font=("Arial", 13))
    text_box.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky=N + W + S + E)

    # name = input("Enter username: ")

    # def create_login_frame():
    #     login_frame = Toplevel()
    #     login_frame.title("Log In")
    #     login_frame.geometry("250x150")
    #
    #     user_label = Label(login_frame, text="User:")
    #     user_label.grid(row=0, column=0, padx=5, pady=5)
    #
    #     user_entry = Entry(login_frame, font=("Helvetica", 11))
    #     user_entry.grid(row=0, column=1, columnspan=2)
    #
    #     login_button = Button(login_frame, text="Log in", command= lambda : create_peer_label(user_entry.get()))
    #     login_button.grid(row=1, column=1, pady=5, columnspan=2)
    #
    #     def create_peer_label(name):
    #         peer_label = Label(peers_frame, text=name, font=("Helvetica", 12))
    #         peer_label.place(x=5, y=30)
    #         peer_label.grid_propagate(0)
    #         login_frame.destroy()
    #
    #     login_frame.mainloop()

    def receive():
        while True:
            try:
                message, _ = client.recvfrom(1024)
                message_list_textbox.insert(END,  message.decode() + "\n")
            except:
                pass

    t = threading.Thread(target=receive)
    t.start()

    client.sendto(f"SIGNUP_TAG:{name}".encode(), ("198.245.101.157", 40000))

    def send_msg():
        message = text_box.get(1.0, END)
        text_box.delete(1.0, END)
        if message.lower() == "exit":
            root.destroy()
        else:
            client.sendto(f"{name}: {message}".encode(), ( "198.245.101.157" , 40000))
            #message_list_textbox.insert(END, f"{name}: " + message)


    # Button
    send_button = Button(root, text="Send", height=2, width=10, command=send_msg)
    send_button.grid(row=2, column=1)

    # menubar = Menu(root)
    # root.config(menu=menubar)
    # file_menu = Menu(menubar)
    # menubar.add_cascade(label="File", menu= file_menu)
    #
    # file_menu.add_command(label="Log in", command= create_login_frame)
    # file_menu.add_separator()
    # file_menu.add_command(label="Exit", command=root.destroy)

    # def login_frame():
    #     login_window = Toplevel(root)
    #     login_window.geometry("150x200")
    #     user_label = Label(login_window, text="User: ")
    #     user_label.place(x=15, y=25)

    root.mainloop()

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client.bind(("198.245.101.157", random.randint(50000, 60000)))

login_window = Tk()
login_window.title("Log In")
login_window.geometry("250x150")

user_label = Label(login_window, text="User:")
user_label.grid(row=0, column=0, padx=5, pady=5)

user_entry = Entry(login_window, font=("Helvetica", 11))
user_entry.grid(row=0, column=1, columnspan=2)


login_button = Button(login_window, text="Log in", command= lambda : root_window(user_entry.get()))
login_button.grid(row=1, column=1, pady=5, columnspan=2)

login_window.mainloop()