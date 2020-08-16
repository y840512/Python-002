import argparse
import os
import socket
import struct
import threading
from concurrent.futures import ThreadPoolExecutor


class NetTool:
    def __init__(self, args):
        self.threads = args.n
        self.exec_type = args.f
        self.ip = args.ip
        self.save = args.w
        self.mutex = threading.Lock()

    def exec(self):
        ip_array = self.parse_ip(self.ip)
        with ThreadPoolExecutor(self.threads) as executor:
            if self.exec_type == 'ping':
                executor.map(self.ping, ip_array)
            if self.exec_type == 'tcp':
                tcp_args = []
                ports = [i for i in range(1025)]
                for ip in ip_array:
                    for port in ports[1:]:
                        tcp_arg = ip+'-'+str(port)
                        tcp_args.append(tcp_arg)
                executor.map(self.tcp, tcp_args)

    def ping(self, ip):
        try:
            response = os.system(f'ping -c 1 -i 1 {ip}')
            if response == 0:
                self.write_result('ping_result.json', ip + ' can be pinged.')
        except Exception as e:
            print(e)

    def tcp(self, tcp_arg):
        ip = tcp_arg.split('-')[0]
        port = int(tcp_arg.split('-')[1])
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            result = s.connect((ip, port))
            if result is None:
                self.write_result('tcp_result.json', ip + ' is listening on port ' + str(port))
        except Exception as e:
            if e.args[0] == 61:
                pass
            else:
                print(ip, port, e)

    def write_result(self, filename, result):
        if self.mutex.acquire():
            with open(filename, 'a+') as f:
                f.write(result+'\n')
        self.mutex.release()

    @staticmethod
    def parse_ip(ip):
        ip_array = []
        start_ip = ip.split('-')[0]
        end_ip = ip.split('-')[1]
        start_num = socket.ntohl(struct.unpack("I", socket.inet_aton(start_ip))[0])
        end_num = socket.ntohl(struct.unpack("I", socket.inet_aton(end_ip))[0])
        for ip_num in range(start_num, end_num + 1):
            new_ip = socket.inet_ntoa(struct.pack('I', socket.htonl(ip_num)))
            ip_array.append(new_ip)
        return ip_array


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int, required=True, help='指定并发数量')
    parser.add_argument('-f', type=str, required=True, choices=['ping', 'tcp'], help='ping: 进行ping测试，tcp: 进行端口测试')
    parser.add_argument('-ip', type=str, required=True, help='连续 IP 地址支持 192.168.0.1-192.168.0.100 写法')
    parser.add_argument('-w', type=str, required=True, help='扫描结果进行保存')
    args = parser.parse_args()
    net_tool = NetTool(args)
    net_tool.exec()