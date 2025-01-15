import json
import math
import socket
import threading
import psycopg2
import os

import time


def CheckIp():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        IP = s.getsockname()[0]
    finally:
        s.close()
    return IP


class Server():
    def __init__(self):
        self.server = socket.socket()
        self.server.setblocking(False)
        self.__ip = CheckIp()
        self.server.bind((self.__ip, 9999))
        self.server.listen(128)
        self.server_listening = False
        self.__client_cnt = 0
        self.clients_socket = []
        self.clients_name = []
        self.user_name = []
        self.client_addr_name = {}
        if not os.path.exists('我的文件'):
            os.makedirs('我的文件')



    def get_msg(self,client_socket, client_name, client_address):
        while self.server_listening:
            try:
                data = client_socket.recv(1024).decode('utf-8')
            except Exception:
                self.__client_cnt -= 1
                if client_socket in self.clients_socket:
                    self.clients_socket.remove(client_socket)
                    self.user_name.remove(self.client_addr_name[client_address])
                    #for c in self.clients_socket:
                        #c.send(('exit' + self.client_addr_name[client_address]).encode('utf-8'))
                if client_name in self.clients_name:
                    self.clients_name.remove(client_name)
                if client_address in self.client_addr_name:
                    del self.client_addr_name[client_address]
                client_socket.close()
                break
            data = json.loads(data)
            print(data)
            if type(data) == list:
                if data[0] == 'register':
                    user = data[1]
                    password = data[2]
                    conn = psycopg2.connect(database='DataMy', user='postgres', password='123456', host='127.0.0.1', port='5432')
                    curr = conn.cursor()
                    curr.execute(f"insert into users values ('{user}', '{password}')")
                    conn.commit()
                    conn.close()
                    client_socket.send(json.dumps('sccess').encode('utf-8'))
                if data[0] == 'login':
                    user = data[1]
                    password = data[2]
                    users_dict = {}
                    conn = psycopg2.connect(database='DataMy', user='postgres', password='chensiyuyi', host='127.0.0.1', port='5432')
                    curr = conn.cursor()
                    curr.execute("select * from users")
                    rews = curr.fetchall()
                    for rew in rews:
                        users_dict[rew[0]] = rew[1]
                        print(users_dict)
                    conn.commit()
                    conn.close()
                    if users_dict[user] == password:
                        client_socket.send(json.dumps('access').encode('utf-8'))
                        self.__client_cnt += 1
                        self.client_addr_name[client_address] = user
                        self.user_name.append(user)
                        print(self.user_name)
                        for c in self.clients_socket:
                            c.send(json.dumps('client' + self.client_addr_name[client_address]).encode('utf-8'))
                    else:
                        client_socket.send(json.dumps('fail').encode('utf-8'))
                    print(self.user_name)
                if data[0] == 'load':
                    file_name = data[1]
                    self.path = os.path.abspath('我的文件' + '\\{}'.format(file_name))
                    size = os.stat(self.path).st_size
                    max_size = 1024
                    self.file_num = math.ceil(size/max_size)
                    data = [self.file_num, file_name]
                    print(data)
                    client_socket.send(bytes(json.dumps(data).encode('utf-8')))
                if type(data[1]) == int:
                    print(data)
                    client_socket.send(json.dumps('alr').encode('utf-8'))
                    file_path = os.path.abspath('我的文件' + '\\{}'.format(data[0]))
                    i=0
                    with open(file_path, "wb") as f:
                        while i < data[1]:
                            data_f = client_socket.recv(1024)
                            f.write(data_f)
                            i += 1
                        print('wenc')
            elif data == 'working':
                if not client_name in self.clients_name:
                    self.clients_name.append(client_name)
            elif data[:8] == 'download':
                path = os.path.abspath('我的文件')
                file_names= os.listdir(path)
                client_socket.send(bytes(json.dumps(file_names).encode('utf-8')))
            elif data[:3] == 'alr':
                while True:
                    with open(self.path, "rb") as f:
                        for i in range(self.file_num):
                            data_f = f.read(1024)
                            client_socket.send(data_f)
                    break
            else:
                msg_data = data
                for c in self.clients_socket:
                    data = (self.client_addr_name[client_address] + " " + time.strftime("%Y-%m-%d, %H:%M:%S") + "\n" + msg_data)
                    c.send(json.dumps(data).encode('utf-8'))






    def Listen(self):
        self.server_listening = True
        while self.server_listening:
            try:
                client_socket, client_address = self.server.accept()
                self.clients_socket.append(client_socket)
                client_socket.setblocking(False)
                client_socket.settimeout(5)
            except BlockingIOError:
                continue
            except ConnectionAbortedError:
                return '连接断开'
            except ConnectionResetError:
                return '连接断开'
            print('连接成功')
            client_name = 'client{}'.format(self.__client_cnt)
            msg_tread = threading.Thread(name=client_name, target=self.get_msg, args=[client_socket, client_name, client_address])
            msg_tread.setDaemon(True)
            msg_tread.start()



if __name__ == '__main__':
    server = Server()
    server.Listen()