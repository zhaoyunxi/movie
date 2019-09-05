from sqlalchemy import Column,Integer,String
from flask_sqlalchemy import SQLAlchemy

'''
dic = {
    'name' :'',
    'time' :'',
    'status' :'',
    'kind' :'',
    'director' :'',
    'hero' :'',
    'area' :'',
    'language' :'',
    'brief' :'',
    'pic' :''
}
'''
db = SQLAlchemy()

class Movie(db.Model):
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(50),unique=False)
    time = Column(String(50))
    status = Column(String(50))
    kind = Column(String(50))
    director = Column(String(50))
    hero = Column(String(100))
    area = Column(String(50))
    language = Column(String(50))
    brief = Column(String(2000))
    pic = Column(String(1000))
    player_url = Column(String(1000))

    def give_data(self,item):
        self.name = item['name']
        self.time = item['time']
        self.status = item['status']
        self.kind = item['kind']
        self.director = item['director']
        self.hero = item['hero']
        self.area = item['area']
        self.language = item['language']
        self.brief = item['brief']
        self.pic = item['pic']
        self.player_url = item['player_url']

    def turn_into_dict(self):
        dic = {}
        dic['name'] = self.name
        dic['time'] = self.time
        dic['status'] = self.status
        dic['kind'] = self.kind
        dic['director'] = self.director
        dic['hero'] = self.hero
        dic['area'] = self.area
        dic['language'] = self.language
        dic['brief'] = self.brief
        dic['pic'] = self.pic
        dic['player_url'] = self.player_url
        return dic