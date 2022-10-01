import os
import time
import nltk

from nltk import word_tokenize
from nltk import PorterStemmer
from nltk import re

from nltk.corpus import stopwords

from tabulate import tabulate


# download the Reuter's-21578 corpus onto computer.
# use that version of the corpus, not the one available in NLTK.
corpus_path = '../reuters21578'

# result directory
result_output_directory = 'Result/'

# result files
sub_project_one_output_file = "sub-project-1.txt"

# the list of punctuations in the content
punctuations = '''=\'+!()[]{};:",<>./`?@#$%^&*_~'''

# dictionary key value pairs of terms-document ID in corpus
dictionary = {}

update_number = 0


# read content from document files end with .sgm in the corpus
def read_from_file():
    for file in os.listdir(corpus_path):
        if file.endswith('.sgm'):
            with open(os.path.join(corpus_path, file), 'r', encoding='latin-1') as f:
                document_file_content = f.read()
                yield document_file_content


# remove duplicate in the list F
def remove_duplicate(F):
    list_after_remove_duplicate = []
    for index in range(len(F) - 1):
        if F[index][0] != F[index + 1][0] or F[index][1] != F[index + 1][1]:
            list_after_remove_duplicate.append([F[index][0], F[index][1]])
    list_after_remove_duplicate.append([F[index][0], F[index][1]])
    return list_after_remove_duplicate


# turning the docIDs paired with the same term into a postings list
def build_posting_list():
    for doc_ID_pair in F:
        posting_list = dictionary.get(doc_ID_pair[0])
        if posting_list is None:
            dictionary[doc_ID_pair[0]] = []
        dictionary.get(doc_ID_pair[0]).append(doc_ID_pair[1])


# store the dictionary with term-document ID pairs in the list
def store_in_disk():
    with open(result_output_directory + sub_project_one_output_file, "w") as f:
        f.write(str(dictionary))


# sub project one module
def naive_indexer(F):
    files = read_from_file()

    # recursively store term-document IDs pairs from the documents
    for file in files:
        for document in re.findall("<REUTERS TOPICS.*?</REUTERS>", file.replace('\n', ' ')):

            # remove messy code
            document = document.replace("&lt", "")
            document = document.replace("&#1;", "")
            document = document.replace("&#2;", "")
            document = document.replace("&#3;", "")
            document = document.replace("&#5;", "")
            document = document.replace("&#22;", "")
            document = document.replace("&#31;", "")

            # recognize document file title in tokens list
            file_title_set = re.search("<TITLE>.*?</TITLE>", document)
            if file_title_set is None:
                continue
            title = file_title_set.group()[7: -8]

            # recognize document file body in tokens list
            file_body_set = re.search("<BODY>.*?</BODY>", document)
            if file_body_set is not None:
                body = file_body_set.group()[6: -7]
            else:
                body = None

            # generate document ID
            document_id = re.search('''NEWID="[0-9]+"''', document).group()[7:-1]
            if document_id is None:
                continue

            # while there are documents to be processed
            # accepts a document as a list of tokens
            # outputs term-documentID pairs to a list F
            if title is not None and body is not None:
                tokens = word_tokenize(title + " " + body)
            else:
                tokens = word_tokenize(title)
            for token in tokens:
                if token == "''":
                    continue
                if len(token) == 1 and token in punctuations:
                    continue
                flag = True
                for character in token:
                    if character == '-':
                        tmp = token.split('-')
                        for single in tmp:
                            F.append([single, document_id])
                        flag = False
                        break
                    if character in punctuations:
                        token_list = list(token)
                        token_list.pop(token.index(character))
                        token = "".join(token_list)
                if flag:
                    F.append([token, document_id])


# sub project two module
def single_term_query_processing():
    with open(result_output_directory + sub_project_one_output_file, "r") as f:
        term_dictionary = eval(f.read())

        # loop for processing single term query
        while True:
            print("please enter the single term query: ")
            term = input()
            posting_list = term_dictionary.get(term)
            if posting_list is None:
                print("no this term")
                continue

            print("posting list length: " + str(len(posting_list)))
            print(posting_list)

            print("do you want to continue? y/n")
            choice = input()
            if choice == "y":
                continue
            if choice == "n":
                break


