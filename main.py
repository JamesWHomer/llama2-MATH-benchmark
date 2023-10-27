import os
import re

import numpy as np

from llm_util import interact_with_local_api, extract_message_content, prompt_chatllm
from math_equivalence import is_equiv
from util import last_boxed_only_string, remove_boxed
import unittest
import requests
import json

# Press the green button in the gutter to run the script.

example_prompt = "Given a mathematics problem, determine the answer. Simplify your answer as much as possible." + "\n" + "Problem: What is $\left(\\frac{7}{8}\\right)^3 \cdot \left(\\frac{7}{8}\\right)^{-3}$?" + "\n" + "Answer: $1$"
example_prompt += "\n" + "###" + "\n" + "Problem: In how many ways can 4 books be selected from a shelf of 6 books if the order in which the books are selected does not matter?" + "\n" + "Answer: $15$"
example_prompt += "\n" + "###" + "\n" + "Problem: Find the distance between the points $(2,1,-4)$ and $(5,8,-3).$" + "\n" + "Answer: $\sqrt{59}$"
example_prompt += "\n" + "###" + "\n" + "Problem: The faces of an octahedral die are labeled with digits $1$ through $8$. What is the probability, expressed as a common fraction, of rolling a sum of $15$ with a pair of such octahedral dice?" + "\n" + "Answer: $\\frac{1}{32}$"
example_prompt += "\n" + "###" + "\n" + "Problem: The first three terms of an arithmetic sequence are 1, 10 and 19, respectively. What is the value of the 21st term?" + "\n" + "Answer: $181$"
example_prompt += "\n" + "###" + "\n" + "Problem: Calculate $6 \\cdot 8\\frac{1}{3}" + "\n" + "Answer: $50$"
example_prompt += "\n" + "###" + "\n" + "Problem: When the binary number $100101110010_2$ is divided by 4, what is the remainder (give your answer in base 10)?" + "\n" + "Answer: $2$"
example_prompt += "\n" + "###" + "\n" + "Problem: How many zeros are at the end of the product 25 $\\times$ 240?" + "\n" + "Answer: $3$" + "\n" + "###"

rootdir = "MATH/test"

def run(max=-1):

    outputs = []
    answers = []
    types = []
    levels = []

    fnames_list = []

    cors = {}
    subject_cors = {}
    level_cors = {}
    correct = 0
    total = 1

    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            fnames_list.append(os.path.join(subdir, file))
            with open(os.path.join(subdir, file), 'r') as fp:
                try:
                    problem_data = json.load(fp)
                except Exception as e:
                    print(f"Error loading JSON from {file}", e)
                    raise e
                prob_level = problem_data["level"]
                prob_type = problem_data["type"]
                try:
                    prob_level = int(prob_level.split("Level ")[1])
                except:
                    prob_level = None
                problem = problem_data["problem"]
                solution = remove_boxed(last_boxed_only_string(problem_data["solution"]))

                response = call_engine(problem)

                answer_pattern = re.compile(r'\$([^$]+)\$')
                matches = answer_pattern.findall(response)
                if matches:
                    # If multiple matches are found, return the first one
                    response = matches[0]
                else:
                    response = "No answer found."

                print("Model output:")
                print(response)
                print("Correct answer:")
                print(solution)
                print("--------------------------------------------")

                try:
                    equiv = is_equiv(response, solution)
                except:
                    equiv = False
                if (prob_level, prob_type) in cors:
                    cors[(prob_level, prob_type)].append(equiv)
                else:
                    cors[(prob_level, prob_type)] = [equiv]
                if prob_level in level_cors:
                    level_cors[prob_level].append(equiv)
                else:
                    if prob_level is not None:
                        level_cors[prob_level] = [equiv]
                if prob_type in subject_cors:
                    subject_cors[prob_type].append(equiv)
                else:
                    if prob_type is not None:
                        subject_cors[prob_type] = [equiv]
                if equiv:
                    correct += 1
                total += 1

                print(str(correct) + "/" + str(total))

            if max > 0 and total >= max:
                break
        if max > 0 and total >= max:
            break

    with open("outputs_answers_llama2-13B_{}.txt".format("q4_0 TEST"), "w+") as f:
        for k, (output, answer, prob_type, prob_level, fname) in enumerate(
                zip(outputs, answers, types, levels, fnames_list)):
            f.write("{} TYPE: {} | LEVEL: {} | OUTPUT: {} | ANSWER: {} | FNAME: {}\n".format(k, prob_type, prob_level,
                                                                                             output, answer, fname))

        f.write("#####################\n")
        # also get accuracies for each
        for subject in ['Prealgebra', 'Algebra', 'Number Theory', 'Counting & Probability', 'Geometry',
                        'Intermediate Algebra', 'Precalculus']:
            for level in range(1, 6):
                key = (level, subject)
                if key not in cors.keys():
                    print("Skipping", key)
                    continue
                cors_list = cors[key]
                print("{} Level {} Accuracy = {}/{} = {:.3f}".format(subject, level, np.sum(cors_list), len(cors_list),
                                                                     np.mean(cors_list)))
                f.write(
                    "{} Level {} Accuracy = {}/{} = {:.3f}\n".format(subject, level, np.sum(cors_list), len(cors_list),
                                                                     np.mean(cors_list)))
        print("#####################")
        f.write("#####################\n")
        for level in sorted(level_cors):
            if level not in level_cors.keys():
                print("Skipping", level)
                continue
            cors_list = level_cors[level]
            print("Level {} Accuracy = {}/{} = {:.3f}".format(level, np.sum(cors_list), len(cors_list),
                                                              np.mean(cors_list)))
            f.write("Level {} Accuracy = {}/{} = {:.3f}\n".format(level, np.sum(cors_list), len(cors_list),
                                                                  np.mean(cors_list)))
        print("#####################")
        f.write("#####################\n")
        for subject in ['Prealgebra', 'Algebra', 'Number Theory', 'Counting & Probability', 'Geometry',
                        'Intermediate Algebra', 'Precalculus']:
            if subject not in subject_cors.keys():
                print("Skipping", subject)
                continue
            cors_list = subject_cors[subject]
            print("{} Accuracy = {}/{} = {:.3f}".format(subject, np.sum(cors_list), len(cors_list), np.mean(cors_list)))
            f.write(
                "{} Accuracy = {}/{} = {:.3f}\n".format(subject, np.sum(cors_list), len(cors_list), np.mean(cors_list)))
        print("#####################")
        f.write("#####################\n")
        print("Overall Accuracy = {}/{} = {:.3f}".format(correct, total, correct / total))
        f.write("Overall Accuracy = {}/{} = {:.3f}\n".format(correct, total, correct / total))


def call_engine(problem):
    test_question = "\nProblem: " + problem + "\n"
    prompt = example_prompt + test_question
    #print(prompt)
    response = interact_with_local_api(prompt, "\n###\nProblem:", 20, 0)
    return extract_message_content(response)


if __name__ == '__main__':
    # iscorrect("trr5542e3@", "42r1rre 12fg€€")
    #message_content = prompt_chatllm("What is 15 + 2?")
    #print(message_content)
    #response = call_engine("How many vertical asymptotes does the graph of $y=\\frac{2}{x^2+x-6}$ have?")
    #print(response)
    run(15000)
