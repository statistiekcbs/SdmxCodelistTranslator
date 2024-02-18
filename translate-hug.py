import sdmx
import sys
import argparse
import logging
import torch
from datetime import datetime
from sdmx.model.v21 import Agency
from sdmx.message import StructureMessage, Header
from transformers import pipeline

""" ---------------------------------------------------------------------------
    Settings
--------------------------------------------------------------------------- """
# logging.basicConfig(level=logging.DEBUG)


""" ---------------------------------------------------------------------------
    Functions
--------------------------------------------------------------------------- """
DEFAULTLANGUAGE = 'en'

device = "cuda:0" if torch.cuda.is_available() else "cpu"
translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-nl", device=device)


def UpdateUrn(code):
    """
    Assign new agency to urn's
    """
    code.urn = code.urn.replace(code.urn_group["agency"], target_agency)

def TranslateText(text):
    translated_text = translator(text, max_length=400)
    return translated_text[0]["translation_text"]

def TranslateCode(code):
    """
    Translate code names to a specified language. Source language is always defaulted to be English
    """
    try:
        translated_name = TranslateText(code.name[DEFAULTLANGUAGE])

        code.name = {DEFAULTLANGUAGE: code.name[DEFAULTLANGUAGE],
                     target_language: translated_name}

        logging.debug("Translated to ", translated_name)
    except Exception as err:
        logging.error(f"Unexpected {err=}, {type(err)=}")


def TranslateCodeList(codelist):
    for row in codelist.items:
        code = codelist.items[row]
        TranslateCode(code)
        UpdateUrn(code)
        logging.debug(code.id, " - ",
                      code.name[DEFAULTLANGUAGE], " - ", code.name[target_language])


def WriteCodeList(codelist, postfix = "translated"):
    """
    Save the codelist to a SDMX file
    """
    header = Header(id=codelist.id,
                    prepared=datetime.now(), sender=Agency(id="DarthVader"))

    message = StructureMessage(codelist={codelist.id: codelist}, header=header)

    with open(codelist.id + "-" + postfix + ".xml", "wb") as f:
        f.write(sdmx.to_xml(message, pretty_print=True))


""" ---------------------------------------------------------------------------
Main
--------------------------------------------------------------------------- """
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--codelist', help='ID of codelist to translate')
    parser.add_argument(
        '--agency', help='Agency ID of the translated codelist', default="NL1")
    parser.add_argument('--language', help='Target language', default="nl")

    args = parser.parse_args()

    codelist_id = args.codelist

    if (codelist_id is None):
        print("No codelist")
        sys.exit(0)

    target_agency = args.agency
    target_language = args.language

    client = sdmx.Client(
        "ESTAT",
        backend="sqlite",
        fast_save=True,
        expire_after=600,
    )

    try:
        codelist = client.codelist(codelist_id).codelist[0]
        WriteCodeList(codelist, "original")
        
        codelist.maintainer = Agency(name=target_agency, id=target_agency)

        UpdateUrn(codelist)
        TranslateCode(codelist)
        TranslateCodeList(codelist)
        WriteCodeList(codelist)
    except Exception as err:
        logging.error(f"Could not translate codelist {err=}, {type(err)=}")
