import re
import random
from urllib import request
from urllib.parse import quote
from nltk.corpus import stopwords


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
    min_ind = 0.05*m
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


def make_hints(t, indices):
    hints = []
    hints_sorted = {}
    for n in indices:
        if n != 0:
            if t[n-1] not in sw and re.match('\d+', t[n-1]) is None:
                hints.append(t[n-1] + ' _____')
        if n != len(t)-1:
            if t[n+1] not in sw and re.match('\d+', t[n+1]) is None:
                hints.append('_____ ' + t[n+1])

    for i in hints:
        if i in hints_sorted:
            hints_sorted[i] += 1
        else:
            hints_sorted[i] = 1

    return hints_sorted


def last_hint(w):
    url = 'https://suggest.yandex.ru/suggest-ya.cgi?callback=jQuery21401326681859008716_1475524354747&srv=morda_ru_desktop&wiz=TrWth&lr=213&uil=ru&fact=1&v=4&icon=1&hl=1&html=1&bemjson=1&yu=163535871426783267&pos=4&part=' + quote(w)
    page = request.urlopen(url).read().decode('utf-8')
    all_hints = re.findall('"bemjson","(.*?)"', page)
    return all_hints


def guessing(w, h, score_computer, hi):
    last_hints = last_hint(w)
    numbers = ['Первая', 'Вторая', 'Третья']
    print(numbers[score_computer] + ' подсказка:', h[-3+hi][0])
    answer = input()
    if answer == word:
        # score_human = 1
        print('\nТы угадал!')
        print('Игра окончена.')
    else:
        score_computer += 1
        if score_computer < 3:
            print('\nТы не угадал!')
            guessing(w, h, score_computer, hi+score_computer)
        else:
            print('\nВнимание! Это твоя последняя попытка!')
            print('Подсказка: ' + random.choice(last_hints))
            answer = input()
            if answer == word:
                print('\nТы угадал!')
                print('Игра окончена.')
            else:
                print('Ты проиграл!')
                print('Это было слово "' + w + '"')


source_file = 'sirena.txt'

t = open_file(source_file)
freq_dict = make_freq_dict(t)
freq_dict = sorted(freq_dict.items(), key=lambda x: x[1])

l_ind = make_indexes(freq_dict)[0]
r_ind = make_indexes(freq_dict)[1]


words_to_guess = freq_dict[l_ind-1:r_ind+1]
sw = set(stopwords.words('russian'))
sw.update(['таких', 'также', 'это', '—'])
words_to_guess = [w for w in words_to_guess if w[0] not in sw and w[0] and len(w[0]) > 3]
#print(words_to_guess)

word = random.choice(words_to_guess)[0]
#print('Слово для отгадывания -', word)

text = open_file(source_file)
text = re.sub('[.,?!:;()"-%#-/]', '', text)
text = text.split()
indices = [i for i, x in enumerate(text) if x == word]

hints = make_hints(text, indices)
hints_sorted = sorted(hints.items(), key=lambda x: x[1])
#print(hints_sorted)

print('Привет!\nДавай поиграем!\nУгадай слово.')

guessing(word, hints_sorted, 0, 0)