//Group 93 CITS3403 Project 2025
//fetch request to get autofilled usernames
//also, POST request to submit a username to share with

document.addEventListener("DOMContentLoaded", function () {
    const loginInput = document.getElementById("login_username");
    const autocompleteResults = document.getElementById("autocomplete-results");

    loginInput.addEventListener("input", function() {
        const query = loginInput.value;

        if (query.length > 0) {
            fetch(`/search_users?q=${query}`)
                .then(response => response.json())
                .then(data => {
                    autocompleteResults.innerHTML = '';
                    data.forEach(username => {
                        const listItem = document.createElement('li');
                        listItem.textContent = username;
                        listItem.classList.add('autocomplete-item');
                        listItem.addEventListener('click', function() {
                            loginInput.value = username;
                            autocompleteResults.innerHTML = '';  // Clear the results
                        });
                        autocompleteResults.appendChild(listItem);
                    });
                });
        } else {
            autocompleteResults.innerHTML = '';  // Clear when input is empty
        }
    });

    // Optional: Submit the form and add friend to the user_friends table
    document.getElementById("shareForm").addEventListener("submit", function(event) {
        event.preventDefault();
        const friendUsername = loginInput.value;
    
        fetch('/share_with_user', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: friendUsername })
        })
        .then(response => response.json().then(data => ({ status: response.status, body: data })))
        .then(({ status, body }) => {
            if (status === 200) {
                // Create and append a new <h2> element
                const friendElement = document.createElement("h2");
                friendElement.classList.add("friend_element");
                friendElement.textContent = friendUsername;
    
                // Append to the about_container
                const container = document.querySelector(".about_container");
                container.appendChild(friendElement);
    
                // Reset input
                loginInput.value = '';
                autocompleteResults.innerHTML = '';
    
                alert(body.message);  // success message
            } else {
                alert(body.error || "Failed to add friend.");
            }
        })
        .catch(error => {
            console.error("Error adding friend:", error);
            alert("Something went wrong.");
        });
    });
});
