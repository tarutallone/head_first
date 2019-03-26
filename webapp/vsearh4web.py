# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 16:13:51 2019

@author: junke
"""

from flask import Flask, render_template, request, escape

app = Flask(__name__)


def search4letters(phrase: str, letters: str='aeiou'):
    """phrase内のlettersの集合を返す。"""
    return set(letters).intersection(set(phrase))

def log_request(req: 'flask_request', res: str) -> None:
    with open('vsearch.log', 'a') as log:
        print(req.form,req.remote_addr,req.user_agent,res, file = log, sep=' | ')

@app.route('/search4', methods = ['POST'])
def do_search() -> str:
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = '検索結果：'
    results = str(search4letters(phrase, letters) )
    log_request(request, results)
    return render_template('results.html',
                            the_phrase = phrase,
                            the_letters = letters,
                            the_title = title,
                            the_results = results
                            )

@app.route('/')
@app.route('/entry')
def entry_page() -> str:
    return render_template('entry.html', the_title = 'Web版のsearch4lettersにようこそ！')

@app.route('/viewlog')
def view_the_log() -> str:
    contents = []
    with open('vsearch.log') as log:
        for line in log:
            contents.append([])
            for item in line.split('|'):
                contents[-1].append(escape(item))
    titles = ('フォームデータ', 'リモートアドレス', 'ユーザーエージェント', '結果')
    return render_template('viewlog.html',
                            the_title = 'ログの閲覧',
                            the_row_titles = titles,
                            the_data = contents
                            )

if __name__ == '__main__':
    app.run(debug = True)
