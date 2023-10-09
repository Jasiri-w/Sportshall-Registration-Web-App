import socket

def getIP():
    ''' print("\n[Server] Server IPv4 : ", socket.gethostbyname(socket.gethostname()))
    print("[Server] Running externally at http://", socket.gethostbyname(socket.gethostname()),":8000/\n") '''
    return socket.gethostbyname(socket.gethostname())
