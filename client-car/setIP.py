print ("Enter IP of the server:")

server_ip = input()

file = open('server_ip.txt','w') 

file.write(server_ip) 

file.close() 


# this code reads the IP from file

file = open('server_ip.txt','r') 

sIP = file.read() 

file.close()

print ("IP set to: [",sIP,"]")
