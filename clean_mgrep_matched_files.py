import pandas as pd

# data = pd.read_csv("/Users/shuxinzhou/Desktop/RCIT_A1_dict.txt", sep="\t")
# no_dup = data.drop_duplicates(subset='concept')
# no_dup = no_dup.astype(str)
# no_dup.to_csv('/Users/shuxinzhou/Desktop/no_dup_dict.txt', index=False, sep="\t", encoding='utf-8', header=False)

#mapping the case number to it's annotation results
input_original_mgrep = '/Users/shuxinzhou/mgrep/Cardiology/1000_CDIT/CIT_1000_all_matched_1111.txt'
output_normalized_file = '/Users/shuxinzhou/Desktop/My Work/research/cluster_focused_comb_annotation_algo/CIT_1000_all_matched_clean_1111.txt'
with open(input_original_mgrep, 'r') as readFile, open(output_normalized_file, 'w') as writeFile:
    case = ''
    for line in readFile:
        if line.startswith('train_data_1000/'):
            case = line.split('/')[1].strip()
        else:
            line = case + '\t' + line
            writeFile.write(line)
writeFile.close()

### remove the duplicate lines in the file ###

# with open('/Users/shuxinzhou/Desktop/covid_noDup/codo.tsv', 'r') as in_file, open('/Users/shuxinzhou/Desktop/COVID-19_combined_noDup.tsv', 'w') as out_file:
#     seen = set()
#     for line in in_file:
#         if line[1] in seen:
#             print(line)
#             continue
#         seen.add(line)
#         out_file.write(line)


# with open('/Users/shuxinzhou/Downloads/big.tsv', 'r') as fileOne, open('/Users/shuxinzhou/Downloads/small.tsv', 'r') as fileTwo:
#     #jan_data = oldData.readlines()
#     kept = fileOne.readlines()
#     #jul_data = newData.readlines()
#     compared = fileTwo.readlines()
#
# w = open('/Users/shuxinzhou/Desktop/1st.tsv', 'w', encoding='utf-8')
#
# for line in kept:
#     text_to_compare = line.split("\t")[0].lower()
#     if text_to_compare not in compared.lower():
#         print(text_to_compare)
#
#     else:
#         continue


#### remove the duplicates from kept file ###
#
# with open('/Users/shuxinzhou/Desktop/cido-new.txt', 'r') as keptFile, open('/Users/shuxinzhou/Desktop/covid-19-new.txt', 'r') as dupFile:
#     #jan_data = oldData.readlines()
#     kept = keptFile.readlines()
#     #jul_data = newData.readlines()
#     dup_list = dupFile.readlines()
#     count = 0
#     for line in kept:
#         if line in dup_list:
#             count += 1
#             print(line)
#         # concept = line[1]
#         # if line[1] in dup_list:
#         #     del line
#     print(count)

# with open('/Users/shuxinzhou/Desktop/clean_file.tsv', 'w') as finalFile:
#     for line in kept:
#         finalFile.write(line)



# sort the txt file for finding the single and double character concepts for removing

# lines = open('/Users/shuxinzhou/mgrep/RCIT_C3/sno_july_dict.txt', 'r').readlines()
# output = open('/Users/shuxinzhou/mgrep/RCIT_C3//sno_dict_sorted.txt', 'w')
#
# for line in sorted(lines, key=lambda line:line.split()[1]):
#     output.write(line)
# output.close()

# '''check the duplicates among the cardiology single freq extracted concepts'''
#
# concate_one_file = open('')






