import csv
import copy
import re
from random import sample
import pprint


# %%
with open('./applications/views/characters/hiragana_roma.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    lis = []
    for kana, roma in dict.items():
        row = kana + roma
        lis.append(row)
    writer.writerows(lis)

# %%
with open('./applications/views/characters/hiragana_roma.csv') as f:
    rows = csv.reader(f)
    dict = {}
    for row in rows:
        if len(row) > 1:
            kana = row[0]
            roma = ''.join(row[1:])
        dict[kana] = roma
    print(dict)

# %%
with open('./applications/views/characters/words.csv') as f:
    rows = csv.reader(f)
    write_rows = []
    for row in rows:
        if len(row) == 0:
            continue
        write_row = copy.copy(row)
        flag = False
        for char in row:
            if flag:
                if char in dict.keys():
                    write_row.append(dict[char])
                elif char in {'ゃ', 'ゅ', 'ょ', 'っ', 'ん', '、', '。'}:
                    write_row.append(char)
                elif char == '）':
                    pass
                else:
                    print('error')
            if char == '（':
                flag = True
        print(write_row)
        write_rows.append(write_row)

# %%
with open('./applications/views/characters/edited_words.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(write_rows)

# %%
with open('./applications/views/characters/words.csv') as f:
    rows = csv.reader(f)
    write_rows = []
    for row in rows:
        if len(row) == 0:
            continue
        write_row = copy.copy(row)
        flag = False
        double = False
        terminal_n = False
        for char in row:
            if flag:
                if char in dict.keys():
                    if double:
                        write_row.append(dict[char][0] + dict[char])
                        double = False
                    else:
                        write_row.append(dict[char])
                elif char == 'っ':
                    double = True
                elif char == '）':
                    if write_row[-1] == 'N':
                        write_row.append('N')
                elif char in {'ゃ', 'ゅ', 'ょ'}:
                    if char == 'ゃ':
                        last_word = 'A'
                    elif char == 'ゅ':
                        last_word = 'U'
                    else:
                        last_word = 'O'
                    write_row[-1] = write_row[-1][0]
                    last_vowel = write_row[-1]
                    if last_vowel == 'S':
                        write_row.append('H' + last_word)
                    elif last_vowel in {'Z', 'J'}:
                        write_row.pop()
                        write_row.append('J' + last_word)
                    else:
                        write_row.append('Y' + last_word)
                elif char in {'、', '。'}:
                    write_row.append(char)
                else:
                    print('error')
            if char == '（':
                flag = True
        write_rows.append(write_row)
    print(write_rows)


# %%
with open('./applications/views/characters/edited_words.csv') as f:
    rows = list(csv.reader(f))
selected_rows = sample(rows, 15)
proverbs = []
for proverb in selected_rows:
    string = ''.join(proverb)
    lis = re.split('（|）', string)
    proverbs.append(lis)
proverbs = dict(enumerate(proverbs, 1))
pprint.pprint(proverbs)
