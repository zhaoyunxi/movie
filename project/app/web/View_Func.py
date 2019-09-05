from . import web
from flask import request,render_template,jsonify,url_for
from app.models.movie_model import db,Movie
from app.view_model.movie import movie_results
from app.spider.movie_detail import main


@web.route('/movie/search',methods=["GET"])
def search():
    keyword = handle_keyword(request.args.get('name'))
    pattern = '%{}%'
    data = db.session.query(Movie).filter(Movie.name.like(pattern.format(keyword))).all()
    print()
    result = movie_results(data)
    return_data = result.dict_class()
    return render_template('search_result.html',data=return_data)
    #这里应该flash几条消息
    '''
    if keyword:
        data = db.session.query(Movie).filter(Movie.name.like(pattern.format(pattern))).all()
    else :
        data = n
    '''


@web.route('/movie',methods=['GET'])
def index():
    data = db.session.query(Movie).filter_by().all()


    return render_template('index.html',movies=data)


@web.route('/movie/<name>/detail')
def movie_detail(name):
    name = handle_keyword(name)
    if name:
        result = db.session.query(Movie).filter_by(name=name).first()
        data = result.turn_into_dict()
    else:
        '''
        这里应该flash
        '''
        pass

    return render_template('detail.html',data=data)
'''
@web.route('/video',methods=['GET'])
def video_player():
    addr = request.args.get('addr')
    return render_template('player.html',data=addr)
'''
def handle_keyword(keyword):
    if keyword:
        real_keyword = keyword.replace(' ','')
        return real_keyword if real_keyword else ''
    else:
        return ''


