import os
from flask import Flask, request, render_template
from wikielections.utils import *
import datetime

app = Flask(__name__)


@app.route('/wiki-elections', methods=['GET', 'POST'])
def elections():
    app.template_folder = os.path.abspath('./wikielections/templates')
    getargs = request.args.to_dict()
    if 'election' in getargs and 'name' in getargs and 'dateFrom' in getargs:
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

    return render_template('elections.html', data={}, getargs={})


if __name__ == '__main__':
    app.run()
