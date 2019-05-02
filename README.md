# AutoLexi
Automated extraction of specialised lexicon from text documents

AutoLexi is meant as a quick-and-dirty vocabulary-building tool for translation and
similar tasks.

## How it works

AutoLexi loads a pure text file (`.txt` or analogous), or a webpage URL, and compares
the frequency of all the words contained in it with their frequencies in average English.

Then, it displays the ones that are more common in the input text compared to English,
which form the specialised lexicon of the text under analysis.

Options:
* **minoccurrences** enforces a threshold on the number of occurrences of the word in
the input text. You may want to include words that appear at least twice in your text,
in which case, set minoccurrences=2, and so on.
* **nshown** sets the maximum number of specialised words to display. Note that the output
is sorted based on the ratio of frequency of occurrence in english / frequency in the text.
Showing more words is equivalent to including less and less specialised words.

## Example

For example, running AutoLexi with minoccurrences=3 and nshown=40 on a World Bank
[report][1] about mental health interventions in Ukraine gives:

`zaporizhia tintle onehealth bromet nonspecialized nonspecialists narcology
narcologists narcologist narcological mhpss lekhan kostyuchenko gluzman mhgap
pobratim cmds polyclinics oblasts poltava raion pinchuk yll ingos dalys
psychotherapists lviv ncds ucu noncommunicable wbg idps informants polyclinic
giz ceta kyiv kharkiv dispensary yld`

[1]:http://documents.worldbank.org/curated/en/310711509516280173/text/120767-WP-Revised-WBGUkraineMentalHealthFINALwebvpdfnov.txt
