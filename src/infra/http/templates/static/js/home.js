function showForm(action) {
  const formContainer = document.getElementById("form-container");
  formContainer.style.display = "flex";
  formContainer.dataset.action = action;
}

async function submitForm() {
  const action = document.getElementById("form-container").dataset.action;
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const credentials = `${username}:${password}`;
  let encodedCredentials = window.btoa(credentials); // Encode to Base64
  const headers = new Headers();

  headers.append("Authorization", `Basic ${encodedCredentials}`);
  headers.append("Content-Type", "application/json");

  const response = await fetch(`/${action}`, {
    method: "GET",
    headers: headers,
  });

  const jsonResponse = await response.json();

  if (jsonResponse.error) {
    showAlert(jsonResponse.error + " Check Username and Password");
  } else {
    const token = jsonResponse.token;
    sessionStorage.setItem("userToken", token);
    window.location.href = "/menu?token=" + token;
  }
}

function showAlert(message) {
  if (!message) return;

  const alert = document.getElementById("alert");
  alert.textContent = message;
  alert.classList.add("show");
  setTimeout(() => {
    alert.classList.remove("show");
  }, 3000);
}
