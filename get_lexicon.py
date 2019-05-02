
# coding: utf-8
# AUTHOR: Martino Sorbaro, 2017
# This code is distributed with absolutely no warranty or fitness for purpose.
import nltk
# from nltk.probability import FreqDist
from pandas import read_csv, DataFrame
from numpy import nan, argsort, empty, unique
from bs4 import BeautifulSoup
from gooey import Gooey, GooeyParser
from urllib import request
import os.path


def FreqDist(words):
    word, count = unique(words, return_counts=True)
    return dict(zip(word, count))


@Gooey()
def get_lexicon():
    desc = """
    This programme compares the frequency of a word in general English with its
    frequency in a given text, and returns them in order of frequency ratio."""
    file_help_msg = """
    Name of the file you want to process. You can select a simple text (.txt)
    file on your computer, or paste the URL of a webpage. In this second case,
    it needs to start with 'http' and be UTF8 encoded."""
    out_help_msg = "Save lexicon to this file (will be printed to screen if empty)"

    gparser = GooeyParser(description=desc)

    gparser.add_argument('-m', '--minoccurrences', default=1, type=int,
                         help='Minimum times a word needs to appear in input.')
    gparser.add_argument('-n', '--nshown', default=100, type=int,
                         help='Number of words to be shown.')
    gparser.add_argument('Source', widget="FileChooser",
                         help=file_help_msg)
    gparser.add_argument('-o', '--output', widget="DirChooser", default='',
                         help=out_help_msg)
    args = gparser.parse_args()

    # Load word occurrences in general English
    script_dir = os.path.dirname(__file__)
    english_counts_path = os.path.join(script_dir, 'count_1w.txt')
    en_wf = read_csv(english_counts_path, delimiter='\t', header=None)
    en_freq = dict(zip(en_wf[0], en_wf[1]))
    # hack, fuck it
    en_freq['NaN'] = en_freq[nan]
    del en_freq[nan]

    # Set parameters and load text
    source = args.Source
    if source[:4] == "http":
        # TO READ URL
        # print("Downloading file...")
        response = request.urlopen(source)
        html = response.read().decode('utf8')
        raw = BeautifulSoup(html, "lxml").get_text()
    else:
        # TO READ TXT FILE
        # print("Reading file from computer...")
        f = open(source, 'r')
        raw = f.read()

    # Analyse
    try:
        words = nltk.word_tokenize(raw)
    except LookupError:
        nltk.download('punkt')
        words = nltk.word_tokenize(raw)

    words = [w.lower() for w in words if w.isalpha()]
    freq = FreqDist(words)
    txt_freq = DataFrame.from_dict(freq, orient='index')
    enfreq = empty(len(txt_freq))

    for i, w in enumerate(txt_freq.index):
        try:
            enfreq[i] = en_freq[w]
        except KeyError:
            enfreq[i] = 0.

    txt_freq['ratio'] = enfreq / txt_freq[0]
    txt_freq['enfreq'] = enfreq / sum(enfreq)
    txt_freq['txtfreq'] = txt_freq[0] / txt_freq[0].sum()

    txt_freq_over = txt_freq[txt_freq[0] > args.minoccurrences]
    lex = list(txt_freq_over.index[argsort(
        txt_freq_over['ratio'])][:args.nshown])

    # # save to file
    if args.output != '':
        source_base = os.path.splitext(os.path.basename(source))[0]
        fname = os.path.join(args.output, source_base + "_lex.txt")
        thefile = open(fname, 'w')
        print("Saving output to", fname)
    for item in lex:
        if args.output != '':
            thefile.write("%s\n" % item)
        else:
            print(item)


if __name__ == "__main__":
    get_lexicon()
