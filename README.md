

# ⚔️ QuestMasterAI

**QuestMasterAI** is an AI-powered two-phase system designed to assist authors in creating interactive narrative experiences. By combining classical planning (PDDL) with modern generative AI (LLMs), the tool guides users from quest design to a playable, web-based adventure game.

---

## 📖 Project Overview

QuestMasterAI consists of two core phases:

### 🛠️ Phase 1 — Story Generation

#### 🎯 Objective
Assist the author in designing a logically consistent story world using a structured **Lore Document**, which gets translated into a valid **PDDL planning problem**.

#### 🧾 Input: Lore Document
- **Quest Description**: Adventure setup with initial state, goal, obstacles, and context.
- **Branching Factor**: Minimum and maximum number of choices at each point.
- **Depth Constraints**: Minimum and maximum steps to reach the goal.

#### 🔁 Workflow
1. **Generate PDDL** from the lore document.
2. **Validate** with Fast Downward to check for solvability.
3. If no valid plan is found:
   - An **LLM Reflection Agent** analyzes and revises the PDDL.
   - Suggests improvements to ensure logical consistency.
   - Updates the Lore file if necessary.

#### 📤 Output
- Validated `domain.pddl` and `problem.pddl` files.
- Updated `lore.json` with resolved inconsistencies.

---

### 🕹️ Phase 2 — Interactive Story Game

#### 🎯 Objective
Turn the logical structure of the quest into a web-based, playable story.

#### ⚙️ Workflow
- Use LLMs to generate an HTML-based story UI.
- Optionally generate images for each state.
- Users interact with dynamically generated buttons and scenes.
- Built using [Streamlit](https://streamlit.io) for quick and elegant deployment.

---

## 🚀 Getting Started

### ✅ Requirements
- Python 3.10+
- [WSL (Windows Subsystem for Linux)](https://learn.microsoft.com/en-us/windows/wsl/) enabled
- [Ollama](https://ollama.com) installed and running (for LLM interactions)
- `streamlit`, `langchain`, and related dependencies (see `requirements.txt`)

### 🧪 Run the Project

```bash
# Start WSL and make sure Ollama is running
ollama serve

# Phase 1: Generate PDDL from lore
python generate_pddl.py

# Optional: Generate narrative story based on PDDL
python generate_story.py

# Phase 2: Launch the interactive web app
python -m streamlit run app.py
````

---

## 📁 Project Structure

```
📦 QuestMasterAI/
├── app.py                  # Streamlit app
├── generate_pddl.py        # Converts lore to PDDL
├── generate_story.py       # Builds interactive story from PDDL
├── domain.pddl             # Output domain file
├── problem.pddl            # Output problem file
├── lore.json               # Lore document (input/output)
├── story.json              # Generated story data
├── README.md               # You're here!
```

---

## 🌟 Example Use Case

A user provides a simple lore:

> *"The hero must traverse a haunted forest, defeat a monster, and retrieve the Sword of Light from a castle."*

QuestMasterAI generates the planning model, refines it if necessary, and produces a browser-playable adventure where users choose their path and uncover the story.

---

## 🧠 Technologies

* 🧩 **PDDL (Planning Domain Definition Language)**
* 🤖 **LLMs (via Ollama)**
* 🛤️ **Fast Downward Planner**
* 🌐 **Streamlit Web Interface**
* 🔁 **LangChain** for prompt management

---

## 🧑‍💻 Authors

Developed by [martinagiacobbee](https://github.com/martinagiacobbee) for the *Artificial Intelligence* master's project.

---



---

