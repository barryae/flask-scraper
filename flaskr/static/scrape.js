const scrapeButton = document.getElementById("scrape-button")
const contentBox = document.getElementById("content")

const htmlFormat = document.getElementById("html-format")
const plainTextFormat = document.getElementById("plain-format")

const input = document.getElementById("input")

const loader = '<div class="loader"><div class="lds-default"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div></div>'

function loadPreviousSearch() {
    let previousSearch = localStorage.getItem('lastSearch')
    contentBox.innerHTML = previousSearch;
}


scrapeButton.addEventListener('click', (e) => {
    e.preventDefault()
    console.log('click')
    let query = input.value
    contentBox.innerHTML = loader
    if (plainTextFormat.checked) {
        fetch('/scrape?search=' + query + "&format=plain")
            .then(response => {
                return response.text()
            })
            .then(result => {
                localStorage.setItem('lastSearch', result)
                contentBox.innerHTML = result;
                // contentBox.append(result);
            })
    } else {
        fetch('/scrape?search=' + query + "&format=html")
            .then(response => {
                return response.text()
            })
            .then(result => {
                localStorage.setItem('lastSearch', result)
                contentBox.innerHTML = result;
                // contentBox.append(result);
            })
    }
})

loadPreviousSearch();