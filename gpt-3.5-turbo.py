#!/bin/env python
import openai
import argparse
import os
import time

def configure_openai():
    global model_cost_per_1k_tokens, openai_temperature, openai_api_model, openai_max_tokens
    
    openai_organization = os.getenv("OPENAI_ORGANIZATION", "--")
    openai_api_key = os.getenv("OPENAI_API_KEY", "--")
    openai_timeout = os.getenv("OPENAI_TIMEOUT", "20")

    openai_temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.1"))
    openai_api_model = os.getenv("OPENAI_API_MODEL","gpt-3.5-turbo")
    openai_max_tokens = os.getenv("OPENAI_MAX_TOKENS", 500)
    model_cost_per_1k_tokens = float(os.getenv("OPENAI_COST_PER_1K_TOKENS", "0.002"))
    
    openai.api_key = openai_api_key
    openai.timeout = openai_timeout
    openai.organization = openai_organization

    # print(f"OPENAI_ORGANIZATION:{openai_organization}, OPENAI_API_KEY:{openai_api_key}.")
    print(f"OPENAI_TEMPERATURE:{openai_temperature}, OPENAI_API_MODEL:{openai_api_model}, OPENAI_MAX_TOKENS:{openai_max_tokens}, OPENAI_COST_PER_1K_TOKENS:{model_cost_per_1k_tokens}, OPENAI_TIMEOUT:{openai_timeout}.")


def chat_with_gpt3(prompt):
    # Generate a response from the GPT-3.5 Turbo model
    start_time = time.time()
    response = openai.ChatCompletion.create(
        model=openai_api_model,
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": prompt}],
        max_tokens=openai_max_tokens,
        n=1,
        stop=None,
        temperature=openai_temperature
    )
    end_time = time.time()
    # Calculate elapsed time
    elapsed_time = end_time - start_time

    # Extract the generated message from the response
    message = response['choices'][0]['message']['content'].strip()

    # Calculate the cost in cents
    total_tokens = response['usage']['total_tokens']
    cost_cents = total_tokens * model_cost_per_1k_tokens / 10 # per cents, for dollars it would be / 1000 

    print(f"Total tokens used: {total_tokens}, cost of this chat: {cost_cents:.5f} cents, the call to took {elapsed_time:.2f} seconds.")

    return message

def main():
    # Create command-line arguments
    parser = argparse.ArgumentParser(description='Chat with GPT-3.5 Turbo')
    parser.add_argument('prompt', type=str, help='The conversation prompt')

    # Parse command-line arguments
    args = parser.parse_args()

    configure_openai()
    
    # Chat with GPT-3.5 Turbo
    response = chat_with_gpt3(args.prompt)
    print(response)

if __name__ == '__main__':
    main()
    
    
# Note that when using the Chat API, you send a list of messages instead of a single prompt. 
# Each message has a 'role' which can be 'system', 'user', or 'assistant', and 'content' which is the text of the message from that role. 
# Typically, a conversation starts with a 'system' message, followed by alternating 'user' and 'assistant' messages. 
# In this case, I've started the conversation with a system message, followed by a user message that contains your prompt.


#    n=1: This parameter specifies the number of generated responses to the given prompt. In this case, you're asking the model to generate one response.
#    stop=None: This parameter is used to specify a set of sequences where the API will stop generating further tokens. 
#         If it is set to None, the API will continue generating tokens up to the max_tokens limit.
#    temperature=0.7: This parameter controls the randomness of the model's output. 
#         A temperature closer to 0 makes the output more focused and deterministic, while a higher temperature value (closer to 1) makes the output more diverse and unpredictable.


