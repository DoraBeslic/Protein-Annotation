## addKEGGPathways.py
**Overview:** Iterates through every BLAST hit in a specified BLAST results file and filters hits to those with evalues < 1e-50 (default). Gets UniProt id of every hit and finds (if available) the associated KEGG orthology ids, KEGG pathway ids, and KEGG pathway descriptions. Annotates every hit (with an e-value below the threshold) with its associated KEGG information (if available) and appends it to a specified output file.    
**Author:** Isidora Beslic  
**Date created:** April 12, 2023  
**Date started:** April 10, 2023  
**Calling on the command line:** 
`python addKEGGPathways.py [input BLAST file] -t [e-value threshold] [output file]`  
## Tests: 
test_addKEGGPathways.py (run with pytest)
- test_getUniProtFromblast_belowThreshold(): pass
- test_getUniProtFromblast_aboveThreshold(): pass
- test_getKeggGenes(): pass
- test_getKeggOrthology(): pass
- test_getKeggPathIDs(): pass
