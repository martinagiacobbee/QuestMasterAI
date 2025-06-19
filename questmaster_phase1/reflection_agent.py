import subprocess
import os
import json
from langchain_ollama import OllamaLLM
from dotenv import load_dotenv

# Carica le variabili dal file local.env
script_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(script_dir, 'local.env'))

def run(domain_path, problem_path, lore_path):
    for attempt in range(10):
        print(f"\n[🔁] Tentativo {attempt + 1}/10 - Reflection Agent avviato...\n")

        with open(domain_path, encoding="utf-8") as f:
            domain_pddl = f.read()

        with open(problem_path, encoding="utf-8") as f:
            problem_pddl = f.read()

        with open(lore_path, encoding="utf-8") as f:
            lore = json.load(f)

        llm = OllamaLLM(model="qwen2.5:3b")

        # === PHASE 1: Domain Generation ===
        print("🔍 Analisi e rigenerazione DOMAIN.PDDL...")
        domain_prompt = f"""
You are a critical reasoning AI for symbolic planning (PDDL).

### TASK
Given a failed planning attempt, analyze and regenerate a valid DOMAIN.PDDL based on the lore below.

First, briefly reflect on WHY the previous domain might have failed. Then build a corrected domain with the simplest possible valid STRIPS structure.

RULES:
- No unused types or predicates.
- Define only necessary actions with clear preconditions/effects.
- Match objects and logic to the lore.
- Output only the DOMAIN.PDDL, no explanations.

LORE (JSON):
{json.dumps(lore, indent=2)}

Original DOMAIN.PDDL:
{domain_pddl}

--- Output only the corrected DOMAIN.PDDL
"""
        domain_output = llm.invoke(domain_prompt)

        with open(domain_path, "w", encoding="utf-8") as f:
            f.write(domain_output.strip())
        print("[✅] Nuovo DOMAIN.PDDL salvato.")

        # === PHASE 2: Problem Generation ===
        print("🧩 Generazione coerente di PROBLEM.PDDL...")

        with open(domain_path, encoding="utf-8") as f:
            updated_domain = f.read()

        problem_prompt = f"""
You are a symbolic planner focused on STRIPS-style logic.

Using the domain below and the original lore, generate a coherent PROBLEM.PDDL file.

RULES:
- Include only relevant objects consistent with the domain.
- Initial state and goal must make logical sense and be achievable.
- Output only valid PDDL — no extra text.

DOMAIN.PDDL:
{updated_domain}

LORE:
{json.dumps(lore, indent=2)}

--- Output only the corrected PROBLEM.PDDL
"""
        problem_output = llm.invoke(problem_prompt)

        with open(problem_path, "w", encoding="utf-8") as f:
            f.write(problem_output.strip())
        print("[✅] Nuovo PROBLEM.PDDL salvato.")

        print("Do you want to modify the generated PDDL files? (y/n): ", end="")
        modify_choice = input().strip().lower()
        if modify_choice == "y":
            print("Please edit the files manually:")
            print(f"Domain: {domain_path}")
            print(f"Problem: {problem_path}")
            input("Press Enter when done...")   
        else:
            print("[✅] Skipping manual modification.")

        # === PHASE 3: Validation ===
        print("\n[🚀] Validazione con Fast Downward (via WSL)...")

        domain_wsl = os.getenv('WSL_DOMAIN_PATH')
        problem_wsl = os.getenv('WSL_PROBLEM_PATH')
        fd_path = os.getenv('WSL_DOWNWARD_PATH')

        if not domain_wsl or not problem_wsl or not fd_path:
            print("[⚠️] Variabili WSL non configurate correttamente.")
            break

        try:
            command_str = f'python3 "{fd_path}" "{domain_wsl}" "{problem_wsl}" --search "astar(blind())"'

            result = subprocess.run(
                [
                    "wsl",
                    "-d", "Ubuntu",
                    "bash", "-c", command_str
                ],
                capture_output=True,
                text=True
            )


            output = result.stdout + result.stderr
            if "Solution found" in output or "Plan found" in output:
                print("[🎉] Piano valido trovato con Fast Downward.")
                break
            else:
                print("[❌] Nessun piano ancora trovato.")
                print(output)
        except Exception as e:
            print("[⚠️] Errore nella validazione Fast Downward:", e)
            break
    else:
        print("\n[⛔] Limite massimo di 10 tentativi raggiunto. Nessun piano valido trovato.")
