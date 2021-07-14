#!/usr/bin/env python3

# Copyright 2021 Dart Dart
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import csv
import os.path

# Validate MAX_MAIL_SIZE.
class MaxMailSizeAction(argparse.Action):
    def __call__(self, parser, namespace, value, option_string=None):
        if value <= 1:
            raise ValueError("Invalid maximum mail size")
        setattr(namespace, self.dest, value)

# Parse command line parameters.
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-m", "--max-mail-size", type=int, default=24, action=MaxMailSizeAction,
                    help="maximum mail size in bytes")
parser.add_argument("-t", "--template-path", type=str, default="./cpp_templates/",
                    help="path to C++ code templates")
parser.add_argument("-s", "--spam", type=str, default="./data/spam.txt",
                    help="a CSV file containing spam strings (one per line)")
parser.add_argument("-o", "--output-path", type=str, default="./",
                    help="output path for generated C++ code")
args = parser.parse_args()

# Replace strings in template files and write to an output file.
def replace_in_template_file(template_file, output_file, replacements):
    with open(os.path.join(args.template_path, template_file), "r") as in_f:
        output = in_f.read()
    for what, with_what in replacements:
        output = output.replace(what, str(with_what))
    with open(os.path.join(args.output_path, output_file), "w") as out_f:
        out_f.write(output)

with open(os.path.join(args.template_path, "contains_spam_def.template"), newline="\n") as def_f:
    contains_spam_def_template = def_f.read()

with open(os.path.join(args.template_path, "contains_spam_call.template"), newline="\n") as call_f:
    contains_spam_call_template = call_f.read()

# Generate containsSpam() definitions and calls.
contains_spam_defs = ""
contains_spam_calls = ""
with open(args.spam, newline="\n") as spam_f:
    spam_reader = csv.reader(spam_f, delimiter="\n", quotechar="\"", escapechar="\\")
    id = 0
    for spam in spam_reader:
        spam_str = spam[0]
        spam_size = len(spam_str)
        if spam_size >= args.max_mail_size:
            raise Exception("Spam string size({}) exceeds MAX_MAIL_SIZE({})".format(spam_size, args.max_mail_size))
        spam_str = spam_str.encode("unicode_escape").decode("utf-8")
        spam_str = spam_str.replace("\"", "\\\"")
        contains_spam_def = contains_spam_def_template.replace("$SPAM_STR$", spam_str)
        contains_spam_def = contains_spam_def.replace("$SPAM_SIZE$", str(spam_size + 1))
        contains_spam_def = contains_spam_def.replace("$ID$", str(id))
        contains_spam_defs += contains_spam_def

        contains_spam_call = contains_spam_call_template.replace("$ID$", str(id))
        contains_spam_calls += contains_spam_call

        contains_spam_defs += "\n"
        contains_spam_calls += "\n"

        id = id + 1
    # Remove redundant new lines to make the code prettier.
    if id != 0:
        contains_spam_defs = contains_spam_defs[:-2]
        contains_spam_calls = contains_spam_calls[:-2]

# Finalize generation by outputting to files.
replace_in_template_file("is_mail_spam.h.template", "is_mail_spam.h", [("$MAX_MAIL_SIZE$", args.max_mail_size)])
replace_in_template_file("is_mail_spam.cc.template", "is_mail_spam.cc",
                        [("$CONTAINS_SPAM_DEFS$", contains_spam_defs), ("$CONTAINS_SPAM_CALLS$", contains_spam_calls)])
