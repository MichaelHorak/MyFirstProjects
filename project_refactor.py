import sqlite3
import requests
import random
from random import shuffle

DATABASE_FILE = "./music.db"

artists_by_genre = {
    'Rock': [
        'The Beatles', 'Led Zeppelin', 'Queen', 'Rolling Stones', 'Pink Floyd',
        'Nirvana', 'U2', 'Jimi Hendrix', 'David Bowie', 'The Who',
        'AC/DC', 'Radiohead', 'Eagles', 'Aerosmith', 'The Doors'
    ],
    'Pop': [
        'Michael Jackson', 'Madonna', 'Beyoncé', 'Justin Bieber', 'Taylor Swift',
        'Ed Sheeran', 'Rihanna', 'Bruno Mars', 'Katy Perry', 'Adele',
        'Mariah Carey', 'Ariana Grande', 'Elton John', 'Whitney Houston', 'Prince'
    ],
    'Hip-Hop/Rap': [
        'Kendrick Lamar', 'Drake', 'Jay-Z', 'Eminem', 'Kanye West',
        'Lil Wayne', 'Nas', 'Snoop Dogg', 'Tupac Shakur', 'Notorious B.I.G.',
        'J. Cole', 'Travis Scott', 'Chance the Rapper', 'OutKast', 'Run-DMC'
    ],
    'Country': [
        'Johnny Cash', 'Dolly Parton', 'Willie Nelson', 'Taylor Swift', 'Garth Brooks',
        'George Strait', 'Kenny Rogers', 'Shania Twain', 'Carrie Underwood', 'Tim McGraw',
        'Blake Shelton', 'Reba McEntire', 'Alan Jackson', 'Brad Paisley', 'Luke Bryan'
    ],
    'Nu Metal': [
        'Linkin Park', 'Limp Bizkit', 'Korn', 'System of a Down', 'Slipknot',
        'Deftones', 'Papa Roach', 'Disturbed', 'Mudvayne', 'Static-X',
        'P.O.D.', 'Incubus', 'Staind', 'Sevendust', 'Rage Against the Machine'
    ],
    'Arabic Pop': [
        'Amr Diab', 'Nancy Ajram', 'Tamer Hosny', 'Elissa', 'Haifa Wehbe',
        'Fairuz', 'Kazem Al Saher', 'Sherine Abdel-Wahab', 'Assala Nasri', 'Samira Said',
        'Saber Rebai', 'Nawal El Zoghbi', 'Myriam Fares', 'Wael Kfoury', 'Majida El Roumi'
    ],
    'Jazz': [
        'Miles Davis', 'John Coltrane', 'Louis Armstrong', 'Duke Ellington', 'Charlie Parker',
        'Billie Holiday', 'Thelonious Monk', 'Ella Fitzgerald', 'Dave Brubeck', 'Oscar Peterson',
        'Sarah Vaughan', 'Art Blakey', 'Count Basie', 'Dizzy Gillespie', 'Stan Getz'
    ]
}
genres = list(artists_by_genre)


class Question:
    def __init__(self, genre):
        self.answer_pool = []
        self.correct_answer = ""
        self.genre = genre

    def get_line_from_db(self):
        with connect_database() as con:
            cur = con.execute(
                'SELECT artist, album, song, date FROM songdata WHERE genre=? ORDER BY RANDOM() LIMIT 1',
                (self.genre,)
            )
            results = cur.fetchall()
            # format result data
            for result in results:
                key_data = list(result)
            artist_name, collection_name, track_name, date = key_data
            return artist_name, collection_name, track_name, date

    def answers_input(self, score):
        print(self.correct_answer)
        for i in range(len(self.answer_pool)):
            print(f"{i + 1} {self.answer_pool[i]}")
        while True:
            try:
                answer = input("Enter the number of your answer and press <enter>: ")
                selected_option = int(answer) - 1

                if 0 <= selected_option < len(self.answer_pool):
                    if self.answer_pool[selected_option] == self.correct_answer:
                        result = 1
                        print(f"Answer {self.correct_answer} is correct.")
                    else:
                        print(f"Wrong, the correct answer is {self.correct_answer}.")
                        result = 0
                    break  # Exit the loop once a valid answer is provided
                else:
                    print(f"Answer must be one of the presented options.")
            except ValueError:
                print(f"Invalid input. Please enter a number.")

        score.update_score(result)
        print(f"Your score is {score.get_score()}")
        return score


