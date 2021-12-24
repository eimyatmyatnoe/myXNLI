"""
Run this script from the main directory.
"""

import csv, sys, os, re

if __name__ == '__main__':

    dev_file = 'xnli-original/xnli.dev.tsv'
    test_file = 'xnli-original/xnli.test.tsv'
    parallel_file = 'xnli-origin/xnli.15way.orig.tsv'

    trans_dir = 'translation'
    my_dev_file = 'output/myxnli.dev.tsv'
    my_test_file = 'output/myxnli.test.tsv'

    # Build a dictionary between EN and MY sentences    
    my_dict = {}

    for fname in os.listdir(trans_dir):
        print ('Processing', fname)   
        state = 0

        with open(os.path.join(trans_dir, fname), encoding='utf-8') as infile:            
            for line in infile.readlines():
                line = line.strip()
                if line.startswith('#'):
                    state = 0
                elif re.match('\d+', line):
                    state = 1
                elif state == 1:
                    en_source = line
                    state = 2
                elif state == 2:
                    if line != '<MYANMAR UNICODE TRANSLATION HERE>':
                        my_dict[en_source] = line
                    state = 0
    print ('%d entries loaded to the dictionary' % len(my_dict.keys()))

    # Create DEV and TEST files from the Originals

    for infn, outfn in [(dev_file, my_dev_file), (test_file, my_test_file)]:
        with open(infn, encoding='utf-8') as infile:

            # Write the header
            print ('Writing ', outfn)
            outfile = open(outfn, 'wt', encoding='utf-8')
            outfile.write(infile.readline())

            for line in infile.readlines():
                if line.startswith('en'):
                    cols = line.split('\t')

                    # Column 7 and 8 are the unparsed English sentences
                    sentence1 = cols[6]
                    sentence2 = cols[7]
                   
                    if my_dict.get(sentence1):
                        cols[6] = my_dict[sentence1]

                    if my_dict.get(sentence2):
                        cols[7] = my_dict[sentence2]

                    outfile.write('\t'.join(cols))

            outfile.close()

    # TODO: Add a new column to the parallel corpus
