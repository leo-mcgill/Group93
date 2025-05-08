export async function get_user_friends() {
    const response = await fetch("/get_friends", {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        },
    });

    if (!response.ok) {
        throw new Error("Failed to fetch friends");
    }

    const data = await response.json();
    return data
}
