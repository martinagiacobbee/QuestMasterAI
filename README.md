

# 🧙‍♀️ QuestMasterAI

**QuestMasterAI** è un sistema modulare basato su tecniche di **intelligenza artificiale generativa** e **pianificazione automatica**, progettato per supportare la creazione di **narrazioni interattive** coerenti, ramificate e logicamente valide.

> Realizzato per il corso di *Intelligenza Artificiale* – A.A. 2024/2025  
> Gruppo: Anna Fratto, Francesca Mirabelli, Martina Giacobbe

---

## 🧩 Architettura del sistema

Il sistema è diviso in **due fasi principali**:

### 1. Generazione della Lore e del Piano PDDL
Utilizzando modelli LLM tramite LangChain e Ollama, il sistema genera:
- `lore.json`: contesto narrativo (eroe, obiettivo, ostacoli, etc.)
- `domain.pddl`: definizione del dominio PDDL
- `problem.pddl`: istanza del problema con stato iniziale e goal
- Validazione automatica con **Fast Downward**
- Correzione automatica iterativa con **Reflection Agent** in caso di errori

### 2. Creazione della Storia Interattiva
Lo script `generate_story.py` costruisce:
- `story.json`: macchina a stati finiti (FSM) che rappresenta la storia
- `app.py`: interfaccia web interattiva con **Streamlit**, dove l’utente può esplorare e giocare la storia.

---

## 🛠️ Tecnologie utilizzate

- **Python** – Linguaggio principale
- **Streamlit** – Interfaccia utente web interattiva
- **LangChain + Ollama** – Generazione LLM locale
- **PDDL** – Modello logico della storia
- **Fast Downward** – Planner simbolico per validazione
- **WSL (Ubuntu)** – Per eseguire strumenti Linux su Windows
- **JSON** – Gestione strutturata dei dati

---

## 🗂️ Struttura del progetto

```

questmaster\_phase1/
├── app.py
├── generate\_pddl.py
├── generate\_story.py
├── reflection\_agent.py
├── example\_files/       # Esempi di lore, PDDL e storie
├── hero\_adventure/      # Esempio completo 1
├── student\_adventure/   # Esempio completo 2
├── knight\_adventure/    # (altro esempio opzionale)
├── lore.json            # Generato/fornito
├── domain.pddl          # Generato
├── problem.pddl         # Generato
├── story.json           # Generato

````

---

## 🚀 Come eseguire il progetto

1. **Genera i file PDDL:**

```bash
python generate_pddl.py
````

2. **Crea la storia interattiva:**

```bash
python generate_story.py
```

3. **Avvia l'interfaccia web:**

```bash
streamlit run app.py
```

⚠️ Assicurati di avere:

* `Ollama` installato e configurato con un modello locale (es. LLaMA, Mistral)
* `Fast Downward` installato su WSL (Ubuntu)

---

## 📖 Esempi inclusi

* **Hero Adventure**: L’eroe deve trovare la Porta dell’Essenza e scoprire il Sussurro del Vento.
* **Student Adventure**: Uno studente affronta ostacoli per sostenere un esame cruciale.

Entrambi gli esempi includono lore, file PDDL, e visualizzazione come FSM.

---

## 🧠 Riflessioni

Il progetto dimostra il potenziale della **sinergia tra AI generativa e pianificazione simbolica**, aprendo la strada a nuovi strumenti per il game design, l’educazione e la creazione di contenuti narrativi interattivi.

---

## 📄 Licenza

Progetto accademico – Università della Calabria
Prof. Francesco Scarcello – Corso di Intelligenza Artificiale


