from math import log2
import matplotlib.pyplot as plt

def conditional_entropy_w(some_text, n):
    old_text = some_text.split()
    text=[]
    for i in old_text:
        if(i == ''):
            continue
        text.append(i)
    some_dict = {}
    N = len(text) - n #total
    total_entropy = 0
    for i in range(N):
        curr_words = tuple(text[i:i+n])
        new_word = text[i+n]
        if (curr_words not in some_dict.keys()):
            some_dict[curr_words] = {}
            some_dict[curr_words][new_word] = 1
            some_dict[curr_words]['nr_of_occurencies'] = 1
        else:
            if (new_word not in some_dict[curr_words].keys()):
                some_dict[curr_words][new_word] = 1
            else:
                some_dict[curr_words][new_word] += 1
            some_dict[curr_words]['nr_of_occurencies'] +=1
    for i in some_dict.keys():
        for j in some_dict[i].keys():
            total_entropy += -some_dict[i][j]/N * log2(some_dict[i][j]/some_dict[i]['nr_of_occurencies'])
    return total_entropy

def conditional_entropy_c(old_text, n): 
    some_text = old_text.split()
    some_text = " ".join([i for i in some_text if i != ''])
    some_dict = {}
    N = len(some_text) - n #total
    total_entropy = 0
    for i in range (N):
        curr_str = some_text[i:i + n]
        new_char = some_text[i + n]
        if (curr_str not in some_dict.keys()):
            some_dict[curr_str] = {}
            some_dict[curr_str][new_char] = 1
            some_dict[curr_str]['nr_of_occurencies'] = 1
        else:
            if (new_char not in some_dict[curr_str].keys()):
                some_dict[curr_str][new_char] = 1
            else:
                some_dict[curr_str][new_char] += 1
            some_dict[curr_str]['nr_of_occurencies'] +=1
    for i in some_dict.keys(): #abc
        for j in some_dict[i].keys(): #d
            total_entropy += -some_dict[i][j]/N * log2(some_dict[i][j]/some_dict[i]['nr_of_occurencies'])
    return total_entropy

def conditional_entropy(some_text, n, parameter):
    if(parameter == 'w'):
        return conditional_entropy_w(some_text, n)
    elif(parameter == 'c'):
        return conditional_entropy_c(some_text, n)
    return None

def write_entropies_to_txt(sample_or_norm, number, some_list, param):
    name = "".join(["entropies_", sample_or_norm, str(number), "_", param, ".txt"])
    f = open(name, "w")
    for i in range (len(some_list)):
        to_write = str(some_list[i])+ ' '
        f.write (to_write)
    f.close()
    print ("{} done".format(name), end = '\n\n')

def plot_many_results(x, all_languages, param, names):
    if (param == 'w'):
        tit = "Conditional entropy of words for all languages"
    else:
        tit = "Conditional entropy of characters for all languages"
    colors = ['navy', 'green', 'red', 'deeppink', 'orange', 'purple', 'dodgerblue']
    for i in range(len(all_languages)):
        plt.plot(x, all_languages[i], color = colors[i], label = names[i])
    plt.xlabel("order of conditional entropy")
    plt.ylabel("conditional entropy")
    plt.title(tit+".png")
    plt.legend()
    plt.show()
    plt.savefig(tit)

def plot_many_results_with_fb(x, all_samples, param, minis, maxis):
    if (param == 'w'):
        tit = "Conditional entropy of words for all samples"
    else:
        tit = "Conditional entropy of characters for all samples"
    colors = ['green', 'red', 'deeppink', 'orange', 'purple', 'dodgerblue']
    for i in range(len(all_samples)):
        plt.plot(x, all_samples[i], color = colors[i], label = "sample{}".format(i))
    plt.xlabel("order of conditional entropy")
    plt.ylabel("conditional entropy")
    plt.title(tit+".png")
    plt.legend()
    mini = [minis[param][i] for i in range(len(x))]
    maxi = [maxis[param][i] for i in range(len(x))]
    plt.fill_between(x, y1 = mini, y2 = maxi, alpha = 0.5)
    plt.show()
    plt.savefig(tit)

def plot_one_sample_with_fb(x, sample, nr_of_sample, param, minis, maxi):
    if (param == 'w'):
        tit = "Conditional entropy of words for sample{}".format(nr_of_sample)
    else:
        tit = "Conditional entropy of characters for sample{}".format(nr_of_sample)
    colors = ['green', 'red', 'deeppink', 'orange', 'purple', 'dodgerblue']
    plt.plot(x, sample, color = colors[nr_of_sample], label = "sample{}".format(nr_of_sample))
    plt.xlabel("order of conditional entropy")
    plt.ylabel("conditional entropy")
    plt.title(tit+".png")
    plt.legend()
    mini = [minis[param][i] for i in range(len(x))]
    maxi = [maxis[param][i] for i in range(len(x))]
    plt.fill_between(x, y1 = mini, y2 = maxi, alpha = 0.5)
    plt.show()
    plt.savefig(tit)

#TASK 1
f1 = open("sample0.txt", "r")
text1 = f1.read()
f1.close()
f2 = open("sample1.txt", "r")
text2 = f2.read()
f2.close()
f3 = open("sample2.txt", "r")
text3 = f3.read()
f3.close()
f4 = open("sample3.txt", "r")
text4 = f4.read()
f4.close()
f5 = open("sample4.txt", "r")
text5 = f5.read()
f5.close()
f6 = open("sample5.txt", "r")
text6 = f6.read()
f6.close()

