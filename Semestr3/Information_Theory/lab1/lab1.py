import random
import copy

def omit_numbers (some_text):
    l=[]
    for i in range (len(some_text)):
        if (ord(some_text[i]) >= 97 or ord(some_text[i]) == 32):
            l.append(some_text[i])
    new_text = "".join(l)
    return new_text

def assign_order (list_of_tuples):
    list_of_tuples.sort(key = lambda x: x[1], reverse = True)
    ordered_list_of_tuples = []
    for i in range(len(list_of_tuples)):
        a, b = list_of_tuples[i]
        ordered_list_of_tuples.append((a, i+1))
    ordered_list_of_tuples.sort(key = lambda x: x[1])
    return ordered_list_of_tuples

def zero_probabilities(letters_and_space):
    some_dict = {}
    for i in range (len(letters_and_space)):
        some_dict[letters_and_space[i]]=1/len(letters_and_space)
    return some_dict

def cummulative_probabilities(some_dict):
    keys = list(some_dict.keys())
    for i in range(1, len(keys)-1):
        some_dict[keys[i]]+=some_dict[keys[i-1]]
    some_dict[keys[-1]] = 1
    return some_dict

def choose_chars(prob, some_dict):
    keys = list(some_dict.keys())
    for i in keys:
        if (prob <= some_dict[i]):
            return i
    return keys[-1]

def generator(N, cumm_probabilities):
    some_text = []
    for i in range(N):
        random_number = random.random()
        some_text.append(choose_chars(random_number, cumm_probabilities))
    final_text="".join(some_text)
    return final_text

def calculate_avg_word(some_text, s):
    words = some_text.split()
    number_of_letters = 0
    for i in words:
        number_of_letters+=len(i)
    print ("Average length of word in {0} is ".format(s), round(number_of_letters / len(words), 2), sep = '')

def frequency_of_characters(some_text, if_numbers = True):
    numbers = {}
    letters = {}
    number_of_letters = 0
    number_of_numbers = 0
    words = some_text.split()
    spaces = some_text.count(" ")
    for i in words:
        for j in range(len(i)):
            if (ord(i[j]) >= 48 and ord(i[j]) <=57 and if_numbers == True):
               if (i[j] not in list(numbers.keys())):
                   numbers[i[j]] = 1
               else:
                   numbers[i[j]]+=1
               number_of_numbers += 1
            elif (ord(i[j]) >= 97):
               if (i[j] not in list(letters.keys())):
                   letters[i[j]] = 1
               else:
                   letters[i[j]]+=1
               number_of_letters += 1
    letters[" "] = spaces
    number_of_letters += spaces
    all_keys =  list(letters.keys()) + list(numbers.keys())
    frequency = {**letters, **numbers}
    freq_list=[]
    for i in all_keys:
        frequency[i] /= number_of_numbers+number_of_letters+spaces
        freq_list.append((i, frequency[i]))
    freq_list = assign_order(freq_list)
    freq_list.sort(key = lambda x: x[0])
    if (if_numbers == True):
        return letters, numbers, number_of_letters, number_of_numbers
    return letters, number_of_letters

def conditional_probability (some_text, x , str = None):  #if str is something, then we look for conditional probabilities of this one particular 
                                                          #string, else we make a conditional probs of all strings occuring in text with length x
    some_dict = {}
    nr_of_occurence = 0
    some_check = 0
    N = len(some_text) - x
    if (str != None):
        for i in range(N):
            if (some_text[i:i+len(str)] == str):
                if (some_text[i:i+len(str) + 1] not in list(some_dict.keys())):
                    some_dict[some_text[i:i+len(str) + 1]] = 1
                else:
                    some_dict[some_text[i:i+len(str) + 1]]+=1
                nr_of_occurence += 1
        for i in list(some_dict.keys()):
            some_dict[i] /= nr_of_occurence
            some_check += some_dict[i]
    else:
        for i in range (N):
            curr_str = some_text[i:i + x]
            new_str = some_text[i:i + x + 1]
            if (curr_str not in list(some_dict.keys())):
                some_dict[curr_str] = {}
                some_dict[curr_str][new_str] = 1
                some_dict[curr_str]['number_of_occurences'] = 1
            else:
                if (new_str not in list(some_dict[curr_str].keys())):
                    some_dict[curr_str][new_str] = 1
                else:
                    some_dict[curr_str][new_str] += 1
                some_dict[curr_str]['number_of_occurences'] += 1
        for i in list(some_dict.keys()):
            for j in list(some_dict[i].keys()):
                if (j == 'number_of_occurences'):
                    continue
                some_dict[i][j] /= some_dict[i]['number_of_occurences']
                some_check += some_dict[i][j]
            some_dict[i].pop('number_of_occurences')
    return some_dict

def dict_to_str (some_dict):
    l = []
    for i in list(some_dict.keys()):
        l.append(str(i))
        s =[]
        for j in list(some_dict[i].keys()):
            s.append(str(j))
            s.append(str(some_dict[i][j]))
        l.append(str(s))
    string = ";".join(l)
    return string

def write_probs_to_txt():
    for i in range (1, 6):
        this_dict = conditional_probability (text, i)
        name = "".join(["Markov", str(i), ".txt"])
        f = open (name, "w")
        to_write = dict_to_str (this_dict)
        f.write (to_write)
        f.close()
        print ("Markov {} done".format(i), end = '\n\n')

