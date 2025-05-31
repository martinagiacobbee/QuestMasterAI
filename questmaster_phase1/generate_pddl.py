import subprocess
import os
import json
from langchain_ollama import OllamaLLM

# Percorsi
base_dir = os.path.dirname(os.path.abspath(__file__))
lore_path = os.path.join(base_dir, "lore.json")
domain_path = os.path.join(base_dir, "domain.pddl")
problem_path = os.path.join(base_dir, "problem.pddl")


# Caricamento lore
with open(lore_path, encoding="utf-8") as f:
    lore = json.load(f)

# Prompt per generazione PDDL
prompt = f"""
Sei un modellatore PDDL. Data questa descrizione di una quest, genera:
1. Un file DOMAIN.PDDL con predicati e azioni, ciascuna con commenti.
2. Un file PROBLEM.PDDL con lo stato iniziale e goal coerente con il dominio.

Lore:
{json.dumps(lore, indent=2)}

Scrivi prima il contenuto completo del domain.pddl, poi una linea '---', poi quello del problem.pddl. Commenta ogni riga significativa.
"""

llm = OllamaLLM(model="llama3")
response = llm.invoke(prompt)

# Estrazione
parts = response.split("---")
with open(domain_path, "w", encoding="utf-8") as f:
    f.write(parts[0].strip())

with open(problem_path, "w", encoding="utf-8") as f:
    f.write(parts[1].strip())

print("[✅] File PDDL generati. Ora procedo con la validazione tramite Fast Downward in WSL...")

# LANCIA fast-downward da WSL
WSL_DOWNWARD_PATH = "~/downward/fast-downward.py"
WSL_DOMAIN_PATH = "/mnt/c/Users/marti/OneDrive/Desktop/Università/Magistrale/Primo Anno/Intelligenza Artificiale/Progetto/questmaster_phase1/questmaster_phase1/domain.pddl"  
WSL_PROBLEM_PATH = "/mnt/c/Users/marti/OneDrive/Desktop/Università/Magistrale/Primo Anno/Intelligenza Artificiale/Progetto/questmaster_phase1/questmaster_phase1/problem.pddl" 

command = f"wsl python3 {WSL_DOWNWARD_PATH} {WSL_DOMAIN_PATH} {WSL_PROBLEM_PATH} --search \"astar(blind())\""

try:
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    output = result.stdout + result.stderr

    if "Solution found" in output or "Plan found" in output:
        print("[🎉] Piano valido trovato.")
    else:
        print("[❌] Nessun piano trovato. Avvio Reflection Agent...")
        import reflection_agent
        reflection_agent.run(domain_path, problem_path, lore_path)

except Exception as e:
    print(f"[⚠️] Errore durante l'esecuzione di Fast Downward da WSL: {e}")
