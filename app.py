from flask import Flask, render_template, request
import pickle
import numpy as np

poppular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(poppular_df['Book-Title'].values),
                           Book_Author	= list(poppular_df['Book-Author'].values),
                           Image_URL_M = list(poppular_df['Image-URL-M'].values),
                           avg_ratings = list(poppular_df['avg_ratings'].values),
                           num_ratings = list(poppular_df['num_ratings'].values),
                           )

@app.route('/recommend')
def recommend():
    return render_template('recommender.html')

@app.route('/recommender_books', methods=['POST'])
def recommender():
    user_input = request.form.get('user_input')
    index = np.where(pt.index== str(user_input))[0][0]
    similarity = sorted(list(enumerate(similarity_scores[index])),key= lambda x: x[1], reverse=True)[1:9]
    recommend = []
    for i in similarity:
        lists=[]
        x = pt.index[i[0]]
        book_temp=books.drop_duplicates('Book-Title')
        lists.extend(list(book_temp[book_temp['Book-Title']==pt.index[i[0]]]['Book-Title'].values))
        lists.extend(list(book_temp[book_temp['Book-Title']==pt.index[i[0]]]['Book-Author'].values))
        lists.extend(list(book_temp[book_temp['Book-Title']==pt.index[i[0]]]['Image-URL-M'].values))
        recommend.append(lists)
    print(recommend)
    return render_template('recommender.html', data= recommend)

if __name__=='__main__':
    app.run(debug=True)