# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 01:49:26 2019

@author: zhenw
"""

import time

import random

import re
import collections


import os


os.chdir(r'Your Path')

class HangmanAPI(object):
    def __init__(self):
        self.guessed_letters = []
        
        full_dictionary_location = "words_250000_train.txt"
        self.full_dictionary = self.build_dictionary(full_dictionary_location)        
        self.full_dictionary_common_letter_sorted = collections.Counter("".join(self.full_dictionary)).most_common()
        
        self.current_dictionary = []
        self.response=Response()
        self.show_end=0
        
    def guess(self, word): # word input example: "_ p p _ e "

        # clean the word so that we strip away the space characters
        # replace "_" with "." as "." indicates any character in regular expressions
        #clean_word = word[::2].replace("_",".")
        clean_word = word.replace("_",".")
        
        # find length of passed word
        len_word = len(clean_word)
        
        # grab current dictionary of possible words from self object, initialize new possible words dictionary to empty
        current_dictionary = self.current_dictionary
        new_dictionary = []
                
        
        # create incorrect guessed list and correct guessed list 
        incorrect_list=set(set(self.guessed_letters)-set(list(clean_word)))
        correct_list=set(set(list(clean_word))-incorrect_list)-{'.'}
        
        # iterate through all of the words in the old plausible dictionary
        for dict_word in current_dictionary:
            # when dict_word shorter than target, make sure it does not contain any undesired chars and contains desired chars
            if len(dict_word)<len_word:
                if len(dict_word)<len_word*0.58:
                #if len(dict_word)<5:
                    continue
                if any(ele in dict_word for ele in incorrect_list):
                    continue
                #if correct_list.issubset(set(list(dict_word))):
                dict_word_exclude=dict_word
                to_hide=set(list(dict_word))-set(correct_list)
                for character in list(to_hide):
                    dict_word_exclude=dict_word_exclude.replace(character,'_')
                ## dict_word_exclude is dict_word masking the letters not in word to be guessed
                desiredwords = re.compile(dict_word_exclude)
                if (desiredwords.search(clean_word.replace('.','_'))):
                    new_dictionary.append(dict_word)

            else:
                desiredwords = re.compile(clean_word) 
                if (desiredwords.search(dict_word)):
                    #new_dictionary.append(re.search(clean_word,dict_word).group())
                    if len_word-clean_word.count('.')>len_word*0.3:
                    # if already more than 30% of information has been revealed
                    # only keeps the part in dict_word that matches the word to be guessed
                        new_dictionary.append(re.search(clean_word,dict_word).group())
                    else:
                        if re.match('.*'+clean_word,dict_word):# check if ends with
                            new_dictionary.append(dict_word)
                        elif re.match(clean_word+'*',dict_word):# check if starts with
                            new_dictionary.append(dict_word)
                        else:
                            pass
                
        
        # overwrite old possible words dictionary with updated version
        self.current_dictionary = new_dictionary
        
        
        # count occurrence of all characters in possible word matches
        full_dict_string = "".join(new_dictionary)
        
        c = collections.Counter(full_dict_string)
        sorted_letter_count = c.most_common()                   
        
        guess_letter = '!'

        self.show_end=0
        # return most frequently occurring letter in all possible words that hasn't been guessed yet
        for letter,instance_count in sorted_letter_count:
            if letter not in self.guessed_letters:
                guess_letter = letter
                break
        

        if guess_letter=='!':
            self.show_end=1
            location=[i for i, ltr in enumerate('_'+clean_word+'_') if ltr == '.']
            dictionary=[]
            for i in location:
                word_piece=('_'+clean_word+'_')[max(i-2,0):min(len_word+2,max(i-2,0)+5)]
                dictionary=dictionary+re.findall(word_piece,"_".join(self.full_dictionary))
            dictionary="".join(dictionary).replace('_','')
            sorted_letter_count=collections.Counter(dictionary).most_common()
            for letter,instance_count in sorted_letter_count:
                if letter not in self.guessed_letters:
                    guess_letter = letter
                    break            
        
        # if still no word matches in training dictionary, default back to ordering of full dictionary
        if guess_letter == '!':
            self.show_end=2
            sorted_letter_count = self.full_dictionary_common_letter_sorted
            for letter,instance_count in sorted_letter_count:
                if letter not in self.guessed_letters:
                    guess_letter = letter
                    break
        
        return guess_letter

    ##########################################################
    # You'll likely not need to modify any of the code below #
    ##########################################################
    
    def build_dictionary(self, dictionary_file_location):
        text_file = open(dictionary_file_location,"r")
        full_dictionary = text_file.read().splitlines()
        text_file.close()
        return full_dictionary
                
    def start_game(self, practice=True, verbose=True):
        # reset guessed letters to empty set and current plausible dictionary to the full dictionary
        self.guessed_letters = []
        self.current_dictionary = self.full_dictionary
        
        self.response.new_game(verbose)
        word = self.response.get('word')
        tries_remains = self.response.get('tries_remains')
        
        if verbose:
            print("Successfully start a new game! tries remaining: {0}. Word: {1}.".format(tries_remains, word))
        while tries_remains>0:
            # get guessed letter from user code
            guess_letter = self.guess(word)
                
            # append guessed letter to guessed letters field in hangman object
            self.guessed_letters.append(guess_letter)
            if verbose:
                print("Guessing letter: {0}".format(guess_letter))
           
            self.response.guessing(self.guessed_letters)
            
            status = self.response.get('status')
            tries_remains = self.response.get('tries_remains')
            if status=="success":
                if verbose:
                    print("Successfully finished game")
                return True
            elif status=="failed":
                if verbose:
                    print("Failed for number of trials left equals {0}".format(tries_remains))
                return False
            elif status=="ongoing":
                word = self.response.get('word')
                if verbose:
                    print("game is ongoing with tries remains = {0} and word = {1}".format(tries_remains,word))
        return status=="success"
        
class Response():
    def __init__(self):
        self.status='ongoing'
        self.tries_remains=6
        train_dictionary_location = "words_250000_train.txt"
        test_dictionary_location = "word_test.txt"
        train_dictionary = self.build_dictionary(train_dictionary_location)  
        test_dictionary = self.build_dictionary(test_dictionary_location)  
        self.test_dictionary=list(set(test_dictionary)-set(train_dictionary))
        
    def new_game(self,verbose):
        self.status='ongoing'
        self.tries_remains=6
        self.true_word=self.test_dictionary[random.randint(0,len(self.test_dictionary))]
        if verbose:
            print("the answer is: {0}".format(self.true_word))
        self.word='_'*len(self.true_word)
        
    def guessing(self,gussed_word):
        fnum=0
        word_temp=list(self.word)
        for i in gussed_word:
            if i in self.true_word:
                position=[pos for pos, char in enumerate(self.true_word) if char == i]
                for j in position:
                    word_temp[j]=i
            else:
                fnum=fnum+1
        self.tries_remains=6-fnum
        self.word = ''.join(word_temp)
        if self.tries_remains<0:
            self.status='failed'
        elif self.tries_remains==0:
            if self.word==self.true_word:
                self.status='success'
            else:
                self.status='failed'
        else:
            if self.word==self.true_word:
                self.status='success'
            else:
                self.status='ongoing'
        
    def build_dictionary(self, dictionary_file_location):
        text_file = open(dictionary_file_location,"r")
        full_dictionary = text_file.read().splitlines()
        text_file.close()
        return full_dictionary
    
    
    def get(self,instruction):
        if instruction=='status':
            return(self.status)
        if instruction=='tries_remains':
            return(self.tries_remains)
        if instruction=='word':
            return(self.word)
    
        
api = HangmanAPI()

#api.start_game(practice=1,verbose=True)
t0 = time.clock()
N=10
win=0
slist=[]
send=[]
flist=[]
flist_answer=[]
fend=[]
for i in range(0,N):
    print(i)
    if api.start_game(practice=1,verbose=False):
        win+=1
        slist.append(api.response.word)
        send.append(api.show_end)
    else:
        flist.append(api.response.word)
        flist_answer.append(api.response.true_word)
        fend.append(api.show_end)
        
success_rate = win/N
print('overall success rate = %.3f' % success_rate)
print('time consumed total = %.3f' % (time.clock() - t0))

import pandas as pd
failure_report=pd.DataFrame({'why':fend,'word':flist,'answer':flist_answer})
#[total_practice_runs,total_recorded_runs,total_recorded_successes] = api.my_status() # Get my game stats: (# of tries, # of wins)
#print('run %d practice games out of an allotted 100,000' %total_practice_runs)
