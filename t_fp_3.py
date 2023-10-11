import json
import requests
from initial_data import *
import sqlite3
import random

artist_ids = []
user_score = 0


def main():
    # select the genre
    selected_genre = introduction()
    print(f"You selected {selected_genre}.")
    print(f"Loading data...\n")
    # based on the genre we generate a list of artists' itunes ids to request more data
    generate_artist_ids(selected_genre)
    # use artists' ids to return data from itunes & save in a sqlite db
    generate_data(artist_ids)
    # # first question
    # score = generate_first_question(user_score)
    # print(f"Your score is {score}.\n")
    # # second question
    # score = generate_second_question(score)
    # print(f"Your score is {score}.\n")
    # # third question
    # score = generate_third_question(score)
    # print(f"Your score is {score}.\n")
    # # fourth question
    # score = generate_fourth_question(score)
    # print(f"Your score is {score}.\n")
    # # fifth question
    # score = generate_fifth_question(score)
    # print(f"Your score is {score}.\n")
    # # sixth question
    # score = generate_sixth_question(score)
    # print(f"Your score is {score}.\n")
    # # seventh question
    # score = generate_seventh_question(score)
    # print(f"Your score is {score}.\n")
    # eighth question
    # score = generate_eighth_question(score)
    score = generate_eighth_question(user_score)
    print(f"Your score is {score}.\n")
    # closing db & deleting the table with data
    delete_db_table()


# select the genre
def introduction():
    print("Welcome to Michael's Brilliant Music Quiz!")
    print("Test your knowledge about your favourite genre.")
    print("Please select a genre from the following options:")
    for i, genre in enumerate(genres):
        print(i + 1, genre)

    # Get user's genre choice
    genre_choice = input("Enter the number of your chosen genre and press <enter>: ")
    selected_genre = genres[(int(genre_choice) - 1)]
    return selected_genre


# based on the genre we generate a list of artists' itunes ids to request more data
def generate_artist_ids(genre):
    selected_artists = artists_by_genre[genre]
    for artist in selected_artists:
        response = requests.get("https://itunes.apple.com/search?entity=musicArtist&term=" + artist)
        o = response.json()
        result = o["results"]
        artist_id = result[0]['artistId']
        artist_ids.append(artist_id)
    return artist_ids


# use artists' ids to return data from itunes & save in a sqlite db
def generate_data(artist_ids):
    for artist in artist_ids:
        str_artist = str(artist)
        # response = requests.get("https://itunes.apple.com/lookup?id=" + str_artist + "&entity=song&limit=8")
        response = requests.get("https://itunes.apple.com/lookup?id=" + str_artist + "&entity=song")
        # print(json.dumps(response.json(), indent=2))

        # send a request to itunes to return artist's songs
        o = response.json()
        del o["results"][0]
        for result in o["results"]:
            try:
                date = result["releaseDate"]
                # vars to save in the database
                artist_id = result["artistId"]
                collection_id = result["collectionId"]
                track_id = result["trackId"]
                artist_name = result["artistName"]
                collection_name = result["collectionName"]
                track_name = result["trackName"]
                # releaseDate = result["releaseDate"]
                # date = result["releaseDate"]
                release_date = date[:4]
                insert_into_db(artist_id, collection_id, track_id, artist_name, collection_name, track_name,
                               release_date)
            except KeyError:
                # skips result if it does not include releaseDate
                continue


def insert_into_db(artist_id, collection_id, track_id, artist_name, collection_name, track_name, release_date):
    # open database
    con = sqlite3.connect("music.db")
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS songdata(artist_id INTEGER, collection_id INTEGER, track_id INTEGER, "
        "artist_name TEXT, collection_name TEXT, track_name TEXT, release_date INTEGER)")
    # insert data into the database
    cur.execute("INSERT INTO songdata VALUES(?, ?, ?, ?, ?, ?, ?)",
                (artist_id, collection_id, track_id, artist_name,
                 collection_name, track_name, release_date))
    # SELECT ALL
    # res = cur.execute("SELECT * FROM songdata")
    # all_res = res.fetchall()
    # print(all_res)
    con.commit()
    con.close()


