import os

pipeline_input_file = "pipeline2.txt"
pipeline_output_file = 'pipeline3.txt'
output_dir = "Result/"


if __name__ == '__main__':
    counts = 0
    actual_output_dir = output_dir + str(counts) + '/'
    while os.path.exists(actual_output_dir):
        for line in open(actual_output_dir + pipeline_input_file):
            token_list = eval(line)
        smallcase_token_list = []
        for token in token_list:
            smallcase_token_list.append(str.lower(token))
        with open(actual_output_dir + pipeline_output_file, "w") as f:
            f.write(str(smallcase_token_list))
        actual_output_dir = output_dir + str(counts) + '/'
        counts += 1