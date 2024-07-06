import pandas as pd
from itertools import permutations, combinations

'''
The purpose of this Python script is to help solve the popular puzzle board game, Scrabble. Once inputs are entered, this script will give you the best words to play and their associated point values. However, it also provides all possible moves in case you want to hold onto certain letters during a turn.

Rules summary: In the game of Scrabble, the objective is to get the most points. Each letter is assigned a point value, and each turn the goal is to make a high scoring word by pulling from the 7 randomly chosen letters on your rack. However, you need to connect the word to existing letters on the board. There are also multiplier squares on the board that can enhance the number of points that you get when a letter is placed on them.

The official Scrabble rules can be found here: https://www.scrabblepages.com/scrabble/rules/

The Scrabble dictionary used to pull legal Scrabble words can be found here: https://www.kaggle.com/datasets/bdelanghe/scrabble-dictionary/data

This script is split into three main parts. Once the scrabble_dictionary_path is defined, only Part 1 requires user input:

Part 1. Manually define input parameters 
Part 2. Find all legal Scrabble words based on the input parameters
Part 3. Calculate and display scores associated with the legal words you can make
'''

# define dictionary file path --> only need to update once

scrabble_dictionary_path = r'C:\Users\matth\Documents\Matt Hakar\Python\Github Scripts\matthakar_scrabble_solver_script\scrabble_dictionary.csv'

#assign multiplier squares to number (do not alter)

double_letter_square = '1'
triple_letter_square = '2'
double_word_square = '3'
triple_word_square = '4'

'''
Part 1. Manually define input parameters 
'''

# Input 1: define the letters on your rack as a string - up to 7 (the letter order and capitalization do not matter)

letters_on_rack = 'atbcdro'

# Input 2: define the letter or letters on the board that you want to add to as a string (the letter order matters for multiple letters, the capitalization does not)

letters_on_board = 'a'

# Input 3: define available squares before and after letters_on_board as integers

number_of_squares_before_letters_on_board = 5
number_of_squares_after_letters_on_board = 8

# Input 4: define before and after multiplier square positions (if any) as dictionaries - ex. {position index 1: type of multiplier square 1, position index 2: type of multiplier square 2} --> position index is an integer, type of multiplier square is a variable
# position index example --> index numbers 0 to 5 are positioned like this: 012345'letters_on_board'012345
# valid multiplier variables --> double_letter_square, triple_letter_square, double_word_square, and triple_word_square

before_multipliers = {2: triple_word_square}
after_multipliers = {1: double_letter_square, 4: double_letter_square}

'''
Part 2. Find all valid Scrabble words based on the input parameters
'''
# convert letters_on_rack and letters_on_board strings to lists, convert each element in the lists to lowercase letters

letters_on_rack = list(letters_on_rack)
letters_on_rack = [letter.lower() for letter in letters_on_rack]

letters_on_board = list(letters_on_board)
letters_on_board = [letter.lower() for letter in letters_on_board]

# create base_list, which defines multiplier square positions based on the given inputs. If there are no multiplier squares, the position element in the base_list defaults to '0'

before_list = ['0'] * number_of_squares_before_letters_on_board
after_list = ['0'] * number_of_squares_after_letters_on_board

def replace_squares(string_list, replacements):
    for pos, new_value in replacements.items():
        if 0 <= pos < len(string_list): 
            string_list[pos] = new_value

replace_squares(before_list, before_multipliers)
replace_squares(after_list, after_multipliers)

base_list = before_list + letters_on_board + after_list

# create a lowercase list from the scrabble dictionary

scrabble_dictionary_df = pd.read_csv(scrabble_dictionary_path)
scrabble_word_list = [word.lower() for word in scrabble_dictionary_df['name'].astype(str).tolist()]

# convert scrabble_word_list to a set to decrease runtime when searching for words

scrabble_word_set = set(scrabble_word_list)

# find all positions with numbers in the base_list

num_positions = [i for i, x in enumerate(base_list) if isinstance(x, str) and x.isdigit()]

# find letter permutations that fit in the number positions, the numbers in the base_list define where the letters_on_rack can be placed

permutation_list = []

for r in range(1, len(letters_on_rack) + 1):
    # generate combinations from letters_on_rack, vary the lengths
    for comb in combinations(letters_on_rack, r):
        # generate letter permutations that fit in the number positions
        for perm in permutations(comb):
            temp_list = base_list[:]
            for pos, char in zip(num_positions, perm):
                temp_list[pos] = char
            permutation_list.append(''.join(temp_list))

