# 作业一：

# 安装并使用 requests、bs4 库，爬取猫眼电影（）的前 10 个
# 电影名称、电影类型和上映时间，
# 并以 UTF-8 字符集保存到 csv 格式的文件中。
# 猫眼电影网址： https://maoyan.com/films?showType=3


#开发人员:yangbin
#开发时间：20200726

import requests
from bs4 import BeautifulSoup as bs

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
header={}
header['user-agent']=user_agent
header['Cookie']='uuid_n_v=v1; uuid=16669340CF1711EA9BFE43BA456BAEDEF1E5F33818F84BFDBCF14504D7155F9F; _csrf=bb75e2cfdb66afa606983c9b19c7d4f40c2ce0ba5c32fb0a701f46dc01e18992; mojo-uuid=d7101a4603827f72ae1eb7106e5b8e6e; _lxsdk_cuid=1738a29ddadc8-02e31f3ba815408-491b3601-13c680-1738a29ddadc8; _lxsdk=16669340CF1711EA9BFE43BA456BAEDEF1E5F33818F84BFDBCF14504D7155F9F; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1595750866,1595753987; mojo-session-id={"id":"74dd8d0846f031922a491c90357d3eca","time":1595647316093}; mojo-trace-id=2; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1595647327; __mta=150247945.1595499635438.1595647316257.1595647327282.8; _lxsdk_s=17383fdccb9-41c-848-528%7C%7C6'

myurl='https://maoyan.com/films?showType=3'

myreponse=requests.get(myurl,headers=header)
#print(myreponse.text)
# print(f'返回码是: {myreponse.status_code}')

bs_info=bs(myreponse.text,'html.parser')
#class="movie-item-hover"
#class="movie-hover-info"

def stripText(text):
    return text.strip().replace('类型:', '').replace('上映时间:', '').replace(' ', '').replace('\n', ' ').replace('\r', '')


myMovies=[]
i=1
for targs in bs_info.find_all('div',attrs={'class','movie-item-hover'}):
    # print(targs.text)
    # print (i)
    movie_list=targs.find_all('div',attrs={'class':'movie-hover-title'})

    movie_title = movie_list[0].find('span').text.strip()
    movie_type = stripText(movie_list[1].text.strip())
    movie_time = stripText(movie_list[3].text.strip())

    myMovie = [movie_title, movie_type, movie_time]
    myMovies.append(myMovie)
    # print (myMovie)
   
    if i==10:
        break
    i=i+1


import pandas as pd
movie1 = pd.DataFrame(data = myMovies)
movie1.to_csv('./movie1.csv', encoding='utf8', index=False, header=False)

