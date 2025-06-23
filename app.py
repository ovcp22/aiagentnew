from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

search_history = []  # 검색 기록 저장 (서버 껐다 켜면 초기화됨)
recommended_keywords = ["양자역학", "반도체", "광학", "나노소자", "초전도체"]

def search_papers(query):
    url = f'https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit=5&fields=title,authors,url,abstract'
    response = requests.get(url)
    return response.json().get('data', [])

@app.route('/', methods=['GET', 'POST'])
def index():
    papers = []
    if request.method == 'POST':
        question = request.form['question']
        if question and question not in search_history:
            search_history.insert(0, question)  # 최근 검색이 위로 오게
            if len(search_history) > 10:        # 최대 10개만 저장
                search_history.pop()
        papers = search_papers(question)
    elif request.method == 'GET' and 'keyword' in request.args:
        question = request.args.get('keyword')
        if question and question not in search_history:
            search_history.insert(0, question)
            if len(search_history) > 10:
                search_history.pop()
        papers = search_papers(question)
    else:
        question = ""
    return render_template(
        'index.html',
        papers=papers,
        search_history=search_history,
        recommended_keywords=recommended_keywords
    )

if __name__ == '__main__':
    app.run(debug=True)
