import nltk
from nltk import word_tokenize
import math
import os

pipeline_output_file = "posting-list.txt"
path = '../reuters21578'
punctuations = '''=\'+!()[]{};:",<>./`?@#$%^&*_~'''
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


def get_L_aver(files):
    length = 0
    for file in files:
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

            docID = nltk.regexp_tokenize(document, '''NEWID="[0-9]+"''')[0][7:-1]
            if docID is None:
                continue
            if title is not None and body is not None:
                length += len(word_tokenize(title + " " + body))
            else:
                length += len(word_tokenize(title))
    return length / N


def get_ranked_document_list(files, L_aver, query, dic):
    ranked = {}
    length = 0

    for file in files:
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

            docID = nltk.regexp_tokenize(document, '''NEWID="[0-9]+"''')[0][7:-1]
            if docID is None:
                continue

            if title is not None and body is not None:
                tokens = word_tokenize(title + " " + body)
            else:
                tokens = word_tokenize(title)
            for token in tokens:
                for character in token:
                    if character in punctuations:
                        token_list = list(token)
                        token_list.pop(token.index(character))
                        token = "".join(token_list)
            rank = 0
            for term in query:
                for character in term:
                    if character in punctuations:
                        token_list = list(term)
                        token_list.pop(term.index(character))
                        term = "".join(token_list)
                if term in tokens:
                    term_frequency = get_term_frequency(term, tokens)
                    document_frequency = len(dic.get(term))
                    rank += math.log(N / document_frequency, 10) * (k1 + 1) * term_frequency / (
                                k1 * ((1 - b) + b * len(tokens) / L_aver) + term_frequency)
            ranked[docID] = rank
    return ranked


def get_term_frequency(term, tokens):
    count = 0
    for token in tokens:
        if token == term:
            count += 1
    return count


if __name__ == '__main__':
    files = read_from_file()
    L_aver = get_L_aver(files)

    with open(pipeline_output_file, "r") as f:
        dic = eval(f.read())
        while True:
            print("please choose your query type and option:")
            print("1. AND query.")
            print("2. OR query.")
            print("3. BM25 query.")
            print("4. Exit.")

            choice = input()

            if choice == 1:
                print()

            elif choice == 2:
                print()

            elif choice == 3:
                print("please input the query term: ")
                query = input()
                term_list = query.split(" ")
                document_list = get_ranked_document_list(read_from_file(), L_aver, term_list, dic)
                print(sorted(document_list.items(), key=lambda kv: (kv[1], kv[0]), reverse=True))

            else:
                False
