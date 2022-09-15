import sys
import os
import re

path = '../reuters21578'
articles_num = 5
documents = []
output_dir = "Output/"
pipeline_output_file = 'pipeline1.txt'


def read_from_file():
    for file in os.listdir(path):
        # find all files ending with .sgm in the folder
        if file.endswith('.sgm'):
            # use latin-1 to decode some characters excluded in utf-8 or gbk
            with open(os.path.join(path, file), 'r', encoding='latin-1') as f:
                reuters_file_content = f.read()
                yield reuters_file_content


if __name__ == '__main__':
    if len(sys.argv) < 2:
        articles_num = 5
    else:
        articles_num = int(sys.argv[1])
    print('the number of extracted files is ' + str(articles_num))

    files = read_from_file()
    # iterate all .sgm files
    counts = 0
    for file in files:
        # get single document
        for document in re.findall("<REUTERS TOPICS.*?</REUTERS>", file.replace('\n', ' ')):
            title = re.search("<TITLE>.*?</TITLE>", document).group()[7: -8]
            body = re.search("<BODY>.*?</BODY>", document).group()[6: -7]
            if body is not None:
                content = title + ' ' + body
                actual_output_dir = output_dir + str(counts) + '/'
                if not os.path.exists(actual_output_dir):
                    os.makedirs(actual_output_dir)
                with open(actual_output_dir + pipeline_output_file, "w") as f:
                    f.write(content)
                counts += 1
            if counts == articles_num:
                sys.exit()
