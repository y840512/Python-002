# 作业三：
# 实现一个 @timer 装饰器，记录函数的运行时间，注意需要考虑函数可能会接收不定长参数。
import time
import os


def timer(func):
    def run_func(*args, **kwargs):
        start_time=time.time()
        start_time_str=time.strftime("%Y-%m-%d %H:%M:%S")
        print (f'#{start_time_str} begin run')

        func(*args, **kwargs)
        end_time=time.time()
        end_time_str=time.strftime("%Y-%m-%d %H:%M:%S")
        print (f'#{start_time_str} run end')

        elapse_time = end_time - start_time 
        print (f'开始时间：{start_time_str}，结束时间：{end_time_str}，耗时：{elapse_time}s')
    return run_func

@timer
def run(sleep_time):
    time.sleep(sleep_time)
    print ('I can runing.')
    time.sleep(sleep_time)


# if __name__ == '__main__':
#     run()

run(5)