def generate_first_question(user_score):
    artistId, collectionId, trackId, artistName, collectionName, trackName, releaseDate = select_data_for_question()
    # save correct answer
    correct_answer = artistName
    # gather the other options
    answer_pool = [correct_answer]
    while len(answer_pool) < 4:
        # open database
        con = sqlite3.connect("music.db")
        cur = con.cursor()
        cur.execute('SELECT * FROM songdata ORDER BY RANDOM() LIMIT 1')
        # res = cur.execute("SELECT * FROM songdata ORDER BY RANDOM() LIMIT 1")
        results = cur.fetchall()
        con.commit()
        # print(results)
        con.close()
        # format result data
        for result in results:
            key_data = list(result)
        artistId2, collectionId2, trackId2, artistName2, collectionName2, trackName2, releaseDate2 = key_data
        if artistName2 not in answer_pool:
            if artistName2 != correct_answer:
                answer_pool.append(artistName2)
    # shuffle answers
    random.shuffle(answer_pool)
    # print correct answer for testing
    print(correct_answer)
    # print question
    print(f"Who is the artist of the song {trackName} on the album {collectionName} from {releaseDate}?")
    # generate answers
    user_score = answers_and_outcome(answer_pool, correct_answer, user_score)
    return user_score


def generate_second_question(user_score):
    # get data from database
    artistId, collectionId, trackId, artistName, collectionName, trackName, releaseDate = select_data_for_question()
    # save correct answer
    correct_answer = collectionName
    # select wrong options / albums
    answer_pool = [correct_answer]
    while len(answer_pool) < 4:
        # open database
        con = sqlite3.connect("music.db")
        cur = con.cursor()
        cur.execute('SELECT * FROM songdata ORDER BY RANDOM() LIMIT 1')
        # res = cur.execute("SELECT * FROM songdata ORDER BY RANDOM() LIMIT 1")
        results = cur.fetchall()
        con.commit()
        # print(results)
        con.close()
        # format result data
        for result in results:
            key_data = list(result)
        artistId2, collectionId2, trackId2, artistName2, collectionName2, trackName2, releaseDate2 = key_data
        if collectionName2 not in answer_pool:
            if collectionName2 != correct_answer:
                answer_pool.append(collectionName2)
    # shuffle answers
    random.shuffle(answer_pool)
    # print correct answer for testing
    print(correct_answer)
    # print question
    print(f"Which album features the song {trackName} by {artistName}?")
    # generate answers
    user_score = answers_and_outcome(answer_pool, correct_answer, user_score)
    return user_score


def generate_third_question(user_score):
    # get data from database
    artistId, collectionId, trackId, artistName, collectionName, trackName, releaseDate = select_data_for_question()
    # save correct answer
    correct_answer = artistName
    # gather the other options
    answer_pool = [correct_answer]
    while len(answer_pool) < 4:
        # open database
        con = sqlite3.connect("music.db")
        cur = con.cursor()
        cur.execute('SELECT * FROM songdata ORDER BY RANDOM() LIMIT 1')
        # res = cur.execute("SELECT * FROM songdata ORDER BY RANDOM() LIMIT 1")
        results = cur.fetchall()
        con.commit()
        # print(results)
        con.close()
        # format result data
        for result in results:
            key_data = list(result)
        artistId2, collectionId2, trackId2, artistName2, collectionName2, trackName2, releaseDate2 = key_data
        if artistName2 not in answer_pool:
            if artistName2 != correct_answer:
                answer_pool.append(artistName2)
    # shuffle answers
    random.shuffle(answer_pool)
    # print correct answer for testing
    print(correct_answer)
    # print question
    # 3. Who is the artist of the album '[Album Name]'?"
    print(f"Who is the artist of the album {collectionName} from {releaseDate}?")
    # generate answers
    user_score = answers_and_outcome(answer_pool, correct_answer, user_score)
    return user_score


