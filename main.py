import csv
import sys

import click
import petl
from fuzzywuzzy import fuzz
from nameparser import HumanName
from prettytable import PrettyTable


@click.command()
@click.option("--input-file", required=True, help="File to parse.")
@click.option("--check-duplicates", default=False, is_flag=True)
def main(input_file, check_duplicates):

    csv.field_size_limit(sys.maxsize)

    table = petl.fromcsv(input_file)
    authors = extract_authors(table)
    authors.tocsv("unique_authors.csv")
    institutes = extract_institutes(table)
    institutes.tocsv("unique_institutes.csv")

    if check_duplicates:

        authors = [" ".join(name) for name in authors]
        institutes = [i[0] for i in institutes]

        print(
            (
                "Potential author duplicates:\n"
                f"{tablify(calculate_distances(authors))}\n\n"
                "Potential institute duplicates:\n"
                f"{tablify(calculate_distances(institutes))}\n\n"
            ),
            file=sys.stderr,
        )


def extract_authors(table):

    def rowgenerator(row):
        for author in row["authors"]:
            hn = HumanName(author)
            yield hn.last, hn.first

    return (
        table.cut("authors")
        .convert("authors", eval)
        .select("authors", lambda l: l is not None)
        .rowmapmany(rowgenerator, header=['lastname', 'firstname'])
        .sort(key=["lastname", "firstname"])
        .distinct(presorted=True)
    )


def extract_institutes(table):

    return (
        table.cut("affiliations")
        .convert("affiliations", lambda s: s.split(",")[0].strip(', .+*"'))
        .select("affiliations", lambda s: s != "")
        .distinct()
    )


def calculate_distances(strings):

    for x, y in zip(strings, strings[1:]):
        score = fuzz.ratio(x, y)
        if score > 90:
            yield x, y, score


def tablify(rows):

    t = PrettyTable()
    t.field_names = ["First", "Second", "Score"]
    t.add_rows(rows)
    t.align = "l"

    return t


if __name__ == "__main__":
    main()
