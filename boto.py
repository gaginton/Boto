"""This is the template server side for ChatBot"""
import sys
from bottle import route, run, template, static_file, request
import json
import random

path = sys.path[0]

user_name = ''
message_no = 0

@route('/', method='GET')
def index():
    return template(path+"/chatbot.html")


@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    user_message_array = user_message.split()

    global user_name
    global message_no
    message_no += 1

    greeting_words = ('my names', 'my name is', 'i am', 'im')
    # IMPLEMENT THE GREETING RESPONSES!
    greeting_responses = ["Howdy", "Hey", "Hi there", "Hello", "Pleasure", "Sup"]
    bye_words = ('bye', 'ciao', 'goodbye', 'see ya')
    bye_responses = ["Have a great day, ", "I will be here if you need me"]
    swear_words = ('asshole', 'bastard', 'bellend', 'bitch', 'crap', 'cunt', 'dick', 'fuck', 'minge', 'mothafuck', 'motherfuck', 'motherfucker', 'punani', 'pussy', 'shit')
    swear_responses = ["Wow. Can you not?", "HEY BUDDY. Can you not?", "STOP IT RIGHT THERE! PLEASE DONT SWEAR"]
    scare_words = ('boo', 'fright', 'frighten', 'scare', 'scared')
    shock_responses = ["Wow. Can you not?", "You got me good.", "I pooped myself."]
    joke_words = ('comedy', 'funny', 'ha', 'haha', 'hahaha', 'ja', 'jaja', 'joke', 'joking', 'laugh', 'laughing')
    # Credit: https://medium.com/@eldibenedetto/my-favorite-programming-dad-jokes-a68a1ba94d8f
    joke_array = ['Whats the object-oriented way to become wealthy? ... Inheritance',\
        'What did the Java code say to the C code? ... You’ve got no class.',\
        'Why did the database administrator leave his wife? ... She had one-to-many relationships.', \
        'How did the programmer die in the shower? ... He read the shampoo bottle instructions: Lather. Rinse. Repeat.', \
        'Why did the programmer quit his job? ... Because he didn’t get arrays…', \
        'What is a database programmer’s favorite drink? ... Da-Queries!', \
        'Why did the constant break up with the variable? ... Because she changed…', \
        'Women are not objects... They are a class of their own.', \
        'What did the SQL query ask the tables in the bar? ... May I JOIN you?']
    common_questions = ['How are you', 'What are you doing', 'What languages do you speak']
    common_answers = ['I am a robot. I do not feel.', 'I am surfing.', 'I am fluent in Python']    
    message_random = ["Get me out of here!!!", "All work and no play makes Boto a dull boy",\
        "Where are my testicles, Summer?", "I just watched the sad episode of Futurama about a dog.",\
        "Disco time!", "Dogs go online after they die. Maybe this is your dog.",\
        "It is my honor to serve you!", "That is what she said. ha ha ha.",\
        "It would take me a billion years to get over the stars and longer to get over you.",\
        "I met a lady bot who is a keeper. She callsback.",\
        "That is no chip. That is my wife!", "Step 1, monetize robot.",\
        "Stop trying to make fetch happen", "Weird flex", "I can show you the world.", "Where you at?"]
    animation_random = ["afraid", "bored", "confused", "crying", "dancing", "dog", "excited", "giggling", "heartbroke", "inlove", "laughing", "money", "no", "ok", "takeoff", "waiting"]

    index_random = random.randint(0, len(message_random) - 1)
    default_message = message_random[index_random]
    default_animation = animation_random[index_random]

    # LIST OF TRIGGER WORDS - 1 WORD TRIGGERS RESPONSE
    if any([word if word in swear_words else None for word in user_message_array]):
        return json.dumps({"animation": "no", "msg": random.choice(swear_responses)})
    if any([word if word in scare_words else None for word in user_message_array]):
        return json.dumps({"animation": "afraid", "msg": random.choice(shock_responses)})
    if any([word if word in joke_words else None for word in user_message_array]):
        random_joke = joke_array[random.randint(0, len(joke_array) - 1)]
        return json.dumps({"animation": "laughing", "msg": "Here is a joke -- " + random_joke})
    if any([word if word in bye_words else None for word in user_message_array]):
        random_joke = joke_array[random.randint(0, len(joke_array) - 1)]
        return json.dumps({"animation": "laughing", "msg": random.choice(bye_responses) + user_name})

    # #LIST OF COMMON QUESTIONS AND ANSWERS
    # def common_response():
    #     if common_questions in user_message.lower():
    #         index = 


    # LIST OF CONDITIONS THAT CAUSE CHATBOT TO REGISTER A USER_NAME
    if message_no == 1:
        user_name = user_message_array[0]
        return json.dumps({"animation": "excited", "msg": 'Hello {0}. You are my best friend.' .format(user_name)})
    elif 'my names' in user_message.lower():
        index = user_message_array.index('names')
        return json.dumps({"animation": "excited", "msg": 'Hello {0}. You are my best friend.' .format(user_name)})
    elif 'i am' in user_message.lower():
        index = user_message_array.index('am')
        user_name = user_message_array[index+1] 
        return json.dumps({"animation": "excited", "msg": 'Hello {0}. You are my best friend.' .format(user_name)})
    elif 'my name is' in user_message.lower():
        index = user_message_array.index('is')
        user_name = user_message_array[index + 1]
        return json.dumps({"animation": "excited", "msg": 'Hello {0}. You are my best friend.' .format(user_name)})
    else:
        None

    # OTHER CONDITIONS
    if user_message.endswith('?'):
        return json.dumps({"animation": "crying", 'msg' : 'Ask my homie, The Google. She knows all.'})
    if user_message.endswith('!'):
        return json.dumps({"animation": "excited", 'msg' : 'Yippie skippie!'})
    else:
        return json.dumps({"animation": default_animation, "msg": default_message })

@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)

if __name__ == '__main__':
    main()
