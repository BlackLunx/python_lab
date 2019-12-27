from nltk.corpus import stopwords
import re
import pymorphy2
import string
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

class appraiser():
    
    def __init__(self, input_file = 'estimations.txt'):
        import nltk
        nltk.download("stopwords")
        self.valuation = dict()
        self.morph = pymorphy2.MorphAnalyzer()
        self.rules = [self.rule1, self.rule2, self.rule3, self.rule4]
        with open(input_file, encoding='utf-8') as f:
            for line in f:
                word, mark = line.split()
                self.valuation[word] = int(mark)

    def hard_work_with_tweet(self, words):
        words = words[17:]
        words = re.sub(r'#\s\w+\s*', ' ', words)
        words = re.sub(r'@\s\w+\s*', ' ', words)
        words = re.sub(r'\sRT\s', ' ', words)
        words = re.sub(r'^https?:\/\/.*[\r\n]*', '', words)
        words = re.sub(r'^http?:\/\/.*[\r\n]*', '', words)
        words = re.sub(r'…—–', '', words)
        words = "".join(l for l in words if l not in string.punctuation).split()
        return words
    def generate_adjectives(self, input_file = 'frequency.txt', output_file = 'adjectives.txt'):
        positive = []
        negative = []
        with open(input_file, encoding='utf-8') as f:
            for line in f:
                if len(line) < 2:
                    continue
                word = line.split(' - ')[0]
                if word in self.valuation:
                    if self.valuation[word] == 1 and len(positive) < 5:
                        positive.append(line)
                    if self.valuation[word] == -1 and len(negative) < 5:
                        negative.append(line)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('Top-5 Positive:\n')
            for line in positive:
                f.write(line)
            f.write('\nTop-5 Negative:\n')
            for line in negative:
                f.write(line)
        
    def generate_dictionary_and_list(self, input_file = 'in.txt'):
        my_dict = {}
        lengths = {}
        f = open(input_file, encoding='utf-8')
        for line in f:
            if len(line) < 17:
                continue
            words = self.hard_work_with_tweet(line)
            set_of_words = set()
            counter = 0
            for filtered_word in words:
                filtered_word = filtered_word.lower()
                p_filtered_word = self.morph.parse(filtered_word)[0] 
                new_word = p_filtered_word.normal_form
                if new_word in stopwords.words('russian'):
                    continue
                if re.fullmatch(r'\b[а-яё]+', new_word):
                    counter += 1
                    set_of_words.add(new_word)
            if counter in lengths:
                lengths[counter] += 1
            else:
                lengths[counter] = 1
            for word in set_of_words:
                if word in my_dict:
                    my_dict[word] += 1
                else:
                    my_dict[word] = 1
        f.close()
        return (my_dict, lengths)

    def generate_frequency(self, input_file = 'in.txt', output_file1 = 'frequency.txt', output_file2 = 'twits_length.txt'):
        my_dict, dict_with_length = self.generate_dictionary_and_list(input_file)
        list_keys = list(my_dict.items())
        list_keys.sort(key=lambda i: -i[1])
        cnt_words = 10000
        with open(output_file1, 'w', encoding='utf-8') as f:
            for key in list_keys:
                f.write(str(key[0]) + ' - ' + str(key[1]) + ' - ' + str(key[1] / cnt_words * 100)[:6] + '%\n')
        list_keys = list(dict_with_length.items())
        list_keys.sort(key=lambda i: -i[1])
        with open(output_file2, 'w', encoding='utf-8') as f:
            for key in list_keys:
                f.write(str(key[0]) + ' - ' + str(key[1]) + ' - ' + str(key[1] / cnt_words * 100)[:6] + '%\n')

    def rule1(self, words, t_low = -2, t_up = 2):
        current_evaluation = 0
        for filtered_word in words:
            filtered_word = filtered_word.lower()
            p_filtered_word = self.morph.parse(filtered_word)[0] 
            new_word = p_filtered_word.normal_form

            if new_word in stopwords.words('russian'):
                continue

            if re.fullmatch(r'\b[а-яё]+', new_word):
                if new_word in self.valuation:
                    current_evaluation += self.valuation[new_word]

        if current_evaluation < t_low:
            return 0
        elif current_evaluation <= t_up:
            return 1
        else:
            return 2
        
    def rule2 (self, words):
        current_counter = {-1: 0, 1: 0, 0: 0}
        for filtered_word in words:
            filtered_word = filtered_word.lower()
            p_filtered_word = self.morph.parse(filtered_word)[0] 
            new_word = p_filtered_word.normal_form
    
            if new_word in stopwords.words('russian'):
                continue

            if re.fullmatch(r'\b[а-яё]+', new_word):
                if new_word in self.valuation:
                    current_counter[self.valuation[new_word]] += 1

        list_keys = list(current_counter.items())
        list_keys.sort(key=lambda i: -i[1])
        return list_keys[0][0] + 1

    def rule3 (self, words):
        current_counter = {-1: 0, 1: 0, 0: 0}
        for filtered_word in words:
            filtered_word = filtered_word.lower()
            p_filtered_word = self.morph.parse(filtered_word)[0] 
            new_word = p_filtered_word.normal_form

            if new_word in stopwords.words('russian'):
                continue

            if re.fullmatch(r'\b[а-яё]+', new_word):
                if new_word in self.valuation:
                    current_counter[self.valuation[new_word]] += 1

        if current_counter[0] >= current_counter[1] + current_counter[-1]:
            return 1
        elif current_counter[1] >= current_counter[-1]:
            return 2
        else:
            return 0

    def rule4 (self, words):
        current_counter = {-1: 0, 1: 0, 0: 0}
        for filtered_word in words:
            filtered_word = filtered_word.lower()
            p_filtered_word = self.morph.parse(filtered_word)[0] 
            new_word = p_filtered_word.normal_form

            if new_word in stopwords.words('russian'):
                continue

            if re.fullmatch(r'\b[а-яё]+', new_word):
                if new_word in self.valuation:
                    current_counter[self.valuation[new_word]] += 1

        if current_counter[-1] > current_counter[1]:
            return 0
        elif current_counter[1] >= current_counter[0]:
            return 2
        else:
            return 1

    def ask_all_rules(self, input_file = 'in.txt'):
        f = open(input_file, encoding='utf-8')
        counter_twits = [[0, 0, 0] for i in range(len(self.rules))]
        for line in f:
            if len(line) < 17:
                continue
            words = self.hard_work_with_tweet(line)
            current = 0
            for rule in self.rules:
                counter_twits[current][rule(words)] += 1  
                current += 1
        f.close()
        return counter_twits

    def generate_rules(self, output_file = 'classifications.txt', input_file = 'in.txt'):
        rules = self.ask_all_rules(input_file)
        self.saved_rules = rules
        names = ['\nRule: standart with the borders\n', '\nRule: prevailing factor\n', '\nRule: the number of neutrals should be double\n', '\nRule: The negative should not be superior to the positive\n']
        with open(output_file,'w', encoding='utf-8') as f:
            counter = 0
            for i in rules:
                f.write(names[counter])
                sums = i[0] + i[1] + i[2]
                f.write('Good - ' + str(i[2]) + ' - ' + str(i[2] / sums * 100)[:4] + '\n')
                f.write('Bad - ' + str(i[0]) + ' - ' + str(i[0] / sums * 100)[:4] + '\n')
                f.write('Neutral - ' + str(i[1]) + ' - ' + str(i[1] / sums * 100)[:4] + '\n')
                counter += 1

    def print_distribution(self, input_file = 'classifications.txt'):
        with open('classifications.txt', encoding='utf-8') as f:
            data = [[],[],[]]
            colnames = []
            ind = 0
            for line in f:
                if len(line) < 2:
                    continue
                if ind % 4 == 0:
                    colnames.append(line[6:len(line) - 1])
                else:
                    data[ind % 4 - 1].append(int(line.split(' - ')[1]))
                ind += 1
        fig, ax = plt.subplots()
        bar_width = 0.3
        x1 = np.arange(1, 5) - 0.45
        x2 = np.arange(1, 5) - 0.15
        x3 = np.arange(1, 5) + 0.15
        ax.bar(x1, data[0], bar_width, color = 'green', label='Good')
        ax.bar(x2, data[1], bar_width, color = 'red', label='Bad')
        ax.bar(x3, data[2], bar_width, color = 'yellow', label='Neutral')
        plt.ylabel('Number of twits')
        plt.xlabel('Rules')
        plt.title('Распределение твитов')
        fig.set_figwidth(15)    #  ширина Figure
        fig.set_figheight(10)    #  высота Figure
        fig.set_facecolor('floralwhite')
        plt.xticks(x2, colnames)
        plt.legend()
        plt.tight_layout()
        plt.show()
    
    def plot_with_adjectives(self, input_file = 'adjectives.txt'):
        with open(input_file, encoding='utf-8') as f:
            y = [[], []]
            words = [[], []]
            ind = 0
            for line in f:
                if len(line) < 2:
                    continue
                if ind % 6 != 0:
                    current_string = line.split(' - ')
                    words[ind // 6].append(current_string[0])
                    y[ind // 6].append(int(current_string[1]))
                ind += 1    
        fig, axs = plt.subplots(1, 2)
        x = [int(i) for i in range(1, 6)]
        colors = ['blue', 'orange']
        names = ['Хорошие слова', 'Плохие слова']
        for i in range(2):
            axs[i].bar(words[i], y[i], 0.3, color = colors[i])
            axs[i].set_ylabel('Кол-во твитов, в которых встр')
            axs[i].set_xlabel('Слово')
            axs[i].set_title(names[i])
       
        fig.set_figwidth(15)    #  ширина Figure
        fig.set_figheight(10)    #  высота Figure
        fig.set_facecolor('floralwhite')
        plt.tight_layout()
        plt.show()    
    def generate_hrs(self, input_file = 'in.txt', output_file = 'hours'):
        gap = 30
        distibuion = [[] for i in range(len(self.rules))]
        last = None
        counter = [[0, 0, 0] for i in range(len(self.rules))]
        first = None
        with open('new_out.txt', encoding='utf-8') as f:
            for line in f:
                if len(line) < 2:
                    continue
                current_time = datetime.strptime(re.search(r'\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}', line)[0], "%Y-%m-%d %H:%M")
                if first is None:
                    first = current_time
                if last is None:
                    last = current_time
                diff = current_time - last
                words = self.hard_work_with_tweet(line[17:])
                ind = 0 
                for rule in self.rules:
                    counter[ind][rule(words)] += 1
                    ind += 1
                if diff.seconds > gap * 60:
                    ind = 0
                    for rule in self.rules:
                        distibuion[ind].append([last, counter[ind][:]])
                        ind += 1
                    last = current_time
        for i in range(len(self.rules)):
            with open(output_file + str(i + 1) + '.txt', 'w', encoding='utf-8') as f:
                for current_time in distibuion[i]:
                    if len(current_time[1]) < 3:
                        print(current_time)
                    f.write(str(first) + ' - ' + str(current_time[0]) + ' ' + str(current_time[1][0]) + ' ' + str(current_time[1][1]) + ' ' + str(current_time[1][2]) + '\n')