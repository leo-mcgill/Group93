export async function get_movie_details() {
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
    return data
}
