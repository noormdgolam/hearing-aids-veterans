document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');

    if (!searchInput || !searchResults) return;

    // Check if there's a query parameter
    const urlParams = new URLSearchParams(window.location.search);
    const query = urlParams.get('q');
    if (query) {
        searchInput.value = query;
        performSearch(query);
    }

    searchInput.addEventListener('input', function(e) {
        performSearch(e.target.value);
    });

    function performSearch(query) {
        query = query.toLowerCase().trim();
        searchResults.innerHTML = '';

        if (query.length < 2) {
            searchResults.innerHTML = '<p>Please enter at least 2 characters to search.</p>';
            return;
        }

        if (!window.searchIndex) {
            searchResults.innerHTML = '<p>Search index is loading...</p>';
            return;
        }

        const results = window.searchIndex.filter(item => {
            return item.content.toLowerCase().includes(query);
        });

        if (results.length === 0) {
            searchResults.innerHTML = '<p>No results found for "'+query+'".</p>';
            return;
        }

        results.forEach(item => {
            const div = document.createElement('div');
            div.className = 'search-result-item';
            div.innerHTML = `
                <h3><a href="${item.url}">${item.title}</a></h3>
                <p>${item.description}</p>
            `;
            searchResults.appendChild(div);
        });
    }
});
