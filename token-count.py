import argparse
import os

def count_tokens(file_path):
    """
    Counts the number of tokens in the given file.
    If the file is not found, prints a warning and returns 0.
    """
    if not os.path.isfile(file_path):
        print(f"Warning: {file_path} not found.")
        return 0
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return 0
    tokens = text.split()
    return len(tokens)

def generate_html_report(rows, output_file):
    """
    Generates an HTML report with the given table rows and writes it to output_file.
    """
    html_content = """<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Token Size Comparison Report</title>
  <style>
    table, th, td {
      border: 1px solid black;
      border-collapse: collapse;
      padding: 8px;
      text-align: center;
    }
    th {
      background-color: #f2f2f2;
    }
    body {
      font-family: Arial, sans-serif;
    }
    h1 {
      text-align: center;
    }
  </style>
</head>
<body>
  <h1>Token Size Comparison Report</h1>
  <table>
    <tr>
      <th>Experiment</th>
      <th>Model</th>
      <th>Reasoning Tokens</th>
      <th>Answer Tokens</th>
      <th>Total Tokens</th>
    </tr>
"""
    for row in rows:
        html_content += row + "\n"
    html_content += """
  </table>
</body>
</html>"""
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"HTML report generated: {output_file}")

def main():
    parser = argparse.ArgumentParser(
        description="Generate an HTML report comparing token sizes (reasoning.txt and answer.txt) across experiments."
    )
    parser.add_argument(
        "--base-dir", default=".", 
        help="Base directory of the project (default: current directory)"
    )
    parser.add_argument(
        "--output", default="token_report.html", 
        help="Output HTML report file (default: token_report.html)"
    )
    args = parser.parse_args()
    base_dir = args.base_dir

    # Define the experiments and their corresponding output folders.
    # Adjust these paths if your folder structure differs.
    experiments = {
        "Tetris Trial 1": {
            "openai-o3-mini": os.path.join("tetris", "trial1", "openai-o3-mini", "outputs"),
            "deepseek-r1": os.path.join("tetris", "trial1", "deepseek-r1", "outputs")
        },
        "Tetris Trial 2": {
            "openai-o3-mini": os.path.join("tetris", "trial2", "openai-o3-mini", "outputs"),
            "deepseek-r1": os.path.join("tetris", "trial2", "deepseek-r1", "outputs")
        },
        "Hangman": {
            "openai-o3-mini": os.path.join("hangman", "openai-o3-mini", "outputs"),
            "deepseek-r1": os.path.join("hangman", "deepseek-r1", "outputs")
        },
        "Magic Square": {
            "openai-o3-mini": os.path.join("magic-square","openai-o3-mini", "outputs"),
            "deepseek-r1": os.path.join("magic-square","deepseek-r1", "outputs")
        }
    }

    rows = []
    # Iterate over each experiment and model, count tokens, and create an HTML table row.
    for experiment, models in experiments.items():
        for model, rel_path in models.items():
            reasoning_path = os.path.join(base_dir, rel_path, "reasoning.txt")
            answer_path = os.path.join(base_dir, rel_path, "answer.txt")
            reasoning_count = count_tokens(reasoning_path)
            answer_count = count_tokens(answer_path)
            total_count = reasoning_count + answer_count
            row = (
                f"<tr>"
                f"<td>{experiment}</td>"
                f"<td>{model}</td>"
                f"<td>{reasoning_count}</td>"
                f"<td>{answer_count}</td>"
                f"<td>{total_count}</td>"
                f"</tr>"
            )
            rows.append(row)
    
    generate_html_report(rows, args.output)

if __name__ == "__main__":
    main()
