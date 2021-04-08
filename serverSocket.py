import socket,os,pathlib
from threading import Thread
class FileDetails:
    def __init__(self,file_name,file_size):
        self.file_name=file_name
        self.file_size=file_size
dict={}
sep=os.path.sep
path=pathlib.Path(str(pathlib.Path.cwd())+sep+"store")
print(path)
for entry in path.iterdir():
    if entry.is_file()==True:
        dict[entry.name]=FileDetails(entry.name,entry.stat().st_size)
def requestProcessor(clientSocket):
    while True:
        br=0
        cs=1024
        header=b''
        while br<cs:
            b=clientSocket.recv(cs-br)
            br+=len(b)
            header+=b
        request_length=int(header.decode("utf-8").strip())
        br=0
        cs=1024
        request=b''
        while br<request_length:
            if request_length-br<cs: 
                cs=request_length-br
            b=clientSocket.recv(cs)
            br+=len(b)
            request+=b
        request=request.decode("utf-8")
        response=""
        
        if request=="quit":
            clientSocket.close()
            break
        elif request=="dir":
            for i in dict.keys():
                response+=i+": "
                response+=str(dict[i].file_size)+"\n"
            clientSocket.sendall(bytes(str(len(response)).ljust(1024),"utf-8"))
            cs=4096
            bs=0
            start=0
            end=4096
            response_length=len(response)
            while bs<response_length:
                if end>response_length: end=response_length
                string_chunks=response[start:end]
                clientSocket.sendall(bytes(string_chunks,"utf-8"))
                end+=4096
                bs+=4096

        elif request[0:3]=="get":
            file_name=request.split()[1]
            sep=os.path.sep
            file_path=pathlib.Path(str(pathlib.Path.cwd())+sep+"store"+sep+file_name)
            if file_path.exists():
                clientSocket.sendall(bytes("True".ljust(100),"utf-8"))
                file_length=file_path.stat().st_size
                clientSocket.sendall(bytes(str(file_length).ljust(1024),"utf-8"))
                with open(file_path,"rb") as file:
                    br=0
                    cs=4096
                    while br<file_length:
                        if file_length-br<cs: cs=file_length-br
                        b=file.read(cs)
                        br+=len(b)
                        clientSocket.sendall(b)

            else:
                clientSocket.sendall(bytes("False".ljust(100),"utf-8"))
    clientSocket.close()
serverSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.bind(("localhost",5500))
serverSocket.listen()
while True:
    print("Server is ready and listening at port 5500")
    clientSocket,clientSocketName=serverSocket.accept()
    t=Thread(target=requestProcessor(clientSocket))
    t.start()




