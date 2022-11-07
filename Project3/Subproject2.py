import nltk
from nltk import word_tokenize
import math
import os

pipeline_output_file = "posting-list.txt"
path = '../reuters21578'
punctuation = '''=\'+!()[]{};:",<>./`?@#$%^&*_~'''

N = 21578
k1 = 1.5
b = 0.75


def read_from_file():
    for file in os.listdir(path):

        # find all files ending with .sgm in the folder
        if file.endswith('.sgm'):
            # use latin-1 to decode some characters excluded in utf-8 or gbk
            with open(os.path.join(path, file), 'r', encoding='latin-1') as f:
                reuters_file_content = f.read()
                yield reuters_file_content


def average_length(corpus_files):
    length = 0

    for file in corpus_files:
        for document in nltk.regexp_tokenize(file.replace('\n', ' '), "<REUTERS TOPICS.*?</REUTERS>"):

            # remove messy code
            document = document.replace("&lt", "")
            document = document.replace("&#1;", "")
            document = document.replace("&#2;", "")
            document = document.replace("&#3;", "")
            document = document.replace("&#5;", "")
            document = document.replace("&#22;", "")
            document = document.replace("&#31;", "")

            # recognize document file title by regular expression
            title_group = nltk.regexp_tokenize(document, "<TITLE>.*?</TITLE>")
            if len(title_group) == 0:
                continue
            title = title_group[0]

            # recognize document file body by regular expression
            body_group = nltk.regexp_tokenize(document, "<BODY>.*?</BODY>")
            if len(body_group) != 0:
                body = body_group[0]
            else:
                body = None

            # recognize document ID by regular expression
            document_id = nltk.regexp_tokenize(document, '''NEWID="[0-9]+"''')[0][7:-1]
            if document_id is None:
                continue
            if title is not None and body is not None:
                length += len(word_tokenize(title + " " + body))
            else:
                length += len(word_tokenize(title))

    return length / N


def term_frequency(term, tokens):
    count = 0
    for token in tokens:
        if token == term:
            count += 1
    return count


def get_ranked_document_list(corpus_files, length_average, search_query, dictionary):
    ranked = {}

    for file in corpus_files:
        for document in nltk.regexp_tokenize(file.replace('\n', ' '), "<REUTERS TOPICS.*?</REUTERS>"):

            # remove messy code
            document = document.replace("&lt", "")
            document = document.replace("&#1;", "")
            document = document.replace("&#2;", "")
            document = document.replace("&#3;", "")
            document = document.replace("&#5;", "")
            document = document.replace("&#22;", "")
            document = document.replace("&#31;", "")

            title_group = nltk.regexp_tokenize(document, "<TITLE>.*?</TITLE>")
            if len(title_group) == 0:
                continue
            title = title_group[0]

            body_group = nltk.regexp_tokenize(document, "<BODY>.*?</BODY>")
            if len(body_group) != 0:
                body = body_group[0]
            else:
                body = None

            document_id = nltk.regexp_tokenize(document, '''NEWID="[0-9]+"''')[0][7:-1]
            if document_id is None:
                continue

            if title is not None and body is not None:
                tokens = word_tokenize(title + " " + body)
            else:
                tokens = word_tokenize(title)

            for token in tokens:
                for character in token:
                    if character in punctuation:
                        token_list = list(token)
                        token_list.pop(token.index(character))
                        token = "".join(token_list)

            rank = 0

            for term in search_query:
                for character in term:
                    if character in punctuation:
                        token_list = list(term)
                        token_list.pop(term.index(character))
                        term = "".join(token_list)
                if term in tokens:
                    term_frequency = term_frequency(term, tokens)
                    document_frequency = len(dictionary.get(term))
                    rank += math.log(N / document_frequency, 10) * (k1 + 1) * term_frequency / (
                            k1 * ((1 - b) + b * len(tokens) / length_average) + term_frequency)
            ranked[document_id] = rank
    return ranked


def get_term_list(query):
    term_list = []

    for term in query.split(" "):
        for character in term:
            if character in punctuation:
                token_list = list(term)
                token_list.pop(term.index(character))
                term = "".join(token_list)
        term_list.append(term)
    return term_list


def intersection_and(term_list, result):
    tmp = []
    i = 0
    j = 0

    if len(result) == 0:
        return term_list
    while i < len(term_list) and j < len(result):
        if int(term_list[i]) == int(result[j]):
            tmp.append(term_list[i])
            i += 1
            j += 1
        elif int(term_list[i]) > int(result[j]):
            j += 1
        else:
            i += 1
    return tmp


def intersection_or(term_list, union_dictionary):
    if term_list is None:
        return
    for document_id in term_list:
        if union_dictionary.get(document_id) is None:
            union_dictionary[document_id] = 1
        else:
            union_dictionary[document_id] = union_dictionary.get(document_id) + 1


if __name__ == '__main__':
    files = read_from_file()
    file_average_length = average_length(files)

    with open(pipeline_output_file, "r") as f:
        dictionary = eval(f.read())

        loop = True
        while loop:
            print("please choose your query type and option:")
            print("1. AND query.")
            print("2. OR query.")
            print("3. BM25 query.")
            print("4. Exit.")

            choice = input()

            if choice == "1":
                with open(pipeline_output_file, "r") as f:
                    dictionary = eval(f.read())
                    print("please input the query term: ")
                    query = input()
                    term_list = get_term_list(query)
                    res = []
                    for term in term_list:
                        res = intersection_and(dictionary.get(term), res)
                        if len(res) == 0:
                            print("No result found")
                            break
                    if len(res) > 0:
                        print(res)
                print()

            elif choice == "2":
                with open(pipeline_output_file, "r") as f:
                    dictionary = eval(f.read())
                    print("please input the query term: ")
                    query = input()
                    term_list = get_term_list(query)
                    union_dic = {}
                    for term in term_list:
                        intersection_or(dictionary.get(term), union_dic)
                    print(sorted(union_dic.items(), key=lambda kv: (kv[1], kv[0]), reverse=True))
                print()

            elif choice == "3":
                print("please input the query term: ")
                query = input()
                term_list = query.split(" ")
                document_list = get_ranked_document_list(read_from_file(), file_average_length, term_list, dictionary)
                print(sorted(document_list.items(), key=lambda kv: (kv[1], kv[0]), reverse=True))
                print()

            else:
                loop = False
