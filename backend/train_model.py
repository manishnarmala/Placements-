import spacy
from spacy.training.example import Example
import random
import json
import os

# Load training data
TRAIN_DATA = []
with open("train_data.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        entry = json.loads(line)
        TRAIN_DATA.append((entry["text"], {"entities": [tuple(ent) for ent in entry["entities"]]}))

# Create blank English model
nlp = spacy.blank("en")

# Add NER pipe
if "ner" not in nlp.pipe_names:
    ner = nlp.add_pipe("ner")
else:
    ner = nlp.get_pipe("ner")

# Add labels
for _, annotations in TRAIN_DATA:
    for ent in annotations["entities"]:
        ner.add_label(ent[2])

# Disable other pipes for training
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
with nlp.disable_pipes(*other_pipes):  
    optimizer = nlp.begin_training()
    
    for i in range(20):
        random.shuffle(TRAIN_DATA)
        losses = {}
        for text, annotations in TRAIN_DATA:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            nlp.update([example], drop=0.2, losses=losses)
        print(f"Iteration {i+1}, Losses: {losses}")

# Save the trained model
output_dir = "./output/model-best"
os.makedirs(output_dir, exist_ok=True)
nlp.to_disk(output_dir)
# Save the trained model
output_dir = "./output/model-best"
os.makedirs(output_dir, exist_ok=True)
nlp.to_disk(output_dir)
print(f"Model saved to {output_dir}")

# === Add this block to test ===
print("\nTesting the trained model:\n")
test_nlp = spacy.load(output_dir)
doc = test_nlp("Dear John Doe, welcome to Acme Corp. Your joining date is 10th April 2025.")
for ent in doc.ents:
    print(ent.text, ent.label_)

print(f"Model saved to {output_dir}")
