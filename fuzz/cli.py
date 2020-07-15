#!/usr/bin/env python3

from fuzzywuzzy import process
from argparse import ArgumentParser
from collections import OrderedDict
from csv import DictReader, writer
from colored import fg, attr

# Reference
# https://github.com/eoglethorpe/humanitarian/blob/master/shelter/utils/text_match.py

MATCH_LIMIT = 6


def import_text(file_name, valid_column_name, invalid_column_name):
    """read in two columns for known text and text to match"""
    known = set()
    match = []

    with open(file_name, 'r') as f:
        reader = DictReader(f)

        # read in csv, assumes there is a col = known and one = match
        for row in reader:
            known_word = row[valid_column_name].strip()
            if known_word != '':
                known.add(known_word)

            match_word = row[invalid_column_name].strip()
            if match_word != '':
                match.append(match_word)

    return known, match


def get_choice(length):
    """prompt to get valid int choice between 0 and MATCH_LIMIT"""
    response = input("Choose one of the options: ").strip()

    if response == 'exit':
        exit()

    if not response.isdigit():
        return get_choice(length)

    value = int(response)

    if not 0 <= value < length:
        return get_choice(length)

    return value


def check_matches(known, match):
    """iterate over known words looking for matches"""
    # array containing tuples of corrected spellings
    out_vals = OrderedDict()

    # NOTE: skip already resolved

    for index, item in enumerate(match):
        print(f'{index+1}/{len(match)} {item}')

        # NOTE: skipping duplicate
        if out_vals.get(item.lower()):
            print(f'{fg("green")}Already matched{attr("reset")}')
            continue

        possible_matches = process.extract(item, known, limit=MATCH_LIMIT)

        first_match_text = possible_matches[0][0]
        first_match_value = possible_matches[0][1]
        if first_match_value < 50:
            print(f'{fg("red")}No match{attr("reset")}')
            out_vals[item.lower()] = (index, item, 'NONE')
        elif first_match_value < 95:
            # append a none option and option for actual val
            possible_matches.insert(0, ("NONE", 0))
            possible_matches.append((item, 100))

            for i, v in enumerate(possible_matches):
                print(f'{fg("blue")}[{i}] {v[0]}: {v[1]}{attr("reset")}')

            choice_index = get_choice(len(possible_matches))
            choice = possible_matches[choice_index]
            out_vals[item.lower()] = (index, item, choice)
        else:
            if first_match_value != 100:
                print(f'{fg("yellow")}Automatically matched{attr("reset")}')
            out_vals[item.lower()] = (index, item, first_match_text)

    return out_vals


def parse():
    parser = ArgumentParser(
        "fuzz",
        description="Match with some fuzz"
    )

    parser.add_argument('-i',
                        '--input-file',
                        dest='input_file',
                        help='Path to input file',
                        metavar='input file',
                        type=str,
                        required=True)

    parser.add_argument('-v',
                        '--valid-column-name',
                        dest='valid_column_name',
                        help='Name of the column with valid values',
                        type=str,
                        required=True)

    parser.add_argument('-iv',
                        '--invalid-column-name',
                        dest='invalid_column_name',
                        help='Name of the column with invalid values',
                        type=str,
                        required=True)

    parser.add_argument('-o',
                        '--output-file',
                        dest='output_file',
                        help='Path to output file',
                        metavar='output file',
                        type=str,
                        required=True)

    return parser.parse_args()


def main():
    args = parse()

    known, match = import_text(args.input_file,
                               args.valid_column_name,
                               args.invalid_column_name)
    matches = check_matches(known, match)

    with open(args.output_file, 'w') as f:
        w = writer(f)
        w.writerow([args.invalid_column_name,
                    f'{args.invalid_column_name}_corrected',
                    'index'])
        for k, v in matches.items():
            w.writerow([v[1], v[2], v[0]])


if __name__ == "__main__":
    main()
