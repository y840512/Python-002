import sys
import multiprocessing as mp
from multiprocessing import Process
from multiprocessing.pool import Pool
import socket
from time import time
import json
import os


# 自定义异常方便raise
class InValidEXception(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


def socket_port(ip, low, high, l, w_argv):
    '''
        low, high:临界端口号
    '''
    # start = time()
    print(f"进程(ID:{os.getpid()})开始扫描" + ip)
    for port in range(low, high):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = s.connect_ex((ip, port))

            if result == 0:
                l.acquire()
                print(f"{ip}:{port} is open")
                print("wait...")
                l.release()
                if w_argv != None:
                    response = {
                        'ip': ip,
                        'port': port
                    }
                    try:
                        l.acquire()
                        output = open(w_argv, 'a', encoding='utf-8')
                        json.dump(response, fp=output, ensure_ascii=False)
                        output.write("\n")
                        output.close()
                    except Exception as e:
                        print(e)
                    finally:
                        l.release()
        except Exception as e:
            print(e)
    # end = time()
    # print("扫描ip(%s)端口%d-%d,耗时%0.2f" % (ip, low, high-1, end-start))


def my_ping(ip, w_argv, l):
    # start = time()
    print(f"进程(ID:{os.getpid()})开始ping " + ip)
    f = os.popen(f"ping {ip}", "r")
    d = f.read()
    if '请求超时' in d:
        print(f"ping {ip} 超时")
    elif w_argv:
        try:
            l.acquire()
            with open(w_argv, "a+", encoding="utf-8") as fa:
                fa.write(ip)
                fa.write('\n')
        except Exception as e:
            print(e)
        finally:
            l.release()
    else:
        print(f"ping {ip} 成功")
    f.close()
    # end = time()
    # print("ping %s 耗时%0.2f" % (ip, end-start))


socket.setdefaulttimeout(0.1)
ARGV_LIST = set(('-n', '-f', '-ip', '-w', '-v'))  # 合法参数
PORT_NUM = 1024  # 指定1-1024端口

if __name__ == "__main__":
    print_lock = mp.Manager().RLock()
    argv_list = sys.argv  # 获取命令行参数
    cpu = mp.cpu_count()
    # 默认值
    n_argv = cpu
    w_argv = None
    v_argv = False
    for i in argv_list:
        if i.startswith('-') and i not in ARGV_LIST:
            raise InValidEXception("无效的参数：" + i)  # 其他不在ARGV_LIST中的例如：-d ...
        elif i == '-n':
            n_argv = int(argv_list[argv_list.index('-n') + 1])
        elif i == '-f':
            f_argv = argv_list[argv_list.index('-f') + 1]
        elif i == '-ip':
            ip_argv = argv_list[argv_list.index('-ip') + 1]
            ip_list = ip_argv.split('-')
        elif i == '-w':
            w_argv = argv_list[argv_list.index('-w') + 1]
        elif i == '-v':
            v_argv = True

    if n_argv > cpu or n_argv == 0:
        if n_argv == 0:
            print(f"并发数不能等于0，默认调整为:{cpu}")
        else:
            print(f"并发数({n_argv})超过最大CPU核心数({cpu})，默认调整为：{cpu}")
        n_argv = cpu

    num = PORT_NUM // cpu
    IP_DIV_LIST = list(range(1, 1024, num+1))  # 分配给每个进程的临界端口

    start = time()
    p_pool = Pool(n_argv)
    if len(ip_list) == 1:
        # 只有一个ip的情况
        ip = ip_list[0]
        if f_argv == "ping":
            p_pool.apply_async(func=my_ping, args=(ip, w_argv, print_lock))
        elif f_argv == "tcp":
            for i in range(n_argv):
                if i == n_argv-1:
                    p_pool.apply_async(func=socket_port, args=(
                        ip, IP_DIV_LIST[i], PORT_NUM, print_lock, w_argv))
                else:
                    p_pool.apply_async(func=socket_port, args=(
                        ip, IP_DIV_LIST[i], IP_DIV_LIST[i+1], print_lock, w_argv))

    elif len(ip_list) == 2:
        # 表示一个范围ip的情况
        split_1 = ip_list[0].split('.')
        split_2 = ip_list[1].split('.')
        if split_1[0] != split_2[0] or split_1[1] != split_2[1] or split_1[2] != split_2[2] or split_1[-1] == split_2[-1]:
            raise InValidEXception("无效的ip范围")
        else:
            ip_part = ip_list[0][:ip_list[0].rfind('.')+1]
            if split_1[-1] > split_2[-1]:
                split_1[-1], split_2[-1] = split_2[-1], split_1[-1]
            for i in range(int(split_1[-1]), int(split_2[-1])+1):
                ip = ip_part + str(i)
                if f_argv == "ping":
                    p_pool.apply_async(
                        func=my_ping, args=(ip, w_argv, print_lock))
                elif f_argv == "tcp":
                    for i in range(n_argv):
                        if i == n_argv-1:
                            p_pool.apply_async(func=socket_port, args=(
                                ip, IP_DIV_LIST[i], PORT_NUM, print_lock, w_argv))
                        else:
                            p_pool.apply_async(func=socket_port, args=(
                                ip, IP_DIV_LIST[i], IP_DIV_LIST[i+1], print_lock, w_argv))

    p_pool.close()
    p_pool.join()

    print(f"{f_argv}活动结束")
    end = time()

    if v_argv:
        print("总计耗时%0.2f" % (end-start))