class Question1(Question):
    def __init__(self, genre):
        super().__init__(genre)
        self.artist, self.album, self.song, self.date = super().get_line_from_db()
        # save the correct answer
        self.correct_answer = self.artist
        self.answer_pool = [self.correct_answer]
        # gather other options
        while len(self.answer_pool) < 4:
            self.artist2, self.album2, self.song2, self.date2 = super().get_line_from_db()
            # check for duplicate data
            if self.artist2 not in self.answer_pool:
                if self.artist2 != self.correct_answer:
                    self.answer_pool.append(self.artist2)
        # shuffle answers
        random.shuffle(self.answer_pool)

    def __str__(self):
        return f"\nWho is the artist of the song {self.song} on the album {self.album} from " \
               f"{self.date}?"


class Question2(Question):
    def __init__(self, genre):
        super().__init__(genre)
        self.artist, self.album, self.song, self.date = super().get_line_from_db()
        # save the correct answer
        self.correct_answer = self.album
        self.answer_pool = [self.correct_answer]
        # gather other options
        while len(self.answer_pool) < 4:
            self.artist2, self.album2, self.song2, self.date2 = super().get_line_from_db()
            # check for duplicate data
            if self.artist2 not in self.answer_pool:
                if self.artist2 != self.correct_answer:
                    self.answer_pool.append(self.album2)
        # shuffle answers
        random.shuffle(self.answer_pool)

    def __str__(self):
        return f"\nWhich album features the song {self.song} by {self.artist}?"


class Question3(Question):
    def __init__(self, genre):
        super().__init__(genre)
        self.artist, self.album, self.song, self.date = super().get_line_from_db()
        # save the correct answer
        self.correct_answer = self.artist
        self.answer_pool = [self.correct_answer]
        # gather other options
        while len(self.answer_pool) < 4:
            self.artist2, self.album2, self.song2, self.date2 = super().get_line_from_db()
            # check for duplicate data
            if self.artist2 not in self.answer_pool:
                if self.artist2 != self.correct_answer:
                    self.answer_pool.append(self.artist2)
        # shuffle answers
        random.shuffle(self.answer_pool)

    def __str__(self):
        return f"\nWho is the artist of the album {self.album} from {self.date}?"


class Question4(Question):
    def __init__(self, genre):
        super().__init__(genre)
        self.artist, self.album, self.song, self.date = super().get_line_from_db()
        # save the correct answer
        self.correct_answer = self.date
        self.answer_pool = [self.correct_answer]
        # gather other options
        while len(self.answer_pool) < 4:
            self.artist2, self.album2, self.song2, self.date2 = super().get_line_from_db()
            # check for duplicate data
            if self.artist2 not in self.answer_pool:
                if self.artist2 != self.correct_answer:
                    self.answer_pool.append(self.date2)
        # shuffle answers
        random.shuffle(self.answer_pool)

    def __str__(self):
        return f"\nIn which year was the album {self.album} by {self.artist} released?"


class Question5(Question):
    def __init__(self, genre):
        super().__init__(genre)
        self.artist, self.album, self.song, self.date = super().get_line_from_db()
        # save the correct answer
        self.correct_answer = self.date
        self.answer_pool = [self.correct_answer]
        # gather other options
        while len(self.answer_pool) < 4:
            self.artist2, self.album2, self.song2, self.date2 = super().get_line_from_db()
            # check for duplicate data
            if self.artist2 not in self.answer_pool:
                if self.artist2 != self.correct_answer:
                    self.answer_pool.append(self.date2)
        # shuffle answers
        random.shuffle(self.answer_pool)

    def __str__(self):
        return f"\nIn which year was the song {self.song} by {self.artist} released?"


class Question6(Question):
    def __init__(self, genre):
        super().__init__(genre)
        self.artist, self.album, self.song, self.date = super().get_line_from_db()
        # save the correct answer
        self.correct_answer = self.song
        self.answer_pool = [self.correct_answer]
        # gather other options
        while len(self.answer_pool) < 4:
            self.artist2, self.album2, self.song2, self.date2 = super().get_line_from_db()
            # check for duplicate data
            if self.song2 not in self.answer_pool:
                if self.artist2 != self.artist:
                    self.answer_pool.append(self.song2)
        # shuffle answers
        random.shuffle(self.answer_pool)

    def __str__(self):
        return f"\nWhich song is by {self.artist}?"


