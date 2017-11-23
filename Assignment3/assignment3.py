import socket, ssl

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="/Users/aryan/server.crt", keyfile="/Users/aryan/server.key")

bindsocket = socket.socket()
bindsocket.bind(("", 10023))
bindsocket.listen(5)

    
while True:
    newsocket, fromaddr = bindsocket.accept()
    connstream = context.wrap_socket(newsocket, server_side=True,do_handshake_on_connect=True)
    try:
        data = connstream.read()
        filename = data.split()[1]
        f = open(filename[1:],'rb')
        outputdata = f.read()
        f.close()
        """
        Send HTTP header line(s) into socket 
        Note: With send(), strings must be encoded into utf-8 first using encode('utf-8') 
        """
        connstream.send(b'HTTP/1.1 200 OK\r\n\r\n')

        #Send the content of the requested file to the client 
        connstream.send(outputdata)
        connstream.send(b'\r\n')
        connstream.shutdown(socket.SHUT_RDWR)
        connstream.close()
    except IOError: 
        """
        Send response message for file not found
        """
        connstream.send(b'HTTP/1.1 404 Not Found\r\n\r\n')
        connstream.send(b'<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n')
        connstream.shutdown(socket.SHUT_RDWR)
        connstream.close()
    except:
        break
 
        

