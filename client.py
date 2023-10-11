import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
import pytun
import socket
from Crypto.Cipher import Kyber
from Crypto.PublicKey import KyberKeypair
# Create a subclass of QWidget to define your main application window
class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Create widgets
        self.label = QLabel('Enter your server ip address:')
        self.input_field = QLineEdit()
        self.label1 = QLabel('Enter message:')
        self.input_field1 = QLineEdit()
        self.button = QPushButton('Send data')
        self.result_label = QLabel('')
        self.result_label2 = QLabel('')

        # Create a vertical layout to arrange the widgets vertically
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input_field)
        layout.addWidget(self.label1)
        layout.addWidget(self.input_field1)
        layout.addWidget(self.button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.result_label2)

        # Set the layout for the main window
        self.setLayout(layout)

        # Connect the button click event to a slot (function)
        self.button.clicked.connect(self.connection)

        # Set the window properties
        self.setWindowTitle('Client App')
        self.setGeometry(100, 100, 400, 200)

    def connection(self):
        # Get the text from the input field
        tun = pytun.TunTapDevice(name='mytun')

        # Configure the IP address for the TUN interface
        tun.addr = '10.0.0.2'
        tun.netmask = '255.255.255.0'

        # Bring the interface up
        tun.up()

        # Create a UDP socket for sending packets to the server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        name = self.input_field.text()
        message = self.input_field1.text()

        # Display a message with the user's input
        self.result_label.setText(f'Connecting to server at address, {name}!')

        # Server's IP and port
        server_ip = name  # Replace with the server's IP address
        server_port = 9000
        server_address = (server_ip,server_port)
        client_socket.connect(server_address)
        while True:
            # Read a packet from the TUN interface
            packet = tun.read(1500)  # Read a packet (max size of 1500 bytes)

            # Send the packet to the server
            client_socket.sendto(packet, (server_ip, server_port))
            client_socket.sendall(message.encode)
            cipher = Kyber.new(KyberKeypair.publickey())
            plaintext = b"Hello, CRYSTALS-KYBER!"
            ciphertext = cipher.encrypt(plaintext)
            # Receive the response packet from the server
            response_packet, _ = client_socket.recvfrom(1500)
            data = client_socket.recv(1024)
            self.result_label2.setText(f'reply from server is:, {data}!')
            #pass

            # Write the response packet to the TUN interface
            tun.write(response_packet)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
