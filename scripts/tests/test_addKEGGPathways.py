#!user/bin/env python3
"""Test behavior of addKEGGPathways.py"""

from addKEGGPathways import getUniProtFromBlast
from addKEGGPathways import getKeggGenes
from addKEGGPathways import getKeggOrthology
from addKEGGPathways import getKeggPathIDs


def test_getUniProtFromblast_belowThreshold():
    """Return UniProt ID from BLAST line."""
    blast_line = "TRINITY_DN21412_c0_g1_i1.p1     Q66HC5  111     819     111     69      62.162  1.25e-37        RecName: Full=Nuclear pore complex protein Nup93; AltName: Full=93 kDa nucleoporin; AltName: Full=Nucleoporin Nup93"
    assert getUniProtFromBlast(blast_line, "1e-30") == "Q66HC5", "Expect the UniProt ID"

def test_getUniProtFromblast_aboveThreshold():
    """Return False because e-value doesn't pass the threshold."""
    blast_line = "TRINITY_DN21412_c0_g1_i1.p1     Q66HC5  111     819     111     69      62.162  1.25e-37        RecName: Full=Nuclear pore complex protein Nup93; AltName: Full=93 kDa nucleoporin; AltName: Full=Nucleoporin Nup93"
    assert getUniProtFromBlast(blast_line, "1e-40") == False, "Expect the e-value threshold to fail"

def test_getKeggGenes():
    """Get a KEGG Gene from a UniProtID."""
    assert getKeggGenes('P02649') == ['hsa:348'], "Expect a list with one entry"

def test_getKeggOrthology():
    """Get a KEGG Orthology from a KEGG Gene."""
    assert getKeggOrthology('hsa:348') == ['ko:K04524'], "Expect a list with one entry"

def test_getKeggPathIDs():
    """Get a KEGG Pathway IDs from a KEGG Orthology ID."""
    assert getKeggPathIDs('ko:K04524') == ['path:map04979', 'path:ko04979', 'path:map05010', 'path:ko05010'], "Expect a list with four entries"
