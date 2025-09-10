from flask import Flask, render_template, request
import pickle
import numpy as np
import os

# Path for models
MODEL_PATH = os.path.join(os.getcwd(), "models")

# Load pickled files
popular_df = pickle.load(open(os.path.join(MODEL_PATH, 'popular.pkl'), 'rb'))
pt = pickle.load(open(os.path.join(MODEL_PATH, 'pt.pkl'), 'rb'))
books = pickle.load(open(os.path.join(MODEL_PATH, 'books.pkl'), 'rb'))
similarity_scores = pickle.load(open(os.path.join(MODEL_PATH, 'similarity_scores.pkl'), 'rb'))

app = Flask(__name__)

# ------------------- ROUTES -------------------

@app.route('/')
def index():
    """Homepage -> Show Top 50 Popular Books"""
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values))

@app.route('/recommend')
def recommend_ui():
    """Page with search box for recommendations"""
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    """Get book recommendations based on user input"""
    user_input = request.form.get('user_input')

    if user_input not in pt.index:
        return render_template('recommend.html', data=[], message=" Book not found. Try another one!")

    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])),
                           key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)

    return render_template('recommend.html', data=data)

@app.route('/contact')
def contact():
    """Contact page"""
    return render_template('contact.html')

# ------------------- MAIN -------------------
if __name__ == '__main__':
    app.run(debug=True)
