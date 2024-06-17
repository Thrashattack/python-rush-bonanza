const token = sessionStorage.getItem("userToken");

function playGame() {
  window.location.href = "/in_game?token=" + token;
}

function transactions() {
  window.location.href = "/transactions?token=" + token;
}
