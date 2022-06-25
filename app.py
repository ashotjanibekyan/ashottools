from email.utils import getaddresses
import os
from randompage import randompage
from flask import Flask, request, render_template, send_from_directory, redirect, jsonify
from wikielections.utils import *
from mea_culpa import utils as mcutils
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
    getargs = request.args.to_dict()
    if 'project' in getargs and getargs['project'] == 'wikidata' and 'with' in getargs and 'without' in getargs:
        with_lang = getargs['with'].split('|')
        without_lang = getargs['without']
        return redirect('https://www.wikidata.org/wiki/' + randompage.get_random_item_by_label(with_lang, without_lang))
    return redirect('https://hy.wikipedia.org/wiki/' + randompage.get_random_not_bot())


@app.route('/wiki-elections', methods=['GET', 'POST'])
def elections():
    getargs = request.args.to_dict()
    if is_request_args_valid(getargs):
        date = datetime.datetime.strptime(getargs['dateFrom'], '%Y-%m-%d')
        try:
            data = get_election_data(getargs['election'], getargs['name'], date)
            if 'format' in getargs and getargs['format'] == 'json':
                return jsonify(data)
            if getargs['election'] == '6':
                return render_template('elections.html', data=data[0], getargs=getargs, pages=data[1])
            return render_template('elections.html', data=data, getargs=getargs)
        except Exception as e:
            if 'format' in getargs and getargs['format'] == 'json':
                return jsonify(e)
            return render_template('elections.html', error=str(e), getargs=getargs)

    return render_template('elections.html', data={}, getargs=getargs)

@app.route('/wikimedia_armenia', methods=['GET', 'POST'])
def wikimedia_armenia():
    getargs = request.args.to_dict()
    if 'name' in getargs and getargs['name'] and 'dateFrom' in getargs and getargs['dateFrom']:
        date = datetime.datetime.strptime(getargs['dateFrom'], '%Y-%m-%d')
        try:
            data = get_election_data('7', getargs['name'], date)
            return render_template('wikimedia_armenia.html', data=data, getargs=getargs)
        except Exception as e:
            return render_template('wikimedia_armenia.html', error=str(e), getargs=getargs)

    return render_template('wikimedia_armenia.html', data={}, getargs=getargs)

@app.route('/wiki-elections/bulk', methods=['GET', 'POST'])
def mass_elections():
    getargs = request.args.to_dict()
    return render_template('masselections.html', data={}, getargs=getargs)


@app.route('/mea_culpa', methods=['GET'])
def mea_culpa():
    getargs = request.args.to_dict()
    if 'name' in getargs and getargs['name'] and 'culpa' in getargs and getargs['culpa']:
        articles = mcutils.get_data(getargs['name'], getargs['culpa'])
        return render_template('mea_culpa.html', username=getargs['name'], articles=articles, culpa=getargs['culpa'])
    return render_template('mea_culpa.html')


if __name__ == '__main__':
    app.run()
