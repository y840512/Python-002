import os
import sys
import socket
import struct
import time
import threading
import json
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


# 默认值
n_argv = 1
f_argv = None
ip_argv = None
ip_list = []
w_argv = None
m_argv = 'thread'
v_argv = None
ARGV_LIST = ('-n', '-f', '-ip', '-w', '-m', '-v')  # 合法参数


def params_check(params):
    print(params)
    if not params:
        print('params is invalid, you must provide param like : pmap.py -n 4 -f ping -ip 192.168.0.1')
        return False
    for p in params:  # sys.argv[1:]:
        if p not in ARGV_LIST:
            continue
        if p.startswith('-') and p not in ARGV_LIST:
            print(f"command '{p}' is invalid")
            return False
        if p == '-n':
            global n_argv
            n_argv = int(params[params.index('-n') + 1])
            continue
        if p == '-f':
            global f_argv
            f_argv = params[params.index('-f') + 1]
            if f_argv != 'ping' and f_argv != 'tcp':
                print(f"command '{p}' param '{f_argv}' is invalid")
                return False
            continue
        if p == '-ip':
            ip_argv = params[params.index('-ip') + 1]
            global ip_list
            ip_list = ip_argv.split('-')
            if(len(ip_list) == 2):
                ip_num1 = int.from_bytes(socket.inet_aton(ip_list[0]), 'big')
                ip_num2 = int.from_bytes(socket.inet_aton(ip_list[1]), 'big')
                if(ip_num1 > ip_num2):
                    print(f"command '{p}' param '{ip_argv}' is invalid")
                    return False

                ip_list = []
                for ip_num in range(ip_num1, ip_num2+1):
                    ip_list.append(socket.inet_ntoa(struct.pack("!I", ip_num)))
            else:
                print(f"command '{p}' param '{ip_argv}' is invalid")
                return False
            continue
        if p == '-w':
            global w_argv
            w_argv = params[params.index('-w') + 1]
            try:
                f = open(w_argv, 'a+', encoding='utf-8')
                f.close()
            except Exception as e:
                print(e)
                print(f"command '{p}' param '{w_argv}' is invalid")
                return False
            continue
        if p == '-m':
            global m_argv
            m_argv = params[params.index('-m') + 1]
            if m_argv != 'proc' and m_argv != 'thread':
                print(f"command '{p}' param '{m_argv}' is invalid")
                return False
            continue
        if p == '-v':
            global v_argv
            v_argv = True
            continue
    print('params checked ok!')
    return True


def ip_test(ip):
    print('ping: ' + ip)
    f = os.popen(f"ping {ip}", "r")
    ping_result = f.read()
    print(ping_result)
    f.close()
    if(ping_result.find('无法访问目标主机') >= 0 or ping_result.find('Destination Host Unreachable') >= 0):
        print(f'ping {ip} failed!')
        return (ip, 'failed!')
    else:
        print(f"ping {ip} success!")
        return (ip, 'success!')


def port_scan(ip_addr):
    print(f'scanning ports(1-1024) of ip: {ip_addr} begin')

    port_list = []
    for port in range(1, 1025):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((ip_addr, port))
            port_list.append(port)
        except:
            print(f"port: {port} is closed!")
        finally:
            client.close()

    print(f'scanning ports(1-1024) of ip: {ip_addr} end!')
    # if w_argv:
    #     try:
    #         with open(w_argv, "a+", encoding="utf-8") as f:
    #             f.write((ip_str, port_list))
    #             f.write(os.linesep)
    #     except Exception as e:
    #         print(e)
    #     finally:
    #         pass
    return (ip_str, port_list)


if __name__ == '__main__':
    t_start = time.time()

    # ip_test('192.168.1.104')

    params = sys.argv[1:]
    # params = ['-n', '4', '-f', 'ping', '-ip',
    #           '192.168.1.100-192.168.1.110', '-w', 'result.json']
    pool = None
    if(params_check(params)):
        if (m_argv == "proc"):
            pool = ProcessPoolExecutor(max_workers=n_argv)
        elif(m_argv == "thread"):
            pool = ThreadPoolExecutor(max_workers=n_argv)
        print(ip_list)
        if (f_argv == "tcp"):
            result = pool.map(port_scan, ip_list)
        else:
            result = pool.map(ip_test, ip_list)
        pool.shutdown()

        if w_argv:
            try:
                json_result = {}
                for i in result:
                    json_result[i[0]] = i[1]
                    print("%s : %s" % (i[0], i[1]))

                with open(w_argv, "a+", encoding="utf-8") as save_file:
                    json.dump(json_result, save_file)
            except Exception as e:
                print(e)
            finally:
                pass

            if(v_argv):
                print("time use: %f" % (time.time() - t_start))