#import pytun
import socket
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from Crypto.Cipher import Kyber
from Crypto.PublicKey import KyberKeypair
import pytun
# Create a subclass of QWidget to define your main application window
class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Create widgets
        self.label = QLabel('Enter your server ip address:')
        self.input_field = QLineEdit()
        self.label1 = QLabel('Enter your server port:')
        self.input_field1 = QLineEdit()
        
        self.button = QPushButton('Start Server')
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
        self.button.clicked.connect(self.serverApp)

        # Set the window properties
        self.setWindowTitle('Server App')
        self.setGeometry(100, 100, 400, 200)

    def serverApp(self):
        # Get the text from the input field
        name = self.input_field.text()
        port = self.input_field1.text()

        # Display a message with the user's input
        self.result_label.setText(f'server listening at, {name}:{port}!')
        # Create a TUN interface named 'mytun'
        tun = pytun.TunTapDevice(name='mytun')

        # Configure the IP address for the TUN interface
        tun.addr = '10.0.0.1'
        tun.netmask = '255.255.255.0'

        # Bring the interface up
        tun.up()

        # Create a UDP socket for forwarding packets
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Server's IP and port
        server_ip = name
        server_port = int(port)

        server_socket.bind((server_ip, server_port))

        while True:
            # Read a packet from the TUN interface
            packet = tun.read(1500)  # Read a packet (max size of 1500 bytes)

            # Forward the packet to a remote destination (e.g., Google's DNS)
            server_socket.sendto(packet, ('8.8.8.8', 53))
            server_socket.sendall(b"baud!!!")
            # Receive the response packet
            response_packet, _ = server_socket.recvfrom(1500)
            client_socket, client_address = server_socket.accept()
            data = client_socket.recv(1024)
            self.result_label2.setText(f'client reply:{data.decode()}!')
            # Write the response packet to the TUN interface
            tun.write(response_packet)
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())


