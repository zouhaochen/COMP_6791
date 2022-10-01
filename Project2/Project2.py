import os
import time
import nltk

from nltk import word_tokenize
from nltk import re

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


def single_term_query_processing():
    with open(result_output_directory + sub_project_one_output_file, "r") as f:
        term_dictionary = eval(f.read())
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