class Question7(Question):
    def __init__(self, genre):
        super().__init__(genre)
        # get three songs by the same artist
        # first I return the artist
        with connect_database() as con:
            cur = con.execute(
                'SELECT artist FROM songdata WHERE genre=? ORDER BY RANDOM() LIMIT 1',
                (self.genre,)
            )
            results = cur.fetchall()
        self.artist = results[0][0]
        # now I need to return three songs by this artist:
        with connect_database() as con:
            cur = con.execute(
                'SELECT DISTINCT song FROM songdata WHERE artist=? AND genre=? ORDER BY RANDOM() LIMIT 3',
                (self.artist, self.genre)
            )
            song_list = cur.fetchall()
        for song_tuple in song_list:
            song_name, = song_tuple
            self.answer_pool.append(song_name)
        # now I need to return one song by a different artist
        # and save it as correct answer
        with connect_database() as con:
            cur = con.execute(
                'SELECT DISTINCT song FROM songdata WHERE artist IS NOT ? AND genre=? ORDER BY RANDOM() LIMIT 1',
                (self.artist, self.genre)
            )
            song = cur.fetchone()
        self.correct_answer = song[0]
        self.answer_pool.append(self.correct_answer)
        # shuffle answers
        random.shuffle(self.answer_pool)

    def __str__(self):
        return f"\nWhich song is NOT by {self.artist}?"


class Question8(Question):
    def __init__(self, genre):
        super().__init__(genre)
        self.song_pool = []
        self.artist_pool = []
        # return a year that has at least three artists
        with connect_database() as con:
            cur = con.execute(
                '''SELECT date FROM songdata WHERE
                 genre=? GROUP BY date HAVING COUNT(DISTINCT artist) >= 3
                 ORDER BY RANDOM() LIMIT 1''',
                (self.genre,)
            )
            result = cur.fetchone()
        self.correct_answer = result[0]
        self.answer_pool.append(self.correct_answer)
        # get three songs from the selected year by distinct artists
        # first select three artists that have songs from the selected year
        with connect_database() as con:
            cur = con.execute(
                '''SELECT DISTINCT artist FROM songdata WHERE
                genre=? AND date=? ORDER BY RANDOM() LIMIT 3''',
                (self.genre, self.correct_answer,)
            )
            results = cur.fetchall()
        for result in results:
            self.artist_pool.append(result[0])
        # then get a song from the year of each artist and save it to the songpool
        for artist in self.artist_pool:
            with connect_database() as con:
                cur = con.execute(
                    '''SELECT DISTINCT song FROM songdata WHERE
                    genre=? AND artist=? ORDER BY RANDOM() LIMIT 1''',
                    (self.genre, artist,)
                )
                result = cur.fetchone()
                self.song_pool.append(result[0])
        # lastly I need to select another three dates
        with connect_database() as con:
            cur = con.execute(
                '''SELECT DISTINCT date FROM songdata WHERE
                date != ? ORDER BY RANDOM() LIMIT 3''',
                (self.correct_answer,)
            )
            results = cur.fetchall()
            for result in results:
                self.answer_pool.append(result[0])
        # shuffle answers
        random.shuffle(self.answer_pool)

    def __str__(self):
        return f"\nThe songs {self.song_pool[0]}, {self.song_pool[1]}, and {self.song_pool[2]} are from year:"


class Question9(Question):
    def __init__(self, genre):
        super().__init__(genre)
        # return two sets of data, artist, album, and date
        with connect_database() as con:
            cur = con.execute(
                '''SELECT DISTINCT artist, album, date FROM songdata WHERE
                genre=? ORDER BY RANDOM() LIMIT 2''',
                (self.genre,)
            )
            results = cur.fetchall()
            self.artist1 = results[0][0]
            self.album1 = results[0][1]
            self.date1 = results[0][2]
            self.artist2 = results[1][0]
            self.album2 = results[1][1]
            self.date2 = results[1][2]
            # correct answer
            if self.date1 < self.date2:
                self.correct_answer = self.album1
            elif self.date1 > self.date2:
                self.correct_answer = self.album2
            else:
                self.correct_answer = "Both were released in the same year."
            # answers
            self.answer_pool = [self.album1, self.album2, "Both were released in the same year."]
            # shuffle answers
            random.shuffle(self.answer_pool)

    def __str__(self):
        return f"\nWhich was released first: the album {self.album1} by {self.artist1} or the album {self.album2} by" \
               f" {self.artist2}?"
        # return "In progress, testing Q9..."


