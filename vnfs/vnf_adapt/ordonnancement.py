import threading
import socket


#@ et num port de la vnf ordonnancement
HOST = '10.0.0.16'
PORTI = 8083
PORTO = 8084
class VNF:
    def __init__(self):
        self.buffer1 = []
        self.buffer2_3 = []    
        self.lock = threading.Lock()

    def bufferize_messages(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((HOST, PORTI))

        while True:
            sock.listen(5) # Fonction pour recevoir les messages
            client, address = sock.accept()
            print "{} connected".format( address )
                
            response = client.recv(255)
            if response != "":
                print response
         
            with self.lock:
                #msg provenant de la GF1
                if adresse == '10.0.0.3':
                    self.buffer1.append(message)
                #msg provenant de la GF2
                elif adresse == '10.0.0.4':
                    self.buffer2_3.append(message)
                #msg provenant de la GF3
                elif adresse == '10.0.0.5':
                    self.buffer2_3.append(message)
        print "Close"
        client.close()
        sock.close()

    def prioritize_and_send(self):

        #host = '10.0.0.11'
        #port = 5000      
        sockOutput = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket with server
        # and port number
        sockOutput.bind((HOST, PORTO))
        # allow maximum 1 connection to
        # the socket
        sockOutput.connect(('10.0.0.2',5000))
        while True:
            with self.lock:
                if self.buffer1:
                    message = self.buffer1.pop(0)
                elif self.buffer2_3:
                    message = self.buffer2_3.pop(0)
                else:
                    message = "Err"
                #self.send_message(message,"10.0.0.2")
                n=sockOutput.send(message)
                if (n != len(message)):
                        print 'Erreur envoi.'
                else:
                        print 'Envoi ok.'      
        # disconnect the server
        sockOutput.close()


 #   def send_message(message, adresse):



if __name__ == "__main__":
    vnf = VNF()
    bufferize_thread = threading.Thread(target=vnf.bufferize_messages)
    prioritize_thread = threading.Thread(target=vnf.prioritize_and_send)

    bufferize_thread.start()
    prioritize_thread.start()