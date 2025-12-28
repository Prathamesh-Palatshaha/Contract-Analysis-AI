import json
import os

CUAD_JSON = "CUAD_v1\CUAD_v1\CUAD_v1.json"
OUTPUT_JSONL = "cuad_instructions.jsonl"

def load_cuad(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)["data"]

def convert_to_instructions(cuad_data):
    samples = []

    for doc in cuad_data:
        context = doc["paragraphs"][0]["context"]

        for qa in doc["paragraphs"][0]["qas"]:
            instruction = qa["question"]
            input_text = context

            if qa["is_impossible"]:
                output = "The contract does not contain this clause."
            else:
                answers = [a["text"] for a in qa["answers"]]
                output = " ".join(set(answers))

            samples.append({
                "instruction": instruction,
                "input": input_text,
                "output": output
            })

    return samples

def save_jsonl(samples, path):
    with open(path, "w", encoding="utf-8") as f:
        for s in samples:
            f.write(json.dumps(s) + "\n")

if __name__ == "__main__":
    cuad_data = load_cuad(CUAD_JSON)
    instructions = convert_to_instructions(cuad_data)
    save_jsonl(instructions, OUTPUT_JSONL)

    print(f"Saved {len(instructions)} instruction samples")
