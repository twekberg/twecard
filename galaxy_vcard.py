#!/usr/bin/env python
"""
Displays vcards as dictionaries
"""


import argparse
import sys

"""
TODO:
Special cases
'X-SAMSUNGADR': 'Washington;;;Washington'
'EMAIL;X-CUSTOM(CHARSET=UTF-8,ENCODING=QUOTED-PRINTABLE,=4D=61=72=69=6C=79=6E=20=gi4D=61=6E=79=6F=6E)': 'mjmanyon@gmail.com'
"""

def build_parser():
    """
    Collect command line arguments.
    """
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-v', '--vcard_filename',
                        default='Contacts.vcf',
                        help='The file name of the vcard file. '
                        ' Default: %(default)s.')
    return parser


def parse_vcard(filename):
    """
    Parse into a list of dictionaries, one for each card.
    """
    vcards = []
    # Skip until an empty line is encountered
    skip_to_empty = False
    # Skip lines that start with '='
    skip_equal_sign_lines = False
    with open(filename) as vcard_file:
        for line in vcard_file:
            line = line.strip() # Get rid of leading/trailing junk
            if skip_to_empty:
                if line:
                    continue    # Skip these non-empty lines
                skip_to_empty = False
                continue        # Start processing with the next line
            if skip_equal_sign_lines:
                if line.startswith('='):
                    continue    # Skip this encoded line
                skip_equal_sign_lines = False

            if line.startswith('BEGIN:VCARD'):
                vcard = {}
            elif line.startswith('END:VCARD'):
                if 'FN' in vcard:
                    # One entry doesn't have a full name and
                    # I don't know how to delete it.
                    vcard.pop('VERSION') # Don't care about this
                    vcards.append(vcard)
            elif line.startswith('X-SAMSUNGADR;ENCODING') or \
                 line.startswith('NOTE;ENCODING'):
                skip_equal_sign_lines = True
            else:
                (key, value) = line.split(':', maxsplit=1)
                if key.startswith('PHOTO;ENCODING=BASE64;'):
                    # Skip over the encoded data.
                    skip_to_empty = True
                    vcard[key] = 'Not processed'
                    continue
                else:
                    value = value.strip(';')
                if key.startswith('TEL;') and len(value) >= 10:
                    value = punctuate_phone(value)
                vcard[key] = value
    return vcards


def punctuate_phone(value):
    """
    Put punctuation in the phone number.
    """
    temp_value = value
    value = ''
    for size in (4, 3, 3, 99):
        sep = '-' if value else ''
        if temp_value:
            value = temp_value[-size:] + sep + value
        temp_value = temp_value[0:-size]
    return value
    

def main(args):
    """
    Process the vcard file.
    """
    vcards = parse_vcard(args.vcard_filename)

    for vcard in vcards:
        if 'FN' not in vcard:
            print(vcard)

    for vcard in sorted(vcards, key=lambda vc: vc['FN'].upper()):
        print(vcard)

if __name__ == '__main__':
    sys.exit(main(build_parser().parse_args()))
