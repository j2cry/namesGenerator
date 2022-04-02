import re
import pathlib
import pandas as pd
from datetime import date, timedelta
from random import randrange
from itertools import zip_longest
from flask import Flask, render_template
from flask_socketio import SocketIO

PORT = 21340
SERVICE_NAME = 'namesgen'
SERVICE_URL = pathlib.Path('/', SERVICE_NAME)
app = Flask(__name__)
socket_io = SocketIO(app, path=SERVICE_URL.joinpath('socket.io').as_posix())

# load data
names = pd.read_csv('data/names.csv')
surnames = pd.read_csv('data/surnames.csv')
midnames = pd.read_csv('data/midnames.csv')


@app.route(SERVICE_URL.as_posix())
def index():
    return render_template('index.jinja2', service_url=SERVICE_URL)


@socket_io.on('generate')
def generate(data):
    ages = re.findall(r'(\d+)', data['ag'])
    size = max(len(data['ln']), len(data['lm']), len(ages))
    gender = data['gd']
    if not size:
        return None
    result = []
    for ln, lm, age in zip_longest(data['ln'], data['lm'], ages):
        name = get_random_from(names, gender=gender, first_letter=ln) if ln != '!' else ''
        midname = get_random_from(midnames, gender=gender, first_letter=lm) if lm != '!' else ''
        surname = get_random_from(surnames, gender=gender) if data['sn'] else ''
        if age:
            age = int(age)
            birthday = random_birthday(age).strftime('%d.%m.%Y')
        else:
            birthday = ''

        result.append({'name': name,
                       'surname': surname,
                       'midname': midname,
                       'birthday': birthday})
    return result


def get_random_from(df: pd.DataFrame, gender=None, first_letter=None):
    gcond = (df['gender'] == gender) if gender else [True] * df.shape[0]
    lcond = (df['lett'] == first_letter.upper()) if (first_letter and first_letter != '*') else [True] * df.shape[0]

    try:
        cond = gcond & lcond
        weights = df.loc[cond, 'num'] / df.loc[cond, 'num'].sum()
        value = df.loc[cond, 'text'].sample(weights=weights).values[0]
    except ValueError:
        value = 'не найдено'
    return value


def random_birthday(age):
    rbound = date(date.today().year - age, date.today().month, date.today().day)
    lbound = date(date.today().year - age - 1, date.today().month, date.today().day + 1)
    delta = rbound - lbound
    return lbound + timedelta(days=randrange(delta.days))


if __name__ == '__main__':
    socket_io.run(app, host="0.0.0.0", port=PORT)
