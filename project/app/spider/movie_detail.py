import requests
from bs4 import BeautifulSoup
import re

first_pattern = r'</span>([\s\S]*?)<span'
second_pattern = r'<span class="zt">...</span>([\s\S]*?)</li>'
hero_pattern = r'<a href=".*?">(.*?)</a>'
pic_pattern = 'http://www.ygdy.tv'
player_url_pattern = r'now="([\s\S]*?)";var pn'
def get_html(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print('错误')
        return ''

def get_detail(html,url):
    soup = BeautifulSoup(html,'html.parser')

    dic = {
        'name':'',
        'time':'',
        'status':'',
        'kind':'',
        'director':'',
        'hero':'',
        'area':'',
        'language':'',
        'brief':'',
        'pic':'',
        'player_url':''
    }
    get_name(soup,dic)
    get_other_data(soup,dic)
    get_picture(soup,dic)
    get_brief(soup,dic)
    get_player_url(url,dic)
    return dic

def get_name(soup,dic):
    namelist = soup.find_all('div','info')
    if namelist:
        short_string = namelist[0].h1.string

        if '迅雷下载' in short_string:
            name = short_string.split('迅')[0]
        dic['name'] = name
    else:
        dic['name'] = ''

def get_other_data(soup,dic):
    taglist = soup.find_all('div','info')
    i = 1
    if taglist:
        for tag in taglist[0].ul.children:
            if tag.name == 'li':
                if i == 1:
                    time_list = re.findall(first_pattern,str(tag))
                    status_list = re.findall(second_pattern,str(tag))
                    dic['time'] = handle_list(time_list)
                    dic['status'] = handle_list(status_list)
                    i = i + 1
                    continue
                if i == 2 :
                    kind_list = re.findall(first_pattern,str(tag))
                    director_list = re.findall(second_pattern,str(tag))
                    dic['kind'] = handle_list(kind_list)
                    dic['director'] = handle_list(director_list)
                    i = i + 1
                    continue
                if i == 3:
                    hero_list = re.findall(hero_pattern,str(tag))
                    dic['hero'] = handle_list(hero_list)
                    i = i + 1
                    continue
                if i == 4:
                    area_list = re.findall(first_pattern,str(tag))
                    language_list = re.findall(second_pattern,str(tag))
                    dic['area'] = handle_list(area_list)
                    dic['language'] = handle_list(language_list)
                    break

def get_picture(soup,dic):
    '''
    获得图片的方法
    taglist = soup.find_all('div', 'pic')
    print(taglist[0].img.attrs['src'])
    '''

    pic_list = soup.find_all('div','pic')
    if pic_list:
        dic['pic'] = pic_pattern+pic_list[0].img.attrs['src']

def get_brief(soup,dic):
    taglist = soup.find_all('span', 'alltext')
    if taglist:
        brief=str(taglist[0]).split('>', 2)[1].split('<', 2)[0]
        if brief:
            dic['brief'] = brief
        else:
            dic['brief'] = '无'

def get_player_url(url,dic):
    pattern = 'http://www.ygdy.tv/video/'
    '''

        http://www.ygdy.tv/video/?32048-0-0.html
        http://www.ygdy.tv/video/32048.html
    '''
    keyword = re.findall(r'\d+',url)
    if keyword:
        realurl = pattern + '?' + keyword[0] + '-0-0.html'
    else:
        print('get_player_url 错误')
    html = get_html(realurl)
    player_soup = BeautifulSoup(html,'lxml')
    taglist = player_soup.find_all('div', 'main')
    result = re.findall(player_url_pattern, taglist[0].script.string)
    if result:
        dic['player_url'] = result[0]
    else:
        dic['player_url'] = '无可播放地址'

def handle_list(List):
    obj = ''
    if List != None:
        i = 1
        for a in List:
            if i == 1:
                obj = obj + a
                i = i + 1
            else:
                obj = obj + ' ' + a
        return obj
    else:
        return '未知'

def movie_trun_into_str(movie):
    result = ''
    for value in movie.values():
        result = result+value+'    '
    return result

def main():
    movie_pattern = 'http://www.ygdy.tv'
    movies = []
    with open('app/spider/movie_url.txt','r') as f:
    
        lines = []
        movie_url = f.readlines()
        for line in movie_url:
            lines.append(movie_pattern+(line.rstrip('\n')))
        for real_url in lines:
            html = get_html(real_url)
            movie = get_detail(html,real_url)
            print(movie)
            movies.append(movie)
    return movies
    '''
    html = get_html('http://www.ygdy.tv/video/51238.html')
    data = get_detail(html,'http://www.ygdy.tv/video/51238.html')
    print(data)
    '''
