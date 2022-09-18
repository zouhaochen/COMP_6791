from nltk import word_tokenize
import os

pipeline_input_file = "pipeline1.txt"
pipeline_output_file = 'pipeline2.txt'
output_dir = "Result/"


if __name__ == '__main__':
    counts = 0
    actual_output_dir = output_dir + str(counts) + '/'
    while os.path.exists(actual_output_dir):
        for line in open(actual_output_dir + pipeline_input_file):
            text = line.replace('\n', '')
            tokens = word_tokenize(text)
        special_symbols = '''!()-[]{};:'",<>./``''?@#$%^&*_~'''
        token_list = []
        # clean all special symbols in the tokens
        for token in tokens:
            have_digital = False
            for character in token:
                if character in '''0123456789''':
                    have_digital = True
                    break
            if token not in special_symbols and token != '--' and not have_digital:
                token_list.append(token)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        with open(actual_output_dir + pipeline_output_file, "w") as f:
            f.write(str(token_list))
        actual_output_dir = output_dir + str(counts) + '/'
        counts += 1