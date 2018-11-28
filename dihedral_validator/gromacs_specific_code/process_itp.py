#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Routines to create .itp file from template"""

import os
import re
from typing import Dict
from typing import Pattern
from typing import Match
from typing import List

SECTION_RE_TEMPLATE = '^\[ {} \]$\n(^.+$\n)+'
DEFINE_RE = '^#define .+'


def prepare_itp_file(in_ipt: str, new_params: dict, params_type: int, out_itp: str,
                     filter_out_comments: Dict[str, bool]):
    defines, sections_dict = parse_itp_file(in_ipt)
    for k, v in sections_dict:
        if filter_out_comments.get(k, False):
            sections_dict[k] = remove_lines_containing_comments[v]

def create_dihedraltypes(params, ):pass


def adapt_input_dihedral_types_to_gromacs_format(input_dihedral:str)
    # example input: CT-CT-CT-OS
    # example output: CT    CT   CT   OS
    splitted = input_dihedral.split('-')
    return splitted[0]+4*' '+splitted[1]+3*' '+splitted[2]+3*' '+splitted[3]


def parse_itp_file(in_file: str, newline='\n', section_re_template: str = SECTION_RE_TEMPLATE,
                   define_re: str = DEFINE_RE):
    with open(in_file, 'r') as f:
        content = f.read()
    defines = re.findall(define_re, content)
    #dihedraltypes = find_section('dihedraltypes', content, section_re_template=section_re_template)
    moleculetype = find_section('moleculetype', content, section_re_template=section_re_template)
    atoms = find_section('atoms', content, section_re_template=section_re_template)
    bonds = find_section('bonds', content, section_re_template=section_re_template)
    angles = find_section('angles', content, section_re_template=section_re_template)
    dihedrals1_math = find_section('dihedrals', content, section_re_template=section_re_template, return_match=True)
    dihedrals1 = dihedrals1_math.group(0)
    pairs = find_section('pairs', content, section_re_template=section_re_template)
    dihedrals2 = find_section('dihedrals', content, section_re_template=section_re_template,
                              start_pos=dihedrals1_math.end())
    ret_dict = {}
    for element in ['moleculetype', 'atoms', 'bonds', 'angles', 'dihedrals1', 'dihedrals2', 'pairs']:
        ret_dict[element] = locals()[element]
    return defines, ret_dict


def remove_lines_containing_comments(itp_file_content: str, newline='\n') -> str:
    ret_lines = []
    for line in itp_file_content.split(newline):
        if not line.lstrip().startswith(';'):
            ret_lines.append(line)
    return newline.join(ret_lines)


def find_section(section_name: str, string_to_be_searched, section_re_template: str = SECTION_RE_TEMPLATE,
                 return_match=False, start_pos=0):
    section_re = section_re_template.format(section_name)
    compiled_regex = re.compile(section_re, re.MULTILINE)
    if return_match:
        return compiled_regex.search(string_to_be_searched, start_pos)
    else:
        return compiled_regex.search(string_to_be_searched, start_pos).group(0)


if __name__ == '__main__':
    from dihedral_validator.input import read_input_file
    params = read_input_file(os.path.join('example', 'input'))
    print(params)
    #print(parse_itp_file(os.path.join('example', 'gromacs_specific_files', 'triacetin_qqAWA_q1_new_t3t4.itp'), {}))
    # TODO program i data puszczania tej analizy w dihedraltypes + dodatki (ładunki czy coś) - czyli zrobienie dihedraltypes od zera
    # TODO ale program jest przez jakiś wyższy skrypt ustawiany