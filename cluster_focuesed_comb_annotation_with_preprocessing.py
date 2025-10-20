import os
import argparse
from tqdm import tqdm
import time
import re

def preprocess_data(input_case_filename, output_folder_name):
    #input_case_filename = 'CDIT_C3_clean_091324.txt' #working
    #input_case_filename = 'updated_CDIT_all_matched_clean_11042024.txt'
    
    os.makedirs(output_folder_name, exist_ok=True)
    
    file_index = 0

    with open(input_case_filename, 'r', encoding='utf-8') as f:
        total_lines = sum(1 for _ in f)

    with open(input_case_filename, 'r', encoding='utf-8') as readfile:
        lines_cur_file = []
        last_sentence = ''
        for index, line in enumerate(tqdm(readfile, total=total_lines, desc="Processing lines")):
            temp_line = line.split('\t')
            if last_sentence == '' or temp_line[5] == last_sentence:
                lines_cur_file.append(line)
            else:    
                with open(output_folder_name + '\\' + str(file_index) + ".txt", "w") as file:
                    if len(lines_cur_file) > 0:
                        file.writelines(lines_cur_file)
                        file_index += 1
                    lines_cur_file = [line]
            last_sentence = temp_line[5]

def dfs_dp_maximum_annotates(sorted_concepts, current_concept_index, num_concepts, last_taken_concept, dp):
    if current_concept_index == num_concepts:
        return 0, 0, []
        
    dp_if_not_taken = (0, 0)
    dp_if_taken = (0, 0)
    
    
    if dp[current_concept_index][1] == None:
        future_data = dfs_dp_maximum_annotates(sorted_concepts, current_concept_index + 1, num_concepts,
                            current_concept_index,  
                            dp)
        dp[current_concept_index][1] = future_data[0], future_data[1], future_data[2]
    
    dp_if_not_taken = dp[current_concept_index][1]    
        
    if dp[current_concept_index][0] == None:
        next_possible_concept_index = current_concept_index + 1
        while next_possible_concept_index < num_concepts and sorted_concepts[next_possible_concept_index][0] <= sorted_concepts[current_concept_index][1]:
            next_possible_concept_index += 1

        future_data = dfs_dp_maximum_annotates(sorted_concepts, next_possible_concept_index, num_concepts,
                        current_concept_index,  
                        dp)
        future_concept_list = [current_concept_index]
        if future_data[2] is not None:
            future_concept_list.extend(future_data[2])
            
        dp[current_concept_index][0] = sorted_concepts[current_concept_index][2] + future_data[0], 1 + future_data[1], future_concept_list

    dp_if_taken = dp[current_concept_index][0]
    
      
    future_words_collected_if_taken = dp_if_taken[0]
    future_words_collected_if_not_taken = dp_if_not_taken[0]
    future_concepts_used_if_taken = dp_if_taken[1]
    future_concepts_used_if_not_taken = dp_if_not_taken[1]
    future_concept_list_if_taken = dp_if_taken[2]
    future_concept_list_if_not_taken = dp_if_not_taken[2]
     
    if (future_words_collected_if_taken > future_words_collected_if_not_taken) or (future_words_collected_if_taken == future_words_collected_if_not_taken and future_concepts_used_if_taken < future_concepts_used_if_not_taken):
        return future_words_collected_if_taken, future_concepts_used_if_taken, future_concept_list_if_taken
    else:
        return future_words_collected_if_not_taken, future_concepts_used_if_not_taken, future_concept_list_if_not_taken


def find_best_combination_of_annotates(sorted_concept_list):
    start = time.time()
    
    num_concepts = len(sorted_concept_list)
    dp = []
    for i in range(num_concepts):
        dp.append([None, None])
    result = dfs_dp_maximum_annotates(sorted_concept_list, 0, num_concepts, -1,  dp)
   
    max_words_collected = result[0]
    min_concepts_used = result[1]
    best_concept_list = result[2]
    
    end = time.time()
    
    return max_words_collected, min_concepts_used, best_concept_list, (end - start)

