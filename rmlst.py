import glob, os, sys, requests, base64, json
import argparse
# from snakemake import shell
# 
# sample        = snakemake.wildcards.sample
# assembly_file = snakemake.input.assembly
# output_json   = snakemake.output.rmlst_json
# output_tab    = snakemake.output.rmlst_tab
# threads       = snakemake.threads
# log           = snakemake.log[0]

def rmlst_api(assembly_file=None, log=None, output_tab=None, output_json=None):
    sample = os.path.splitext(os.path.split(assembly_file)[1])[0]
    if output_tab is None:
        output_tab = f"{os.path.splitext(os.path.split(assembly_file)[1])[0]}_rmlst.tab"
    if output_json is None:
        output_json = f"{os.path.splitext(os.path.split(assembly_file)[1])[0]}_rmlst.json"
    if log is None:
        log = f"{os.path.splitext(os.path.split(assembly_file)[1])[0]}_rmlst.log"
    # with open(log, "w") as f:
    # sys.stderr = sys.stdout = f
    sys.stderr = sys.stdout = open(log, 'w')
    uri = 'http://rest.pubmlst.org/db/pubmlst_rmlst_seqdef_kiosk/schemes/1/sequence'
    #    with open(args.file, 'r') as x: 
    #        fasta = x.read()
    fasta = open(assembly_file, 'r').read()
    payload = '{"base64":true,"details":true,"sequence":"' + base64.b64encode(fasta.encode()).decode() + '"}'
    response = requests.post(uri, data=payload)
    if response.status_code == requests.codes.ok:
        data = response.json()
        try: 
            data['taxon_prediction']
        except KeyError:
            # f.write("No match")
            print("No match")
            sys.exit(0)
        # This is for logging
        for match in data['taxon_prediction']:
                print("Rank: " + match['rank'] + "\n")
                print("Taxon: " + match['taxon'] + "\n")
                print("Support: " + str(match['support']) + "%\n")
                print("Taxonomy: " + match['taxonomy'] + "\n")
        # This is for tab output
        outhandle_output_tab = open(output_tab, 'w') 
        for match in data['taxon_prediction']:
            outhandle_output_tab.write("{sample}\t{rank}\t{support}\t{taxon}\t{taxonomy}\n".format(
                                        sample=sample,
                                        rank=match['rank'],
                                        support=match['support'],
                                        taxon=match['taxon'],
                                        taxonomy=match['taxonomy']
                                        ))
        outhandle_output_tab.close()
    else:
        print(response.text)
    
    with open(output_json, 'w') as outhandle_output_json:
        outhandle_output_json.write(json.dumps(data, indent=4))
    
    return data

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="assembly file", required=True)
    parser.add_argument("-l", "--log", help="log file. default is <input>_rmlst.log")
    parser.add_argument("--output_tab", help="rMLST tab output. default is <input>_rmlst.tab")
    parser.add_argument("--output_json", help="rMLST json output. default is <input>_rmlst.json")
    args = parser.parse_args()
    
    if args.output_tab is None:
        output_tab = f"{os.path.splitext(os.path.split(args.input)[1])[0]}_rmlst.tab"
        # output_tab = f"{os.path.splitext(args.input)[0]}_rmlst.tab"
    else:
        output_tab = args.output_tab
    
    if args.output_json is None:
        output_json = f"{os.path.splitext(os.path.split(args.input)[1])[0]}_rmlst.json"
    else:
        output_json = args.output_json
    
    if args.log is None:
        log = f"{os.path.splitext(os.path.split(args.input)[1])[0]}_rmlst.log"
    else:
        log = args.log
    
    rmlst_api(assembly_file=args.input, log=log, output_tab=output_tab, output_json=output_json)
