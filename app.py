from flask import Flask, request, jsonify, render_template
import spacy
import os

app = Flask(__name__)

nlp = None

def get_nlp():
    global nlp
    if nlp is None:
        print("Loading spaCy model...")
        nlp = spacy.load("en_ner_bc5cdr_md")
        print("Model loaded")
    return nlp


@app.route("/")
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

        doc = get_nlp()(text)

        entities = [
            {"text": ent.text, "label": ent.label_}
            for ent in doc.ents
        ]

        return jsonify({"entities": entities})

    except Exception as e:
        print("NER ERROR:", e)
        return jsonify({"error": "NER failed"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
