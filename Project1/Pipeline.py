import sys
import os
import re

# use NLTK for this project.
import nltk
from nltk import word_tokenize

# download the Reuter's-21578 corpus onto computer.
# use that version of the corpus, not the one available in NLTK.
corpus_path = '../reuters21578'
result_output_directory = 'Result/'
step_one_output_file = 'step1.txt'
step_two_output_file = 'step2.txt'

documents = []


# pipeline step one: read the Reuter's collection and extract the raw text of each article from the corpus
def read_and_extract():
    for file_name in sorted(os.listdir(corpus_path)):
        if file_name.endswith('.sgm'):
            with open(os.path.join(corpus_path, file_name), 'r', encoding='latin-1') as f:
                reuters_file_content = f.read()
                yield reuters_file_content


# execution of pipeline step one
def step_one_execute():
    if len(sys.argv) < 2:
        document_number = 5
    else:
        document_number = int(sys.argv[1])

    files = read_and_extract()
    count = 0

    for file in files:
        for document in re.findall("<REUTERS TOPICS.*?</REUTERS>", file.replace('\n', ' ')):
            title = re.search("<TITLE>.*?</TITLE>", document).group()[7: -8]
            body = re.search("<BODY>.*?</BODY>", document).group()[6: -7]
            if body is not None:
                content = title + ' ' + body
                document_output_directory = result_output_directory + str(count + 1) + '/'
                if not os.path.exists(document_output_directory):
                    os.makedirs(document_output_directory)
                with open(document_output_directory + step_one_output_file, "w") as f:
                    f.write(content)
                count += 1
            if count == document_number:
                return


# execution of pipeline step two
def step_two_execute():
    count = 0
    document_output_directory = result_output_directory + str(count + 1) + '/'

    while os.path.exists(document_output_directory):
        for line in open(document_output_directory + step_one_output_file):
            content = line.replace('\n', '')
            tokens = word_tokenize(content)

        specific_symbol = '''!()-[]{};:'",<>./``''?@#$%^&*_~'''
        token_list = []

        for token in tokens:
            digital_number = False
            for character in token:
                if character in '''0123456789''':
                    digital_number = True
                    break
            if token not in specific_symbol and token != '--' and not digital_number:
                token_list.append(token)

        if not os.path.exists(result_output_directory):
            os.makedirs(result_output_directory)

        with open(document_output_directory + step_two_output_file, "w") as f:
            f.write(str(token_list))
        document_output_directory = result_output_directory + str(count + 1) + '/'
        count += 1


if __name__ == '__main__':

    print("pipeline step one start.")
    step_one_execute()
    print("pipeline step one finish.")

    print("pipeline step two start.")
    step_two_execute()
    print("pipeline step two finish.")
