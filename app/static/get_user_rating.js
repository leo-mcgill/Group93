export async function get_user_rating() {
    const response = await fetch("/get_movies", {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        },
    });

    if (!response.ok) {
        throw new Error("Failed to fetch movies");
    }

    const data = await response.json();
    const resultDiv = document.getElementById("movie_list_container");
    return data
}
