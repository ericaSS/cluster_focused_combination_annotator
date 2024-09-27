import os

def main():
    input_case_filename = 'CDIT_C3_clean_091324.txt'
    
    file_count = 0

    data_folder_path = "test_folder"
    if not os.path.exists(data_folder_path):
        os.makedirs(data_folder_path)

    with open(input_case_filename, 'r', encoding='utf-8') as readfile:
        lines_cur_file = []
        last_sentence = ''
        for line in readfile:
            temp_line = line.split('\t')
            if last_sentence == '' or temp_line[5] == last_sentence:
                lines_cur_file.append(line)
            else:    
                with open(data_folder_path + '\\' + str(file_count) + ".txt", "w") as file:
                    if len(lines_cur_file) > 0:
                        file.writelines(lines_cur_file)
                        file_count += 1
                    lines_cur_file = [line]
            last_sentence = temp_line[5]
    
    print("Number of files:", file_count)
    

if __name__=="__main__":
    main()