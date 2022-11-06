import os
import json
import time
import nltk

index = dict()
path = '../reuters21578'
result_output_directory = 'Result/'


def extract_text(body):
    whitelist = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 \n')
    body = ''.join(filter(whitelist.__contains__, body))


def segment_documents(file):
    doc_regex = r"<REUTERS.*?>.*?</REUTERS>"
    body_regex = r"<BODY>(.*?)</BODY>"
    id_regex = r'NEWID="(.*?)"'
    document = nltk.regexp_tokenize(file, doc_regex)

    for doc in document:
        new_id = nltk.regexp_tokenize(doc, id_regex)
        body = nltk.regexp_tokenize(doc, body_regex)
        if len(body) == 0:
            body = ""
        else:
            body = body[0]
        extract_text(body)
        body = body.replace('\n', ' ')
        body = body.replace('/', ' ')
        body = " ".join(body.split())
        yield new_id, [token for token in body.split(' ')]


def readMsg(path):
    os.chdir(path)
    for file_name in sorted(os.listdir(".")):
        if file_name.endswith(".sgm"):
            f = open(file_name, 'r', encoding='utf-8', errors='ignore')
            file_content = f.read()
            file_num = file_name[-6:-4]
            yield file_num, file_content


def preprocessing(F):
    cur_num = 0
    for file_num, file_content in readMsg(path):
        for id, token_list in segment_documents(file_content):
            for token in token_list:
                if len(token) != 0:
                    F.append((token, id[0]))
                    cur_num += 1
                if cur_num == 10000:
                    return F
    return F


def remove_dup_sort(F):
    print('Length before remove duplicates: ', len(F))
    F = list(set(F))
    print('Length after remove duplicates: ', len(F))
    F = sorted(F, key=lambda t: (t[0], int(t[1])))
    print("Done sorting F")
    # print(*F)
    return F


def invert(F):
    index.clear()
    for term, id in F:
        if term not in index:
            index[term] = []
        index[term] = index[term] + [id]
    print(f'number of terms in index: {len(index.keys())}')
    return index


def sub1(num):
    F = []
    preprocessing(F)
    F = remove_dup_sort(F)
    invert(F)


def SPIMI(index, pairs_num):
    file = readMsg(path)
    cur_num = 0
    for num, content in file:
        for id, token_list in segment_documents(content):
            for token in token_list:
                if token not in index:
                    index[token] = []
                if len(token) != 0:
                    index[token].append(id[0])
                    cur_num += 1
                if (pairs_num == cur_num):
                    print(str(pairs_num) + ' processed')
                    return
    print(str(pairs_num) + ' processed')


if __name__ == '__main__':

    results = ""
    s_index = dict()
    s_t0 = time.time()
    SPIMI(s_index, 10000)
    s_t1 = time.time()

    n_t0 = time.time()
    sub1(10000)
    n_t1 = time.time()

    message = 'SPIMI took: ' + str(s_t1 - s_t0)
    print(message)
    results += message
    results += '\n'

    message = 'Naive took: ' + str(n_t1 - n_t0)
    print(message)
    results += message
    results += '\n'

    f = open('../Project3/Result/subproject1.txt', 'w')
    f.write(results)
    f.close()

    json.dump(s_index, open('../Project3/Result/index_10000.json', "w", encoding="utf−8"), indent=3)
