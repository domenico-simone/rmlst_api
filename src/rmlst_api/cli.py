from .rmlst import rmlst_api
from .rmlst import write_output_json
from .rmlst import write_output_tab
import sys
import click
from .constants import *

@click.group()
# @click.version_option()
def main():
    pass

@click.command()
@click.option("--sample", default="sample", help="sample name used in tab output")
@click.option("--output-tab", default=default_output_tab, help="rMLST tab output file")
@click.option("--output-json", default=default_output_json, help="rMLST json output file")
@click.argument('assembly_file')

def run_all(assembly_file: str, sample: str = None,
            output_tab: str = "rmlst_output.tab",
            output_json: str = "rmlst_output.json"):
    """
    Run rMLST API, then write output files (tab and json).
    
    ``sample`` can be optionally defined and will be used in the tabular
    output.
    If neither ``output_tab`` and ``output_json`` are provided,
    they will default to ``rmlst_output.tab`` and ``rmlst_output.json``
    respectively.
    
    :param assembly_file: bacterial assembly file
    :param sample: sample name
    :param output_tab: name of tabular output file
    :param output_json: name of json output file
    :return: 
    """
    rmlst_api_output_sample = rmlst_api(assembly_file=assembly_file, sample=sample)
    write_output_tab(rmlst_api_output_sample, output_tab=output_tab)
    write_output_json(rmlst_api_output_sample, output_json=output_json)