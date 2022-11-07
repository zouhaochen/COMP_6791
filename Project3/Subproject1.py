import os
import json
import time
import nltk

naive_index = dict()
spimi_index = dict()
path = '../reuters21578'


# extract body content text
def body_content(body):
    # while list for text content
    white_list = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 \n')

    body = ''.join(filter(white_list.__contains__, body))


# segment document file content text
def segment_document(file):
    # regular expression
    document_regex = r"<REUTERS.*?>.*?</REUTERS>"
    body_regex = r"<BODY>(.*?)</BODY>"
    id_regex = r'NEWID="(.*?)"'

    documents = nltk.regexp_tokenize(file, document_regex)

    # extract document from corpus and attach id
    for document in documents:
        document_id = nltk.regexp_tokenize(document, id_regex)
        body = nltk.regexp_tokenize(document, body_regex)
        if len(body) == 0:
            body = ""
        else:
            body = body[0]
        body_content(body)
        body = body.replace('\n', ' ')
        body = body.replace('/', ' ')
        body = " ".join(body.split())
        yield document_id, [token for token in body.split(' ')]


# read content from document files end with .sgm in the corpus
def read_from_file(file_path):
    os.chdir(file_path)

    for file_name in sorted(os.listdir(".")):
        if file_name.endswith(".sgm"):
            file = open(file_name, 'r', encoding='utf-8', errors='ignore')
            file_content = file.read()
            file_number = file_name[-6:-4]
            yield file_number, file_content


# pre process step for naive indexer: 10000 pairs
def pre_processing(F):
    pair_number = 0

    for file_num, file_content in read_from_file(path):
        for id_list, token_list in segment_document(file_content):
            for token in token_list:
                if len(token) != 0:
                    F.append((token, id_list[0]))
                    pair_number += 1
                if pair_number == 10000:
                    return F
    return F


# remove duplicate and sort
def remove_duplicate_and_sort(F):
    print()
    print('before remove duplicates in F: ', len(F), 'pairings in dictionary')
    F = list(set(F))
    print('finish remove duplicates in F: ', len(F), 'pairings in dictionary')
    F = sorted(F, key=lambda t: (t[0], int(t[1])))
    print("finish sort F")
    return F


# inverted index
def invert(F):
    naive_index.clear()

    for term, document_id in F:
        if term not in naive_index:
            naive_index[term] = []
        naive_index[term] = naive_index[term] + [document_id]
    print()
    print(f'total number of terms in index: {len(naive_index.keys())}')
    return naive_index


# naive indexer implementation from previous project
def naive_indexer(num):
    F = []
    pre_processing(F)
    F = remove_duplicate_and_sort(F)
    invert(F)


# SPIMI implementation
def SPIMI(index_list, pairing_number):
    file = read_from_file(path)
    number_count = 0

    for number, content in file:
        for id_list, token_list in segment_document(content):
            for token in token_list:
                if token not in index_list:
                    index_list[token] = []
                if len(token) != 0:
                    index_list[token].append(id_list[0])
                    number_count += 1
                if pairing_number == number_count:
                    print(str(pairing_number) + ' term-docID pairings processed')
                    return
    print(str(pairing_number) + ' term-docID pairings processed')


if __name__ == '__main__':
    # record the result
    result = ""

    # record the time for SPIMI indexer
    spimi_start_time = time.time()
    SPIMI(spimi_index, 10000)
    spimi_end_time = time.time()

    # record the time for naive indexer
    n_t0 = time.time()
    naive_indexer(10000)
    n_t1 = time.time()

    output = 'Time for SPIMI: ' + str(spimi_end_time - spimi_start_time) + ' second.'
    print(output)
    result += output
    result += '\n'

    output = 'Time for naive indexer: ' + str(n_t1 - n_t0) + ' second.'
    print(output)
    result += output
    result += '\n'

    f = open('../Project3/Result/sub—project1.txt', 'w')
    f.write(result)
    f.close()

    json.dump(spimi_index, open('../Project3/Result/index.json', "w", encoding="utf−8"), indent=3)
