from flask import Flask, request, jsonify, render_template
import spacy
import os
import sys

app = Flask(__name__)

# 🔴 LOAD MODEL AT STARTUP (IMPORTANT)
try:
    print("Loading spaCy model...")
    nlp = spacy.load("en_ner_bc5cdr_md")
    print("spaCy model loaded successfully.")
except Exception as e:
    print("FAILED TO LOAD MODEL:", e)
    sys.exit(1)   # stop app if model fails


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/ner", methods=["POST"])
def medical_ner():
    try:
        data = request.get_json(force=True)

        if not data or "text" not in data:
            return jsonify({"error": "Text field is required"}), 400

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
