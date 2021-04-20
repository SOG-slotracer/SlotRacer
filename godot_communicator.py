import socket


class Connection:
    def __init__(self, ip: str, listener_port: int):
        self.godot_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.godot_socket.bind((ip, listener_port))
        print("waiting for client")
        data, self.godot_address = self.godot_socket.recvfrom(1024)
        print("received message:", data)

    def receive_data(self):
        try:
            self.godot_socket.settimeout(0.0001)
            data, addr = self.godot_socket.recvfrom(1024)
            return data
        except socket.timeout:
            return

    def send_data(self, text):
        self.godot_socket.sendto(text.encode('utf-8'), self.godot_address)
