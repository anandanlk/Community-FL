import re
import os
import sys
import subprocess
import pandas as pd

def generate_metrics(logs) -> dict:
    rounds = []
    training_accuracies = []
    testing_accuracies = []
    model_sizes = []

    metrics = {
        "Round": rounds,
        "Training Accuracy": training_accuracies,
        "Testing Accuracy": testing_accuracies,
        "Model Size (MiB)": model_sizes,
    }

    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]') 
    logs = ansi_escape.sub('', logs)

    round_pattern = re.compile(r"INFO \[step decentralized_federated_learning_round_(\d+)\] completed success")
    train_acc_pattern = re.compile(r"Training accuracy: ([\d\.]+)")
    test_acc_pattern = re.compile(r"Testing accuracy: ([\d\.]+)")
    size_pattern = re.compile(r"INFO \[job receive_weights_\d+\] Max memory used: (\d+)MiB")
    time_pattern = re.compile(r"(\d+m\d+\.\d+s)")

    for match in round_pattern.finditer(logs):
        rounds.append(int(match.group(1)))
        
    for match in train_acc_pattern.finditer(logs):
        training_accuracies.append(float(match.group(1)))
    
    for match in test_acc_pattern.finditer(logs):
        testing_accuracies.append(float(match.group(1)))
    
    for match in size_pattern.finditer(logs):
        model_sizes.append(int(match.group(1)))

    total_time_matches = time_pattern.findall(logs)
    if total_time_matches:
        total_time = total_time_matches[0]
    else:
        total_time = None

    return total_time, metrics

def main(foldername):
    output_dir = os.path.join("Results", foldername)
    os.makedirs(output_dir, exist_ok=True)
    output_log_path = os.path.join(output_dir, "output.log")

    command = "{{ time cwltool --enable-ext --parallel decentralizedFL.cwl decentralized_input.yml; }} > {} 2>&1 2>> {}".format(output_log_path, output_log_path)
    subprocess.run(command, shell=True)

    with open(output_log_path, "r") as output_file:
        logs = output_file.read()

    total_time, metrics = generate_metrics(logs)
    print(f"Total_Time: {total_time}")

    df = pd.DataFrame(metrics)
    print(df)

    metrics_file_path = os.path.join(output_dir, "metrics.txt")
    with open(metrics_file_path, "w") as metrics_file:
        metrics_file.write(f"Total_Time: {total_time}\n")
        df.to_string(metrics_file, index=False)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python metrics.py <Results folder name>")
        sys.exit(1)

    foldername = sys.argv[1]
    main(foldername)