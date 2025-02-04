import argparse

def count_tokens(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return 0
    tokens = text.split()
    return len(tokens)

def main():
    parser = argparse.ArgumentParser(
        description="Generate a token score card for four files: o3_reasoning, o3_code, r1_reasoning, r1_code."
    )
    parser.add_argument("o3_reasoning", nargs="?", default="o3.txt",
                        help="Path to the o3 reasoning text file (default: o3.txt)")
    parser.add_argument("o3_code", nargs="?", default="tetris_o3.py",
                        help="Path to the o3 code file (default: tetris_o3.py)")
    parser.add_argument("r1_reasoning", nargs="?", default="r1.txt",
                        help="Path to the r1 reasoning text file (default: r1.txt)")
    parser.add_argument("r1_code", nargs="?", default="tetris_r1.py",
                        help="Path to the r1 code file (default: tetris_r1.py)")
    args = parser.parse_args()

    # Count tokens in each file.
    o3_reasoning_count = count_tokens(args.o3_reasoning)
    o3_code_count      = count_tokens(args.o3_code)
    r1_reasoning_count = count_tokens(args.r1_reasoning)
    r1_code_count      = count_tokens(args.r1_code)

    # Calculate totals for each group.
    total_o3 = o3_reasoning_count + o3_code_count
    total_r1 = r1_reasoning_count + r1_code_count

    # Print the score card.
    print("\nScore Card")
    print("==========")
    print(f"o3_reasoning: {o3_reasoning_count} tokens")
    print(f"o3_code:      {o3_code_count} tokens")
    print(f"Total tokens o3: {total_o3} tokens")
    print("----------")
    print(f"r1_reasoning: {r1_reasoning_count} tokens")
    print(f"r1_code:      {r1_code_count} tokens")
    print(f"Total tokens r1: {total_r1} tokens")
    print("==========\n")

if __name__ == "__main__":
    main()
