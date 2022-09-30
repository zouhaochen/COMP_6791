from nltk import word_tokenize
import os
import re
import time

pipeline_output_file = "postings-list.txt"
path = '../reuters21578'
punctuations = '''=\'+!()[]{};:",<>./`?@#$%^&*_~'''
dictionary = {}


def read_from_file():
    for file in os.listdir(path):
        # find all files ending with .sgm in the folder
        if file.endswith('.sgm'):
            # use latin-1 to decode some characters excluded in utf-8 or gbk
            with open(os.path.join(path, file), 'r', encoding='latin-1') as f:
                reuters_file_content = f.read()
                yield reuters_file_content


def remove_duplicate(F):
    new_list = []
    for index in range(len(F) - 1):
        if F[index][0] != F[index + 1][0] or F[index][1] != F[index + 1][1]:
            new_list.append([F[index][0], F[index][1]])
    new_list.append([F[index][0], F[index][1]])
    return new_list


def construct_posting_list():
    for pair in F:
        posting_list = dictionary.get(pair[0])
        if posting_list is None:
            dictionary[pair[0]] = []
        dictionary.get(pair[0]).append(pair[1])


def store_in_disk():
    with open(pipeline_output_file, "w") as f:
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









