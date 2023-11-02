import random
import sqlite3

import requests

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


def get_random_songs(count: int, genre=None) -> list:
    with connect_database() as con:
        if genre:
            cur = con.execute(
                'SELECT artist, album, song, date FROM songdata WHERE genre=? ORDER BY RANDOM() LIMIT ?',
                (genre, count),
            )
        else:
            cur = con.execute(
                'SELECT artist, album, song, date FROM songdata ORDER BY RANDOM() LIMIT ?',
                (count,),
            )
        return list(cur.fetchall())


def ask_question(selected_genre: str) -> int:
    songs = get_random_songs(4, genre=selected_genre)
    correct = songs[0]
    random.shuffle(songs)
    correct_artist, correct_album, correct_song, correct_date = correct
    print(f"Who is the artist of the song {correct_song} on the album {correct_album} from {correct_date}?")
    artists = sorted(set(song[0] for song in songs))
    answer = prompt_from_options(artists)
    if answer == correct_artist:
        print(f"Answer {correct_artist} is correct.")
        return 1
    else:
        print(f"Wrong, the correct answer is {correct_artist}.")
        return 0


def main():
    selected_genre = introduction()
    with requests.Session() as sess:
        generate_data(sess, selected_genre)
    score = 0
    for x in range(5):
        score += ask_question(selected_genre)
    print(f"Your score is {score}/5")


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


def generate_data(sess: requests.Session, genre: str):
    print("Gathering data...\n")
    selected_artists = artists_by_genre[genre]
    artist_name_to_artist_id = dict(get_artist_ids(sess, selected_artists))

    # send a request to itunes to return artist's songs
    with connect_database() as con:
        con.execute("CREATE TABLE IF NOT EXISTS songdata(artist TEXT, album TEXT, song TEXT, date INTEGER, genre TEXT)")
        for artist_name, artist_id in artist_name_to_artist_id.items():
            res = con.execute("SELECT COUNT(*) FROM songdata WHERE artist=?", (artist_name,))
            count, = res.fetchone()
            if count > 0:
                print(f"Skipping {artist_name} because we already have {count} songs by them")
                continue
            response = sess.get(f"https://itunes.apple.com/lookup?id={artist_id}&entity=song")
            response.raise_for_status()
            # print(json.dumps(response.json(), indent=2))

            o = response.json()
            del o["results"][0]
            for result in o["results"]:
                date = result.get("releaseDate")
                if not date:
                    continue
                # vars to save in the database
                artist = result["artistName"]
                album = result["collectionName"]
                song = result["trackName"]
                date = date[:4]
                # Filter out albums we don't want in db
                # Check if any unwanted pattern is in album
                if not has_unwanted_pattern(album) and artist in selected_artists:
                    con.execute(
                        "INSERT INTO songdata VALUES(?, ?, ?, ?, ?)",
                        (artist, album, song, date, genre),
                    )
                    con.commit()


def get_artist_ids(sess, selected_artists):
    for artist in selected_artists:
        response = sess.get("https://itunes.apple.com/search?entity=musicArtist&term=" + artist)
        response.raise_for_status()
        o = response.json()
        result = o["results"]
        artist_id = result[0]['artistId']
        yield (artist, artist_id)


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



if __name__ == "__main__":
    main()
