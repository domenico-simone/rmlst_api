import base64
import json
import os
import requests
from collections import namedtuple
from typing import Optional, Tuple

from .constants import default_output_tab, default_output_json, uri


def rmlst_api(assembly_file: str, sample: Optional[str] = None, uri: str = uri) -> Tuple[str, requests.Response, dict]:
    if sample is None:
        sample = os.path.splitext(os.path.split(assembly_file)[1])[0]
    
    uri: str = uri  # Ensure `uri` is defined elsewhere in your code
    fasta: str = open(assembly_file, 'r').read()
    payload: str = "{'base64': True, 'details': True, 'sequence': '" + base64.b64encode(fasta.encode()).decode() + "'}"
    
    api_response: requests.Response = requests.post(uri, data=payload)
    
    if api_response.status_code == requests.codes.ok:
        data: dict = api_response.json()
        data["sample"] = sample
    else:
        data = {}
        print(api_response.text)
    
    RmlstApiOutput = namedtuple('RmlstApiOutput', ['sample', 'api_response', 'data'])
    rmlst_api_output_sample = RmlstApiOutput(sample=sample, api_response=api_response, data=data)
    
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
