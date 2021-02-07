import csv

def calc_edit_dist(word1, word2):
  '''
  First, create a 2D array to enable dynamic programming.
  Then, use dynamic programming to alculate 
  edit distance between two words.
  '''
  #this method needs fixing
  comparison_matrix = create_comparision_matrix(word1, word2)
  num_rows = len(comparison_matrix)
  num_cols = len(comparison_matrix[0])
  cost_to_replace = 1
  cost_to_insert = 1
  for row in range(1, num_rows):
    for col in range(1, num_cols):
      if row == col:
        if word1[row] == word2[col]:
          comparison_matrix[row][col] = comparison_matrix[row-1][col-1]
        else:
          comparison_matrix[row][col] = comparison_matrix[row-1][col-1] + cost_to_replace
      else:
        comparison_matrix[row][col] = comparison_matrix[row-1][col-1] + cost_to_insert
  return comparison_matrix[num_rows-1][num_cols-1]

def create_comparision_matrix(word1, word2):
  '''
  Create a 2D array with the all entires containing
  all 0s except for the first row and first column
  '''
  word1_length = len(word1)
  word2_length = len(word2)
  comparison_matrix = []
  for i in range(word1_length):
    comparison_matrix.append([])
    for j in range(word2_length):
      comparison_matrix[i].append(0)
  if word1[0] != word2[0]:
    comparison_matrix[0][0] = 2
  for r in range(1, word1_length):
    try:
      if word1[r] == word2[r]:
        comparison_matrix[r][0] = comparison_matrix[r-1][0]
      else:
        comparison_matrix[r][0] = comparison_matrix[r-1][0] + 2
    except:
        comparison_matrix[r][0] = comparison_matrix[r-1][0] + 1
      
  for c in range(1, word2_length):
    comparison_matrix[0][c] = comparison_matrix[0][c-1] + 1
  return comparison_matrix

def load_dictionary_as_list():
  dictionary_as_list = list(open('corncob_lowercase.txt', 'r')) 
  for i in range(len(dictionary_as_list)):
    dictionary_as_list[i] = dictionary_as_list[i].strip()
  return dictionary_as_list

def suggest_word(input_text, dictionary):
  '''
  With the text the user has provided, 
  suggest a word to type.
  '''
  closest_word = '______________________________________________________________________________________'
  for word in dictionary:
    if len(input_text) >= len(word):
      continue
    else:
      if input_text == word[0:len(input_text)]:
        if len(word) < len(closest_word):
          closest_word = word
  if closest_word == '______________________________________________________________________________________':
    closest_word = ''
  return closest_word

def autocorrect_word(input_text, dictionary):
  ''':
  With the text the user has provided, if the 
  the word is not in the dictionary, provide 
  an alternative word that autocorrects the 
  given text.
  '''
  possible_words = ['', '', '']
  least_edit_distances = [9999, 9999, 9999]
  if input_text in dictionary:
    return input_text
  for word in dictionary:
    edit_distance = calc_edit_dist(word, input_text)
    for i in range(len(least_edit_distances)):
      if edit_distance < least_edit_distances[i]:
        least_edit_distances[i] = edit_distance
        possible_words[i] = word
        break   
  print(f"These were the possible words: {possible_words}")
  closest_word = find_most_frequent_word(possible_words) 
  return closest_word

def find_most_frequent_word(possible_words):
  most_frequent_word = possible_words[0]
  highest_frequency = 0
  word_frequencies = convert_frequency_csv_to_array()
  for row in word_frequencies:
    for possible_word in possible_words:
      word = row[1]
      if word == possible_word:
        word_frequency = int(row[2])
        if word_frequency > highest_frequency:
          highest_frequency = word_frequency
          most_frequent_word = word
  return most_frequent_word

def convert_frequency_csv_to_array():
  with open('word_frequency.csv') as word_frequencies_csv:
    csv_reader = list(csv.reader(word_frequencies_csv)) 
    csv_reader = csv_reader[1:]
    return csv_reader

def main():
  while True:
    input_text = input('Enter a word: ')
    dictionary = load_dictionary_as_list()
    if len(input_text) == 0:
      continue
    elif len(input_text) < 2: 
      suggested_word = suggest_word(input_text, dictionary)
    else:
      closest_word = autocorrect_word(input_text, dictionary)
      suggested_word = suggest_word(input_text, dictionary)
      print(f"Did you mean this word? {closest_word}")  
    print(f"Were you about to type: {suggested_word}")
     
main()