# When using the OpenAI chat models, there are typically three roles you can use: "system", "user", and "assistant". 
# These roles are used to guide the model's behavior during the conversation. Here's what each role typically means:
# 
#     "system": This role is usually used to set up the behavior of the assistant at the beginning of the conversation. 
#           For example, "You are a helpful assistant." instructs the model to behave like a helpful assistant. 
#           This message is generally only used once at the start of the conversation, but it can be used again later to change the behavior of the assistant.
# 
#     "user": This role represents the human user in the conversation. The content of a "user" message is usually a question, instruction, or statement that the assistant will respond to.
# 
#     "assistant": This role represents the AI model itself. In an ongoing conversation, "assistant" messages are the model's previous responses.
# 
# The "content" field for each message is the actual text of the message from that role. For a "system" message, it's typically a brief instruction guiding the behavior of the assistant. 
#   For a "user" message, it's the user's input that the assistant will respond to. For an "assistant" message, it's the model's previous responses.
# 
# When starting a conversation with the ChatCompletion.create method, you typically pass an array of messages to set up the conversation. 
# Each message is a dictionary with "role" and "content" fields. The messages are processed in the order they appear in the array, and the model generates a response to the final message.
# 
# Here's an example of a conversation with more roles and messages:
# 
# python
# 
# response = openai.ChatCompletion.create(
#     model='gpt-3.5-turbo',
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "Who won the world series in 2020?"},
#         {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
#         {"role": "user", "content": "Where was it played?"}
#     ],
#     max_tokens=100,
# )
# 
# In this example, the assistant's response to the question "Who won the world series in 2020?" is included in the messages. 
# The model will generate a response to the final question "Where was it played?" based on all the previous messages.

# $ OPENAI_TEMPERATURE=0.01 gpt-3.5-turbo.py "Who was Hercules? What did he do? Is ge god?"
# OPENAI_ORGANIZATION:org-hDkGirIJ0yFUxPWjNLXpLKRx, OPENAI_API_KEY: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, OPENAI_TIMEOUT:10.
# OPENAI_TEMPERATURE:0.01, OPENAI_API_MODEL:gpt-3.5-turbo, OPENAI_MAX_TOKENS:500, OPENAI_COST_PER_1K_TOKENS:0.002.
# Total tokens used: 214, cost of this chat: 0.04280 cents, the call to took 16.34 seconds.
# Hercules, also known as Heracles in Greek mythology, was a legendary hero and demigod. He was the son of Zeus, the king of the gods, and a mortal woman named Alcmene.
# Hercules was known for his incredible strength and courage. He performed many great feats, including slaying the Nemean Lion, capturing the Erymanthian Boar, and cleaning the Augean Stables in a single day. He also completed twelve labors assigned to him by King Eurystheus, which included tasks such as capturing the Golden Hind and bringing back the three-headed dog Cerberus from the underworld.
# While Hercules was not a god, he was considered a demigod because of his divine parentage. He was worshipped as a hero and protector, and his legend has been passed down through the ages as a symbol of strength and perseverance.

# $ OPENAI_TEMPERATURE=0.9 gpt-3.5-turbo.py "Who was Hercules? What did he do? Is ge god?"
# OPENAI_ORGANIZATION:org-hDkGirIJ0yFUxPWjNLXpLKRx, OPENAI_API_KEY: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, OPENAI_TIMEOUT:10.
# OPENAI_TEMPERATURE:0.9, OPENAI_API_MODEL:gpt-3.5-turbo, OPENAI_MAX_TOKENS:500, OPENAI_COST_PER_1K_TOKENS:0.002.
# Total tokens used: 115, cost of this chat: 0.02300 cents, the call to took 8.46 seconds.
# Hercules was a hero in Greek mythology. He was known for his incredible strength and his many legendary feats, such as slaying the Nemean lion, completing the 12 Labors assigned to him by King Eurystheus, and ascending to godhood after his death. While he was not considered a god, he was the son of Zeus, the king of the gods, and a mortal woman.

# $ OPENAI_TEMPERATURE=0.01 gpt-3.5-turbo.py "Who was Hercules? What did he do? Is ge god?"
# OPENAI_TEMPERATURE:0.01, OPENAI_API_MODEL:gpt-3.5-turbo, OPENAI_MAX_TOKENS:500, OPENAI_COST_PER_1K_TOKENS:0.002, OPENAI_TIMEOUT:20.
# Total tokens used: 214, cost of this chat: 0.04280 cents, the call to took 16.93 seconds.
# Hercules, also known as Heracles in Greek mythology, was a legendary hero and demigod. He was the son of Zeus, the king of the gods, and a mortal woman named Alcmene.
# Hercules was known for his incredible strength and courage. He performed many great feats, including slaying the Nemean Lion, capturing the Erymanthian Boar, and cleaning the Augean Stables in a single day. He also completed twelve labors assigned to him by King Eurystheus, which included tasks such as capturing the Golden Hind and bringing back the three-headed dog Cerberus from the underworld.
# While Hercules was not a god, he was considered a demigod because of his divine parentage. He was worshipped as a hero and protector, and his legend has been passed down through the ages as a symbol of strength and bravery.


