import json, string

with open("words.txt") as file:
    words = [line.rstrip() for line in file] 

WORD_COUNT = len(words)

positional_char_frequencies = [{letter: 0 for letter in list(string.ascii_lowercase)} for _ in range(5)] # a separate char count for each space in the word, as the rarity of certain letters changes based on the position in the word.

for word in words:
    for char_idx, char in enumerate(word):
        positional_char_frequencies[char_idx][char] += 1 / WORD_COUNT

positional_score_dict = {}

for word in words:
    positional_score = 0
    unique_chars = [] # list of the unique letters in the word. words with more are preferable as they provide more information

    for char_idx, char in enumerate(word):
        positional_score += positional_char_frequencies[char_idx][char]
        
        if char not in unique_chars:
            unique_chars.append(char) # if letter has not appeared in word previously, add to list

    positional_score *= len(unique_chars) / 5 # multiply the score by the number of unique letters in word. divided by 5 so final score remains between 0 and 1

    positional_score = round(positional_score, 6) # round the score to 6dp so scores aren't too long

    positional_score_dict[word] = positional_score # add word: score pair to dict

positional_score_dict = dict(sorted(positional_score_dict.items(), key=lambda x:x[1], reverse=True)) # sort the dictionaries from highest score to lowest

with open("positional_scores.json", "w") as file:
    json.dump(positional_score_dict, file) # write dict to json file
    