# app.py
from flask import Flask, render_template, request, redirect, url_for        # import flask
from query_clean import query_cleaner
from data_extraction import connect_n_select, conclusion_pick
from search_engine import covid_search

app = Flask(__name__)             # create an app instance

@app.route("/", methods = ['GET','POST'])
def search():
    if request.method == 'POST':
        data = connect_n_select("./covid_tables.db")
        user_query = request.form.get('user_query')
        clean_user_query = query_cleaner(user_query)
        global final_results 
        final_results = covid_search(data = data, query = clean_user_query)
        return redirect(url_for("search_results",user_query = user_query, results = [final_results.to_html(classes='data', header="true")]))
    else:
        return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/random_insight_generator")
def random_insight_generator():
    random_insights = conclusion_pick("./covid_tables.db")
    return render_template("rand_insight.html", table = [random_insights.to_html(classes = 'data', header = "true", index = False)])

@app.route("/search_results")
def search_results():
    user_query = request.args.get('user_query', None)
    return render_template("search_results.html", user_query = user_query, results = [final_results.to_html(classes='data',header="true", index = False)])

if __name__ == "__main__":
    app.run(debug=True)