import os
import re
import time
import nltk

from nltk import word_tokenize

# download the Reuter's-21578 corpus onto computer.
# use that version of the corpus, not the one available in NLTK.
corpus_path = '../reuters21578'

# result directory
result_output_directory = 'Result/'

# result files
sub_problem_one_output_file = "postings-list.txt"

# the dictionary of punctuations
punctuations = '''=\'+!()[]{};:",<>./`?@#$%^&*_~'''

# dictionary key value pairs of terms in corpus
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
def construct_posting_list():
    for doc_ID_pair in F:
        posting_list = dictionary.get(doc_ID_pair[0])
        if posting_list is None:
            dictionary[doc_ID_pair[0]] = []
        dictionary.get(doc_ID_pair[0]).append(doc_ID_pair[1])


def store_in_disk():
    with open(result_output_directory + sub_problem_one_output_file, "w") as f:
        f.write(str(dictionary))


if __name__ == '__main__':
    start = time.time()
    F = []
    files = read_from_file()
    # iterate all .sgm files
    counts = 0
    pairs_num = 10000
    for file in files:
        # if pairs_num < 0:
        #     break
        # get single document
        for document in re.findall("<REUTERS TOPICS.*?</REUTERS>", file.replace('\n', ' ')):
            document = document.replace("&lt", "")
            document = document.replace("&#3;", "")
            title_group = re.search("<TITLE>.*?</TITLE>", document)
            if title_group is None:
                continue
            title = title_group.group()[7: -8]
            body_group = re.search("<BODY>.*?</BODY>", document)
            if body_group is not None:
                body = body_group.group()[6: -7]
            else:
                body = None
            docID = re.search('''NEWID="[0-9]+"''', document).group()[7:-1]
            if docID is None:
                continue
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
                            F.append([single, docID])
                            pairs_num -= 1
                        flag = False
                        break
                    if character in punctuations:
                        token_list = list(token)
                        token_list.pop(token.index(character))
                        token = "".join(token_list)
                if flag:
                    F.append([token, docID])
                    pairs_num -= 1

    F = sorted(F, key=(lambda x: [x[0]]))
    print("sort completed!")

    F = remove_duplicate(F)
    print("removal completed!")

    construct_posting_list()

    end = time.time()
    print("the total time of 10000 term-docID pairs of naive indexer is " + str("%.2f" % ((end - start) * 1000)) + " ms")

    store_in_disk()









