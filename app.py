from flask import Flask, render_template, request
import spacy

# Load Medical NER Model
nlp = spacy.load("en_ner_bc5cdr_md")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    entities = []
    text = ""

    if request.method == "POST":
        text = request.form.get("text")
        doc = nlp(text)

        for ent in doc.ents:
            entities.append({
                "text": ent.text,
                "label": ent.label_
            })

    return render_template("index.html", text=text, entities=entities)

if __name__ == "__main__":
    app.run(debug=True)
