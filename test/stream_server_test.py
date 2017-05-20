__author__ = 'zhengwang'

import numpy as np
import cv2
import socket


class VideoStreamingTest(object):

    def get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]

    def __init__(self):

        self.server_socket = socket.socket()
        self.ip_address = self.get_ip_address()
        print("Binding to IP: {}:{}".format(self.ip_address, 8002))
        self.server_socket.bind(self.ip_address, 8000)
        self.server_socket.listen(0)
        self.connection, self.client_address = self.server_socket.accept()
        self.connection = self.connection.makefile('rb')
        self.streaming()

    def streaming(self):
        i = 0;
        try:
            print ("Connection from: ", self.client_address)
            print ("Streaming...")
            print ("Press 'q' to exit")

            stream_bytes = b""
            while True:
                myerror = self.connection.read(1024)
                # stream_bytes.append(int(myerror, 8))
                stream_bytes += myerror
                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')

                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    # image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.CV_LOAD_IMAGE_GRAYSCALE)
                    image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
                    # try:
                    cv2.imshow('image', image)
                    # except:
                    #     cv2.imwrite('im'+str(i)+".jpg", image)
                    #     i+=1
                    # if cv2.waitKey(1) & 0xFF == ord('q'):
                    #     break
        finally:
            self.connection.close()
            self.server_socket.close()

if __name__ == '__main__':
    VideoStreamingTest()