def from_txt_to_dict (i):
    name = "".join(["Markov", str(i), ".txt"])
    f = open(name, "r")
    text = f.read()
    f.close()

    l = text.split(';')
    some_dict = {}

    for j in range(len(l)//2):
        key = str(l[2*j])
        s = l[2*j + 1].split(', ')
        some_dict[key] = {}
        for k in range(len(s)//2):
            if (len(s)//2 == 1):
                number = s[2*k+1][:len(s[2*k + 1]) - 1]
                some_dict[key][s[0][2:-1]] = float(number[1:-1])
            else:
                if (k == 0):
                    number = s[2*k + 1][:len(s[2*k+1])]
                    some_dict[key][s[2*k][2:-1]] = float(number[1:-1])
                elif (k == -1 + len(s)//2):
                    number = s[2*k + 1][:len(s[2*k+1])-1]
                    some_dict[key][s[2*k][1:-1]] = float(number[1:-1])
                else:
                    number = s[2*k + 1][:len(s[2*k + 1])]
                    some_dict[key][s[2*k][1:-1]] = float(number[1:-1])
    return some_dict

def generate_one_letter_Markov(order_of_markov, cond_probs, letters_freq, start, random_number = None):
    if(random_number == None):
        random_number = random.random()
    if (start == None or order_of_markov == 0):
        return choose_chars(random_number, cummulative_probabilities(letters_freq))
    if (start in list(cond_probs[order_of_markov - 1].keys())):
        return choose_chars(random_number, cummulative_probabilities(cond_probs[order_of_markov - 1][start]))
    else: #if such fragment was never found, then we go one information source 'down'
        return generate_one_letter_Markov(order_of_markov - 1, cond_probs, letters_freq, start[2:], random_number)

def generate_Markov(order_of_markov, cond_probs, N, letters_freq, start = None):
    if (start == None):
        start = ""
    string = copy.deepcopy(start)
    if (start == "" or len(start) < order_of_markov):
        iterations  = order_of_markov - len(start)
        for i in range (iterations):
            start = "".join([start, generate_one_letter_Markov(order_of_markov, cond_probs, letters_freq, start)])
    nr_of_iterations = N - len(start)
    for i in range(nr_of_iterations):
        previous_str = string[-order_of_markov:]
        next_letter = generate_one_letter_Markov(order_of_markov, cond_probs, letters_freq, previous_str)[-1]
        string = "".join([string, next_letter])
    return string


#TASK 1
print ("TASK 1", end='\n')
f1 = open("norm_hamlet.txt", "r")
text1 = f1.read()
f1.close()
f2 = open("norm_romeo_and_juliet.txt", "r")
text2 = f2.read()
f2.close()
f3 = open("norm_wiki_sample.txt", "r")
text3 = f3.read()
f3.close()
text = omit_numbers(text1+text2)
textt = text1+text2+text3

#setting some seed - for simplicity
random.seed(100)

#TASK 2 - zeroth order approximation:
print ("TASK 2", end="\n")
letters_and_space = [chr(i) for i in range (97, 123)]
letters_and_space= letters_and_space+[' ']
some_text = generator(10017, cummulative_probabilities(zero_probabilities(letters_and_space)))
calculate_avg_word(some_text, "zeroth order approximation")
print ("\n")

#TASK 3:
print ("TASK 3", end='\n')
letters_freq1, number_of_letters = frequency_of_characters(textt, False)
print (letters_freq1)
#letters, numbers, number_of_letters, number_of_numbers = frequency_of_characters(text[:500])
#General pattern seems to be that the more often letter occurs in English (based on given texts) the shorter is signal for the letter
#For example letters 'e', 't', 'a', 's', 'n', 'i' occured the most times in the text, and signal for 'e' lasts 1 dit, for 'i' 3 dits (2 dotts and one space) etc
#On the other hand 'z', 'j', 'x', 'q' occur rarely compared to 'e' and duration of the signal for 'q' is 13 dits
#Of course pattern doesn't go perfectly one to one, but besides some exceptions this theory works quite good.
#Numbers is different case since - they are ordered from 0-9 and they shold be treated other way because they don't appear as often as letters in the text.
print ("\n")

#TASK 4:
print ("TASK 4", end='\n')
keys = list(letters_freq1.keys())
for i in keys:
    letters_freq1 [i] /= number_of_letters
some_text2 = generator (1000, cummulative_probabilities(letters_freq1))
print (some_text2)
calculate_avg_word(some_text2, "first order approximation")
print ("\n")

#TASK 5:
#Most common letters in the text are 'e' and 'a'
print ("TASK 5", end = "\n")
for i in ['e', 'a']:
    print(conditional_probability (text, len(i), str = i), end = '\n\n')

#TASK 6:
print ("TASK 6", end = '\n')
#write_probs_to_txt () #function to write all the dictionaries to txt file just to avoid computing all the probabilities each time. Instead it takes like 5 seconds to read it
cond_probs = []
for i in range (1, 6):
    cond_probs.append(from_txt_to_dict(i))
for i in [1, 3, 5]:
    if (i == 5):
        start = 'probability'
    else:
        start = None #if we dont give any string on the start, then it will be generated with some probabilities
    print ("{} order Markov source:".format(i))
    new_text=(generate_Markov(i, cond_probs, i*100, letters_freq1, start))
    print(new_text)
    calculate_avg_word(new_text, "{} order Markov source".format(i))
#5 order Markov source looks most interesting so let's generate longest string with help of it - first and third don't look so nice ;)