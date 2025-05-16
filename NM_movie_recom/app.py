from flask import Flask, request, render_template_string, redirect, url_for, session
from project_dataset import load_movies, recommend_movies

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session

movies = load_movies('./movies.csv')

HTML_NAME = """
<!DOCTYPE html>
<html>
<head><title>Movie Recommendation</title></head>
<body>
    <h2 style="text-align-center;">Welcome! What is your name?</h2>
    <form action="/genres" method="post">
        <input type="text" name="username" required>
        <input type="submit" value="Next">
    </form>
</body>
</html>
"""

HTML_GENRES = """
<!DOCTYPE html>
<html>
<head><title>Movie Recommendation</title></head>
<body>
    <h2>Hi {{name}}, select your favorite genres:</h2>
    <form action="/recommend" method="post">
        <input type="checkbox" name="genres" value="Action">Action<br>
        <input type="checkbox" name="genres" value="Comedy">Comedy<br>
        <input type="checkbox" name="genres" value="Drama">Drama<br>
        <input type="checkbox" name="genres" value="Horror">Horror<br>
        <input type="checkbox" name="genres" value="Sci-Fi">Sci-Fi<br>
        <input type="checkbox" name="genres" value="Romance">Romance<br><br>
        <input type="submit" value="Get Recommendations">
    </form>
</body>
</html>
"""

HTML_RESULT = """
<!DOCTYPE html>
<html>
<head><title>Recommendations</title></head>
<body>
    <h2>Hi {{name}}, here are your recommended movies:</h2>
    {% if movies %}
        <ul>
        {% for movie in movies %}
            <li>{{movie}}</li>
        {% endfor %}
        </ul>
    {% else %}
        <p>No movies found for the selected genres.</p>
    {% endif %}
    <a href="/">Start Over</a>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def name():
    return render_template_string(HTML_NAME)

@app.route('/genres', methods=['POST'])
def genres():
    session['username'] = request.form.get('username', 'User')
    return render_template_string(HTML_GENRES, name=session['username'])

@app.route('/recommend', methods=['POST'])
def recommend():
    name = session.get('username', 'User')
    selected_genres = request.form.getlist('genres')
    recommended = recommend_movies(selected_genres, movies)
    titles = recommended['title'].tolist()
    return render_template_string(HTML_RESULT, name=name, movies=titles)

if __name__ == '__main__':
    app.run(debug=True)