### How to build and run the code

Requirements on how this code would be used were not provided so I skipped the whole packaging and kept it simple.

```bash

    python -m venv venv
    source venv/bin/acivate
    pip install -r requirements.txt
    python main.py --check-duplicates --input-file publications_min.csv.gz

```

Last command will result with two files being generated `unique_authors.csv` and `unique_institutes.csv`.
Using `--check-duplicates` results with potential duplicates being printed to stderr. That part was not
required but I used for investigation so I decided to leave it here.

### Documentation on your approach, i.e. what did you do and why?

I used `petl` to create a simple data processing pipelines for authors and institutes. I used `nameparser`
to work with names and `fuzzywuzzy` to investigate potential duplicates by calculating Levenshtein
distance between each of elements.

I assumed that first element in `affiliations` column is an institute.
I am not sure though if that is correct choice and maybe we should be joining first two elements instead -
institutes may have same names over different universities.

### A reporting of potential failure points and bottlenecks

1. As performance or memory consumption was not mentioned I totally ignored that issue for now.
   This script works good enough for this amount of data, however to work with larger amounts
   of data maybe some optimizations could be required.
2. `nameparser` has some bugs and some names are not being parsed correctly. It is also biggest bottleneck
   in this code - maybe it could be tweaked to perform way less comparison and regex matches.
3. I did not go further with solving potential duplicates because from what I noticed it would require
   further discussions on how to handle different cases. Some of these are pretty obvious and seem like typos,
   but with most of these similar names I would not be sure enough if I can assume it is a same person without
   looking up each case individually. We would need a precise set of rules on how to handle each of these.

### An accounting of the remaining steps needed before putting deploying your code to a production system

1. Unittests are missing.
2. I would like to test performance with different, possibly largerst dataset I could get
   and then investigate potential bottlenecks.
3. Read further into petl docs to double check if I did everything by the book - maybe there is a better way of doing it.
4. Investigate some weird looking lines in output files like ",", leading spaces, few last names missing in
   `unique_authors.csv`. Most probably related to bugs in namerparser package, but that would need to be handled.
5. Discussion on how to handle potential duplicates, types, etc.