# $ OPENAI_TEMPERATURE=0.01 gpt-3.5-turbo.py "Кто победил медузу Гаргону? Answer in English please."
# OPENAI_TEMPERATURE:0.01, OPENAI_API_MODEL:gpt-3.5-turbo, OPENAI_MAX_TOKENS:500, OPENAI_COST_PER_1K_TOKENS:0.002, OPENAI_TIMEOUT:20.
# Total tokens used: 52, cost of this chat: 0.01040 cents, the call to took 1.89 seconds.
# Perseus defeated the Gorgon Medusa.


# $ OPENAI_TEMPERATURE=0.01 gpt-3.5-turbo.py "What is the difference between Perseus and Hercules?"
# OPENAI_TEMPERATURE:0.01, OPENAI_API_MODEL:gpt-3.5-turbo, OPENAI_MAX_TOKENS:500, OPENAI_COST_PER_1K_TOKENS:0.002, OPENAI_TIMEOUT:20.
# Total tokens used: 205, cost of this chat: 0.04100 cents, the call to took 16.83 seconds.
# Perseus and Hercules are both famous heroes from Greek mythology, but they have different stories and accomplishments.
# Perseus is known for slaying the Gorgon Medusa and rescuing Andromeda from a sea monster. He was also the son of Zeus and a mortal woman, and he possessed a magical sword and shield, as well as a helmet of invisibility.
# Hercules, on the other hand, is known for his incredible strength and his twelve labors, which included slaying the Nemean Lion, capturing the Erymanthian Boar, and cleaning the Augean Stables. 
# He was also the son of Zeus and a mortal woman, and he was often depicted carrying a club and wearing a lion skin.
# In summary, while both Perseus and Hercules were heroic figures in Greek mythology, they had different stories and accomplishments.


# $ OPENAI_TEMPERATURE=0.01 gpt-3.5-turbo.py "What is the difference between Perseus and Hercules? Ответьте по русски пожалуйста."
# OPENAI_TEMPERATURE:0.01, OPENAI_API_MODEL:gpt-3.5-turbo, OPENAI_MAX_TOKENS:500, OPENAI_COST_PER_1K_TOKENS:0.002, OPENAI_TIMEOUT:20.
# Total tokens used: 275, cost of this chat: 0.05500 cents, the call to took 20.95 seconds.
# Персей и Геракл - это два разных героя греческой мифологии. Персей был сыном бога Зевса и Данаи, а Геракл - сыном бога Зевса и смертной женщины Алкмены. 
# Персей совершил множество подвигов, включая убийство Медузы и спасение Андромеды от морского чудовища. 
# Геракл также известен своими подвигами, включая убийство льва нимфы и очищение Авгиевых конюшен. Однако, Геракл совершил 12 легендарных подвигов, которые стали его главным достижением.

# $ OPENAI_TEMPERATURE=0.01 gpt-3.5-turbo.py "Are Perseus amd Hercules brothers?"
# OPENAI_TEMPERATURE:0.01, OPENAI_API_MODEL:gpt-3.5-turbo, OPENAI_MAX_TOKENS:500, OPENAI_COST_PER_1K_TOKENS:0.002, OPENAI_TIMEOUT:20.
# Total tokens used: 81, cost of this chat: 0.01620 cents, the call to took 5.31 seconds.
# Yes, Perseus and Hercules (also known as Heracles) are half-brothers in Greek mythology. 
# They share the same father, Zeus, but have different mothers. Perseus' mother was Danae, while Hercules' mother was Alcmene.

# $ OPENAI_TEMPERATURE=0.01 gpt-3.5-turbo.py "В чем разница между Гераклом и Геркулесом?"
# OPENAI_TEMPERATURE:0.01, OPENAI_API_MODEL:gpt-3.5-turbo, OPENAI_MAX_TOKENS:500, OPENAI_COST_PER_1K_TOKENS:0.002, OPENAI_TIMEOUT:20.
# Total tokens used: 224, cost of this chat: 0.04480 cents, the call to took 16.11 seconds.
# Геракл - это имя, которое было дано герою в древнегреческой мифологии, а Геркулес - это его римское имя. 
# Они представляют одного и того же героя, который был известен своей силой и подвигами, такими как убийство льва немея, очищение Авгиевых конюшен и выполнение 12 подвигов. 
# Различия между Гераклом и Геркулесом заключаются только в их именах и в том, как они были изображены в разных культурах.
