#!/usr/bin/env python3

# load the libraries

import os
import sys
import openai
import IPython

# from langchain.llms import OpenAI
# from langchain_community.llms import OpenAI
# from langchain_openai import OpenAI
from openai import OpenAI
from rich.tree import Tree
from rich import print
from dotenv import load_dotenv
import argparse
import tomllib
from urllib.parse import urlparse
import requests
from pypdf import PdfReader
import markdown


# ############# PROGRAM DESCRIPTION ###########################################

# initialize arg parser with a description
parser = argparse.ArgumentParser(description=text)
parser.add_argument("-V", "--version", help="show program version", action="store_true")
parser.add_argument(
    "-i",
    "--input",
    help="specify input content: either path to file or omegat project or URL to team project",
)
parser.add_argument(
    "-p",
    "--prepp",
    help="specify whether the file should be prepared in OmegaT: bool value",
)

# read arguments from the command cur_str
args = parser.parse_args()

# check for -V or --version
version_text = "foo 0.1.0"
if args.version:
    print(version_text)
    sys.exit()

if args.input:
    call_input = args.input.strip()
else:
    print(
        "No 'input' argument has been provided. Run this script with `--help` for details."
    )
    sys.exit()

# log...
# parent_dir = os.path.dirname(os.path.realpath(__file__))
# log_dpath = os.path.join(parent_dir, "_log")
# os.makedirs(log_dpath, exist_ok=True)
# log_file = os.path.join(log_dpath, "log.txt") # @todo: add timestamp to log file


# ############# CONFIGURATION ###########################################


# load the environment variables
load_dotenv()

# API configuration
openai.api_key: str = os.getenv("OPENAI_API_KEY")

# read toml config
with open("config/settings.toml", mode="rb") as fp:
    config: dict = tomllib.load(fp)

jrebin_fpath: str = config["omegat"]["jrebin_fpath"]
omegat_jpath: str = config["omegat"]["omegat_jpath"]
config_dpath: str = config["omegat"]["config_dpath"]
script_fpath: str = config["omegat"]["script_fpath"]


# ############# FUNCTIONS ###########################################


def uri_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except AttributeError:
        return False


def extract_omegat_text():
    # /home/souto/Repos/capstanlqc/omegat/build/install/OmegaT/OmegaT.jar
    # omegat_init_command = f"{jrebin_fpath} -jar {omegat_jpath} team init en {locale}"
    omegat_xlat_command = f"{jrebin_jpath} -jar {omegat_jpath} {omtprj_dpath} --mode=console-translate --config-dir={config_dpath} --script={script_fpath}"


def get_completion(messages, model="gpt-4-turbo", temperature=0, max_tokens=300):
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content


# ############# TEST ###########################################

if uri_validator(call_input):
    filename: str = os.path.basename(call_input).split("?")[0]
    response = requests.get(call_input)
    # print(response.url)
    # print(response.ok)
    # print(response.status_code)
    with open("temp/file.pdf", mode="wb") as file:
        file.write(response.content)
        # q: write to file first or for the record, or use directly?
elif os.path.isfile(call_input):
    reader = PdfReader("temp/file.pdf")
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"


input_type = "text"

prompt = """

TASK
====

You are an expert terminologist. Your task is to extract the terminology found in the 
document provided. Terminology is to be understood as the collection of terminological units and 
specialized expressions used in the document.

CRITERIA
========

- Your should select the 20 most frequent terms.
- The minimum frequency threshold should be 10 occurrences.
- Terms should have a maximum length of 5 lexical units.
- Do not include years in terms.

METADATA
========

Include the following data:

- lemma of the term (dictionary form of the term)
- frequency of the lemma (how many times the term appears)
- acronym (abbreviation of the term, if any)

OUTPUT FORMAT
=============

Your only output should be a human-readable table, including one column for each piece of data:

- lemma
- frequency
- acronym

For example, terms "national versions" and "Computer-Based Assessment" would be listed as:

| Lemma                         | Frequency | Acronym |
|-------------------------------|-----------|---------|
| national version              | 60        |         |
| computer-based assessment     | 38        | CBA     |      

"""


# prompt = "Which word or words start with upper case in this text?"
# text = "bananas apple Pear apricot"
messages = [
    {"role": "system", "content": prompt},
    {"role": "user", "content": text[0:1000]},
]

# the text has been limited to the first 1000 characters, not sure waht is the limit but the file.pdf is too long
response = get_completion(messages, temperature=0)
print(response)

































exit()
# other tests... 
match input_type:
    case "doc_path":
        print("doc_path")
        pass
    case "doc_url":
        # https://www.oecd.org/pisa/data/pisa2022technicalreport/PISA-2022-Technical-Report-Ch-7-PISA-Translation.pdf
        print("doc_url")
        pass
    case "omegat_omt":
        print("omegat_omt")
        pass
    case "omegat_git":
        print("omegat_git")
        pass
    case _:  # text
        print("_")
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": text},
        ]
        print(f"{prompt=}")
        print(f"{text[0:100]=}")
        exit()
        response = get_completion(messages, temperature=0)
        print(response)
        with open("data/test5.md", mode="w") as file:
            file.write(response)


sys.exit()


# cases

# file: text file -> import directly
# omegat project: unzip
# url to git repo: download
# url to document


###################################################################################################

system_instruction = """
Your trask is to extract all the verbs from the poem provided in the input.
For each verbal form found, please provide its lemma, its actual form found, and how many times that verb is used.
Please include also the total number of lemmas and verbal forms found.
Provide the results as a table. 

For example: 

INPUT
=====

She tries to do what I try and did achieve.

OUTPUT
======

|  LEMMA  |    FORMS   | FREQUENCY |
|:-------:|:----------:|:---------:|
| try     | tries, try | 2         |
| do      | do, did    | 2         |
| achieve | achieve    | 1         |

Total number of lemmas: 3
Total number of forms: 5
"""

user_message = """
Deep into that darkness peering,
Long I stood there, wondering, fearing,
Doubting, dreaming dreams no mortals
Ever dared to dream before;
But the silence was unbroken,
And the stillness gave no token,
And the only word there spoken
Was the whispered word, "Lenore!"
This I whispered, and an echo
Murmured back the word, "Lenore!"
Merely this, and nothing more.
"""

messages = [
    {"role": "system", "content": system_instruction},
    {"role": "user", "content": user_message},
]

response = get_completion(messages)
print(response)

"""
|  LEMMA   |      FORMS      | FREQUENCY |
|:--------:|:---------------:|:---------:|
| peer     | peering         | 1         |
| stand    | stood           | 1         |
| wonder   | wondering       | 1         |
| fear     | fearing         | 1         |
| doubt    | doubting        | 1         |
| dream    | dreaming, dream | 2         |
| dare     | dared           | 1         |
| be       | was             | 1         |
| break    | unbroken        | 1         |
| give     | gave            | 1         |
| speak    | spoken          | 1         |
| whisper  | whispered       | 2         |
| murmur   | murmured        | 1         |

Total number of lemmas: 13
Total number of forms: 15
"""

# also https://platform.openai.com/playground/p/WKgxdT9LsORPFl49soIH2kvI?model=gpt-4-turbo&mode=chat
