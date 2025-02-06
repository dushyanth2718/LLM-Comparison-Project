# LLM Model Comparison Observations

## Objective

This exercise was designed to compare two prominent language models—**deepseek-r1** and **openai-o3-mini**—from a consumer perspective. Using fun and engaging examples such as Tetris (Trials 1 & 2), Hangman, and a Magic Square puzzle, our goal was to test the models’ reasoning abilities, cost efficiency, and basic code quality. The idea is to present these results in a way that everyday users can relate to, while also rigorously evaluating the models for tasks that require robust reasoning.

*This exercise was also showcased to a YouTube audience to highlight the performance differences. However, these observations, based on four experiments, do not tell the complete story. We encourage you to design similar experiments with a sufficiently large number of trials to better suit the specific use cases within your organization.*

## Evaluation Criteria

For each experiment, we measured the following metrics:
- **Reasoning Time:** Time taken by the model to generate its reasoning.
- **Pylint Score:** A basic code standard check using [Pylint](https://pylint.org/). (NA indicates the score was not applicable.)
- **Token Metrics:**  
  - **Reasoning Tokens:** Tokens used during the reasoning process.  
  - **Answer Tokens:** Tokens used in the final answer.  
  - **Total Tokens:** The sum of reasoning and answer tokens.  
  - **Input Tokens:** Tokens from the initial prompt.
- **Cost Metrics:**  
  - **Cost per 1M (Output/Input):** These are the cost per 1M tokens as per OpenAi and Deepseek website respectively.  
  - **Output Cost, Input Cost, Total Cost:** Derived cost estimates based on the token counts and the cost per 1M tokens.

Pylint was used to ensure that our evaluation scripts met a basic standard of code quality.


## Project Structure
```plaintext
LLM-Comparison-Project/
├── tetris/
│   ├── trial1/
│   │   ├── model1/
│   │   │   └── outputs/
│   │   │       ├── reasoning.txt
│   │   │       └── answer.txt
│   │   └── model2/
│   │       └── outputs/
│   │           ├── reasoning.txt
│   │           └── answer.txt
│   └── trial2/
│       ├── model1/
│       │   └── outputs/
│       │       ├── reasoning.txt
│       │       └── answer.txt
│       └── model2/
│           └── outputs/
│               ├── reasoning.txt
│               └── answer.txt
├── hangman/
│   ├── model1/
│   │   └── outputs/
│   │       ├── reasoning.txt
│   │       └── answer.txt
│   └── model2/
│       └── outputs/
│           ├── reasoning.txt
│           └── answer.txt
└── math_puzzle/
    └── outputs/
        ├── reasoning.txt
        └── answer.txt


## Results

| **Metric**              | **Tetris Trial 1 - deepseek-r1** | **Tetris Trial 1 - openai-o3-mini** | **Tetris Trial 2 - deepseek-r1** | **Tetris Trial 2 - openai-o3-mini** | **Hangman - deepseek-r1** | **Hangman - openai-o3-mini** | **Magic Square - deepseek-r1** | **Magic Square - openai-o3-mini** |
|-------------------------|----------------------------------|-------------------------------------|----------------------------------|-------------------------------------|---------------------------|------------------------------|---------------------------------|------------------------------------|
| **Reasoning Time**      | 512                              | 144                                 | 41                               | 143                                 | 233                       | 21                           | 250                             | 261                                |
| **Pylint Score**        | 5.86                             | 6.04                                | 4.83                             | 5.11                                | 10                        | 9.5                          | NA                              | NA                                 |
| **Reasoning Tokens**    | 5934                             | 771                                 | 638                              | 157                                 | 4007                      | 365                          | 4136                            | 1471                               |
| **Answer Tokens**       | 1051                             | 1412                                | 798                              | 1361                                | 664                       | 767                          | 209                             | 251                                |
| **Total Tokens**        | 6985                             | 2183                                | 1436                             | 1518                                | 4671                      | 1132                         | 4345                            | 1722                               |
| **Input Tokens**        | 13                               | 13                                  | 13                               | 13                                  | 86                        | 86                           | 237                             | 237                                |
| **Cost per 1M (Output)**| $2.19                            | $4.40                               | $2.19                            | $4.40                               | $2.19                     | $4.40                        | $2.19                           | $4.40                              |
| **Cost per 1M (Input)** | $0.14                            | $1.10                               | $0.14                            | $1.10                               | $0.14                     | $1.10                        | $0.14                           | $1.10                              |
| **Output Cost**         | $0.01530                         | $0.00961                            | $0.00314                         | $0.00668                            | $0.01023                  | $0.00498                     | $0.00952                        | $0.00758                           |
| **Input Cost**          | $0.00000                         | $0.00001                            | $0.00000                         | $0.00001                            | $0.00001                  | $0.00009                     | $0.00003                        | $0.00026                           |
| **Total Cost**          | $0.01530                         | $0.00962                            | $0.00315                         | $0.00669                            | $0.01024                  | $0.00508                     | $0.00955                        | $0.00784                           |

## Commentary

The observations reveal several interesting insights:

- **openai-o3-mini:**  
  OpenAI demonstrates outstanding reasoning capabilities; at the same time, its reasoning is concise, uses fewer tokens yet produces accurate results with better code standards.

- **deepseek-r1:**  
  Deepseek does good in reasoning but it takes far too many tokens to achieve the objective. Note that Deepseek has a max token limit of 8000K; for prompts requiring longer output, its reasoning needs to be further evaluated carefully as it might take more than one request to get the complete answer.

**Evaluation Criteria Recap:**  
The models were evaluated based on reasoning time, token usage (reasoning, answer, total, and input tokens), cost estimates, and code quality (via Pylint). These metrics provide a balanced view of performance, efficiency, and overall cost-effectiveness.

**Note:** Although the deepseek-r1 model is open source, the cost per million tokens across cloud providers for this model is roughly the same as the API pricing listed on the deepseek website. Therefore, we have used these rates to compute the total cost.
---
## Final Thoughts

While this exercise provides a snapshot of the performance of two competitive language models through engaging, real-world tasks, it represents only a fraction of the full story. We encourage you to design similar experiments—with a larger number of trials tailored to your specific applications—to arrive at more comprehensive and robust conclusions.

*Happy experimenting, and may these insights guide you to new perspectives in the ever-evolving world of language model innovation!*
