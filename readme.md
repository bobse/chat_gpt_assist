# LLM Assistant: WIP

This is a open-source assistant that uses LLMs to power it's decisions through prompts and json responses.

The idea is to make an assistant much like Alexa or Google Assistant, but with a modular architecture so that any developer can improve upon the current design.

This base system comes with some examples for commands that you can implement: `[lights, tv_control, ask_gpt]`

Browse these folders and files to get a better understanding of how to implement your own commands.

## Installation

- Clone this repository into your local computer
- Create and activate a python environment
- Rename .env.example to .env
- Fill out `OPENAI_API_KEY` with your OpenAI API key
- Install dependencies `pip install -r requirements.txt`

<br />

## Using the assistant

- Run `python main.py`

<br />

## TTS

Currently we have switched to use TTS from OpenAi as well. There's also an implemented googleTTS module that you can switch if you want to experiment with.

## Setup Google TTS (if you want to use TTS from Google)

Since there's a generous free limit for google TTS we decided to use this solution as the main one.
Of course, due to the modular nature of this implementation you can always substitute for a different TTS of your choice.
Instructions on how to setup Google TTS:

- Follow the first part of this guide: https://cloud.google.com/text-to-speech/docs/before-you-begin?hl=pt-br
- Save the json file in your folder.
- Edit the `.env` variable `GOOGLE_APPLICATION_CREDENTIALS` to point to your json file.

<br />

## Changing Input or Output

- Input: Currently there are two options for command inputing. Text or Audio.
- Output: Audio or Text
- Running in text mode: `python main.py --input text`

<br />

## Creating your own commands

To create a new command on cli type `python new_command` and fill out the name for your new command (must be in snake_case format).

Three files are included in your newly created command folder:

- `response.py` - Pydantic validator file. It validates expected response from the model and also the examples
- `examples.json` - Examples of the response from the user input. You can add any field you like, but I suggest you keep user_input. These examples are sent with the prompt to the model.
- `<you-cmd-name.py>` - This file has an `execute` method. This is where you should put all the logic for your new command.
