
import os
import re
import time

def dfs_dp_maximum_annotates(sorted_concepts, current_concept_index, num_concepts, dp):
    if current_concept_index == num_concepts:
        return 0, 0, []
    
    if dp[current_concept_index] != None:
        return dp[current_concept_index]


    #Ignoring this concept    
    future_data = dfs_dp_maximum_annotates(sorted_concepts, current_concept_index + 1, 
                            num_concepts,
                            dp)
    dp_if_not_taken= future_data[0], future_data[1], future_data[2]
    

    #Taking this concept    
    next_possible_concept_index = current_concept_index + 1
    while next_possible_concept_index < num_concepts and sorted_concepts[next_possible_concept_index][0] <= sorted_concepts[current_concept_index][1]:
        next_possible_concept_index += 1

    future_data = dfs_dp_maximum_annotates(sorted_concepts, next_possible_concept_index, 
                        num_concepts,  
                        dp)
    future_concept_list = [current_concept_index]
    if future_data[2] is not None:
        future_concept_list.extend(future_data[2])
            
    dp_if_taken = sorted_concepts[current_concept_index][2] + future_data[0], 1 + future_data[1], future_concept_list

    #Find the best one 
    future_words_collected_if_taken = dp_if_taken[0]
    future_words_collected_if_not_taken = dp_if_not_taken[0]
    future_concepts_used_if_taken = dp_if_taken[1]
    future_concepts_used_if_not_taken = dp_if_not_taken[1]
    future_concept_list_if_taken = dp_if_taken[2]
    future_concept_list_if_not_taken = dp_if_not_taken[2]
  
    if (future_words_collected_if_taken > future_words_collected_if_not_taken) or (future_words_collected_if_taken == future_words_collected_if_not_taken and future_concepts_used_if_taken < future_concepts_used_if_not_taken):
        dp[current_concept_index] = future_words_collected_if_taken, future_concepts_used_if_taken, future_concept_list_if_taken
    else:
        dp[current_concept_index] = future_words_collected_if_not_taken, future_concepts_used_if_not_taken, future_concept_list_if_not_taken
    
    return dp[current_concept_index]
    


def find_best_combination_of_annotates(sorted_concept_list):
    start = time.time()
    
    num_concepts = len(sorted_concept_list)
    dp = []
    for i in range(num_concepts):
        dp.append(None)

    result = dfs_dp_maximum_annotates(sorted_concept_list, 0, num_concepts, dp)

    max_words_collected = result[0]
    min_concepts_used = result[1]
    best_concept_list = result[2]
    
    end = time.time()
    
    return max_words_collected, min_concepts_used, best_concept_list, (end - start)

def annotated_single_case(input_mgrep, annotation_style, output_html):
    concept_list = []
    cur_sent = ""
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

            ## Prepare the result
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


def annotate_batch():
    input_folder_name = 'test_folder'
    out_folder_name = 'out_test_folder'
    annotation_style = ""
    with open('annotation_style.txt', 'r') as file:
        annotation_style = file.read()

    file_names = os.listdir(input_folder_name)
    if not os.path.exists(out_folder_name):
        os.makedirs(out_folder_name)

    total_algo_time = 0
    total_words_count = 0
    num_anno_count = 0
    num_concepts = 0
    for file in file_names:
        output_html = out_folder_name + "\\" 'out_' + file + '.html'
        file_path = input_folder_name + "\\" + file
        res = annotated_single_case(file_path, annotation_style, output_html)
        num_anno_count += res[0]
        num_concepts += res[1]
        total_words_count += res[2]
        total_algo_time += res[3]
    
    print(num_anno_count, num_concepts, total_words_count)    
    print("Coverage:", num_anno_count / total_words_count * 100)
    print("Breadth:", num_anno_count / num_concepts)
    print("Total time taken:", total_algo_time)

if __name__=="__main__":
    annotate_batch()