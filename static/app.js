const form = document.getElementById("searchbar");

form.addEventListener("submit", function (e) {
  e.preventDefault();

  const username = document.getElementById("Username").value;
  console.log(`Submitting username: ${username}`);

  fetch("/", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      "X-Requested-With": "XMLHttpRequest",
    },
    body: `username=${encodeURIComponent(username)}`,
  })
    .then((response) => response.text())
    .then((data) => {
      console.log(`Received data: ${data}`);
      document.querySelector(".stat-text h2").textContent = data;
    })
    .catch((error) => console.error("Error:", error));
});
