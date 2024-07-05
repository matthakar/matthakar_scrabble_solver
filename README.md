# matthakar_scrabble_solver

The purpose of this Python script is to help solve the popular puzzle board game, Scrabble. Once inputs are entered, this script will give you the best words to play and their associated point values. However, it also provides all possible moves in case you want to hold onto certain letters during a turn.

Rules summary: In the game of Scrabble, the objective is to get the most points. Each letter is assigned a point value, and each turn the goal is to make a high scoring word by pulling from the 7 randomly chosen letters on your rack. However, you need to connect the word to existing letters on the board. There are also multiplier squares on the board that can enhance the number of points that you get when a letter is placed on them.

The official Scrabble rules can be found here: https://www.scrabblepages.com/scrabble/rules/

The Scrabble dictionary used to pull legal Scrabble words can be found here: https://www.kaggle.com/datasets/bdelanghe/scrabble-dictionary/data

This Script is split into three main parts. Once the scrabble_dictionary_path is defined, only Part 1 requires user input:

Part 1. Manually define input parameters

Part 2. Find all legal Scrabble words based on the input parameters

Part 3. Calculate and display scores associated with the legal words you can make
