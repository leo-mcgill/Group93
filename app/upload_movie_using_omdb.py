#Group 93 CITS3403 Project 2025

# NOTE, This route is kept here because it is not used in production. This route uses the omdb key specified in .env file to add movies to the database. Since we have already collected test data in a JSON file, we are not currently using this code. It is also missing the required imports. If you want to use this route, then you have to copy it into routes.py.
### ROUTE TO MAKE THE OMDB REQUEST, AND STORE THE RESPONSE IN THE DB ###
@application.route('/upload_omdb_movie', methods=['POST'])
@login_required
def upload_omdb_movie():
    try:
        data = request.get_json()
        title = data.get('movie_title')
        user_rating = data.get('user_rating')
        
        # These lines of code add new movies to the database using the OMDB API Key.
        response = requests.get(f"https://www.omdbapi.com/?t={title}&apikey={Config.API_KEY}")
        movie_data = response.json()

        if movie_data.get("Response") == "False":
            return jsonify({"error": f"Movie: {title} not found"}), 404

        # Safely extract fields
        runtime_str = movie_data.get("Runtime", "0").replace(" min", "")
        runtime = safe_int(runtime_str, default=0)

        imdb_rating = safe_float(movie_data.get("imdbRating"))
        metascore = safe_int(movie_data.get("Metascore"))
        rt_rating = (
            movie_data.get("Ratings", [{}])[1].get("Value")
            if len(movie_data.get("Ratings", [])) > 1
            else None
        )
        
        
        movie = Movie.query.filter_by(
            title=movie_data.get("Title", "Unknown"),
            year=movie_data.get("Year")).first()
        
        
        if not movie:
            movie = Movie(
                title=movie_data.get("Title", "Unknown"),
                year=movie_data.get("Year"),
                rated=movie_data.get("Rated"),
                released=movie_data.get("Released"),
                runtime=movie_data.get("Runtime"),
                genre=movie_data.get("Genre"),
                director=movie_data.get("Director"),
                writer=movie_data.get("Writer"),
                actors=movie_data.get("Actors", "Unknown"),
                language=movie_data.get("Language"),
                country=movie_data.get("Country"),
                imdb_rating=movie_data.get("imdbRating"),
                rt_rating=rt_rating,
                metascore=movie_data.get("Metascore"),
                box_office=movie_data.get("BoxOffice"),
                poster_url=movie_data.get("Poster")
            )
            db.session.add(movie)
            db.session.commit()
            
        existing_link = UserMovie.query.filter_by(user_id=current_user.id, movie_id=existing.id).first()

        if existing_link:
            existing_link.user_rating = user_rating
            message = f"Movie: {title} rating updated!"
        else:
            # Change existing to movie when you want to add movies to db using OMDB API Key
            user_movie = UserMovie(user_id=current_user.id, movie_id=movie.id, user_rating=user_rating)
            db.session.add(user_movie)
            message = f"Movie: {title} added to your list!"
        
        
        db.session.commit()
        return jsonify({"message": message}), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Failed to store movie: {str(e)}"}), 500
