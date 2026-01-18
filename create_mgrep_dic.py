infile = "/Users/shuxinzhou/Desktop/NLP/Disease_ABBR/disease_ontology.tsv"

index = 1
#
with open('/Users/shuxinzhou/Desktop/NLP/Disease_ABBR/DOID_mgrep_dict_0405.txt', 'w') as outfile:
    with open(infile, 'r') as f:
        for line in f:
            tokens = line.strip().split('\t')

            if len(tokens) <= 1:
                continue
            tokens = tokens[1:]

            for token in tokens:
                if len(token) == 0:
                    continue
                if "|" in token:
                    synonyms = token.split('|')
                    for syn in synonyms:
                        outfile.write(str(index) + '\t' + syn + '\n')
                else:
                    outfile.write(str(index) + '\t' + token + '\n')
            index += 1

# with open('/Users/shuxinzhou/Desktop/cido_dict.txt', 'w') as outfile:
#     with open(infile, 'r') as f:
#         for line in f:
#             tokens = line.strip().split('\t')
#             id = tokens[0]
#
#             if len(tokens) <= 1:
#                 continue
#             tokens = tokens[1:]
#
#             for token in tokens:
#                 if len(token) == 0:
#                     continue
#                 outfile.write(str(index) + '\t'+ id + '\t' + token + '\n')
#             index +=1
#
# with open('/Users/shuxinzhou/Desktop/cido-new.txt', 'w') as outfile:
#     with open(infile, 'r') as f:
#         for line in f:
#             tokens = line.strip().split('\t')
#
#             if len(tokens) <= 1:
#                 continue
#             tokens = tokens[1:]
#
#             for token in tokens:
#                 if len(token) == 0:
#                     continue
#                 outfile.write(token + '\n')
#             index +=1