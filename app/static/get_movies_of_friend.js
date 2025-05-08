export async function get_movies_of_friend(friendUsername) {
    const response = await fetch(`/get_movies_friend?friend_username=${friendUsername}`, {
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
