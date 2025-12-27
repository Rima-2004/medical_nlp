from flask import Flask, request, jsonify, render_template
import spacy
import os

app = Flask(__name__)

nlp = None

def load_nlp():
    global nlp
    if nlp is None:
        nlp = spacy.load("en_ner_bc5cdr_md")
    return nlp


# UI Page
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


# Medical NER API
@app.route("/ner", methods=["POST"])
def medical_ner():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "Text field is required"}), 400

    text = data["text"]

    nlp_model = load_nlp()
    doc = nlp_model(text)

    entities = []
    for ent in doc.ents:
        entities.append({
            "text": ent.text,
            "label": ent.label_
        })

    return jsonify({
        "text": text,
        "entities": entities
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
