function countChars() {
  const text = document.getElementById("textInput").value;
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
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text: text }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Server error");
      }
      return response.json();
    })
    .then((data) => {
      const resultDiv = document.getElementById("result");
      resultDiv.innerHTML = "";

      if (!data.entities || data.entities.length === 0) {
        resultDiv.innerHTML = "<p>No medical entities found.</p>";
        return;
      }

      let html = "<h3>Extracted Medical Entities</h3><ul>";
      data.entities.forEach((ent) => {
        html += `<li><b>${ent.text}</b> — ${ent.label}</li>`;
      });
      html += "</ul>";

      resultDiv.innerHTML = html;
    })
    .catch((error) => {
      console.error("Fetch error:", error);
      alert("Error analyzing text.");
    });
}
