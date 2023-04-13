#!/usr/bin/env python
"""annotate blast hits with KEGG orthology id, KEGG pathway id, and KEGG pathway description"""

import argparse
import requests

def get_args():
    """Return parsed command-line arguments."""

    parser = argparse.ArgumentParser(
        description="annotate blast hits with KEGG orthology id, KEGG pathway id, and KEGG pathway description",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('BLAST_results', # name of the argument, we will later use args.BLAST_results to get this user input
                        metavar='BLAST FILE', # shorthand to represent the input value
                        help='BLAST results file', # message to the user, it goes into the help menu
                        type=str, # type of input expected, could also be int or float
                        )

    parser.add_argument('-t', '--threshold', # name of the argument, we will later use args.threshold to get this user input
                        metavar='E-VALUE', # shorthand to represent the input value
                        help='e-value threshold', # message to the user, it goes into the help menu
                        type=str, # type of input expected, could also be int or float
                        default=1e-50, # default option if no input is given by the user
                        required=False # whether this input must be given by the user, could also be True
                        )
    
    parser.add_argument('BLAST_annotated', # name of the argument, we will later use args.BLAST_annotated to get this user input
                        metavar='FILE PATH', # shorthand to represent the input value
                        help='output file', # message to the user, it goes into the help menu
                        type=str, # type of input expected, could also be int or float
                        )

    return(parser.parse_args())

def getUniProtFromBlast(blast_line, threshold):
    """Return UniProt ID from the BLAST line if the evalue is below the threshold.

    Returns False if evalue is above threshold.
    """
    cleaned_line = blast_line.strip()
    blast_fields = cleaned_line.split("\t")
    if float(blast_fields[6]) < float(threshold):
        return(blast_fields[1])
    else:
        return(False)

def loadKeggPathways(): 
    """Return dictionary of key=pathID, value=pathway name from http://rest.kegg.jp/list/pathway/ko 

    Example: keggPathways["path:ko00564"] = "Glycerophospholipid metabolism"
    """
    keggPathways = {}
    result = requests.get('https://rest.kegg.jp/list/pathway/ko')
    for entry in result.iter_lines():
        str_entry = entry.decode(result.encoding)  # convert from binary value to plain text
        fields = str_entry.split("\t")
        keggPathways[fields[0]] = fields[1]
    return(keggPathways)

def getKeggGenes(uniprotID):
    """Return a list of KEGG organism:gene pairs for a provided UniProtID."""
    keggGenes = []
    result = requests.get(f'https://rest.kegg.jp/conv/genes/uniprot:{uniprotID}')
    for entry in result.iter_lines():
        str_entry = entry.decode(result.encoding)  # convert from binary value to plain text
        fields = str_entry.split("\t")
        if len(fields) < 2:
            continue
        keggGenes.append(fields[1])  # second field is the keggGene value
    return(keggGenes)

def getKeggOrthology(KeggGene):
    """Return a list of KEGG orthology ids for a provided KEGG gene."""
    ko_list = []
    result = requests.get(f'https://rest.kegg.jp/link/ko/{KeggGene}')
    for entry in result.iter_lines():
        str_entry = entry.decode(result.encoding)  # convert from binary value to plain text
        fields = str_entry.split("\t")
        ko_list.append(fields[1])  # second field is the ko ID
    return(ko_list)

def getKeggPathIDs(ko):
    """Return a list of KEGG pathway ids for a provided KEGG orthology id."""
    pathIDs = []
    result = requests.get(f'https://rest.kegg.jp/link/pathway/{ko}')
    for entry in result.iter_lines():
        str_entry = entry.decode(result.encoding)  # convert from binary value to plain text
        fields = str_entry.split("\t")
        if len(fields) < 2:
            continue
        else:
            pathIDs.append(fields[1])
    return(pathIDs)

def addKEGGPathways(pathIDs):
    """Return dictionary of key=pathID, value=pathway name for a provided list of path IDs"""
    pathways = {}
    KeggPathways = loadKeggPathways()
    for path in pathIDs:
        path_id = path.split(':')[1]
        pathways[path] = KeggPathways[path_id] 
    return pathways

if __name__ == "__main__":
    args = get_args()

    # iterate through every line of input file
    with open(args.BLAST_results, 'r') as input:
        for blast_line in input:

            # ignore header lines
            if blast_line.startswith("#"):
                continue 
            
            # get uniprotID of every BLAST hit
            uniprotID = getUniProtFromBlast(blast_line, threshold=args.threshold)

            # for BLAST hits that are lower than threshold...
            # get a list of KEGG organism:gene pairs (KeggGenes)
            if uniprotID != False:
                KeggGenes = getKeggGenes(uniprotID)

                # for idenitified KeggGenes only, get Kegg orthology id 
                # and the associated pathway ids
                if len(KeggGenes) > 0:
                    for KeggGene in KeggGenes:
                        ko_list = getKeggOrthology(KeggGene)

                        # for identified Kegg orthology ids only, get pathway ids
                        if len(ko_list) > 0:
                            for ko in ko_list:
                                pathIDs = getKeggPathIDs(ko)

                            # for identified pathway ids only, get associated pathway descriptions
                            if len(pathIDs) > 0:

                                # only get reaction pathways 
                                for path in pathIDs:
                                    if path.startswith('path:map'):
                                        pathIDs.remove(path)
                                    
                                pathways = addKEGGPathways(pathIDs)

                                # append Kegg orthology id, Kegg pathway id, and Kegg pathway
                                # description for each uniprotID to end of BLAST hit.
                                # Append annoted blast hits to output file
                                with open(args.BLAST_annotated, 'a') as output:
                                    for key, value in pathways.items():
                                        output.write(f'\n{blast_line}\t{ko}\t{key}\t{value}')