# create potential_word_list from all letter permutations in the permutation_list

potential_word_list = [''.join([char.lower() for char in item if not char.isdigit()]) for item in permutation_list]

# search scrabble_word_set to find matching words to add to legal_word_list

legal_word_list = [elem for elem in potential_word_list if elem in scrabble_word_set]

# remove duplicate words from resulting legal_word_list

legal_word_list = list(dict.fromkeys(legal_word_list))

'''
Part 3. Calculate and display scores associated with the legal words you can make
'''

# make dictionary to define scrabble_letter_points based on Scrabble rules

scrabble_letter_points = {'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1,'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 
                          'n': 1, 'o': 1,'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1,'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10}

# make sublists for legal words in the legal_word_list

letter_lists = [[char for char in word] for word in legal_word_list]

# define each function to align the legal word with the base_list to map letter multipliers onto letters for each legal word

def find_first_occurrence(letters_on_board, base_list):
    # convert letters_on_board to a list for easier comparison
    letters_list = list(letters_on_board)
    len_letters = len(letters_list)
    first_index = None
    # iterate through base_list to find the first occurrence of letters_on_board
    for i in range(len(base_list) - len_letters + 1):
        if base_list[i:i+len_letters] == letters_list:
            first_index = i
            break
    return first_index

# add NAs to the legal_word_list based on the first occurrence index. This aligns the element positions of matching letters in the letter_list and base_list

number_of_NAs_to_add = find_first_occurrence(letters_on_board, base_list)

NA_list = ['NA']*number_of_NAs_to_add

# define function to calculate the value of a single legal_word given the aligned legal_word and base_list along with the dictionary for scrabble_letter points

def calculate_points(legal_word, base_list, scrabble_letter_points):
    total_points = 0
    multiplier = 1
    for i in range(len(legal_word)):
        # apply double and triple letter multipliers to scrabble_letter_points, update multiplier total for every word multiplier present in the base_list
        if base_list[i] == '1':
            total_points += (2 * scrabble_letter_points.get(legal_word[i], 0))
        elif base_list[i] == '2':
            total_points += (3 * scrabble_letter_points.get(legal_word[i], 0))
        elif base_list[i] == '3':
            total_points += (scrabble_letter_points.get(legal_word[i], 0))
            multiplier *= 2 
        elif base_list[i] == '4':
            total_points += (scrabble_letter_points.get(legal_word[i], 0))
            multiplier *= 3
        else:
            total_points += (scrabble_letter_points.get(legal_word[i], 0))
    # apply the product of the word multipliers to the total_points at the end
    total_points *= multiplier 
    return total_points

# use a for loop to add to the legal_word_name_list and point_list for every legal_word found

legal_word_name_list = []
points_list = []

for legal_word in legal_word_list:
    legal_word_name_list.append(legal_word)
    legal_word = list(legal_word)
    legal_word =  NA_list + legal_word
    # adjust length of the legal_word to equal that of the base_list if they're not already equal
    if len(legal_word) == len(base_list):
        pass
    elif len(legal_word)<len(base_list):
        legal_word = legal_word + (['NA']*(len(base_list)-len(legal_word)))
    # remove NAs from the legal_word and remove the corresponding multipliers from the base_list, append the shortened lists
    legal_word_shortened = []
    base_list_shortened = []
    for word, base in zip(legal_word, base_list):
        if word != 'NA':
            legal_word_shortened.append(word)
            base_list_shortened.append(base)
    # calculate the points for a legal_word using the legal_word_shortened and base_list_shortened lists
    points = calculate_points(legal_word_shortened, base_list_shortened, scrabble_letter_points)
    points_list.append(points)

# convert the legal_word_list and points_list to a single df

legal_word_df = pd.DataFrame(legal_word_list, columns=['legal word:'])
points_df = pd.DataFrame(points_list, columns=['points:'])

output_df = pd.concat([legal_word_df, points_df], axis=1)

# sort the results in alphabetical order for the legal words, and descending order for the points
               
output_df = output_df.sort_values(by = ['points:', 'legal word:'], ascending = [False, True])

# display the results

print('- Legal Scrabble Moves and Associated Points -')
print(output_df.to_string(index=False))




















