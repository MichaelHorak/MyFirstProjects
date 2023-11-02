import random
import sqlite3

import requests

DATABASE_FILE = "./music.db"
artist_ids = []

genres = ['Rock', 'Pop', 'Hip-Hop/Rap', 'Country', 'Nu Metal', 'Arabic Pop', 'Jazz']
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


class Question:
    def __init__(self):
        self.answer_pool = ""
        self.correct_answer = ""
        self.key_data = ""
        self.result = 0
        self.artist = ""
        self.album = ""
        self.song = ""
        self.date = ""

    def get_line_from_db(self):
        con = connect_database()
        cur = con.cursor()
        cur.execute('SELECT * FROM songdata ORDER BY RANDOM() LIMIT 1')
        # res = cur.execute("SELECT * FROM songdata ORDER BY RANDOM() LIMIT 1")
        results = cur.fetchall()
        con.commit()
        con.close()
        # format result data
        for result in results:
            self.key_data = list(result)
        artist, album, song, date = self.key_data
        return artist, album, song, date

    def answers_input(self):
        answer = prompt_from_options(self.answer_pool)
        if answer == self.correct_answer:
            self.result = 1
            print(f"Answer {self.correct_answer} is correct.")
        else:
            print(f"Wrong, the correct answer is {self.correct_answer}.")
            self.result = 0
        return self.result


class Question1(Question):
    def __init__(self):
        super().__init__()
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
        return f"{self.correct_answer}\nWho is the artist of the song {self.song} on the album " \
               f"{self.album} from {self.date}?"


def main():
    selected_genre = introduction()
    with requests.Session() as sess:
        generate_data(sess, selected_genre)
    q1 = Question1()
    print(q1)
    q1.answers_input()
    # generate_questions()
    delete_db_table()


def connect_database():
    return sqlite3.connect(DATABASE_FILE)


def introduction():
    print("MUSIC QUIZ")
    print("Select genre:")
    return prompt_from_options(genres)


def prompt_from_options(options) -> str:
    for i, option in enumerate(options, 1):
        print(i, option)
    while True:
        try:
            choice = int(input("Enter a number and press <enter>: "))
            if choice in range(1, len(options) + 1):
                selection = options[(int(choice) - 1)]
                print(f"You selected {selection}")
                return selection
        except ValueError:
            print(f"Enter a number between 1 and {len(options)}")


def generate_data(sess: requests.Session, selected_genre):
    print("Gathering data...\n")
    selected_artists = artists_by_genre[selected_genre]
    for artist in selected_artists:
        response = sess.get("https://itunes.apple.com/search?entity=musicArtist&term=" + artist)
        response.raise_for_status()
        o = response.json()
        result = o["results"]
        artist_id = result[0]['artistId']
        artist_ids.append(artist_id)

    # send a request to itunes to return artist's songs
    for artist in artist_ids:
        str_artist = str(artist)
        response = sess.get("https://itunes.apple.com/lookup?id=" + str_artist + "&entity=song")
        response.raise_for_status()
        # print(json.dumps(response.json(), indent=2))

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
                # Check if any unwanted pattern is in album
                if not has_unwanted_pattern(album) and artist in selected_artists:
                    try:
                        con = connect_database()
                        cur = con.cursor()
                        cur.execute("CREATE TABLE IF NOT EXISTS songdata(artist TEXT, album TEXT, song TEXT, date INTEGER)")
                        # insert data into the database
                        cur.execute("INSERT INTO songdata VALUES(?, ?, ?, ?)",
                                    (artist, album, song, date))
                        con.commit()
                        con.close()
                    except Exception as e:
                        print(f"Error occurred: {e}")

            except KeyError:
                # skips result if it does not include date
                continue


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
        'expanded edition'
    ]
    return any(pattern in album.lower() for pattern in unwanted_patterns)


def delete_db_table():
    con = connect_database()
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS songdata")
    con.commit()
    con.close()


if __name__ == "__main__":
    main()
