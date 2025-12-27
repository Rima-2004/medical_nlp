function countChars() {
  let text = document.getElementById("textInput").value;
  document.getElementById("charCount").innerText = text.length + " characters";
}

function clearText() {
  document.getElementById("textInput").value = "";
  document.getElementById("charCount").innerText = "0 characters";
  document.getElementById("result").innerHTML = "";
}

function analyzeText() {
  const text = document.getElementById("textInput").value;

  if (!text.trim()) {
    alert("Please enter some medical text.");
    return;
  }

  fetch("/ner", {
    method: "POST", // ✅ MUST be POST
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text: text }),
  })
    .then((response) => response.json())
    .then((data) => {
      const resultDiv = document.getElementById("result");
      resultDiv.innerHTML = "";

      if (!data.entities || data.entities.length === 0) {
        resultDiv.innerHTML = "<p>No medical entities found.</p>";
        return;
      }

      let list = "<ul>";
      data.entities.forEach((ent) => {
        list += `<li><b>${ent.text}</b> — ${ent.label}</li>`;
      });
      list += "</ul>";

      resultDiv.innerHTML = list;
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Error analyzing text.");
    });
}
