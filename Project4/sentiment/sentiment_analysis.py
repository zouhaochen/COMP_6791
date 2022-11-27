
if __name__ == "__main__":
    clusters_6 = []
    clusters_3 = []
    print("3 clusters:")
    for line in open("Kmeans-3.txt", "r", encoding='utf-8'):
        print(eval(line))
        clusters_3.append(eval(line))
    print("3 clusters:")
    for line in open("Kmeans-6.txt", "r", encoding='utf-8'):
        print(eval(line))
        clusters_6.append(eval(line))
    afinn = dict()
    for line in open("AFINN-111.txt"):
        words = line.split('\t')
        afinn[words[0]] = int(words[1])

    print("For scores of 3 clusters:")
    index = 0
    for cluster in clusters_3:
        score = 0
        for term in cluster:
            if afinn.get(term) is not None:
                score += afinn.get(term)
        print("The score for cluster " + str(index) + " is " + str(score))
        index += 1
    index = 0
    print("For scores of 6 clusters:")
    for cluster in clusters_6:
        score = 0
        for term in cluster:
            if afinn.get(term) is not None:
                score += afinn.get(term)
        print("The score for cluster " + str(index) + " is " + str(score))
        index += 1