# table of statistic about term without numbers
def no_numbers(information, term_dictionary):
    number = 0

    for key in term_dictionary.keys():
        number += len(term_dictionary.get(key))
    information.get('number (non positional postings)').append(number)

    keys_to_be_removed = []

    for key in term_dictionary.keys():
        if re.search("[0-9]", key) is not None:
            keys_to_be_removed.append(key)

    for key in keys_to_be_removed:
        term_dictionary.pop(key)

    global update_number

    term_list = information.get('number (distinct terms)')
    term_list.append(len(term_dictionary))
    information.get('Δ %').append('{:0.2f}'.format(-100 * (term_list[0] - term_list[1]) / term_list[0]))
    information.get('T %').append('{:0.2f}'.format(-100 * (term_list[0] - term_list[1]) / term_list[0]))


# table of statistic about non positional postings
def non_positional_postings(information, term_dictionary):
    number = 0

    for key in term_dictionary.keys():
        number += len(term_dictionary.get(key))

    term_list = information.get('number (non positional postings)')
    term_list.append(number)
    information.get('Δ % ').append('{:0.2f}'.format(-100 * (term_list[0] - term_list[1]) / term_list[0]))
    information.get('T % ').append('{:0.2f}'.format(-100 * (term_list[0] - term_list[1]) / term_list[0]))


# table of statistic about non positional postings with index
def non_positional_postings_with_index(information, term_dictionary, index):
    number = 0

    for key in term_dictionary.keys():
        number += len(term_dictionary.get(key))

    term_list = information.get('number (non positional postings)')
    term_list.append(number)
    information.get('Δ % ').append('{:0.2f}'.format(-100 * (term_list[index] - term_list[index + 1]) / term_list[index]))
    information.get('T % ').append('{:0.2f}'.format(-100 * (term_list[0] - term_list[index + 1]) / term_list[0]))


# merge list in order
def merge_list(upper_list, lower_list):
    temp_list = []
    i = 0
    j = 0

    while i < len(upper_list) and j < len(lower_list):
        if int(upper_list[i]) < int(lower_list[j]):
            temp_list.append(upper_list[i])
            i += 1
        elif int(upper_list[i]) > int(lower_list[j]):
            temp_list.append(lower_list[j])
            j += 1
        else:
            temp_list.append(upper_list[i])
            i += 1
            j += 1

    while j < len(lower_list):
        temp_list.append(lower_list[j])
        j += 1

    while i < len(upper_list):
        temp_list.append(upper_list[i])
        i += 1

    return temp_list


# table of statistic about case folding
def case_folding(information, term_dictionary):
    new_term_dictionary = {}

    for key in term_dictionary:
        if new_term_dictionary.get(key.lower()) is None:
            new_term_dictionary[key.lower()] = term_dictionary.get(key)
        else:
            new_term_dictionary[key.lower()] = merge_list(term_dictionary.get(key), new_term_dictionary[key.lower()])

    term_list = information.get('number (distinct terms)')
    term_list.append(len(new_term_dictionary))
    information.get('Δ %').append('{:0.2f}'.format(-100 * (term_list[1] - term_list[2]) / term_list[1]))
    information.get('T %').append('{:0.2f}'.format(-100 * (term_list[0] - term_list[2]) / term_list[0]))
    return new_term_dictionary


# table of statistic about remove stop words from terms
def remove_stop_word(information, term_dictionary, number, index):
    stopwords_list = stopwords.words('english')[0: number - 1]
    new_term_dictionary = {}

    for key in term_dictionary.keys():
        if key not in stopwords_list:
            new_term_dictionary[key] = term_dictionary.get(key)

    term_list = information.get('number (distinct terms)')
    term_list.append(len(new_term_dictionary))
    information.get('Δ %').append('{:0.2f}'.format(-100 * (term_list[2] - term_list[index]) / term_list[2]))
    information.get('T %').append('{:0.2f}'.format(-100 * (term_list[0] - term_list[index]) / term_list[0]))
    return new_term_dictionary