def annotated_single_case(input_mgrep, output_html, annotation_style):
    concept_list = []
    cur_sent = ""
    final_concept_map = None
    with open(input_mgrep, 'r') as f:
        with open(output_html, 'w') as out_file:
            out_file.write('<html>')
            out_file.write('<body>')
            out_file.write(annotation_style)
            for line in f:
                temp_line = line.split('\t')
                cur_sent = temp_line[5]
                concept_list.append((int(temp_line[2]), int(temp_line[3]), len(temp_line[4].split()), temp_line[4]))
                        
            sorted_concept_list = sorted(concept_list)

            final_concept_map = find_best_combination_of_annotates(sorted_concept_list)

            # Write the result to a HTML file
            i = 0
            sentence = temp_line[5]
            entity_type = 'CIT'       
            while i < len(sentence):
                for s in final_concept_map[2]:
                    if(i >= len(sentence) - 1):
                        break
                    concept = sorted_concept_list[s]
                    start_index = concept[0] - 1
                    end_index = concept[1] - 1
                    if start_index <= i <= end_index:
                        out_file.write('<span class="spark-nlp-display-entity-wrapper" style="background-color: #800080"> \
                                       <span class="spark-nlp-display-entity-name">%s</span> \
                                       <span class="spark-nlp-display-entity-type">%s</span></span>' %(sentence[start_index:end_index+1], entity_type))
                        i = i + len(sentence[start_index:end_index+1])
                
                out_file.write('<span class="spark-nlp-display-others" style="background-color: white">%s</span>' %sentence[i])
                i += 1
            out_file.write('<div>')
            out_file.write('<br>')
            out_file.write('</body>')
            out_file.write('</html>')
        out_file.close()
    
    number_of_words = len((re.sub(' +', ' ', cur_sent)).strip().split(' '))
    return final_concept_map[0], final_concept_map[1], number_of_words, final_concept_map[3]

def annotate_data(input_folder_name, output_folder_name, annotation_style):
    file_names = os.listdir(input_folder_name)
    total_time = 0
    total_words_count = 0
    num_anno_count = 0
    num_concepts = 0

    os.makedirs(output_folder_name, exist_ok=True)
    for index, file in enumerate(tqdm(file_names, total=len(file_names), desc="Annotating data")):
    #for file in file_names:
        annotation_html = output_folder_name + "\\" 'sent_' + file + '_new.html'
        file_path = input_folder_name + "\\" + file
        res = annotated_single_case(file_path, annotation_html, annotation_style)
        num_anno_count += res[0]
        num_concepts += res[1]
        total_words_count += res[2]
        total_time += res[3]
        #print(num_anno_count, num_concepts, total_words_count)
    
    print("Percentage of Annotated Words:", num_anno_count / total_words_count * 100)
    print("#Annotated words / #Concepts:", num_anno_count / num_concepts)
    print("Total time taken by the algorithm:", total_time)

def get_annotation_style():
    # Using Fansy Annotation Styly
    annotation_style = "<style> \
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap'); \
        @import url('https://fonts.googleapis.com/css2?family=Vistol Regular:wght@300;400;500;600;700&display=swap'); \
        \
        .spark-nlp-display-scroll-entities {\
            border: 1px solid #E7EDF0;\
            border-radius: 3px;\
            text-align: justify;\
            \
        }\
        .spark-nlp-display-scroll-entities span {  \
            font-size: 14px;\
            line-height: 24px;\
            color: #536B76;\
            font-family: 'Montserrat', sans-serif !important;\
        }\
        \
        .spark-nlp-display-entity-wrapper{\
        \
            display: inline-grid;\
            text-align: center;\
            border-radius: 4px;\
            margin: 0 2px 5px 2px;\
            padding: 1px\
        }\
        .spark-nlp-display-entity-name{\
            font-size: 14px;\
            line-height: 24px;\
            font-family: 'Montserrat', sans-serif !important;\
            \
            background: #f1f2f3;\
            border-width: medium;\
            text-align: center;\
            \
            font-weight: 400;\
            \
            border-radius: 5px;\
            padding: 2px 5px;\
            display: block;\
            margin: 3px 2px;\
        \
        }\
        .spark-nlp-display-entity-type{\
            font-size: 14px;\
            line-height: 24px;\
            color: #ffffff;\
            font-family: 'Montserrat', sans-serif !important;\
            \
            text-transform: uppercase;\
            \
            font-weight: 500;\
    \
            display: block;\
            padding: 3px 5px;\
        }\
        \
        .spark-nlp-display-entity-resolution{\
            font-size: 14px;\
            line-height: 24px;\
            color: #ffffff;\
            font-family: 'Vistol Regular', sans-serif !important;\
            \
            text-transform: uppercase;\
            \
            font-weight: 500;\
    \
            display: block;\
            padding: 3px 5px;\
        }\
        \
        .spark-nlp-display-others{\
            font-size: 14px;\
            line-height: 24px;\
            font-family: 'Montserrat', sans-serif !important;\
            \
            font-weight: 400;\
        }\
    \
    </style>"

    return annotation_style

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cluster Focused Comb Algorithm")
    parser.add_argument("--input_file", required=True, help="Input_case_filename")
    parser.add_argument("--temp_folder", required=True, help="Processed_output_folder_name")
    parser.add_argument("--out_folder", required=True, help="Final_output_folder_name")

    args = parser.parse_args()

    preprocess_data(args.input_file, args.temp_folder)
    annotation_style = get_annotation_style()
    annotate_data(args.temp_folder, args.out_folder, annotation_style)
