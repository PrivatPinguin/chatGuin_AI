import random
import json
import numba
import torch
from torch.testing._internal.common_cuda import TEST_NUMBA, TEST_MULTIGPU, TEST_NUMBA_CUDA

# from model import NeuralNet
# from nltk_utils import bag_of_words, tokenize

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

if TEST_MULTIGPU:
    print('multi CPU\tTRUE ')
print(numba.__version__)
if TEST_NUMBA_CUDA:
    import numba.cuda
    device = torch.device('cuda')
else:
    device = torch.device('cpu')
# device = torch.device( 'cuda' if torch.cuda.is_available()  else 'cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Botguin"

def saveLog(logText):
    f = open("F:\Programme\python\discordBot\logs\chatInhalteNeu.log", "a")
    f.write(logText + '\n')
    f.close()
    print('\n\nNEW WORD in log\t{}\n\n'.format(logText))

def replaceUmlaute(msg):
    for word in msg:
        word = word.replace("ü","ue")
        word = word.replace("ö","oe")
        word = word.replace("ä","ae")
        word = word.replace("Ü","Ue")
        word = word.replace("Ö","Oe")
        word = word.replace("Ä","Ae")
        word = word.replace("ß","sz")
    return msg

def say(sentence):
    cleanContent = sentence.clean_content
    sentence = tokenize(sentence.clean_content)
    replaceUmlaute(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)
    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    #gets max(prob.item())
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75:
        for intent in intents['intents']:
            #searches for right tag to the prob
            if tag == intent["tag"]:
                return random.choice(intent['responses'])
    else:
        saveLog(cleanContent)
        wtfMsg = ['Das kenne ich noch nicht, aber das lerne ich noch.', 'Ich weisz nicht was ich dazu sagen soll, ich werde es wissen.', 'Das kann ich noch nicht beantworten.']
        return random.choice(wtfMsg)