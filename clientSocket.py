import socket,os,pathlib
clientSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientSocket.connect(("localhost",5500))
while True:
    inputString=input("tmclient->")
    if inputString=="dir":
        clientSocket.sendall(bytes(str(len(inputString)).ljust(1024),"utf-8"))
        clientSocket.sendall(bytes(inputString,"utf-8"))
        br=0
        response_length=b''
        while br<1024:
            b=clientSocket.recv(1024-br)
            br+=len(b)
            response_length+=b
        response_length=int(response_length.decode("utf-8").strip())
        br=0
        cs=4096
        response=b''
        while br<response_length:
            if response_length-br<cs: 
                cs=response_length-br
            b=clientSocket.recv(cs)
            br+=len(b)
            response+=b
        response=response.decode("utf-8").strip()
        print(response)
    elif inputString[0:4]=="get ":
        clientSocket.sendall(bytes(str(len(inputString)).ljust(1024),"utf-8"))
        clientSocket.sendall(bytes(inputString,"utf-8"))
        existance=clientSocket.recv(100).decode("utf-8").strip()
        if existance=="True":
            file_name=input("Save as?")
            file_length=int(clientSocket.recv(1024).decode("utf-8").strip())
            sep=os.path.sep
            path=pathlib.Path(str(pathlib.Path.cwd())+sep+"downloads"+sep+file_name)
            with open(str(path),"wb") as file:
                cs=4098
                br=0
                while br<file_length:
                    if file_length-br<cs: cs=file_length-br
                    b=clientSocket.recv(cs)
                    br+=len(b)
                    file.write(b)
        else:
            print("File does not exist.")
    if inputString=="quit":
        clientSocket.sendall(bytes(str(len(inputString)).ljust(1024),"utf-8"))
        clientSocket.sendall(bytes(inputString,"utf-8"))
        clientSocket.close()
        break