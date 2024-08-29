const username = document.querySelector(".entered_username").innerHTML;

document.getElementById("github-link").href = `https://github.com/${username}`;
document.getElementById("github-link").innerText = `@${username}`;

document.getElementById("Username").addEventListener("submit", function () {
  document.getElementById("github-link").value = "";
});
document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("github-link").value = "";
});
