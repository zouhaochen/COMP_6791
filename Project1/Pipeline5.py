import os

pipeline_input_file = "pipeline4.txt"
pipeline_output_file = 'pipeline5.txt'
output_dir = "Result/"


if __name__ == '__main__':
    counts = 0
    actual_output_dir = output_dir + str(counts) + '/'
    print("please input the stop word split by ',' like to,a,the")
    stop_word_list = input().split(',')
    while os.path.exists(actual_output_dir):
        for line in open(actual_output_dir + pipeline_input_file):
            token_list = eval(line.replace('\n', ''))
        token_without_stop_word_list = []
        for token in token_list:
            if token not in stop_word_list:
                token_without_stop_word_list.append(token)
        with open(actual_output_dir + pipeline_output_file, "w") as f:
            f.write(str(token_without_stop_word_list))
        actual_output_dir = output_dir + str(counts) + '/'
        counts += 1