def generate_fourth_question(user_score):
    # get data from database
    artistId, collectionId, trackId, artistName, collectionName, trackName, releaseDate = select_data_for_question()
    # save correct answer
    correct_answer = releaseDate
    # gather the other options
    answer_pool = [correct_answer]
    while len(answer_pool) < 4:
        # open database
        con = sqlite3.connect("music.db")
        cur = con.cursor()
        cur.execute('SELECT * FROM songdata ORDER BY RANDOM() LIMIT 1')
        # res = cur.execute("SELECT * FROM songdata ORDER BY RANDOM() LIMIT 1")
        results = cur.fetchall()
        con.commit()
        # print(results)
        con.close()
        # format result data
        for result in results:
            key_data = list(result)
        artistId2, collectionId2, trackId2, artistName2, collectionName2, trackName2, releaseDate2 = key_data
        if releaseDate2 not in answer_pool:
            if releaseDate2 != correct_answer:
                answer_pool.append(releaseDate2)
    # shuffle answers
    random.shuffle(answer_pool)
    # print correct answer for testing
    print(correct_answer)
    # print question
    # 4. In which year was the album '[Album Name]' by [Artist Name] released?
    print(f"In which year was the album {collectionName} by {artistName} released?")
    # generate answers
    user_score = answers_and_outcome(answer_pool, correct_answer, user_score)
    return user_score


def generate_fifth_question(user_score):
    # get data from database
    artistId, collectionId, trackId, artistName, collectionName, trackName, releaseDate = select_data_for_question()
    # save correct answer
    correct_answer = releaseDate
    # gather the other options
    answer_pool = [correct_answer]
    while len(answer_pool) < 4:
        # open database
        con = sqlite3.connect("music.db")
        cur = con.cursor()
        cur.execute('SELECT * FROM songdata ORDER BY RANDOM() LIMIT 1')
        # res = cur.execute("SELECT * FROM songdata ORDER BY RANDOM() LIMIT 1")
        results = cur.fetchall()
        con.commit()
        # print(results)
        con.close()
        # format result data
        for result in results:
            key_data = list(result)
        artistId2, collectionId2, trackId2, artistName2, collectionName2, trackName2, releaseDate2 = key_data
        if releaseDate2 not in answer_pool:
            if releaseDate2 != correct_answer:
                answer_pool.append(releaseDate2)
    # shuffle answers
    random.shuffle(answer_pool)
    # print correct answer for testing
    print(correct_answer)
    # print question
    # 5. "In which year was the song '[Song Title]' by [Artist Name] released?"
    print(f"In which year was the song {trackName} by {artistName} released?")
    # generate answers
    user_score = answers_and_outcome(answer_pool, correct_answer, user_score)
    return user_score


def generate_sixth_question(user_score):
    # get data from database
    artistId, collectionId, trackId, artistName, collectionName, trackName, releaseDate = select_data_for_question()
    # save correct answer
    correct_answer = trackName
    # gather the other options
    answer_pool = [trackName]
    artist_pool = [artistName]
    while len(answer_pool) < 4:
        # open database
        con = sqlite3.connect("music.db")
        cur = con.cursor()
        cur.execute('SELECT * FROM songdata ORDER BY RANDOM() LIMIT 1')
        # res = cur.execute("SELECT * FROM songdata ORDER BY RANDOM() LIMIT 1")
        results = cur.fetchall()
        con.commit()
        # print(results)
        con.close()
        # format result data
        for result in results:
            key_data = list(result)
        artistId2, collectionId2, trackId2, artistName2, collectionName2, trackName2, releaseDate2 = key_data
        if artistName2 not in artist_pool:
            if trackName2 != correct_answer:
                artist_pool.append(artistName2)
                answer_pool.append(trackName2)
    # shuffle answers
    random.shuffle(answer_pool)
    # print correct answer for testing
    print(correct_answer)
    # print question
    # 6. Which song is by this artist:
    print(f"Which song is by {artistName}?")
    # generate answers
    user_score = answers_and_outcome(answer_pool, correct_answer, user_score)
    return user_score


