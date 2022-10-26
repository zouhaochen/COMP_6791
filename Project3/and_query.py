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


def get_intersection(listA, res):
    tmp = []
    i = 0
    j = 0
    if len(res) == 0:
        return listA
    while i < len(listA) and j < len(res):
        if int(listA[i]) == int(res[j]):
            tmp.append(listA[i])
            i += 1
            j += 1
        elif int(listA[i]) > int(res[j]):
            j += 1
        else:
            i += 1
    return tmp


if __name__ == '__main__':
    with open(pipeline_output_file, "r") as f:
        dic = eval(f.read())
        while True:
            print("please input the query term: ")
            query = input()
            term_list = get_term_lsit(query)
            res = []
            for term in term_list:
                res = get_intersection(dic.get(term), res)
                if len(res) == 0:
                    print("No result found")
                    break
            if len(res) > 0:
                print(res)