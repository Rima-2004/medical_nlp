function countChars() {
  let text = document.getElementById("textInput").value;
  document.getElementById("charCount").innerText = text.length + " characters";
}

function clearText() {
  document.getElementById("textInput").value = "";
  document.getElementById("charCount").innerText = "0 characters";
}
