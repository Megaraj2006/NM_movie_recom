import pandas as pd

def load_movies(csv_path='movies.csv'):
    """Load and preprocess movies dataset."""
    movies = pd.read_csv(csv_path)
    movies['genres'] = movies['genres'].apply(lambda x: x.split('|'))
    return movies

def recommend_movies(preferred_genres, movies):
    """
    Recommend movies based on preferred genres.
    Args:
        preferred_genres (list): List of genres (strings).
        movies (DataFrame): Movies DataFrame with 'genres' column as list.
    Returns:
        DataFrame: Filtered movies matching any preferred genre.
    """
    def has_genre(movie_genres):
        return any(genre in movie_genres for genre in preferred_genres)
    return movies[movies['genres'].apply(has_genre)]

if __name__ == "__main__":
    # Example usage for testing
    movies = load_movies()
    user_input = input("Enter preferred genres (comma-separated, e.g., Action,Comedy): ")
    preferred_genres = [genre.strip() for genre in user_input.split(',')]
    recommended = recommend_movies(preferred_genres, movies)
    if not recommended.empty:
        print("\nRecommended Movies:")
        for title in recommended['title']:
            print("-", title)
    else:
        print("No movies found for the selected genres.")