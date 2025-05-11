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

        // You can now send this username to the server to add the friend
        // Example:
        fetch('/add_friend', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: friendUsername })
        }).then(response => {
            if (response.ok) {
                alert("Friend added successfully!");
            } else {
                alert("Invalid friend");
            }
        });
    });
});
