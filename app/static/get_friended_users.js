export async function get_friended_users() {
    const response = await fetch("/get_friended_users", {
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