# table of statistic about stemming
def stemming_list(information, term_dictionary, index):
    new_term_dictionary = {}

    for key in term_dictionary.keys():
        term_after_stemming = PorterStemmer().stem(key)
        if new_term_dictionary.get(term_after_stemming) is None:
            new_term_dictionary[term_after_stemming] = term_dictionary.get(key)
        else:
            new_term_dictionary[term_after_stemming] = merge_list(new_term_dictionary[term_after_stemming], term_dictionary.get(key))

    term_list = information.get('number (distinct terms)')
    term_list.append(len(new_term_dictionary))
    information.get('Δ %').append('{:0.2f}'.format(-100 * (term_list[index - 1] - term_list[index]) / term_list[index - 1]))
    information.get('T %').append('{:0.2f}'.format(-100 * (term_list[0] - term_list[index]) / term_list[0]))
    return new_term_dictionary


# sub project three module
def lossy_dictionary_compression_implementation():
    with open(result_output_directory + sub_project_one_output_file, "r") as f:
        term_dictionary = eval(f.read())

    information = {' ': ['unfiltered', 'no numbers', 'case folding', '30 stop words', '150 stop words', 'stemming'],
            'number (distinct terms)': [len(term_dictionary)],
            'Δ %': [' '],
            'T %': [' '],
            'number (non positional postings)': [],
            'Δ % ': [' '],
            'T % ': [' ']
            }

    # remove numbers from terms
    no_numbers(information, term_dictionary)
    non_positional_postings(information, term_dictionary)

    # case folding
    term_dictionary = case_folding(information, term_dictionary)
    non_positional_postings_with_index(information, term_dictionary, 1)

    # remove 30 stop words
    stopwords30_dic = remove_stop_word(information, term_dictionary, 30, 3)
    non_positional_postings_with_index(information, stopwords30_dic, 2)

    # remove 150 stop words
    term_dictionary = remove_stop_word(information, term_dictionary, 150, 4)
    non_positional_postings_with_index(information, term_dictionary, 3)

    # implement stemming
    term_dictionary = stemming_list(information, term_dictionary, 5)
    non_positional_postings_with_index(information, term_dictionary, 4)

    print(tabulate(information, headers='keys'))

    while True:
        print("please enter the single term query: ")
        term = input()
        posting_list = term_dictionary.get(PorterStemmer().stem(term))
        if posting_list is None:
            print("no such term.")
            continue
        print("term after stemmed: " + PorterStemmer().stem(term) + ", posting list length: " + str(len(posting_list)))
        print(posting_list)

        print("do you want to continue? y/n")
        choice = input()
        if choice == "y":
            continue
        if choice == "n":
            break


if __name__ == '__main__':

    # sub project one: naive indexer
    print("sub project 1 begin")

    # begin time cumulative reduction
    begin_time = time.time()

    # list F for storing the outputs of term-documentID pairs
    F = []

    # naive indexer step one
    naive_indexer(F)
    print("finish sub project 1 step 1: accepts a document as a list of tokens and outputs term-documentID pairs to list F")

    # naive indexer step two
    F = sorted(F, key=(lambda x: [x[0]]))
    F = remove_duplicate(F)
    print("finish sub project 1 step 2: sort F and remove duplicates")

    # naive indexer step three
    build_posting_list()
    print("finish sub project 1 step 3: turn the sorted F into an index")

    end = time.time()
    print("the overall running time is " + str("%.2f" % ((end - begin_time) * 1000)) + " ms")

    # sub project one result storage
    store_in_disk()
    print("sub project 1 finish")
    print()

    print("sub project 2 begin")
    single_term_query_processing()
    print("sub project 2 finish")
    print()

    print("sub project 3 begin")
    lossy_dictionary_compression_implementation()
    print("sub project 3 finish")
    print()
















