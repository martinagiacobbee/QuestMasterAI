import subprocess
import os
import json
from langchain_ollama import OllamaLLM

def run(domain_path, problem_path, lore_path):
    for attempt in range(10):
        print(f"\n[🔁] Tentativo {attempt + 1}/10 - Reflection Agent avviato...\n")

        # 1. Carica i file esistenti
        with open(domain_path, encoding="utf-8") as f:
            domain_pddl = f.read()

        with open(problem_path, encoding="utf-8") as f:
            problem_pddl = f.read()

        with open(lore_path, encoding="utf-8") as f:
            lore = json.load(f)

        # 2. Prompt per LLM
        prompt = f"""
Sei un agente riflessivo che aiuta a correggere modelli PDDL. È stato generato il seguente dominio e problema, ma nessun piano valido è stato trovato.

Analizza i due file PDDL e suggerisci una versione corretta e coerente con la seguente Lore:

IMPORTANTE: Usa esattamente questo formato. Separa ogni blocco con '---' su una singola riga. Non inserire testo descrittivo.

LORE:
{json.dumps(lore, indent=2)}

--- DOMAIN.PDDL ORIGINALE:
{domain_pddl}

--- PROBLEM.PDDL ORIGINALE:
{problem_pddl}

Restituisci solo i nuovi file PDDL in questo formato:
1. Nuovo DOMAIN.PDDL
---
2. Nuovo PROBLEM.PDDL
---
(se necessario) 3. Nuova LORE aggiornata
        """

        llm = OllamaLLM(model="llama3")
        response = llm.invoke(prompt)

        # 3. Parsing output
        parts = [p.strip() for p in response.split("---") if p.strip()]
        if len(parts) < 2:
            print("[❌] Risposta del modello non valida. Attesi almeno DOMAIN e PROBLEM separati da '---'.")
            print("[🧾] Output ricevuto:\n", response)
            break

        new_domain = parts[0]
        new_problem = parts[1]
        new_lore = parts[2] if len(parts) > 2 else None

        # 4. Scrittura file aggiornati
        with open(domain_path, "w", encoding="utf-8") as f:
            f.write(new_domain)

        with open(problem_path, "w", encoding="utf-8") as f:
            f.write(new_problem)

        if new_lore:
            try:
                new_lore_json = json.loads(new_lore)
                with open(lore_path, "w", encoding="utf-8") as f:
                    json.dump(new_lore_json, f, indent=2)
                print("[📝] Lore aggiornata.")
            except json.JSONDecodeError:
                print("[⚠️] Lore aggiornata non valida JSON. Ignorata.")

        print("[✅] File PDDL rigenerati dal Reflection Agent.")

        # 5. Rivalidazione con Fast Downward via WSL
        print("\n[🚀] Validazione con Fast Downward (via WSL)...")

        domain_wsl = "/mnt/c/Users/marti/OneDrive/Desktop/Università/Magistrale/Primo\\ Anno/Intelligenza\\ Artificiale/Progetto/questmaster_phase1/questmaster_phase1/domain.pddl"
        problem_wsl = "/mnt/c/Users/marti/OneDrive/Desktop/Università/Magistrale/Primo\\ Anno/Intelligenza\\ Artificiale/Progetto/questmaster_phase1/questmaster_phase1/problem.pddl"

        try:
            result = subprocess.run(
                [
                    "wsl",
                    "python3",
                    "/home/utente/downward/fast-downward.py",
                    "--alias", "seq-sat-lama-2011",
                    domain_wsl,
                    problem_wsl
                ],
                capture_output=True,
                text=True
            )

            if "Solution found" in result.stdout:
                print("[✅] Piano valido trovato con Fast Downward.")
                break
            else:
                print("[❌] Nessun piano ancora trovato.")
                print(result.stdout)
        except Exception as e:
            print("[⚠️] Errore durante la validazione con Fast Downward:", e)
            break
    else:
        print("\n[⛔] Limite massimo di 10 tentativi raggiunto. Nessun piano valido trovato.")
