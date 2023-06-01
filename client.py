import os
import socket
import struct


def send_file(sock: socket.socket, filename):
	# Aqui obtenemos el tamaño del archivo
	
	filesize = os.path.getsize(filename)
	# Informar la cantidad de bytes que seran enviados al servidor
	sock.sendall(struct.pack("<Q", filesize))
	
	file = open(filename, "rb")
	
	while read_bytes := file.read(1024):
		sock.sendall(read_bytes)


with socket.create_connection(("localhost", 8690)) as conn:
	print("Conectado al servidor.")
	print("Enviando archivo...")
	filename = input("Ruta del archivo a enviar: ")
	conn.send(filename.encode())
	send_file(conn, filename)
	print("Enviado.")
	
print("Conexion cerrada.")
	
