import base64
import json
import os
import requests
from collections import namedtuple
from .constants import *


def rmlst_api(assembly_file, sample=None):
    if sample is None:
        sample = os.path.splitext(os.path.split(assembly_file)[1])[0]
    uri = 'http://rest.pubmlst.org/db/pubmlst_rmlst_seqdef_kiosk/schemes/1/sequence'
    fasta = open(assembly_file, 'r').read()
    payload = '{"base64":true,"details":true,"sequence":"' + base64.b64encode(fasta.encode()).decode() + '"}'
    api_response = requests.post(uri, data=payload)
    if api_response.status_code == requests.codes.ok:
        data = api_response.json()
    else:
        data = {}
        print(api_response.text)
    rmlst_api_output = namedtuple('rmlst_api_output', ['sample', 'api_response', 'data'])
    rmlst_api_output_sample = rmlst_api_output(sample = sample, api_response = api_response, data = data)
    return rmlst_api_output_sample

def write_output_tab(rmlst_api_output, output_tab="rmlst_output.tab"):
    with open(output_tab, 'w') as outhandle_output_tab:
        outhandle_output_tab.write("sample\trank\texact_matches\tsupport\ttaxon\ttaxonomy\n")
        for match in rmlst_api_output.data['taxon_prediction']:
            outhandle_output_tab.write("{sample}\t{rank}\t{exact_matches}\t{support}\t{taxon}\t{taxonomy}\n".format(
                                        sample=rmlst_api_output.sample,
                                        rank=match['rank'],
                                        exact_matches=len(rmlst_api_output.data['exact_matches']),
                                        support=match['support'],
                                        taxon=match['taxon'],
                                        taxonomy=match['taxonomy']
                                        ))

def write_output_json(rmlst_api_output, output_json="rmlst_output.json"):
    with open(output_json, 'w') as outhandle_output_json:
           outhandle_output_json.write(json.dumps(rmlst_api_output.data, indent=4))