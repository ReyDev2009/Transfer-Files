import socket
import struct


def receive_file_size(sock: socket.socket):
	# Funcion que asegura que se reciban los bytes que indican el tamaño del archivo que es enviado, que es codificado por el client
	# via struct.pack(), funcion la cual genera una secuencia de bytes que representan el tamaño del archivo
	
	fmt = "<Q"
	expected_bytes = struct.calcsize(fmt)
	received_bytes = 0
	
	stream = bytes()
	
	while received_bytes < expected_bytes:
		chunk = sock.recv(expected_bytes - received_bytes)
		stream += chunk
		received_bytes = len(chunk)
	
	filesize = struct.unpack(fmt, stream)[0]
	return filesize
	

def recieve_file(sock: socket.socket, filename):
	# Leer en el socket la cantidad de bytes que se recibe del archivo
	
	filesize = receive_file_size(sock)
	
	# Crear un nuevo archivo donde se guardara la informacion
	
	file = open(filename, 'wb')
	
	received_bytes = 0
	
	while received_bytes < filesize:
		chunk = sock.recv(1024)
		if chunk:
			file.write(chunk)
			received_bytes += len(chunk)
			

with socket.create_server(("localhost", 8690)) as server:
	print("Esperando conexion con el cliente...")
	
	conn, addr = server.accept()
	
	print(f"{addr[0]}:{addr[1]} conectado.")
	print("Recibiendo archivo...")
	
	filename = conn.recv(1024)
	recieve_file(conn, filename.decode() if not "/" else filename.decode().split("/")[-1])
	print("Archivo recibido")
	
	
print("Conexion cerrada")


