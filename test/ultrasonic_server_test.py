__author__ = 'zhengwang'

import socket
import time


class SensorStreamingTest(object):

    def get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]


    def __init__(self):

        self.server_socket = socket.socket()
        self.ip_address = self.get_ip_address()
        print("Binding to IP: {}:{}".format(self.ip_address, 8002))
        self.server_socket.bind((self.ip_address, 8002))
        self.server_socket.listen(0)
        self.connection, self.client_address = self.server_socket.accept()
        self.streaming()

    def streaming(self):

        try:
            print "Connection from: ", self.client_address
            start = time.time()

            while True:
                sensor_data = float(self.connection.recv(1024))
                print "Distance: %0.1f cm" % sensor_data

                # testing for 10 seconds
                if time.time() - start > 10:
                    break
        finally:
            self.connection.close()
            self.server_socket.close()

if __name__ == '__main__':
    SensorStreamingTest()
