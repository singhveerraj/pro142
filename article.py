from flask import Flask, jsonify, request
import pandas as pd
from article_demographic import output
from article_content import get_recommendations

articles_data = pd.read_csv('D:/whjr/Movie Recommendation App/movie_app/Scripts/articles.csv')
all_articles = articles_data[['url' , 'title' , 'text' , 'lang' , 'total_events']]
liked_articles = []
not_liked_articles = []

app = Flask(__name__)

def assign_val():
    m_data = {
        "url": all_articles.iloc[0,0],
        "title": all_articles.iloc[0,1],
        "text": all_articles.iloc[0,2] or "N/A",
        "lang": all_articles.iloc[0,3],
        "total_events": all_articles.iloc[0,4]/2
    }
    return m_data

@app.route("/get-article")
def get_article():

    article_info = assign_val()
    return jsonify({
        "data": article_info,
        "status": "success"
    })

@app.route("/liked-article")
def liked_article():
    global all_articles
    article_info = assign_val()
    liked_articles.append(article_info)
    all_articles.drop([0], inplace=True)
    all_articles = all_articles.reset_index(drop=True)
    return jsonify({
        "status": "success"
    })

@app.route("/unliked-article")
def unliked_article():
    global all_articles
    article_info = assign_val()
    not_liked_articles.append(article_info)
    all_articles.drop([0], inplace=True)
    all_articles = all_articles.reset_index(drop=True)
    return jsonify({
        "status": "success"
    })

# API to return most popular articles.
@app.route("/popular-articles")
def popular_articles():
    article_info = []
    for index , row in output.iterrows():
        p_d = {
            "url": row['url'],
            "title": row['title'],
            "text": row['text'],
            "lang": row['lang'],
            "total_events": row['total_events']
        }
        article_info.append(p_d)

    return jsonify({
        "data": article_info,
        "status": "success"
    })


# API to return top 10 similar articles using content based filtering method.
@app.route("/recommended-articles")
def recommended_articles():
    global liked_articles
    col_names=['url', 'title', 'text', 'lang', 'total_events']
    all_recommended = pd.DataFrame(columns=col_names)
    
    for i in liked_articles:
        output = get_recommendations(i["contentId"])
        all_recommended=all_recommended.append(output)

    all_recommended.drop_duplicates(subset=["title"],inplace=True)

    recommended_article_data=[]

    for index, row in all_recommended.iterrows():
        _p = {
            "url": row['url'],
            "title": row['title'],
            "text": row['text'],
            "lang": row['lang'],
            "total_events": row['total_events']
        }
        recommended_article_data.append(_p)

    return jsonify({
        "data":recommended_article_data,
        "status": "success"
    })

    

if __name__ == "__main__":
    app.run()