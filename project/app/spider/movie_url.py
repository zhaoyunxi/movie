import requests

from bs4 import BeautifulSoup

"""
    爬取网站：http://www.ygdy.tv/
   由于阳光电影网的每部电影都是根据它的subject_id来对应的
   所以比较麻烦，那么就用爬虫爬下每部电影和它的id，
   然后在继续调用豆瓣的api
   过程是 搜索一个名字先查找
   由于太麻烦了且怕被封ip我就先爬1000部电影
"""
list_movie = 'http://www.ygdy.tv/movie/1{}.html'
total = 50

with open('movie_url.txt','a+') as f:
    lis = []
    for i in range(total):
        k = i + 1
        if k == 1:
            real_list_movie = list_movie.format('')
        else:
            real_list_movie = list_movie.format('_'+str(k))
        try:
            r = requests.get(real_list_movie)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
        except:
            print('movie_url.txt错误')

        soup = BeautifulSoup(r.text,'html.parser')
        taglist = soup.find_all('li')

        for child in taglist[11:]:
            f.write(child.a.attrs['href']+'\n')




