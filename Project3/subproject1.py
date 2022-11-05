from nltk import word_tokenize
import os
import re
import time

pipeline_output_file = "posting-list.txt"
result_output_directory = 'Result/'
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


if __name__ == '__main__':
    pairs_num = 10000
    start = time.time()
    files = read_from_file()
    # iterate all .sgm files
    counts = 0
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
                            dictionary_token_list = dictionary.get(single)
                            if dictionary_token_list is None:
                                tmp_list = [docID]
                                dictionary[single] = tmp_list
                                pairs_num -= 1
                            else:
                                if dictionary_token_list[len(dictionary_token_list) - 1] != docID:
                                    dictionary_token_list.append(docID)
                                    pairs_num -= 1
                        flag = False
                        break
                    if character in punctuations:
                        token_list = list(token)
                        token_list.pop(token.index(character))
                        token = "".join(token_list)
                if flag:
                    dictionary_token_list = dictionary.get(token)
                    if dictionary_token_list is None:
                        tmp_list = [docID]
                        dictionary[token] = tmp_list
                        pairs_num -= 1
                    else:
                        if dictionary_token_list[len(dictionary_token_list) - 1] != docID:
                            dictionary_token_list.append(docID)
                            pairs_num -= 1
    end = time.time()
    print("the total time of 10000 term-docID pairs in assignment3 is " + str("%.2f" % ((end - start) * 1000)) + " ms")







