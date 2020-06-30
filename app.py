import os
from randompage import randompage
from flask import Flask, request, render_template, send_from_directory, redirect, jsonify
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
    if 'election' in getargs and getargs['election'] and 'name' in getargs and getargs[
        'name'] and 'dateFrom' in getargs and getargs['dateFrom']:
        date = datetime.datetime.strptime(getargs['dateFrom'], '%Y-%m-%d')
        try:
            if getargs['election'] == '1':
                if 'format' in getargs and getargs['format'] == 'json':
                    return jsonify(article_of_year(getargs['name'], date))
                return render_template('elections.html', data=article_of_year(getargs['name'], date), getargs=getargs)
            elif getargs['election'] == '2':
                if 'format' in getargs and getargs['format'] == 'json':
                    return jsonify(featured_article(getargs['name'], date))
                return render_template('elections.html', data=featured_article(getargs['name'], date), getargs=getargs)
            elif getargs['election'] == '3':
                if 'format' in getargs and getargs['format'] == 'json':
                    return jsonify(good_article(getargs['name'], date))
                return render_template('elections.html', data=good_article(getargs['name'], date), getargs=getargs)
            elif getargs['election'] == '4':
                if 'format' in getargs and getargs['format'] == 'json':
                    return jsonify(admin(getargs['name'], date))
                return render_template('elections.html', data=admin(getargs['name'], date), getargs=getargs)
            elif getargs['election'] == '5':
                if 'format' in getargs and getargs['format'] == 'json':
                    return jsonify(deletion(getargs['name'], date))
                return render_template('elections.html', data=deletion(getargs['name'], date), getargs=getargs)
        except Exception as e:
            return render_template('elections.html', error=str(e), getargs=getargs)

    return render_template('elections.html', data={}, getargs=getargs)


@app.route('/wiki-elections/bulk', methods=['GET', 'POST'])
def mass_elections():
    app.template_folder = os.path.abspath('./wikielections/templates')
    getargs = request.args.to_dict()
    return render_template('masselections.html', data={}, getargs=getargs)


if __name__ == '__main__':
    app.run()
