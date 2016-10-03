import re
import random
import nltk
from nltk.corpus import stopwords

# t = open_file('1.txt')
# freq_dict = make_freq_dict(t)
#
#
#
#
#
#


def open_file(file):
    o = open(file, 'r', encoding='utf-8')
    t = o.read()
    t = t.lower()
    o.close()
    return t


def make_freq_dict(text):
    dictionary = {}
    text = re.sub('[.,?!:;()"-%#-/«»]', '', text)
    text = re.sub('[0-9]', '', text)
    text = text.split()
    for word in text:
        if word in dictionary:
            dictionary[word] += 1
        else:
            dictionary[word] = 1
    return dictionary


def make_indexes(dictionary):
    frequencies = [x[1] for x in dictionary]
    m = max(frequencies)
    min_ind = 0.02*m
    max_ind = 0.15*m
    ind1 = 0
    ind2 = 0
    for n in frequencies:
        if n < min_ind:
            ind1 += 1
        else:
            left_index = ind1
            break

    for n in frequencies:
        if n < max_ind:
            ind2 += 1
    right_index = ind2
    return left_index, right_index


t = open_file('ruwiki.txt')
freq_dict = make_freq_dict(t)
freq_dict = sorted(freq_dict.items(), key=lambda x: x[1])

l_ind = make_indexes(freq_dict)[0]
r_ind = make_indexes(freq_dict)[1]

words_to_guess = freq_dict[l_ind:r_ind]
sw = set(stopwords.words('russian'))
sw.update(['таких', 'также', 'это'])
words_to_guess = [w for w in words_to_guess if w[0] not in sw and w[0] and len(w[0]) > 2]

word = random.choice(words_to_guess)[0]
print('Слово для угадывания -', word)

text = open_file('ruwiki.txt')
text = re.sub('[.,?!:;()"-%#-/]', '', text)
text = text.split()
indices = [i for i, x in enumerate(text) if x == word]

hints = []
hints_sorted = {}

for n in indices:
    if n != 0:
        if text[n-1] not in sw:
            hints.append(text[n-1] + ' _____')
    if n != len(text)-1:
        if text[n+1] not in sw:
            hints.append('_____ ' + text[n+1])

for i in hints:
    if i in hints_sorted:
        hints_sorted[i] += 1
    else:
        hints_sorted[i] = 1


hints_sorted = sorted(hints_sorted.items(), key=lambda x: x[1])

print('Угадайте слово. Первая подсказка:', hints_sorted[-3][0])
answer = input()
if answer == word:
    score = 1
    print('Вы угадали!')
else:
    print('Неверный ответ. Вторая подсказка:', hints_sorted[-2][0])
    answer = input()
    if answer == word:
        score = 1
        print('Вы угадали!')
    else:
        print('Неверный ответ. Третья подсказка:', hints_sorted[-1][0])
        answer = input()
        if answer == word:
            score = 1
            print('Вы угадали!')