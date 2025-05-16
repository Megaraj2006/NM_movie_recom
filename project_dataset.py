import pandas as pd

try:
    df_movies = pd.read_csv('movies.csv')
    display(df_movies.head())
except FileNotFoundError:
    print("Error: 'movies.csv' not found. Please ensure the file is in the correct location and accessible.")
    df_movies = None
except pd.errors.ParserError:
    print("Error: Could not parse 'movies.csv'. Please check the file format.")
    df_movies = None
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    df_movies = None

print("Shape of the DataFrame:", df_movies.shape)
print("\nInfo:")
df_movies.info()

# Descriptive Statistics
print("\nDescriptive Statistics for Numerical Columns:")
print(df_movies.describe(include='number'))

# Categorical Analysis
print("\nGenres Distribution:")
print(df_movies['genres'].value_counts())

# Missing Value Analysis
print("\nMissing Values:")
print(df_movies.isnull().sum())

# Initial Observations
print("\nInitial Observations:")
# Add observations here after running the code.


# Genre Analysis
genre_counts = df_movies['genres'].str.split('|').explode().value_counts()
print("Top 10 most frequent genres:\n", genre_counts.head(10))

# Title Analysis
df_movies['title_length'] = df_movies['title'].str.len()
average_title_length = df_movies['title_length'].mean()
print(f"\nAverage movie title length: {average_title_length}")

# Numerical Analysis (movieId)
print("\nmovieId descriptive statistics:")
print(df_movies['movieId'].describe())
# Check for gaps in movieId sequence
movieId_diffs = df_movies['movieId'].diff().dropna()
print("\nmovieId differences:\n", movieId_diffs.describe())

# Look for potential outliers in movieId
print("\nPotential movieId outliers (beyond 3 standard deviations):")
std_dev = movieId_diffs.std()
mean = movieId_diffs.mean()
print(movieId_diffs[(movieId_diffs > mean + 3 * std_dev) | (movieId_diffs < mean - 3 * std_dev)])


import matplotlib.pyplot as plt

# 1. Histogram of movieId
plt.figure(figsize=(10, 6))
plt.hist(df_movies['movieId'], bins=50, color='skyblue', edgecolor='black')
plt.title('Distribution of Movie IDs')
plt.xlabel('Movie ID')
plt.ylabel('Frequency')
plt.show()

# 2. Bar chart of top 10 most frequent genres
genre_counts = df_movies['genres'].str.split('|').explode().value_counts().head(10)
plt.figure(figsize=(12, 6))
genre_counts.plot(kind='bar', color='coral')
plt.title('Top 10 Most Frequent Genres')
plt.xlabel('Genre')
plt.ylabel('Frequency')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# 3. Box plot of title_length
plt.figure(figsize=(8, 6))
plt.boxplot(df_movies['title_length'], patch_artist=True, boxprops=dict(facecolor='lightgreen'))
plt.title('Distribution of Movie Title Lengths')
plt.ylabel('Title Length')
plt.show()

# 4. Scatter plot of movieId vs. title_length (with color based on a specific genre)
plt.figure(figsize=(12, 8))
# Example: color points based on whether the movie is 'Drama'
df_movies['is_drama'] = df_movies['genres'].str.contains('Drama')
plt.scatter(df_movies['movieId'], df_movies['title_length'], c=df_movies['is_drama'], cmap='viridis')
plt.title('Movie ID vs. Title Length (Colored by Drama Genre)')
plt.xlabel('Movie ID')
plt.ylabel('Title Length')
plt.colorbar(label='Is Drama?')
plt.show()

