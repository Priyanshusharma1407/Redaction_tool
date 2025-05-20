from redactor import redact_all
import json
import os

def evaluate(text, true_labels):
    redacted_text, log, _ = redact_all(text)
    pred_set = set((t.lower(), l) for l, t in log)
    true_set = set((item["text"].lower(), item["label"]) for item in true_labels)

    tp = len(pred_set & true_set)
    fp = len(pred_set - true_set)
    fn = len(true_set - pred_set)

    precision = tp / (tp + fp + 1e-8)
    recall = tp / (tp + fn + 1e-8)
    f1 = 2 * precision * recall / (precision + recall + 1e-8)

    return precision, recall, f1


def run_batch_eval(folder="eval_cases"):
    total_p = total_r = total_f1 = 0
    count = 0

    for file in os.listdir(folder):
        if file.endswith(".txt"):
            base = file[:-4]
            txt_path = os.path.join(folder, file)
            label_path = os.path.join(folder, base + "_labels.json")

            if not os.path.exists(label_path):
                print(f"⚠️ Missing label file for {base}")
                continue

            with open(txt_path, "r", encoding="utf-8") as f:
                text = f.read()
            with open(label_path, "r", encoding="utf-8") as f:
                labels = json.load(f)

            p, r, f1 = evaluate(text, labels)
            print(f"{base}: Precision={p:.2f} Recall={r:.2f} F1={f1:.2f}")
            total_p += p
            total_r += r
            total_f1 += f1
            count += 1

    if count > 0:
        print("\n🔍 Overall Avg: Precision={:.2f} Recall={:.2f} F1={:.2f}".format(
            total_p / count, total_r / count, total_f1 / count
        ))
    else:
        print("❌ No valid evaluation cases found.")


if __name__ == "__main__":
    run_batch_eval()
