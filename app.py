from flask import Flask, render_template, request
import wikipediaapi
from similarities import Similarity

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keyword = request.form['keyword']
        user_input = request.form['user_input']

        wiki_wiki = wikipediaapi.Wikipedia('Eigen (eigen@eigen.com)', 'en')
        page_py = wiki_wiki.page(keyword)
        
        if page_py.exists():
            wikipedia_summary = page_py.summary[0:1000]
        else:
            wikipedia_summary = None

        if wikipedia_summary:
            model = Similarity()
            similarity_score = model.similarity(wikipedia_summary, user_input)
            score = round(float(similarity_score) * 100, 2)
        else:
            score = False

        return render_template('index.html', score=score, keyword=keyword, user_input=user_input)

    return render_template('index.html', score=None, keyword=None, user_input=None)

if __name__ == '__main__':
    app.run(debug=True)
