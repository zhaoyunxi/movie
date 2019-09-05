
class movie_results():
    def __init__(self,item):
        self.movies = movie_results.handle_data(item)
        self.total = 0
    @classmethod
    def turn_into_dict(cls,obj):
        dic = {}
        dic['name'] = obj.name
        dic['time'] = obj.time
        dic['kind'] = obj.kind
        dic['pic'] = obj.pic
        return dic

    @classmethod
    def handle_data(cls,item):
        lis = []
        for obj in item:
            dic = cls.turn_into_dict(obj)
            lis.append(dic)
        return lis


    def dict_class(self):
        dic = {}
        if len(self.movies) != 0:
            dic['movies'] = self.movies
            dic['total'] = len(self.movies)
        return dic


