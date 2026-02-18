from core.logging_system import SystemLogger
from core.port_scanner import PortScanner
from utils.encryptor import EncryptDecryptData
from os import path


encryptor = EncryptDecryptData()
# port = PortScanner('listen').connections
# encrypted_data = encryptor.encrypt(port)
# SystemLogger('info', 'for test', encrypted_data)
# print(encrypted_data)


pathss = path.join(path.dirname(__file__), 'reports', 'logs', '2026-02-18', '17-06-13_1.log')
decrypted_data = encryptor.decrypt(pathss)
print(decrypted_data)

