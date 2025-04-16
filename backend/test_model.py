import spacy

nlp = spacy.load("./output/model-best")

text = "Dear John Doe, welcome to Acme Corp. Your joining date is 10th April 2025."
doc = nlp(text)

print("Entities detected:")
for ent in doc.ents:
    print(f"{ent.text} → {ent.label_}")