def generate_seventh_question(user_score):
    # get data from database
    artistId, collectionId, trackId, artistName, collectionName, trackName, releaseDate = select_data_for_question()
    # save correct answer
    wrong_answer = trackName
    answer_pool = [wrong_answer]
    # now I need another two songs by the same artistName
    while len(answer_pool) < 3:
        # open database
        con = sqlite3.connect("music.db")
        cur = con.cursor()
        cur.execute('SELECT * FROM songdata ORDER BY RANDOM() LIMIT 1')
        # res = cur.execute("SELECT * FROM songdata ORDER BY RANDOM() LIMIT 1")
        results = cur.fetchall()
        con.commit()
        # print(results)
        con.close()
        # format result data
        for result in results:
            key_data = list(result)
        artistId2, collectionId2, trackId2, artistName2, collectionName2, trackName2, releaseDate2 = key_data
        if artistName2 == artistName:
            if trackName2 not in answer_pool:
                answer_pool.append(trackName2)
    # and one song by another artistName2
    # open database
    con = sqlite3.connect("music.db")
    cur = con.cursor()
    cur.execute('SELECT * FROM songdata ORDER BY RANDOM() LIMIT 1')
    # res = cur.execute("SELECT * FROM songdata ORDER BY RANDOM() LIMIT 1")
    results = cur.fetchall()
    con.commit()
    # print(results)
    con.close()
    # format result data
    for result in results:
        key_data = list(result)
    artistId2, collectionId2, trackId2, artistName2, collectionName2, trackName2, releaseDate2 = key_data
    if artistName2 != artistName:
        answer_pool.append(trackName2)
    correct_answer = trackName2
    # shuffle answers
    random.shuffle(answer_pool)
    # print correct answer for testing
    print(correct_answer)
    # print question
    # 7. Which song is not by this artist:
    print(f"Which song is NOT by {artistName}?")
    # generate answers
    user_score = answers_and_outcome(answer_pool, correct_answer, user_score)
    return user_score


def generate_eighth_question(user_score):
    # get data from database
    artistId, collectionId, trackId, artistName, collectionName, trackName, releaseDate = select_data_for_question()
    # and another - artistName2
    artistName2 = artistName
    while artistName2 == artistName:
        artistId2, collectionId2, trackId2, artistName2, collectionName2, trackName2, releaseDate2 = select_data_for_question()
    # correct answer
    if releaseDate < releaseDate2:
        correct_answer = collectionName
    elif releaseDate2 < releaseDate:
        correct_answer = collectionName2
    else:
        correct_answer = "Both were released in the same year."
    # answers
    answer_pool = [collectionName, collectionName2, "Both were released in the same year."]
    # shuffle answers
    random.shuffle(answer_pool)
    # print correct answer for testing
    print(releaseDate, releaseDate2)
    print(correct_answer)
    # print question
    # 8. "Which was released first: the album '[Album Name]' by [Artist Name] or the album '[Another Album]' by [Another Artist]?
    print(f"Which was released first: the album {collectionName} by {artistName} or the album {collectionName2} by {artistName2}?")
    # generate answers
    user_score = answers_and_outcome(answer_pool, correct_answer, user_score)
    return user_score


# 9. multiple songs from the same year, guess the year
# 10. which album is not by the following artist
#     Which of the following albums is not part of [Artist Name]'s discography?"


def select_data_for_question():
    # get data from database
    # open database
    con = sqlite3.connect("music.db")
    cur = con.cursor()
    cur.execute('SELECT * FROM songdata ORDER BY RANDOM() LIMIT 1')
    # res = cur.execute("SELECT * FROM songdata ORDER BY RANDOM() LIMIT 1")
    results = cur.fetchall()
    con.commit()
    # print(results)
    con.close()
    # format result data
    for result in results:
        key_data = list(result)
    artistId, collectionId, trackId, artistName, collectionName, trackName, releaseDate = key_data
    return artistId, collectionId, trackId, artistName, collectionName, trackName, releaseDate


def answers_and_outcome(answer_pool, correct_answer, user_score):
    for i in range(len(answer_pool)):
        print(f"{i + 1} {answer_pool[i]}")
    # print(f"1. {answer_pool[0]}")
    # print(f"2. {answer_pool[1]}")
    # print(f"3. {answer_pool[2]}")
    # print(f"4. {answer_pool[3]}")
    # user's input
    answer = input("Enter the number of your answer and press <enter>: ")
    # if user's input is correct, add a point
    if answer_pool[int(answer) - 1] == correct_answer:
        user_score += 1
        print(f"Answer {correct_answer} is correct.")
    else:
        print(f"Wrong, the correct answer is {correct_answer}.")
    return user_score


# don't forget to close the connection and drop all tables once the score is printed
def delete_db_table():
    con = sqlite3.connect("music.db")
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS songdata")
    con.commit()
    con.close()


if __name__ == "__main__":
    main()
