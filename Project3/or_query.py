pipeline_output_file = "./posting-list.txt"
punctuations = '''=\'+!()[]{};:",<>./`?@#$%^&*_~'''


def get_term_lsit(query):
    term_list = []
    for term in query.split(" "):
        for character in term:
            if character in punctuations:
                token_list = list(term)
                token_list.pop(term.index(character))
                term = "".join(token_list)
        term_list.append(term)
    return term_list


def get_intersection(listA, union_dic):
    if listA is None:
        return
    for docId in listA:
        if union_dic.get(docId) is None:
            union_dic[docId] = 1
        else:
            union_dic[docId] = union_dic.get(docId) + 1


if __name__ == '__main__':
    with open(pipeline_output_file, "r") as f:
        dic = eval(f.read())
        while True:
            print("please input the query term: ")
            query = input()
            term_list = get_term_lsit(query)
            union_dic = {}
            for term in term_list:
                get_intersection(dic.get(term), union_dic)
            print(sorted(union_dic.items(), key = lambda kv:(kv[1], kv[0]), reverse=True))