import socket
import threading
import subprocess
import os
from subprocess import Popen, PIPE, STDOUT 

bind_ip = '0.0.0.0'
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)  # max backlog of connections

print 'Listening on {}:{}'.format(bind_ip, bind_port)


def handle_client_connection(client_socket):
    request = client_socket.recv(1024)
    print 'Received {}'.format(request)
    #process = Popen(format(request), cwd=r"c:\python27\Scripts")
    process = os.system(format(request))
    print 'Checking status...'
    #check_status = subprocess.Popen("python z:\check_test_times.py 1000 c:\python27\Scripts\output.xml", cwd=r"c:\python27\Scripts")
    check_status = Popen("python z:\check_test_times.py 1000 c:\python27\Scripts\output.xml", shell = True, stdout=PIPE)
    
    client_socket.send(format(check_status.communicate()[0]))
    client_socket.close()

while True:
    client_sock, address = server.accept()
    print 'Accepted connection from {}:{}'.format(address[0], address[1])
    
    client_handler = threading.Thread(
        target=handle_client_connection,
        args=(client_sock,)  # without comma you'd get a... TypeError: handle_client_connection() argument after * must be a sequence, not _socketobject
    )
    client_handler.start()

    
