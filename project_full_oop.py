from initial_data import *
import requests
import sqlite3
import random


class Quiz:
    def __init__(self):
        self.score = 0
        self.selected_genre = ""
        self.selected_artists = ""
        self.response = ""
        self.o = ""
        self.result = ""
        self.artist_id = ""
        self.artist_ids = []
        self.str_artist = ""
        self.date = ""
        # vars to save in the database
        self.artist_name = ""
        self.collection_name = ""
        self.track_name = ""
        self.release_date = ""
        # filter out albums we don't want in db
        self.unwanted_albums = ""
        self.key_data = ""

    def introduction(self):
        print("Welcome to Michael's Brilliant Music Quiz!")
        print("Test your knowledge about your favourite genre.")
        print("Please select a genre from the following options:")
        for i, genre in enumerate(genres):
            print(i + 1, genre)

        # Get user's genre choice
        genre_choice = input("Enter the number of your chosen genre and press <enter>: ")
        self.selected_genre = genres[(int(genre_choice) - 1)]
        print(f"You selected {self.selected_genre}")
        print(f"Gathering data...\n")

    def generate_data(self):
        self.selected_artists = artists_by_genre[self.selected_genre]
        for artist in self.selected_artists:
            self.response = requests.get("https://itunes.apple.com/search?entity=musicArtist&term=" + artist)
            self.o = self.response.json()
            self.result = self.o["results"]
            self.artist_id = self.result[0]['artistId']
            self.artist_ids.append(self.artist_id)
        # send a request to itunes to return artist's songs
        for artist in self.artist_ids:
            self.str_artist = str(artist)
            self.response = requests.get("https://itunes.apple.com/lookup?id=" + self.str_artist + "&entity=song")
            # print(json.dumps(response.json(), indent=2))

            self.o = self.response.json()
            del self.o["results"][0]
            for result in self.o["results"]:
                try:
                    self.date = result["releaseDate"]
                    # vars to save in the database
                    self.artist_name = result["artistName"]
                    self.collection_name = result["collectionName"]
                    self.track_name = result["trackName"]
                    self.release_date = self.date[:4]
                    # filter out albums we don't want in db
                    self.unwanted_albums = ['special edition', 'deluxe edition', 'single', 'soundtrack',
                                            'motion picture', 'collection', 'remastered']
                    for album in self.unwanted_albums:
                        if album in self.collection_name.lower():
                            continue
                        else:
                            self.insert_into_db()
                except KeyError:
                    # skips result if it does not include releaseDate
                    continue

    def insert_into_db(self):
        # open database
        con = sqlite3.connect("music.db")
        cur = con.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS song_data(artist_name TEXT, collection_name TEXT, track_name TEXT, "
            "release_date INTEGER)")
        # insert data into the database
        cur.execute("INSERT INTO song_data VALUES(?, ?, ?, ?)",
                    (self.artist_name, self.collection_name, self.track_name, self.release_date))
        # SELECT ALL
        # res = cur.execute("SELECT * FROM song_data")
        # all_res = res.fetchall()
        # print(all_res)
        con.commit()
        con.close()

    def generate_questions(self):
        q1 = Question1()
        print(q1)
        self.result = q1.answers_input()
        self.update_score()

        q2 = Question2()
        print(q2)
        self.result = q2.answers_input()
        self.update_score()

        q3 = Question3()
        print(q3)
        self.result = q3.answers_input()
        self.update_score()

    @staticmethod
    def delete_db_table():
        con = sqlite3.connect("music.db")
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS song_data")
        con.commit()
        con.close()

    def update_score(self):
        self.score += self.result
        print(f"Score: {self.score}\n")

    # def get_score(self):
    #     return self.score


class Question:
    def __init__(self):
        self.answer_pool = ""
        self.correct_answer = ""
        self.key_data = ""
        self.result = 0

    # @staticmethod
    def get_line_from_db(self):
        # get data from database
        # open database
        con = sqlite3.connect("music.db")
        cur = con.cursor()
        cur.execute('SELECT * FROM song_data ORDER BY RANDOM() LIMIT 1')
        # res = cur.execute("SELECT * FROM song_data ORDER BY RANDOM() LIMIT 1")
        results = cur.fetchall()
        con.commit()
        # print(results)
        con.close()
        # format result data
        for result in results:
            self.key_data = list(result)
        artist_name, collection_name, track_name, release_date = self.key_data
        return artist_name, collection_name, track_name, release_date

    def answers_input(self):
        # print(self.correct_answer)
        for i in range(len(self.answer_pool)):
            print(f"{i + 1} {self.answer_pool[i]}")
        # user's input
        answer = input("Enter the number of your answer and press <enter>: ")
        # if user's input is correct, add a point
        if self.answer_pool[int(answer) - 1] == self.correct_answer:
            self.result = 1
            print(f"Answer {self.correct_answer} is correct.")
        else:
            print(f"Wrong, the correct answer is {self.correct_answer}.")
            self.result = 0
        return self.result


class Question1(Question):
    def __init__(self):
        super().__init__()
        self.artist_name, self.collection_name, self.track_name, self.release_date = super().get_line_from_db()
        # save the correct answer
        self.correct_answer = self.artist_name
        self.answer_pool = [self.correct_answer]
        # gather other options
        while len(self.answer_pool) < 4:
            self.artist_name2, self.collection_name2, self.track_name2, self.release_date2 \
                = super().get_line_from_db()
            # check for duplicate data
            if self.artist_name2 not in self.answer_pool:
                if self.artist_name2 != self.correct_answer:
                    self.answer_pool.append(self.artist_name2)
        # shuffle answers
        random.shuffle(self.answer_pool)

    def __str__(self):
        return f"{self.correct_answer}\nWho is the artist of the song {self.track_name} on the album " \
               f"{self.collection_name} from {self.release_date}?"


class Question2(Question):
    def __init__(self):
        super().__init__()
        self.artist_name, self.collection_name, self.track_name, self.release_date = super().get_line_from_db()
        # save the correct answer
        self.correct_answer = self.collection_name
        self.answer_pool = [self.correct_answer]
        # gather other options
        while len(self.answer_pool) < 4:
            self.artist_name2, self.collection_name2, self.track_name2, self.release_date2 \
                = super().get_line_from_db()
            # check for duplicate data
            if self.collection_name2 not in self.answer_pool:
                if self.collection_name2 != self.correct_answer:
                    self.answer_pool.append(self.collection_name2)
        # shuffle answers
        random.shuffle(self.answer_pool)

    def __str__(self):
        return f"{self.correct_answer}\nWhich album features the song {self.track_name} by {self.artist_name}?"


class Question3(Question):
    def __init__(self):
        super().__init__()
        self.artist_name, self.collection_name, self.track_name, self.release_date = super().get_line_from_db()
        # save the correct answer
        self.correct_answer = self.artist_name
        self.answer_pool = [self.correct_answer]
        # gather other options
        while len(self.answer_pool) < 4:
            self.artist_name2, self.collection_name2, self.track_name2, self.release_date2 \
                = super().get_line_from_db()
            # check for duplicate data
            if self.artist_name2 not in self.answer_pool:
                if self.artist_name2 != self.correct_answer:
                    self.answer_pool.append(self.artist_name2)
        # shuffle answers
        random.shuffle(self.answer_pool)

    def __str__(self):
        return f"{self.correct_answer}\nWho is the artist of the album {self.collection_name} from {self.release_date}?"


def main():
    quiz = Quiz()
    quiz.introduction()
    quiz.generate_data()
    quiz.generate_questions()

    # always include at the end
    quiz.delete_db_table()


if __name__ == "__main__":
    main()
