document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("movieForm");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const movieTitle = form.elements["movie_title"].value;
        const userRating = form.elements["user_rating"].value;

        try {
            const response = await fetch("/fetch_movie", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    movie_title: movieTitle,
                    user_rating: userRating
                })
            });

            const result = await response.json();
            const resultDiv = document.getElementById("movieResult");
            if (response.ok) {
                resultDiv.textContent = result.message;
                resultDiv.style.color = "lightgreen";
            } else {
                resultDiv.textContent = result.error || "Error occurred";
                resultDiv.style.color = "red";
            }
        } catch (error) {
            console.error("Error submitting movie:", error);
            document.getElementById("movieResult").textContent = "Request failed.";
        }
    });
});
