# Group93  
## Agile Web Development project created by Group 93  
The purpose of this application is to record your ratings, etc of the movies that you have watched  
from a sample set of movies.  The sample set of movies information was pulled from the OMDB  
(Open movie database). Users can share their recorded movies with other users.  

## Agile Web Development Project (Group 93) – Team Member Information

| UWA ID   | Name           | GitHub Username |
|---------:|----------------|-----------------|
| 23334544 | Leo McGill     | leo-mcgill      |
| 21988007 | Dex June       | lebicahl        |
| 23673779 | Fubin Qiu      | WGDS            |
| 23994507 | Khai Ling Ang  | khailing        |

## Relevant licensing of data used from OMDB  
https://www.omdbapi.com/legal.htm    (Section 4.1 is relevant)  
https://www.omdbapi.com/    (OMDB Website)  

APA Referencing:  
OMDb API - The Open Movie Database. (2000). Omdbapi.com. https://www.omdbapi.com/  

## References of AI LLMs used
APA Referencing:
OpenAI. (2025). ChatGPT (May 15 version) [Large language model]. https://chat.openai.com/chat

## Instructions to run Flask application  
**1:** create a python virtual environment (Only need to do this once)  
**2:** activate your virtual environment  
**3:** upgrade pip to the latest version  
**4:** install requirements on your virtual environments  
**5:** initialise your local DB  
**6:** add .env file  
**7:** run the flask application  

**1:**  Create python virtual environment (Only need to do this once):  
$ python -m venv venv  

**2:** Activate your virtual environment:  
$ source venv/bin/activate # macOS/Linux  
$ .\venv\Scripts\Activate.ps1 # Windows  

If you encounter the following error on Windows:  
.\venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled on this system.  

Please run PowerShell as Administrator (press Win + X → choose Windows PowerShell (Admin)), and enter the following command:  
$ set-executionpolicy remotesigned  
Then type Y and press Enter to confirm.  

To verify if the change was successful, run:  
$ get-executionpolicy  
If the output is 'RemoteSigned', the policy has been updated successfully.  

**3.** Upgrade pip to the latest version:  
$ python.exe -m pip install --upgrade pip  

**4:** Install requirements on Venv (only need to do this once):  
$ pip install -r requirements.txt  

## DATABASE

There are scripts in /scripts to manage the database

**5:** Create the db using alembic (ORM):
using the python virtual environment:  
$ flask db upgrade  

### IMPORTANT  
Add sample_movies to db so that you can select and upload data about them:  
$ python scripts/add_sample_movies.py  

**5:** run the app:  
$ python app.py  

## ENV FILE  

**6:** create a .env file  
create a .env file in /app  
append to .env file:  
SECRET_KEY = "example_secret_key"  

append to .env file:  
DATABASE_URL=sqlite:///yourdb.sqlite3  

append to .env file:  
API_KEY=OMDB_API_KEY (This is used to pull movie details from OMDB.  
it is not required as we can add a test sample of movies from a json file in instruction 5.  

**7:** open your browser and go to:  
http://127.0.0.1:5000/  

---

To quit:  
ctrl + c in terminal  

Make sure to leave your virtual environment once you want to commit or pull/push:  
$ deactivate  

May need to cd into Group93 to activate venv depending on where you create it.s  

## Migrations  
### Create a migration using:  
flask db migrate  
### upgrade or downgrade the database:  
flask db upgrade  
flask db downgrade  

## Database Schema ##
---

### User Model

Represents a registered user of the website.

**Fields:**
- `id` — Unique identifier for each user.
- `username` — Unique login name.
- `password_hash` — Hashed password for secure login.
- `avatar_color` — User profile avatar color.
- `bio` — User profile bio.

**Relationships:**
- `user_movies` — The movies this user has added to their list (via the `UserMovie` table).
- `friends` — Other users this person has added as friends (see `Friendship` model below).

---

### Movie Model

Represents a movie retrieved from the OMDB API. Each movie is only stored **once**, regardless of how many users add it.

**Fields:**
- `id` — Unique ID for each movie.
- `title`
- `year`
- `rated`
- `released`
- `runtime`
- `genre`
- `director`
- `writer`
- `actors`
- `language`
- `country`
- `imdb_rating`
- `rt_rating`
- `metascore`
- `box_office`

> These fields represent metadata from the OMDB API.

**Relationships:**
- `user_movies` — Users who have added this movie, along with their personal ratings (via the `UserMovie` table).

---

### UserMovie Association Table

Represents a many-to-many relationship between `User` and `Movie`, with additional data.

**Fields:**
- `id` — Unique for each user-movie pair.
- `user_id` — The user who added the movie.
- `movie_id` — The movie that was added.
- `user_rating` — The rating the user gave this movie.

**Constraints:**
- The combination of `user_id` and `movie_id` is **unique** to prevent duplicate entries.

---

### Friendship Model

Represents one-way friendships — if User A adds User B, B doesn't need to accept or confirm.

**Fields:**
- `id` — Unique friendship record ID.
- `user_id` — The user who adds a friend.
- `friend_id` — The user who is added as a friend.

**Constraints:**
- The combination of `user_id` and `friend_id` is **unique**, so the same friend can't be added twice.

---


