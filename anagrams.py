"""
This is the naive implementation done without regard for time complexity.
Avoids use of libraries etc.
Directed acyclic word graph forthcoming...
"""

import sys
import operator
import re
from timeit import default_timer as timer

anagrams = []
currentdepth = 0

# opens 'wordlist' file and returns each word as element in list
def try_open(filename):
	results = []
	with open(filename) as fp:
		wordlist = fp.readlines()
	for word in wordlist:
		word = word.split()[0]
		results.append(word)
	return results

# Check each word in the word list - are it's characters are a subset of the characters in the input word?
# Also, making sure to not include normal single word anagrams as we are only looking for multi word anagrams
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

def combine_subset(subset, inputword, awesomestring, originalinput):
	subset = wordlist_subset(subset,inputword)
	if len(awesomestring.replace(" ","")) == len(originalinput) and contains_all(awesomestring.replace(" ",""), originalinput):
		anagrams.append(awesomestring)
		print "ANAGRAMS : : ::::  "+ str(len(anagrams))
		splitopop = awesomestring.split(" ")
		poppedword1 = splitopop.pop()
		# poppedword2 = splitopop.pop()
		awesomestring = str(' '.join(splitopop))
		# print "Unshifting the last added words which were " + poppedword1 + " " + poppedword2
		return awesomestring
	elif len(subset) == 0 or len(awesomestring.replace(" ","")) >= len(originalinput):
		splitopop = awesomestring.split(" ")
		poppedword1 = splitopop.pop()
		poppedword2 = splitopop.pop()
		awesomestring = str(' '.join(splitopop))
		print "Unshifting the last added words which were " + poppedword1 + " " + poppedword2
		return awesomestring
	else:
		for i, word in enumerate(subset):
			print("Doing subset word : " + word + " with awesomestring = " + awesomestring)
			if len(awesomestring.replace(" ","")) > len(originalinput) or len(subset)<2:
				print "Looks like we failed at a leaf node - " + awesomestring
				splitopop = awesomestring.split(" ")
				poppedword = splitopop.pop()
				awesomestring = str(' '.join(splitopop))
				print "Unshifting the last added word which was " + poppedword
			elif len(re.findall(r"\b[A-Z|a-z]{1}\b", awesomestring))==1 and len(word)<2:
				print "Skipping "+ word +" because it's a single letter word and we already have one."
			elif len(awesomestring.replace(" ","")) < len(originalinput):
				awesomestring += " " + word
				print "awesome string : " + awesomestring  + " : length :  "+str(len(awesomestring.replace(" ","")))+" / "+str(len(originalinput))
				# print "single letter words : " + str(len(re.findall(r"\b[A-Z|a-z]{1}\b", awesomestring)))
				shorterinput = removecharsfrominput(awesomestring.replace(" ",""), originalinput)
				print("shorterinput  :  " + shorterinput)
				print("subset  :  "+str(subset))
				subsub = wordlist_subset(subset,shorterinput)
				print("sub-subset  :  " + str(subsub))
				awesomestring = combine_subset(subsub, shorterinput, awesomestring, originalinput)
			else:
				print "Skipping...." + word
				print "single letter words : " + str(len(re.findall(r"\b[A-Z|a-z]{1}\b", awesomestring))) + " or the length : " + str(len(awesomestring.replace(" ","")))
				print "========================================================================="

	return awesomestring


def removecharsfrominput(word, inputword):
	print "Removing " + word + " from " + inputword
	charlist = list(inputword)
	if contains_all(word, inputword):
		for char in word:
			charlist.remove(char)
		# Use the leftover letters
		shorterinput = str(''.join(charlist))
		return shorterinput
		print "shorterinput after removing chars : " + shorterinput
	else:
		print "returning nothing !!!"
		return ""


def run(inputword):
	start = timer()
	twowords = []
	mostwords = []
	print('start', start)
	inputword = inputword
	wordlist = try_open("Word_List.txt")
	# subset = wordlist_subset(wordlist, inputword)
	# print(subset)
	# print("Found " + str(len(subset)) + " words in the list that can be formed from the letters in the input.")
	combine_subset(wordlist, inputword, "", inputword)
	print "ANAGRAMS : : FINAL ::::  \n ===================================================================================="+ str(anagrams)
	print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	anagrams.sort(key = len)
	for anagram in anagrams:
		# remove the single word ones
		if len(anagram.strip().split(' ')) == 1:
			anagrams.remove(anagram)
		# find the two word ones
		elif len(anagram.strip().split(' ')) == 2:
			twowords.append(anagram)
	print twowords[0]
	print anagrams[-1]


if __name__ == '__main__': run(sys.argv[1])
