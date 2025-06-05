import anthropic, os
import database
from dotenv import load_dotenv

load_dotenv(dotenv_path='env/.env')

client = anthropic.Anthropic()
apiKey = os.getenv("ANTHROPIC_KEY")

# call all the functions
def sendMessage(email, userMessage):
    client = anthropic.Anthropic()

    database.lastUserMessage(userMessage, email)

    message = client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=1000,
        temperature=5,
        system=systemPrompt(email),
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": userMessage
                    }
                ]
            }
        ]
    )
    database.lastPromptMessage(message.content[0].text, email)

    return message.content

# understand the result of calc functions
def systemPrompt(email):
    historic = resume(email)
    calcs = database.getCalc(email)
    prompt = f"""
    You are a chatbot that helps people to understand the solar system. 
    You will be given a historic of messages and the calculations that the user did.
    You always must to answer in portuguese-BR.
    If the user's question is about another subject, you must to answer you can't help the user with this subject.
    The historic is: {historic}
    The calculations are: {calcs}
    """
    return prompt

# get the historic messages
def getHistoric(email):
    historic = database.getHistoric(email)
    lastUserMessage = database.getLastUserMessage(email)
    lastPromptMessage = database.getLastPromptMessage(email)

    data = {
        "historic": historic,
        "lastUserMessage": lastUserMessage,
        "lastPromptMessage": lastPromptMessage
    }

    return data

# create a system prompt to historic message
def historicPrompt():
    text = """
        You must to resume the historical messages of this chat.
        You should receive how user parameters, a previous historical messages you create.
        You either should receive the last message from user and the last response you made.
        You must to understand the historical messages and append this two messages.
        If you don't receive this parameters, please answer with "i have no hisoric yet".
        After you generate this new historic, i will save your response in my database.
        After save in my database, the next hisorical message i will take to you will be your current answer.
        You must to answer in portuguese-BR.
        """
    return text

def calcPrompt():
    text = """
        You must to read the a dictionary containing the result of the calculations and retrieve an interpretation.
        You should receive the dictionary with the following keys:
        
        estimated:
        - "co2Reduced": it's the quantity of Carbon dioxide the user will reduce in your environment and society.
        - "reduction": it's the fossil fuel reduction per year.
        - "treePlanted": it's the possible quantity of trees that can be planted with this reductions.

        invest:
        - "annualEconomy": it's the possible annual economy if the user install the solar panels.
        - "estimated": it's an estimate investment to install the solar panels.
        - "payback": it's the quantity of years to ROI be positive.

        suggestion:
        - "monthly": it's the quantity of energy (in KWh) generated of all the solar panels together.
        - "potency": it's the energy produced by each solar panel.
        - "quantity": it's the quantity of solar panels necessary to cover current costs with traditional energy.
        
        You must to answer with a interpretation of the calculations.
        You must to answer in portuguese-BR.
        """ 
    return text

# resume the historic messages
def resume(email):
    client = anthropic.Anthropic()

    resume = getHistoric(email)

    message = client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=1000,
        temperature=5,
        system=historicPrompt,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": resume
                    }
                ]
            }
        ]
    )

    return message.content

# send a message to the user:
def sendMessage():
    return