import subprocess
import os, re
import json
from langchain_ollama import OllamaLLM
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), 'local.env'))

# Paths
base_dir = os.path.dirname(os.path.abspath(__file__))
lore_path = os.path.join(base_dir, "lore.json")
domain_path = os.path.join(base_dir, "domain.pddl")
problem_path = os.path.join(base_dir, "problem.pddl")
domain_path_example = os.path.join(base_dir, "../example_files/domain.pddl")
problem_path_example = os.path.join(base_dir, "../example_files/problem.pddl")
lore_example_path = os.path.join(base_dir, "../example_files/lore.json")

# Load example files
with open(domain_path_example, encoding="utf-8") as f:
    domain_example = f.read()
with open(problem_path_example, encoding="utf-8") as f:
    problem_example = f.read()

# Ask for lore
use_existing = input("📚 Do you want to use an existing lore.json? (y/n): ").strip().lower()
if use_existing == "y":
    if not os.path.exists(lore_path):
        print("[❌] lore.json not found. Please create one first.")
        exit()
    else:
        print("[✅] Using existing lore.json")
else:
    with open(lore_example_path, encoding="utf-8") as f:
        lore_example = json.load(f)

    print("🧙‍♂️ Let's create your custom adventure story!")
    hero = input("👤 Who is the hero of your story? ")
    goal = input("🎯 What must the hero achieve? ")
    obstacles = input("🧱 What are some obstacles in the hero's way? (comma-separated) ")
    setting = input("🌍 Describe the world or setting of your story: ")

    min_depth = 4
    max_depth = 6
    min_branch = 2
    max_branch = 3

    llm = OllamaLLM(model="qwen2.5:3b")
    lore_prompt = f"""
You are a reflective AI designed to construct structured fantasy quests for symbolic planning.

Inputs:
- Hero: {hero}
- Goal: {goal}
- Obstacles: {obstacles}
- Setting: {setting}
- Depth: min {min_depth}, max {max_depth}
- Branching: min {min_branch}, max {max_branch}

Use this format as a reference:
{json.dumps(lore_example, indent=2)}

Return a valid JSON object matching this structure. No comments or explanations.
"""
    print("🧠 Generating lore with LLM...")
    lore_response = llm.invoke(lore_prompt)

    try:
        match = re.search(r"\{[\s\S]+\}", lore_response)
        if match:
            lore_data = json.loads(match.group())
        else:
            raise ValueError("No valid JSON object found in LLM response.")

        with open(lore_path, "w", encoding="utf-8") as f:
            json.dump(lore_data, f, indent=2, ensure_ascii=False)
        print("[✅] Lore file saved as lore.json.")
    except Exception as e:
        print("[❌] Failed to parse/save lore JSON:", e)
        print("Raw LLM output:\n", lore_response)
        exit()

# Load lore
with open(lore_path, encoding="utf-8") as f:
    lore = json.load(f)

# === 1️⃣ Generate domain.pddl ===
llm = OllamaLLM(model="qwen2.5:3b")
domain_prompt = f"""
You are a PDDL domain generator.

Given the following structured lore for a symbolic planning task, create a valid PDDL domain file with clear types, predicates, and actions.

Use {domain_example} as a reference for structure and syntax.

Lore:
{json.dumps(lore, indent=2)}

Output only the full domain.pddl content. No explanations, no extra text.
"""
print("🛠️  Generating domain.pddl...")
domain_response = llm.invoke(domain_prompt)

with open(domain_path, "w", encoding="utf-8") as f:
    f.write(domain_response.strip())
print("[✅] domain.pddl saved.")

# === 2️⃣ Generate problem.pddl ===
problem_prompt = f"""
You are a PDDL problem generator.

Given the following:
1. A structured lore for a planning task.
2. The corresponding domain definition.

Create a valid problem.pddl that uses the domain and defines a reasonable initial state and goal based on the lore.

Lore:
{json.dumps(lore, indent=2)}

--- DOMAIN.PDDL:
{domain_response.strip()}

Use {problem_example} as a format reference.

Output only the full problem.pddl content. No extra text.
"""
print("🧩 Generating problem.pddl...")
problem_response = llm.invoke(problem_prompt)

with open(problem_path, "w", encoding="utf-8") as f:
    f.write(problem_response.strip())
print("[✅] problem.pddl saved.")

print("Do you want to modify the generated PDDL files? (y/n): ", end="")
modify_choice = input().strip().lower()
if modify_choice == "y":
    print("Please edit the files manually:")
    print(f"Domain: {domain_path}")
    print(f"Problem: {problem_path}")
    input("Press Enter when done...")   
else:
    print("[✅] Skipping manual modification.")

# === 3️⃣ Validate using Fast Downward ===
print("🧪 Running validation with Fast Downward via WSL...")

WSL_DOWNWARD_PATH = os.getenv('WSL_DOWNWARD_PATH')
WSL_DOMAIN_PATH = os.getenv('WSL_DOMAIN_PATH')
WSL_PROBLEM_PATH = os.getenv('WSL_PROBLEM_PATH')

command = [
    "wsl",
    "-d", "Ubuntu",
    "bash", "-c",
    f"python3 {os.getenv('WSL_DOWNWARD_PATH')} {os.getenv('WSL_DOMAIN_PATH')} {os.getenv('WSL_PROBLEM_PATH')} --search \"astar(blind())\""
]



try:
    result = subprocess.run(command, capture_output=True, text=True)
    output = result.stdout + result.stderr

    if "Solution found" in output or "Plan found" in output:
        print("[🎉] A valid plan was found.")
    else:
        print("[❌] No valid plan found. Launching the Reflection Agent...")
        import reflection_agent
        reflection_agent.run(domain_path, problem_path, lore_path)
except Exception as e:
    print(f"[⚠️] Error running Fast Downward from WSL: {e}")
