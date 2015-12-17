#!/usr/bin/env python
from os.path import realpath
import os

from waflib.Configure import conf
import clibtool

tooldir = os.environ['WAF_TOOLDIR']

fragment= """
#include "numini/reader.hxx"

int main()
{
    numini::Reader ini;
}
"""

def options(opt):
    opt.load('yaml-cpp', tooldir=tooldir)
    clibtool.options(opt, pkg='numini')

def configure(conf):
    conf.load('yaml-cpp', tooldir=tooldir)
    conf.check_yaml_cpp()
    clibtool.configure(conf, pkg='numini')

@conf
def check_numini(conf):
    conf.check_cxx(
        fragment = fragment,
        use = ['NUMINI', 'YAML-CPP', 'BOOST'],
        msg = 'Checking to link with numini',
    )
