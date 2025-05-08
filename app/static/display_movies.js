export function display_movies(movies, movie_list) {
    // Display the movies of the selected friend
    for (let i = 0; i < movies.length; i++) {
        const movie_element = document.createElement('div');
        movie_element.classList.add('centered_div', 'row_direction', 'movie');

        const movie_image = document.createElement('img');
        movie_image.src = movies[i].poster_url;

        const movie_image_container = document.createElement('div');
        movie_image_container.classList.add('movie_image_container');
        movie_image_container.appendChild(movie_image);

        const movie_details_title = document.createElement('p');
        movie_details_title.classList.add('movie_section_font', 'white_font');
        movie_details_title.textContent = "Movie Details";

        const movie_title = document.createElement('p');
        movie_title.classList.add('movie_list_font', 'white_font');
        movie_title.textContent = "Title: " + movies[i].title;

        const movie_year = document.createElement('p');
        movie_year.classList.add('movie_list_font', 'white_font');
        movie_year.textContent = "Year: " + movies[i].year;

        const movie_rated = document.createElement('p');
        movie_rated.classList.add('movie_list_font', 'white_font');
        movie_rated.textContent = "Rated: " + movies[i].rated;

        const movie_released = document.createElement('p');
        movie_released.classList.add('movie_list_font', 'white_font');
        movie_released.textContent = "Released: " + movies[i].released;

        const movie_genre = document.createElement('p');
        movie_genre.classList.add('movie_list_font', 'white_font');
        movie_genre.textContent = "Genre: " + movies[i].genre;

        const movie_imdb_rating = document.createElement('p');
        movie_imdb_rating.classList.add('movie_list_font', 'white_font');
        movie_imdb_rating.textContent = "IMDB Rating: " + movies[i].imdb_rating;

        const movie_metascore = document.createElement('p');
        movie_metascore.classList.add('movie_list_font', 'white_font');
        movie_metascore.textContent = "Metascore: " + movies[i].metascore;

        const user_ratings_title = document.createElement('p');
        user_ratings_title.classList.add('movie_section_font', 'white_font');
        user_ratings_title.textContent = "Their Rating";

        const user_rating = document.createElement('p');
        user_rating.classList.add('movie_list_font', 'white_font');
        user_rating.textContent = "Rating: " + movies[i].user_rating;

        const movie_details_container = document.createElement('div');
        movie_details_container.classList.add('movie_container');
        movie_details_container.appendChild(movie_details_title);
        movie_details_container.appendChild(movie_title);
        movie_details_container.appendChild(movie_year);
        movie_details_container.appendChild(movie_rated);
        movie_details_container.appendChild(movie_released);
        movie_details_container.appendChild(movie_genre);
        movie_details_container.appendChild(movie_imdb_rating);
        movie_details_container.appendChild(movie_metascore);
        movie_details_container.appendChild(user_ratings_title);
        movie_details_container.appendChild(user_rating);

        movie_element.appendChild(movie_image_container);
        movie_element.appendChild(movie_details_container);

        movie_list.appendChild(movie_element);
    }
}
