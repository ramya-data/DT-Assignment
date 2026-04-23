import json

def load_tree(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def ask_question(question):
    print("\n" + question["text"])
    for opt in question["options"]:
        print(f'{opt["id"]}) {opt["text"]}')
    
    while True:
        choice = input("Select option (A/B/C/D): ").strip().upper()
        if choice in [opt["id"] for opt in question["options"]]:
            return next(opt for opt in question["options"] if opt["id"] == choice)
        print("Invalid input. Try again.")

def run_agent(tree):
    state = {}
    answers = []

    print("\n--- Daily Reflection ---")

    for qid in tree["logic"]["sequence"]:
        question = next(q for q in tree["questions"] if q["id"] == qid)
        answer = ask_question(question)

        # store mapped value
        state[question["axis"]] = answer["maps_to"]

        # store raw answer for interpolation
        answers.append({
            "question": question["text"],
            "answer": answer["text"]
        })

    # build key
    key = f'{state["locus"]}_{state["orientation"]}_{state["radius"]}'
    outcome = tree["outcomes"][key]

    return state, answers, outcome

def generate_summary(state, answers, outcome):
    print("\n--- Reflection Summary ---\n")

    print("Your Responses:")
    for a in answers:
        print(f'- {a["answer"]}')

    print("\nYour Reflection Type:")
    print(f'{outcome["label"]}')

    print("\nInsight:")
    print(outcome["insight"])

    print("\nPrompt:")
    print(outcome["prompt"])

    print("\nState Breakdown:")
    for k, v in state.items():
        print(f'- {k}: {v}')

def main():
    tree = load_tree("tree.json")
    state, answers, outcome = run_agent(tree)
    generate_summary(state, answers, outcome)

if __name__ == "__main__":
    main()