class Question10(Question):
    def __init__(self, genre):
        super().__init__(genre)
        # I need to select an artist that has at least three albums
        with connect_database() as con:
            cur = con.execute(
                '''SELECT artist, COUNT(DISTINCT album) AS album_count FROM songdata WHERE 
                genre=? GROUP BY artist HAVING album_count > 2 ORDER BY RANDOM() LIMIT 1''',
                (self.genre,)
            )
            results = cur.fetchone()
            self.artist = results[0]
        # now select three albums by this fella
        with connect_database() as con:
            cur = con.execute(
                '''SELECT DISTINCT album FROM songdata WHERE
                genre=? AND artist=? ORDER BY RANDOM() LIMIT 3''',
                (self.genre, self.artist,)
            )
            results = cur.fetchall()
            for result in results:
                self.answer_pool.append(result[0])
        # now generate one album by somebody else
        with connect_database() as con:
            cur = con.execute(
                '''SELECT album FROM songdata WHERE 
                genre=? AND artist IS NOT ? ORDER BY RANDOM() LIMIT 1''',
                (self.genre, self.artist,)
            )
            result = cur.fetchone()
            self.correct_answer = result[0]
        self.answer_pool.append(self.correct_answer)
        # shuffle
        random.shuffle(self.answer_pool)

    def __str__(self):
        return f"\nWhich of the following albums is NOT part of {self.artist}'s discography?"
        # return "In progress, testing Q10..."


class Score:
    def __init__(self):
        self.score = 0

    def update_score(self, result):
        self.score += result

    def get_score(self):
        return self.score


def main():
    genre = introduction()
    generate_data(genre)
    score = Score()
    generate_questions(genre, score)
    delete_db_table()


def introduction():
    print("Welcome to Michael's Brilliant Music Quiz!")
    print("Test your knowledge about your favourite genre.\n")
    print("Please select a genre from the following options:")
    return prompt_from_options(genres)


def prompt_from_options(options) -> str:
    for i, option in enumerate(options, 1):
        print(i, option)
    while True:
        try:
            choice = int(input("\nEnter the genre number and press <enter>: "))
            if choice in range(1, len(genres) + 1):
                selection = options[(int(choice) - 1)]
                print(f"You selected {selection}")
                return selection
        except ValueError:
            print(f"Enter a number between 1 and {len(genres)}")


def connect_database():
    return sqlite3.connect(DATABASE_FILE)


def generate_data(genre):
    print("Gathering data...\n")
    selected_artists = artists_by_genre[genre]
    artist_ids = get_itunes_ids(selected_artists)

    # send a request to itunes to return artist's songs
    with connect_database() as con:
        con.execute("CREATE TABLE IF NOT EXISTS songdata(artist TEXT, album TEXT, song TEXT, date INTEGER, genre TEXT)")
        for artist in artist_ids:
            str_artist = str(artist)
            response = requests.get(f"https://itunes.apple.com/lookup?id={str_artist}&entity=song")
            o = response.json()
            del o["results"][0]
            for result in o["results"]:
                try:
                    date = result["releaseDate"]
                    # vars to save in the database
                    artist = result["artistName"]
                    album = result["collectionName"]
                    song = result["trackName"]
                    date = date[:4]
                    # Filter out albums we don't want in db
                    # Check if any unwanted pattern is in collection_name
                    if not has_unwanted_pattern(album) and artist in selected_artists:
                        con.execute(
                            "INSERT INTO songdata VALUES(?, ?, ?, ?, ?)",
                            (artist, album, song, date, genre),
                        )
                        con.commit()
                except KeyError:
                    # skips result if it does not include releaseDate
                    continue


def get_itunes_ids(artists):
    artist_ids = []
    for artist in artists:
        response = requests.get("https://itunes.apple.com/search?entity=musicArtist&term=" + artist)
        o = response.json()
        result = o["results"]
        # print(f"Results for artist {artist}: {result}")
        artist_id = result[0]['artistId']
        artist_ids.append(artist_id)
    return artist_ids


def has_unwanted_pattern(album):
    unwanted_patterns = [
        'special edition',
        'deluxe edition',
        'single',
        'soundtrack',
        'motion picture',
        'collection',
        'remastered',
        'remaster',
        'mix',
        'expanded edition',
        'deluxe version',
        'deluxe video edition',
        'version',
        'deluxe'
    ]
    return any(pattern in album.lower() for pattern in unwanted_patterns)


def generate_questions(genre, score):
    questions = [
        Question1(genre),
        Question2(genre),
        Question3(genre),
        Question4(genre),
        Question5(genre),
        Question6(genre),
        Question7(genre),
        Question8(genre),
        Question9(genre),
        Question10(genre)
    ]
    shuffle(questions)

    for question in questions:
        print(question)
        question.answers_input(score)


def delete_db_table():
    with connect_database() as con:
        con.execute("DROP TABLE IF EXISTS songdata")
        con.commit()


if __name__ == "__main__":
    main()
