from os.path import join

from waflib.Configure import conf
import clibtool

fragment= """
#include "yaml-cpp/yaml.h"

int main()
{
    YAML::Node node;
}
"""

def options(opt):
    clibtool.options(opt, pkg='yaml-cpp')
    opt.load('boost')

def configure(conf):
    clibtool.configure(conf, pkg='yaml-cpp')
    conf.load('boost')

@conf
def check_yaml_cpp(conf):
    conf.check_boost()
    conf.check_cxx(
        fragment = fragment,
        use = ['YAML-CPP','BOOST'],
        msg = 'Checking to link with yaml-cpp',
    )
