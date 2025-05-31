import json, re, ollama, os

base_dir = os.path.dirname(os.path.abspath(__file__))
lore_path = os.path.join(base_dir, "lore.json")
domain_path = os.path.join(base_dir, "domain.pddl")
problem_path = os.path.join(base_dir, "problem.pddl")
story_path = os.path.join(base_dir, "story_example.json")

# Carica la lore
with open(lore_path, encoding="utf-8") as f:
    lore = json.load(f)

# Carica i file PDDL
with open(domain_path, encoding="utf-8") as f:
    domain = f.read()

with open(problem_path,  encoding="utf-8") as f:
    problem = f.read()

with open(story_path, encoding="utf-8") as f:
    example_structure = json.load(f)

prompt = f"""Sei uno storyteller interattivo.
Dati questi file PDDL e questa lore, crea una rappresentazione JSON della storia come macchina a stati finiti (FSM). 

Lore: {json.dumps(lore, indent=2)}

DOMAIN.PDDL:
{domain}

PROBLEM.PDDL:
{problem}

Genera uno story.json con la seguente struttura e niente altro. Fai riferimento ad una struttura esempio rendendola più originale e dinamica:
STRUTTURA ESEMPIO:
{example_structure}
"""

response = ollama.chat(model="llama3", messages=[{"role":"user","content":prompt}])

json_text = re.search(r"\{[\s\S]*\}", response['message']['content']).group(0)
story = json.loads(json_text)

with open("story.json", "w") as f:
    json.dump(story, f, indent=2)

print("story.json generato.")
