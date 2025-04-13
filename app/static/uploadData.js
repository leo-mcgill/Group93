document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");

    form.addEventListener("submit", async function (event) {
        event.preventDefault(); // Stop the form from submitting the traditional way

        const movieTitle = form.movie_title.value;
        const userRating = form.user_rating.value;

        if (!movieTitle || !userRating) {
            alert("Please enter both a movie title and a rating.");
            return;
        }

        try {
            const response = await fetch("/fetch_movie", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ title: movieTitle })
            });

            const data = await response.json();
            console.log("OMDB API Response:", data);

            if (data.Response === "False") {
                alert("Movie not found. Please check the title.");
            } else {
                alert(`Movie found: ${data.Title} (${data.Year})`);
                // You could also post to another Flask route to save this in the DB
                // Or render info dynamically on the page
            }
        } catch (error) {
            console.error("Error fetching movie data:", error);
            alert("There was an error contacting the server.");
        }
    });
});