import tiktoken
import openai
import os
import json
import logging

logger = logging.getLogger('main_logger')


def process_command(user_prompt, model="gpt-3.5-turbo"):
    logger.info(f"Prompt: {user_prompt} | Price: {calculate_price(user_prompt)}")
    openai.api_key = os.getenv('OPENAI_API_KEY')
    commands = ['turn_on',
                'turn_off',
                'search_google',
                'tell_time',
                'ask_chatgpt',
                'shopping_list',
                'tv_control',
                'stereo_control'
                ]

    training_prompt = f"""
    your job is to classify the text separated by || into the itens bellow.

    Here are some of examples:
    Example 1:
    - User input: "turn tv on"
    - Expected output in JSON format:
    {{
    "command": "turn_on",
    "keywords": ["tv"],
    "full_text" : "turn tv on"
    }}

    Example 2:
    User Input: "Turn off dinning room lights"
    - Expected output in JSON format:
    {{
    "command" :  "turn_off",
    "keywords" : ["dinning_room_lights"],
    "full_text" : "Turn off dinning room lights"
    }}

    Example 3:
    User Input: "Play Madonna Like a Virgin"
    - Expected output in JSON format:
    {{
    "command" :  "stereo_control",
    "keywords" : ["play", "madonna", "like_a_virgin"],
    "full_text": "Play Madonna"
    }}

    Example 4:
    User Input: "ask google how old William Hurt is."
    - Expected output in JSON format:
    {{
    "command" :  "ask_google",
    "keywords" : ["how_old_is_william_hurt"],
    "full_text" : "ask google how old William Hurt is."
    }}

    Example 5:
    User Input: "Add a banana and olive oil to my shopping list"
    - Expected output in JSON format:
    {{
    "command" :  "shopping_list",
    "keywords" : ['banana', 'olive_oil'],
    "full_text" : "Add a banana and olive oil to my shopping list"
    }}

    Example 6:
    - User input: "turn on the tv and the living room lights"
    - Expected output in JSON format:
    {{
    "command": "turn_on",
    "keywords": ["tv", "living_room_lights"],
    "full_text" :  "turn on the tv and the living room lights"
    }}

    Example 7:
    - User input: "turn the volume on the tv up"
    - Expected output in JSON format:
    {{
    "command": "tv_control",
    "keywords": ["volume", "up"],
    "full_text" :  "turn on the tv and the living room lights"
    }}

    Example 8:
    - User input: "change the music"
    - Expected output in JSON format:
    {{
    "command": "stereo_control",
    "keywords": ["change"],
    "full_text" :  "turn on the tv and the living room lights"
    }}

    Example 9:
    - User input: "pause this song"
    - Expected output in JSON format:
    {{
    "command": "stereo_control",
    "keywords": ["pause"],
    "full_text" :  "turn on the tv and the living room lights"
    }}

    Your response must always be in json format in snake case typing  in the following format with the following keys 
    "command" and "keywords".

    if you can't classify the command or the keywords, the value must be "unknown".

    Here's  a list of allowed commands:
    {', '.join([f"{n+1}. {c}" for n,c in enumerate(commands)])}

    ANSWERS CAN ONLY BE IN JSON FORMAT. IT SHOULD ALSO CONTAIN THE NUMBER OF TOKENS IN THE FULL_TEXT
    || {user_prompt} || 
    """

    messages = [{"role": "user", "content": training_prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    try:
        return json.loads(response.choices[0].message["content"])   
    except Exception as e:  
        logger.error(e._message)
        return None


def calculate_price(prompt, model="gpt-3.5-turbo", cost_per_token=0.002 / 1000):
    enc = tiktoken.encoding_for_model(model)
    return format(cost_per_token * len(enc.encode(prompt)), '.8f')
