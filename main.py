from llm_util import interact_with_local_api, extract_message_content
from math_equivalence import is_equiv
from util import last_boxed_only_string, remove_boxed
import unittest
import requests
import json

# Press the green button in the gutter to run the script.

train_prompt = "Given a mathematics problem, determine the answer. Simplify your answer as much as possible." + "\n" + "Problem: What is $\left(\\frac{7}{8}\\right)^3 \cdot \left(\\frac{7}{8}\\right)^{-3}$?" + "\n" + "Answer: $1$"
train_prompt += "\n" + "###" + "\n" + "Problem: In how many ways can 4 books be selected from a shelf of 6 books if the order in which the books are selected does not matter?" + "\n" + "Answer: $15$"
train_prompt += "\n" + "###" + "\n" + "Problem: Find the distance between the points $(2,1,-4)$ and $(5,8,-3).$" + "\n" + "Answer: $\sqrt{59}$"
train_prompt += "\n" + "###" + "\n" + "Problem: The faces of an octahedral die are labeled with digits $1$ through $8$. What is the probability, expressed as a common fraction, of rolling a sum of $15$ with a pair of such octahedral dice?" + "\n" + "Answer: $\\frac{1}{32}$"
train_prompt += "\n" + "###" + "\n" + "Problem: The first three terms of an arithmetic sequence are 1, 10 and 19, respectively. What is the value of the 21st term?" + "\n" + "Answer: $181$"
train_prompt += "\n" + "###" + "\n" + "Problem: Calculate $6 \\cdot 8\\frac{1}{3}" + "\n" + "Answer: $50$"
train_prompt += "\n" + "###" + "\n" + "Problem: When the binary number $100101110010_2$ is divided by 4, what is the remainder (give your answer in base 10)?" + "\n" + "Answer: $2$"
train_prompt += "\n" + "###" + "\n" + "Problem: How many zeros are at the end of the product 25 $\\times$ 240?" + "\n" + "Answer: $3$" + "\n" + "###"


def iscorrect(model_output, answer):
    cleaned_answer = remove_boxed(last_boxed_only_string(answer))
    print(cleaned_answer)
    return


if __name__ == '__main__':
    iscorrect("trr5542e3@", "42r1rre 12fg€€")

# Given your response
response = {
    'id': 'chatcmpl-qv1d7vbq5myrg2qpdo3f7',
    'object': 'chat.completion',
    'created': 1697819418,
    'model': 'C:\\Users\\User_1\\.cache\\lm-studio\\models\\TheBloke\\Llama-2-13B-GGUF\\llama-2-13b.Q4_0.gguf',
    'choices': [{
        'index': 0,
        'message': {'role': 'assistant', 'content': '```\nHello World!\n```\n\n'},
        'finish_reason': 'stop'
    }],
    'usage': {'prompt_tokens': 0, 'completion_tokens': 9, 'total_tokens': 9}
}

instruction = "### Instruction: Whats the meaning of life?\n###Response: "
response = interact_with_local_api(instruction)

message_content = extract_message_content(response)
print(message_content)