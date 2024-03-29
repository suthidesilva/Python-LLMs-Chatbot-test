# Commented out IPython magic to ensure Python compatibility.
# %pip install langchain
# %pip install langchain-community
# %pip install langchain-core
# %pip install langchain-experimental
# %pip install "langserve[all]"
# %pip install langchain-cli
# %pip install langsmith

# Commented out IPython magic to ensure Python compatibility.
# %pip install openai

# Commented out IPython magic to ensure Python compatibility.
# %pip install --upgrade --quiet  google-search-results

# Commented out IPython magic to ensure Python compatibility.
# %pip install python-dotenv
# %pip install wolframalpha

import requests
import os
import openai

from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from langchain_community.tools.google_scholar import GoogleScholarQueryRun
from langchain_community.utilities.google_scholar import GoogleScholarAPIWrapper
from langchain_community.utilities.wolfram_alpha import WolframAlphaAPIWrapper

# Set your OpenAI GPT-3 API key and google scholar (serp) key

os.environ["WOLFRAM_ALPHA_APPID"] = wolf_api_key
os.environ["SERP_API_KEY"] = serp_api_key
openai.api_key = gpt_api_key

#This is the big function that calls all the other stuff
def help_with_physics(user_input):
    #So I want to take the user input, determine what kind of output the user wants, and then to give them that output.
    #determining question type:
    question_type = determine_question_type(user_input)
    if (question_type == 'sources'):
        print("sources")
        #go find me some sources and then select the best one
        return Go_do_the_search(user_input)

    elif (question_type == 'solve'):
        #go query me some wolfram
        print("solve")
        return solve_problem(user_input)

    else:
        print(question_type)
        return 'Somehow you broke the AI, congrats?'



#determine what the user wants
def determine_question_type(question):
    #returns 'solve' or 'sources' depending on the question being asked
    DetermineRole = "Classify the user's query into one of two categories: 'sources' or 'solve.' If the user is inquiring about where and how to obtain information on a particular subject, label it as 'sources' If the user is seeking the solution to a problem or asking for an equation to solve a specific issue, label it as 'solve'. You only even answer with the singular word 'solve' if they want a specific answer and the singular word 'sources' if they want more information. Regardless, you must only answer with one word, either 'solve' or 'sources'"
    prompt = "Determine whether this question is asking for information about the subject of the question or if they are asking for you to solve it. Here is the question: " + question
    response = openai_request(DetermineRole, prompt)
    return response["choices"][0]["message"]["content"].strip()

######################################################
###   SOURCES section
######################################################
#determines what subject the user is looking at
def determine_key_concepts(question):
    DeterminePrompt = "Your job is to determine what subject in physics the user is asking about while ignoring the answer to the question they are asking. If the user is not asking about physics, respond only with the word 'none'. Otherwise, give as concise an answer possible about what subject the user is looking into and if it is undergraduate or graduate level work. Remember to be as concise as humanly possible with your answers."
    response = openai_request(DeterminePrompt, question)
    print(response)
    return response["choices"][0]["message"]["content"].strip()

#grabs article/book titles from google scholar, which should include stuff like textbooks
def Go_do_the_search(user_input):
    #Go get some articles from google scholar
    topics = determine_key_concepts(user_input)
    if (topics != 'none'):
        print(topics)
        articles = GoogleScholarQueryRun(api_wrapper=GoogleScholarAPIWrapper()).run(topics)
    else:
        return "You are either not asking about physics or the AI is returning a buggy result. Please try again with a new question"
    #then give those topics and the skill level (in topics) to the ai to hand pick relevant articles
    prompt = 'Your job is to look through the list of articles provided by the user and select the one that best matches both the subject and level of education provided here, with a particular emphasis on textbooks:'
    response = openai_request(prompt, topics + articles)
    return response["choices"][0]["message"]["content"].strip()

######################################################
### SOLVE section
######################################################

#Asks wolfram the question
def solve_problem(user_input):
    prompt = 'Your job is to take the following physics question and first classify if it is a theoretical or computational question. Then have the very first word of your response be either "Theoretical" or "Computational" respectively.'
    question = 'Have the very first word of your response be either "Theoretical" or "Computational" depending on how you classified the question. Then if the answer is computational, please write an equation with a single variable equal to some numerical values (substituting in a variables value instead of writing the variable) to solve for your solution, and keep the response focused on the equation itself without additional explanations or elaborations, speaking only in math (for instance "x=5*9.8" would be the entire output). If the answer is theoretical, write the answer to the problem as the rest of your response. Here is the question: \n'
    question = question + user_input
    response = openai_request(prompt, question)
    response = response["choices"][0]["message"]["content"].strip()
    words = response.split()
    first_word = words[0]
    rest = ' '.join(words[1:])
    #here we then look at the very first word and determine if we need to query wolfram
    if ('theoretical' in first_word.lower()):
        print("Theoretical")
        return rest
    elif ('computational' in first_word.lower()):
        print("Computational")
        return WolframAlphaAPIWrapper().run(rest)
    else:
        print(first_word)
        print(rest)
        return "AI is broken, send help"




# Function to make a request to the GPT-3 API
def openai_request(role, task):

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages=[{"role": "system", "content": role},
                                            {"role": "user", "content": task}])
    print(response)
    return response

"""
    https://colab.research.google.com/drive/133H-tr2uRKTiY9q6XW4k5loz2nAGLAdP
"""

#Expected answer of 37.04051835, derived from potential energy
question = "Could you give me the answer to this problem: A rock falls from a height of 70m with a downwards acceleration of g=9.8m/s^2, how fast is it going when it hits the ground in m/s? (ignoring air resistance)"
help_with_physics(question)

question = "Could you give me the answer to this question? A satellite of mass m orbits a planet of mass M in a circular orbit of radius R. What is the time required for one revolution?"
help_with_physics(question)

question = "Where can I find information to help me solve this problem: Five positive charges of magnitude q are arranged symmetrically around the circumference of a circle of radius r. What is the magnitude of the electric field at the center of the circle?"
help_with_physics(question)

question = "Can you give me some information on where to start looking in order to learn how to answer the following question? In a nonrelativistic, one-dimensional collision, a particle of mass 2m collides with a particle of mass m at rest. If the particles stick together after the collision, what fraction of the initial kinetic energy is lost in the collision? "
help_with_physics(question)
