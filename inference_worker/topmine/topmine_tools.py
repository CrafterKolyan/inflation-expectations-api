#
# Created by Maksim Eremeev (mae9785@nyu.edu)
#


def create_topmine_input(texts, output_path):
    topmine_input = ''
    for i, doc in enumerate(texts):
        topmine_input += f'{i} {doc["title"]} {doc["body"]}\n'
    topmine_input = topmine_input[:-1]
    with open(output_path, 'w') as f:
        f.write(topmine_input)
    return topmine_input


def add_ngrams(transformed_file_path, texts, tf):
    with open(transformed_file_path, 'r') as f:
        for line in f:
            tokens = line.split()
            id = int(tokens[0])

            texts[id]['bigrams'] = ''
            texts[id]['trigrams'] = ''
            texts[id]['fourgrams'] = ''

            ngram_mapping = {2: 'bigrams', 3: 'trigrams', 4: 'fourgrams'}

            for token in tokens[1:]:
                n = len(token.split('_'))
                if 1 < n < 5:
                    texts[id][ngram_mapping[n]] += f'{token} '
                if token not in tf:
                    tf[token] = 0
                tf[token] += 1

    return texts, tf