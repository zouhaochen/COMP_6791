import os

step_four_output_file = "step4.txt"
step_five_output_file = 'step5.txt'
result_output_directory = "Result/"


if __name__ == '__main__':
    count = 0
    actual_output_dir = result_output_directory + str(count + 1) + '/'
    print("please input the stop word split by ',' like to,a,the")
    stop_word_list = input().split(',')
    while os.path.exists(actual_output_dir):
        for line in open(actual_output_dir + step_four_output_file):
            token_list = eval(line.replace('\n', ''))
        token_without_stop_word_list = []
        for token in token_list:
            if token not in stop_word_list:
                token_without_stop_word_list.append(token)
        with open(actual_output_dir + step_five_output_file, "w") as f:
            f.write(str(token_without_stop_word_list))
        actual_output_dir = result_output_directory + str(count + 1) + '/'
        count += 1