texts = [text1, text2, text3, text4, text5, text6]
names = ["en", "eo", "et", "ht", "la", "nv", "so"]
norms = []

for i in names:
    name = "".join(["norm_wiki_", i, ".txt"])
    f = open(name, "r")
    curr_norm = f.read()
    f.close
    norms.append(curr_norm)
    
entropies_samples = {"sample{}".format(i): {'w': [], 'c': []} for i in range(0, 6)}
entropies_norms = {"norm{}".format(i): {'w': [], 'c': []} for i in range(0, 7)}

#for i in range(len(texts)):
#    for param in ['w', 'c']:
#        entropies = []
#        for j in range(0, 6):
#            ent = conditional_entropy(texts[i], j, param)
#            print("For sample{} and order{}:".format(i, j), ent)
#            entropies.append(ent)
#        entropies_samples["sample{}".format(i)][param] = entropies
#        write_entropies_to_txt("sample", i, entropies, param)

#for i in range(len(norms)):
#    for param in ['w', 'c']:
#        entropies = []
#        for j in range(0, 6):
#            ent = conditional_entropy(norms[i], j, param)
#            print("For norm{} and order{}".format(i, j), ent)
#            entropies.append(ent)
#        entropies_norms[i][param] = entropies
#        write_entropies_to_txt("norm", i, entropies, param)

entropies_languages_c = []
entropies_languages_w = []
entropies_samples_c = []
entropies_samples_w = []
n = list(range(6))

lang_names = ['English', 'Esperanto', 'Estonian', 'Haitian', 'Latin', 'Navasho', 'Somali']
samples_names = ["sample{}".format(i) for i in range(6)]


for param in ['c', 'w']:
    for i in range(6):
        name = "entropies_sample{}_{}.txt".format(i, param)
        f = open(name, "r")
        l = (f.read()).split()
        ents = []
        for j in range(len(l)):
            ents.append(float(l[j]))
        entropies_samples["sample{}".format(i)][param] = ents
        if(param == 'c'):
            entropies_samples_c.append(ents)
        else:
            entropies_samples_w.append(ents)

for param in ['c', 'w']:
    for i in range(7):
        name = "entropies_norm{}_{}.txt".format(i, param)
        f = open(name, "r")
        l = (f.read()).split()
        ents = []
        for j in range(len(l)):
            ents.append(float(l[j]))
        entropies_norms["norm{}".format(i)][param] = ents
        if(param == 'c'):
            entropies_languages_c.append(ents)
        else:
            entropies_languages_w.append(ents)

minis = {'c': [], 'w': []}
maxis = {'c': [], 'w': []}

for param in ['c', 'w']:
    for i in range(6):
        mini = float('Inf')
        maxi = 0
        for j in range(7):
            key = "norm{}".format(j)
            mini = min(mini, entropies_norms[key][param][i])
            maxi = max(maxi, entropies_norms[key][param][i])
        minis[param].append(mini)
        maxis[param].append(maxi)

print("For English language")
for param in ['c', 'w']:
    for i in range(len(entropies_norms['norm0'][param])):
        if (i == 0):
            if (param == 'w'):
                print("Entropy of words:", entropies_norms['norm0'][param][i])
            else:
                print("Entropy of characters:", entropies_norms['norm0'][param][i])
        else:
            if (param == 'w'):
                print("Entropy of rank {} of words:".format(i), entropies_norms['norm0'][param][i])
            else:
                print("Entropy of rank {} of characters:".format(i), entropies_norms['norm0'][param][i])
    print('')

print('')
print("For Latin language")
for param in ['c', 'w']:
    for i in range(len(entropies_norms['norm4'][param])):
        if (i == 0):
            if (param == 'w'):
                print("Entropy of words:", entropies_norms['norm4'][param][i])
            else:
                print("Entropy of characters:", entropies_norms['norm4'][param][i])
        else:
            if (param == 'w'):
                print("Entropy of rank {} of words:".format(i), entropies_norms['norm4'][param][i])
            else:
                print("Entropy of rank {} of characters:".format(i), entropies_norms['norm4'][param][i])
    print('')

#1. all languages - chars
plot_many_results(n, entropies_languages_c, 'c', lang_names)
#2. all languages - words
plot_many_results(n, entropies_languages_w, 'w', lang_names)
#3. all samples with fill between - chars
plot_many_results_with_fb(n, entropies_samples_c, 'c', minis, maxis)
#4. all samples with fill between - words
plot_many_results_with_fb(n, entropies_samples_w, 'w', minis, maxis)
#5. each language with fill between- chars
for i in range(len(entropies_samples)):
    plot_one_sample_with_fb(n, entropies_samples["sample{}".format(i)]['c'], i, 'c', minis, maxis)
#6. each language with fill between- words
for i in range(len(entropies_samples)):
    plot_one_sample_with_fb(n, entropies_samples["sample{}".format(i)]['w'], i, 'w', minis, maxis)
#7. guessing natural languages:
print("Natural languages:", 1, 3) #1 and 3 behave very similar to natural languages and are very close or in boundaries
print("Not natural languages:", 0, 2, 4, 5) #4 and 5 are evident - they decrease barely or decrease very sharply. 0 and 2 are also not in boundaries but their slope is not that extreme.
#However they are still not in boundaries

#First remark - in this program two spaces do not contain word of length 0
#Second remark - I computed entropies some time ago, exported it to .txt files and when I restarted the program I just loaded data from .txt instead of losing 45 minutes
#for computations