from flask import Flask, request, jsonify, render_template
import spacy
import os

app = Flask(__name__)

# 🔹 Load LIGHT spaCy model (Render-safe)
print("Loading spaCy small model...")
nlp = spacy.load("en_core_web_sm")
print("spaCy model loaded successfully")


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/ner", methods=["POST"])
def medical_ner():
    try:
        data = request.get_json(force=True)

        if not data or "text" not in data:
            return jsonify({"entities": []})

        text = data["text"].strip()
        if not text:
            return jsonify({"entities": []})

        doc = nlp(text)

        entities = [
            {"text": ent.text, "label": ent.label_}
            for ent in doc.ents
        ]

        return jsonify({"entities": entities})

    except Exception as e:
        print("NER ERROR:", e)
        return jsonify({"error": "Error analyzing text"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
