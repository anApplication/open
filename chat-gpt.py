#!/bin/env python
# python chat-gpt.py "Translate the following English text to French: 'Hello, world!'"
import openai
import sys
import os
import time


def calculate_token_cost(openai_api_model, number_of_tokens):
    model_cost = {
        "text-ada-001": 0.0004,
        "text-babbage-001": 0.0005,
        "text-curie-001": 0.0004,
        "text-davinci-002": 0.0200,
        "text-davinci-003": 0.0200
    }
    return model_cost[openai_api_model] * (number_of_tokens / 10)

def run_openai_completion(prompt):

    dry_mode = os.getenv("OPENAI_DRY_MODE", "0")

    if dry_mode == "0":
        openai_api_key = os.getenv("OPENAI_API_KEY", "-")
        openai_timeout = os.getenv("OPENAI_TIMEOUT", "15")
        openai_organization = os.getenv("OPENAI_ORGANIZATION", "-")
        openai_api_model = os.getenv("OPENAI_API_MODEL","text-davinci-003")

        if openai_api_model not in ["text-davinci-003", "text-davinci-002", "text-curie-001", "text-babbage-001", "text-ada-001"]:
            openai_api_model = "text-davinci-003"


        openai.api_key = openai_api_key
        openai.timeout = openai_timeout
        openai.organization = openai_organization


        openai_temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.1"))
        openai_max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "200"))
        verbose_mode= os.getenv("OPENAI_VERBOSE", "0")
        start_time = time.time()

        # print(f"OPENAI_API_KEY:{openai.api_key}, OPENAI_ORGANIZATION:{openai.organization},  OPENAI_TIMEOUT:{openai.timeout}, Base URL:{openai.api_base}.")
        print(f"OPENAI_API_MODEL:{openai_api_model}, OPENAI_TEMPERATURE:{openai_temperature}, OPENAI_MAX_TOKENS:{openai_max_tokens}, OPENAI_DRY_MODE:{dry_mode}, OPENAI_VERBOSE:{verbose_mode}, prompt: {prompt}") 
        
        response = openai.Completion.create(
            model=openai_api_model,
            prompt=prompt,
            temperature=openai_temperature,
            max_tokens=openai_max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        end_time = time.time()
        # Calculate elapsed time
        elapsed_time = end_time - start_time

        # Print all attributes of the response object
        if verbose_mode == "1":
            print("Response Attributes:")
            for attribute in dir(response):
                if not attribute.startswith("_"):
                    value = getattr(response, attribute)
                    if value:
                        print(f"{attribute}: {value}")
        else:
            print(response.choices[0].text.strip())
            prompt_tokens=response['usage']['prompt_tokens']
            completion_tokens=response['usage']['completion_tokens']
            total_tokens = response['usage']['total_tokens']
            cost_cents=calculate_token_cost(openai_api_model, response['usage']['total_tokens'])
            print(f"Total tokens used: {total_tokens}({prompt_tokens}/{completion_tokens}), cost: {cost_cents:.5f} cents, elapsed:{elapsed_time:.2f} seconds.")
            
    else:
        print("DRY MODE")

def main():
    try:
        # Get the prompt from the command-line arguments
        prompt = sys.argv[1]
    except IndexError:
        print("Please provide prompt")
        sys.exit(1)

    run_openai_completion(prompt)

if __name__ == "__main__":
    main()
    

# Comparison tool: 
# https://gpttools.com/comparisontool


# $ OPENAI_DRY_MODE=0 OPENAI_VERBOSE=0 OPENAI_API_MODEL="text-ada-001" chat-gpt.py "В чем разница между Гераклом и Геркулесом?"
# OPENAI_API_MODEL:text-ada-001, OPENAI_TEMPERATURE:0.9, OPENAI_MAX_TOKENS:200, OPENAI_DRY_MODE:0, OPENAI_VERBOSE:0, prompt: В чем разница между Гераклом и Геркулесом?
# Гераклом составы ядра, Геркулес руки, Острова составы ядра, Гераклом тяжёлые руки, Геркулес тяжёлые руки, Острова тяжёлые руки, Гераклом тройный руки, Геркулес тройный руки, Остров тройный
# Total tokens used: 247(47/200), cost: 0.00988 cents, elapsed:1.71 seconds.

# $ OPENAI_DRY_MODE=0 OPENAI_VERBOSE=0 OPENAI_API_MODEL="" chat-gpt.py "В чем разница между Гераклом и Геркулесом?"
# OPENAI_API_MODEL:text-davinci-003, OPENAI_TEMPERATURE:0.9, OPENAI_MAX_TOKENS:200, OPENAI_DRY_MODE:0, OPENAI_VERBOSE:0, prompt: В чем разница между Гераклом и Геркулесом?
# Геракл и Геркулес являются двумя древними греческими героями. Геракл был протагонистом в рассказах о Троянской войне. Геракл был исключительно сильным и храбрым бойцом, который использ
# Total tokens used: 247(47/200), cost: 0.49400 cents, elapsed:13.73 seconds.

# $ OPENAI_DRY_MODE=0 OPENAI_VERBOSE=0 OPENAI_API_MODEL="" chat-gpt.py "В чем разница между Гераклом и Геркулесом? Дай короткий ответ"
# OPENAI_API_MODEL:text-davinci-003, OPENAI_TEMPERATURE:0.1, OPENAI_MAX_TOKENS:500, OPENAI_DRY_MODE:0, OPENAI_VERBOSE:0, prompt: В чем разница между Гераклом и Геркулесом? Дай короткий ответ
# Геракл - герой древнегреческой мифологии, Геркулес - герой римской мифологии.
# Total tokens used: 150(68/82), cost: 0.30000 cents, elapsed:4.35 seconds.

# $ OPENAI_TEMPERATURE="0.7" OPENAI_MAX_TOKENS=70 chat-gpt.py "Summarize this for a second-grade student: What is the difference between Hercules dnd Heracles?"
# OPENAI_API_MODEL:text-davinci-003, OPENAI_TEMPERATURE:0.7, OPENAI_MAX_TOKENS:70, OPENAI_DRY_MODE:0, OPENAI_VERBOSE:0, prompt: Summarize this for a second-grade student: What is the difference between Hercules dnd Heracles?
# Hercules and Heracles are two names for the same mythical Greek hero. He was known for his amazing strength and courage.
# Total tokens used: 50(22/28), cost: 0.10000 cents, elapsed:4.14 seconds.

# $ OPENAI_TEMPERATURE="0.1" OPENAI_MAX_TOKENS=70 chat-gpt.py "Summarize this for a second-grade student: What is the difference between Hercules dnd Heracles?"
# OPENAI_API_MODEL:text-davinci-003, OPENAI_TEMPERATURE:0.1, OPENAI_MAX_TOKENS:70, OPENAI_DRY_MODE:0, OPENAI_VERBOSE:0, prompt: Summarize this for a second-grade student: What is the difference between Hercules dnd Heracles?
# Hercules and Heracles are two names for the same hero from Greek mythology. Hercules is the name used in Roman stories, and Heracles is the name used in Greek stories.
# Total tokens used: 61(22/39), cost: 0.12200 cents, elapsed:2.04 seconds.

# $ OPENAI_TEMPERATURE="0.1" OPENAI_MAX_TOKENS=70 OPENAI_API_MODEL="text-davinci-002" chat-gpt.py "Summarize this for a second-grade student: What is the difference between Hercules dnd Heracles?"

# https://platform.openai.com/account/rate-limits

# https://openai.com/pricing
# Multiple models, each with different capabilities and price points. Prices are per 1,000 tokens. 
# You can think of tokens as pieces of words, where 1,000 tokens is about 750 words. This paragraph is 35 tokens.

# gpt-4
# Model         Prompt            | Completion
# 8K context    $0.03 / 1K tokens | $0.06 / 1K tokens
# 32K context   $0.06 / 1K tokens | $0.12 / 1K tokens


# Model endpoint compatibility
# Endpoint                  Model name
# /v1/chat/completions      gpt-4, gpt-4-0314, gpt-4-32k, gpt-4-32k-0314, gpt-3.5-turbo, gpt-3.5-turbo-0301
# /v1/completions           text-davinci-003, text-davinci-002, text-curie-001, text-babbage-001, text-ada-001
# /v1/edits                 text-davinci-edit-001, code-davinci-edit-001
# /v1/audio/transcriptions  whisper-1
# /v1/audio/translations    whisper-1
# /v1/fine-tunes            davinci, curie, babbage, ada
# /v1/embeddings            text-embedding-ada-002, text-search-ada-doc-001
# /v1/moderations           text-moderation-stable, text-moderation-latest


# https://platform.openai.com/docs/models/gpt-3-5
# Latest model	     | Max tokens	| Training data
# gpt-3.5-turbo	     | 4,096 tokens	| Up to Sep 2021
#   Most capable GPT-3.5 model and optimized for chat at 1/10th the cost of text-davinci-003. Will be updated with our latest model iteration.	
# gpt-3.5-turbo-0301 | 4,096 tokens | Up to Sep 2021
#   Snapshot of gpt-3.5-turbo from March 1st 2023. Unlike gpt-3.5-turbo, this model will not receive updates, and will be deprecated 3 months after a new version is released.	
# text-davinci-003   | 4,097 tokens	| Up to Jun 2021
#   Can do any language task with better quality, longer output, and consistent instruction-following than the curie, babbage, or ada models. Also supports inserting completions within text.
# text-davinci-002	| 4,097 tokens	| Up to Jun 2021
#   Similar capabilities to text-davinci-003 but trained with supervised fine-tuning instead of reinforcement learning	
# code-davinci-002 | 8,001 tokens	Up to Jun 2021
#   Optimized for code-completion tasks	


# https://platform.openai.com/docs/model-index-for-researchers
# Models referred to as "GPT 3.5"
# GPT-3.5 series is a series of models that was trained on a blend of text and code from before Q4 2021. The following models are in the GPT-3.5 series:
#    code-davinci-002 is a base model, so good for pure code-completion tasks
#    text-davinci-002 is an InstructGPT model based on code-davinci-002
#    text-davinci-003 is an improvement on text-davinci-002
#    gpt-3.5-turbo-0301 is an improvement on text-davinci-003, optimized for chat

# InstructGPT models
# We offer variants of InstructGPT models trained in 3 different ways:
# Training Method	
# SFT
# Supervised fine-tuning on human demonstrations	
# Models: davinci-instruct-beta1
# FeedME
# Supervised fine-tuning on human-written demonstrations and on model samples rated 7/7 by human labelers on an overall quality score	
# Models: text-davinci-001, text-davinci-002, text-curie-001, text-babbage-001
# PPO
# Reinforcement learning with reward models trained from comparisons by humans	
# Models: text-davinci-003
#
# The SFT and PPO models are trained similarly to the ones from the InstructGPT paper. 
# FeedME (short for "feedback made easy") models are trained by distilling the best completions from all of our models. 
# Our models generally used the best available datasets at the time of training, and so different engines using the same training methodology might be trained on different data.

# Models featured in OpenAI Research
# These are the most proximate models featured in our research papers that are available in the API today. 
# Please note that not all models available in the API correspond to a paper, and even for models that are listed below there may be subtle differences that do not allow for exact replication of the paper. 
# Paper	Published	Model Name in Paper	Model Name in API	Parameters2
# [2005.14165] Language Models are Few-Shot Learners	22 Jul 2020	GPT-3 175B	davinci	175B
# GPT-3 6.7B	curie	6.7B
# GPT-3 1B	babbage	1B
# [2107.03374] Evaluating Large Language Models Trained on Code	14 Jul 2021	Codex 12B	code-cushman-0013	12B
# [2201.10005] Text and Code Embeddings by Contrastive Pre-Training	14 Jan 2022	GPT-3 unsupervised cpt-text 175B	text-similarity-davinci-001	175B
# GPT-3 unsupervised cpt-text 6B	text-similarity-curie-001	6B
# GPT-3 unsupervised cpt-text 1.2B	No close matching model on API	1.2B
# [2009.01325] Learning to summarize from human feedback	15 Feb 2022	GPT-3 6.7B pretrain	No close matching model on API	6.7B
# GPT-3 2.7B pretrain	No close matching model on API	2.7B
# GPT-3 1.3B pretrain	No close matching model on API	1.3B
# [2203.02155] Training language models to follow instructions with human feedback	4 Mar 2022	InstructGPT-3 175B SFT	davinci-instruct-beta	175B
# InstructGPT-3 175B	No close matching model on API	175B
# InstructGPT-3 6B	No close matching model on API	6B
# InstructGPT-3 1.3B	No close matching model on API	1.3B