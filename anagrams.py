"""
This is a naive implementation done without regard for time complexity.
Avoids use of libraries etc.
Directed acyclic word graph forthcoming
"""

import sys
import operator
import sets
import re

anagrams = []

def try_open(filename):
	results = []
	with open(filename) as fp:
		wordlist = fp.readlines()
	for word in wordlist:
		word = word.split()[0]
		results.append(word)
	return results

# Check each word in the word list - are it's characters are a subset of the characters in the input word?
def wordlist_subset(wordlist, inputword):
	subset = []
	for word in wordlist:
		if contains_all(word, inputword) == True:
			subset.append(word)
	return subset


# Checks to see if the dictionary word's characters are a subset of the input word's characters
# Does not do the length check...
def contains_all(word, inputword):
	inputword = list(inputword)
	for char in word:
		if char not in inputword:
			return False
		else:
			inputword.remove(char)
	return True

def combine_subsets(subset, inputword, awesomestring, originalinput):
	subset = wordlist_subset(subset,inputword)
	if len(awesomestring.replace(" ","")) == len(originalinput) and contains_all(awesomestring.replace(" ",""), originalinput):
		anagrams.append(awesomestring)
		splitopop = awesomestring.split(" ")
		poppedword1 = splitopop.pop()
		awesomestring = str(' '.join(splitopop))
		return awesomestring
	elif len(subset) == 0 or len(awesomestring.replace(" ","")) >= len(originalinput):
		splitopop = awesomestring.split(" ")
		poppedword1 = splitopop.pop()
		awesomestring = str(' '.join(splitopop))
		return awesomestring
	else:
		for i, word in enumerate(subset):
			if len(awesomestring.replace(" ","")) > len(originalinput) or i == len(subset)-1:
				splitopop = awesomestring.split(" ")
				poppedword = splitopop.pop()
				awesomestring = str(' '.join(splitopop))
			elif len(re.findall(r"\b[A-Z|a-z]{1}\b", awesomestring))==1 and len(word)<2:
				# print "Skipping "+ word +" because it's a single letter word and we already have one."
				continue
			elif len(awesomestring.replace(" ","")) < len(originalinput):
				awesomestring += " " + word
				shorterinput = removecharsfrominput(awesomestring.replace(" ",""), originalinput)
				subsub = wordlist_subset(subset,shorterinput)
				awesomestring = combine_subsets(subsub, shorterinput, awesomestring, originalinput)
			else:
				## 'I think this is covered by the other cases now...
				continue

	return awesomestring


def removecharsfrominput(word, inputword):
	charlist = list(inputword)
	if contains_all(word, inputword):
		for char in word:
			charlist.remove(char)
		# Use the leftover letters
		shorterinput = str(''.join(charlist))
		return shorterinput
	else:
		return ""


def run(inputword):
	twowords = []
	mostwords = []
	inputword = inputword
	wordlist = try_open("Word_List.txt")

	combine_subsets(wordlist, inputword, "", inputword)
	# print str(anagrams)
	print "Found "+ str(len(anagrams)) + " anagrams"
	if len(anagrams) > 0:
		anagrams.sort(key = len)
		for anagram in anagrams:
			# remove the single word ones
			if len(anagram.strip().split(' ')) == 1:
				anagrams.remove(anagram)
			# find the two word ones
			elif len(anagram.strip().split(' ')) == 2:
				twowords.append(anagram)
		if len(twowords) >0:
			print "Two word anagram :: " + twowords[0]
			print "Anagram with the most words :: " + anagrams[-1]
		else:
			print "No two word "
	else:
		print "There were no valid multi-word anagrams found"

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print "Please provide a string to check for anagrams"
	else:
		run(sys.argv[1])
