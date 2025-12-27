from flask import Flask, render_template, request
import spacy

app = Flask(__name__)

nlp = None

def load_model():
    global nlp
    if nlp is None:
        nlp = spacy.load("en_ner_bc5cdr_md")
    return nlp

@app.route("/", methods=["GET", "POST"])
def index():
    entities = []
    text = ""

    if request.method == "POST":
        text = request.form.get("text")
        doc = load_model()(text)
        for ent in doc.ents:
            entities.append({"text": ent.text, "label": ent.label_})

    return render_template("index.html", text=text, entities=entities)

if __name__ == "__main__":
    app.run()
