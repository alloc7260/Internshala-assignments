import openai
import re
import time

# set up OpenAI API key
openai.api_key = "INSERT_YOUR_API_KEY_HERE"

# function to generate a story based on a given prompt
def generate_story(prompt):
    # set up OpenAI GPT-3 parameters
    model_engine = "text-davinci-002"
    temperature = 0.7
    max_tokens = 1024
    stop_sequence = "\n\n"

    # generate story using OpenAI GPT-3 API
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        stop=stop_sequence
    )

    # extract story from OpenAI response
    story = response.choices[0].text
    story = re.sub('[^0-9a-zA-Z\n\.\?,!]+', ' ', story)
    story = story.strip()

    return story

# example usage
prompt = "a time travel adventure"
prompt = "a haunted house"
prompt = "an unexpected visitor"
story = generate_story(prompt)
print(story)
