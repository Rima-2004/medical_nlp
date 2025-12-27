# from flask import Flask, render_template, request
# import spacy

# # Load Medical NER Model
# nlp = spacy.load("en_ner_bc5cdr_md")

# app = Flask(__name__)

# @app.route("/", methods=["GET", "POST"])
# def index():
#     entities = []
#     text = ""

#     if request.method == "POST":
#         text = request.form.get("text")
#         doc = nlp(text)

#         for ent in doc.ents:
#             entities.append({
#                 "text": ent.text,
#                 "label": ent.label_
#             })

#     return render_template("index.html", text=text, entities=entities)

# if __name__ == "__main__":
#     app.run(debug=True)



from flask import Flask, request, jsonify
import spacy
import os

app = Flask(__name__)

# Global NLP object (lazy-loaded)
nlp = None


def load_nlp():
    """
    Load the spaCy model only once.
    Prevents Railway build/startup crashes.
    """
    global nlp
    if nlp is None:
        nlp = spacy.load("en_ner_bc5cdr_md")
    return nlp


@app.route("/", methods=["GET"])
def health_check():
    return jsonify({
        "status": "ok",
        "message": "Medical NLP API running successfully"
    })


@app.route("/ner", methods=["POST"])
def medical_ner():
    """
    Input:
    {
        "text": "Aspirin is used to treat headache."
    }

    Output:
    {
        "entities": [
            {"text": "Aspirin", "label": "CHEMICAL"},
            {"text": "headache", "label": "DISEASE"}
        ]
    }
    """
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
