import os
from randompage import randompage
from flask import Flask, request, render_template, send_from_directory, redirect
from wikielections.utils import *
import datetime

app = Flask(__name__)


@app.errorhandler(404)
def handle_error(error):
    return index()


@app.route('/')
def index():
    return send_from_directory('static', filename='index.html')


@app.route('/random')
def random():
    return redirect('https://hy.wikipedia.org/wiki/' + randompage.get_random_not_bot())


@app.route('/wiki-elections', methods=['GET', 'POST'])
def elections():
    app.template_folder = os.path.abspath('./wikielections/templates')
    getargs = request.args.to_dict()
    if 'election' in getargs and getargs['election'] and 'name' in getargs and getargs['name'] and 'dateForm' in getargs and getargs['dateForm']:
        date = datetime.datetime.strptime(getargs['dateFrom'], '%Y-%m-%d')
        if getargs['election'] == '1':
            try:
                return render_template('elections.html', data=article_of_year(getargs['name'], date), getargs=getargs)
            except Exception as e:
                return render_template('elections.html', error=str(e), getargs=getargs)
        elif getargs['election'] == '2':
            try:
                return render_template('elections.html', data=featured_article(getargs['name'], date), getargs=getargs)
            except Exception as e:
                return render_template('elections.html', error=str(e), getargs=getargs)
        elif getargs['election'] == '3':
            try:
                return render_template('elections.html', data=good_article(getargs['name'], date), getargs=getargs)
            except Exception as e:
                return render_template('elections.html', error=str(e), getargs=getargs)
        elif getargs['election'] == '4':
            try:
                return render_template('elections.html', data=admin(getargs['name'], date), getargs=getargs)
            except Exception as e:
                return render_template('elections.html', error=str(e), getargs=getargs)
        elif getargs['election'] == '5':
            try:
                return render_template('elections.html', data=deletion(getargs['name'], date), getargs=getargs)
            except Exception as e:
                return render_template('elections.html', error=str(e), getargs=getargs)

    return render_template('elections.html', data={}, getargs=getargs)


if __name__ == '__main__':
    app.run()
