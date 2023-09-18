// Fetch and insert the header
fetch('components/header.html')
    .then((response) => response.text())
    .then((html) => {
        document.getElementById('header-container').innerHTML = html;
    });

// Fetch and insert the footer
fetch('components/footer.html')
    .then((response) => response.text())
    .then((html) => {
        document.getElementById('footer-container').innerHTML = html;
    });
