# rmlst_api

Run rmlst API through python script for species identification of a bacterial assembly.

```bash
Usage: rmlst-api [OPTIONS] ASSEMBLY_FILE

  Run rMLST API, then write output files (tab and json).

  ``sample`` can be optionally defined and will be used in the tabular output.
  If neither ``output_tab`` and ``output_json`` are provided, they will
  default to ``rmlst_output.tab`` and ``rmlst_output.json`` respectively.

  :param assembly_file: bacterial assembly file :param sample: sample name
  :param output_tab: name of tabular output file :param output_json: name of
  json output file :return:

Options:
  --sample TEXT       sample name used in tab output
  --output-tab TEXT   rMLST tab output file
  --output-json TEXT  rMLST json output file
  --help              Show this message and exit.
```

API source: https://pubmlst.org/species-id/species-identification-via-api.
  