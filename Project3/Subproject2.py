from nltk import word_tokenize
import math
import os
import re

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
                length += len(word_tokenize(title + " " + body))
            else:
                length += len(word_tokenize(title))
    return length / N


def get_ranked_document_list(files, L_aver, query, dic):
    ranked = {}
    length = 0
    for file in files:
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
                    rank += math.log(N / document_frequency, 10) * (k1 + 1) * term_frequency / (k1 * ((1 - b) + b * len(tokens) / L_aver) + term_frequency)
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
            print("please input the query term: ")
            query = input()
            term_list = query.split(" ")

            document_list = get_ranked_document_list(read_from_file(), L_aver, term_list, dic)
            print(sorted(document_list.items(), key = lambda kv:(kv[1], kv[0]), reverse=True))


