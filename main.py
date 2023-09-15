import sqlite3

# Read the file and copy content to a list
filename = 'stephen_king_adaptations.txt'
with open(filename, 'r') as file:
    stephen_king_adaptations_list = file.readlines()
# Establish a connection with SQLite database
conn = sqlite3.connect('stephen_king_adaptations.db')
cursor = conn.cursor()

# Create table in the database
create_table_sql = '''
        CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table 
                  (movieID INTEGER PRIMARY KEY AUTOINCREMENT,
                  movieName TEXT,
                  movieYear INTEGER,
                  imdbRating REAL
                  )
                  '''
cursor.execute(create_table_sql)
# Insert content into the table
for adaptation in stephen_king_adaptations_list:
    movie_data = adaptation.strip().split(',')
    cursor.execute('''INSERT INTO stephen_king_adaptations_table
                      (movieName, movieYear, imdbRating)
                      VALUES (?, ?, ?)''',
                   (movie_data[1], int(movie_data[2]), float(movie_data[3])))

# Function to search for movies in the database by name
def search_movie_by_name():
    movie_name = input('Enter the name of the movie: ')
    cursor.execute('''SELECT * FROM stephen_king_adaptations_table
                      WHERE movieName LIKE ?''',
                   ('%' + movie_name + '%',))
    movies = cursor.fetchall()
    if movies:
        for movie in movies:
            print('Movie Name:', movie[1])
            print('Movie Year:', movie[2])
            print('IMDB Rating:', movie[3])
    else:
        print('No such movie exists in our database.')


# Function to search for movies in the database by year

def search_movie_by_year():
    movie_year = input('Enter the year: ')
    cursor.execute('''SELECT * FROM stephen_king_adaptations_table
                      WHERE movieYear = ?''',
                   (int(movie_year),))
    movies = cursor.fetchall()
    if movies:
        for movie in movies:
            print('Movie Name:', movie[1])
            print('Movie Year:', movie[2])
            print('IMDB Rating:', movie[3])
    else:
        print('No movies were found for that year in our database.')


# Function to search for movies in the database by rating
def search_movie_by_rating():
    movie_rating = input('Enter the minimum rating: ')
    cursor.execute('''SELECT * FROM stephen_king_adaptations_table
                      WHERE imdbRating >= ?''',
                   (float(movie_rating),))
    movies = cursor.fetchall()
    if movies:
        for movie in movies:
            print('Movie Name:', movie[1])
            print('Movie Year:', movie[2])
            print('IMDB Rating:', movie[3])
    else:
        print('No movies at or above that rating were found in the database.')


# Main loop to present options to the user
while True:
    print('Please select an option:')
    print('1. Search for movies by name')
    print('2. Search for movies by year')
    print('3. Search for movies by rating')
    print('4. Quit')

    option = input('Enter your choice: ')

    if option == '1':
        search_movie_by_name()
    elif option == '2':
        search_movie_by_year()
    elif option == '3':
        search_movie_by_rating()
    elif option == '4':
        break
    else:
        print('Invalid option. Please try again.')

# Commit changes and close the connection
conn.commit()
conn.close()
