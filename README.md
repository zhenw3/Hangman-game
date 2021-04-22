# Hangman-game

This is a project that plays Hangman game with rougly 60% success rate.

An example of a hangman game:
suppose the answer is python.
the game will starts with _ _ _ _ _ _
at each round, I can guess a letter.
for instance, in the first round, I guess: e.
Because 'python' doesn't have e. It counts as 1 false.
In second round, I guess: p.
Then it becomes p _ _ _ _ _.

In this project, if I successfully find out what the word is before 6 false guesses, I win. If not, I fail.
For more information on Hangman game:
https://en.wikipedia.org/wiki/Hangman_(game)

The code has 2 objects.
1. Response
This is basically the question setter and judger.
It gives the question (for instance, _ _ _ _ _ _ or p _ t h _ _ ) to HangmanAPI and let it guess a letter.
It also judges if the game should go on or be terminated, either because HangmanAPI succeeds or fails.

2. HangmanAPI
This where all the guessing strategies happen. for detailed explanation of the algorithm, please view "Algorithm by Zhen Wang.pdf"

Data
'words_250000_train.txt'   ---  for training, containing 250000 English words
'word_test.txt'  ---  its difference set with training set is used for testing
