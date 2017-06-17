import threading
import time
import socket


class ImageCaptureSensor (threading.Thread):
	def get_ip_address(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("8.8.8.8", 80))
		return s.getsockname()[0]

	def __init__(self):
		threading.Thread.__init__(self)
		self.server_socket = socket.socket()
		self.ip_address = self.get_ip_address()
		print("Image server: attempting to bind to {}:{}".format(self.ip_address, 8000))
		self.server_socket.bind((self.ip_address, 8000))
		print("Image server: up and running.")
		print("Image server: please connect the Image sensor server and connect to{}:{}"
			.format(self.ip_address, 8000))
		self.server_socket.listen(0)
		self.connection, self.client_address = self.server_socket.accept()
		print("Immage server: connected.")
		self.connection = self.connection.makefile('rb')

	def run(self):
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
					cv2.imshow('image', image)                    
					if cv2.waitKey(1) & 0xFF == ord('q'):
						break
		finally:
			self.connection.close()
			self.server_socket.close()

class UltraSonicSensor (threading.Thread):
	def get_ip_address(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("8.8.8.8", 80))
		return s.getsockname()[0]

	def __init__(self):
		threading.Thread.__init__(self)
		self.server_socket = socket.socket()
		self.ip_address = self.get_ip_address()
		print("Ultrasonic server: attempting to bind to {}:{}".format(self.ip_address, 8002))
		self.server_socket.bind((self.ip_address, 8002))
		print("Ultrasonic server: up and running.")
		print("Ultrasonic server: please connect the Image sensor server and connect to{}:{}"
			.format(self.ip_address, 8002))
		self.server_socket.listen(0)
		self.connection, self.client_address = self.server_socket.accept()
		print("Immage server: connected.")

	def run(self):
		try:
			print("Connection from: ", self.client_address)
			start = time.time()

			while True:
				sensor_data = float(self.connection.recv(1024))
				print("Distance: %0.1f cm" % sensor_data)

				# testing for 10 seconds
				if time.time() - start > 10:
					break
		finally:
			self.connection.close()
			self.server_socket.close()

# Create new threads
imageSensorThread = ImageCaptureSensor()
ultraSonicThread = UltraSonicSensor()

# Start new Threads
imageSensorThread.start()
ultraSonicThread.start()
# thread1.join()
# thread2.join()
print ("Exiting Main Thread")