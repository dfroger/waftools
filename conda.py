#!/usr/bin/env python
import json
from subprocess import check_output
from os.path import join
import os
import site

from waflib.Configure import conf
from waflib.Errors import ConfigurationError

def tolist(option, opt, value, parser):
    setattr(parser.values, option.dest, value.split(','))

def get_conda_environments():
    args = 'conda info --json'.split()
    try:
        json_str = check_output(args)
    except OSError:
        raise OSError, "Command 'conda info --json' failed, " \
                       "is conda installed and in PATH?"
    json_data = json.loads(json_str)
    env_paths = [str(p) for p in json_data['envs']]
    active_env_path = str(json_data['default_prefix'])
    return env_paths, active_env_path

def options(opt):
    group = opt.add_option_group('Conda environment configure options. ' \
        'Python and BOOST will be searched in conda environment.')

    group.add_option('--conda', action='store_true', default=False,
                   help='Set PKG_CONFIG_PATH and RPATH to conda environment')

    group.add_option('--conda-global', action='store_true', default=False,
                   help='Add conda environment to INCLUDE, LIBPATH and RPATH')

@conf
def detect_conda(conf):
    env_paths, active_env_path = get_conda_environments()

    conf.env.CONDA_ENV_PATH = active_env_path

    conf.env.INCLUDES_CONDA_ENV = [join(active_env_path, 'include'),]
    conf.env.LIBPATH_CONDA_ENV = [join(active_env_path, 'lib'),]
    conf.env.PYTHONDIR_CONDA_ENV = site.getsitepackages()[0]
    conf.env.PKG_CONFIG_PATH_ENV = join(active_env_path, 'lib', 'pkgconfig')

@conf
def conda_boost(conf):
    from waflib.extras import boost
    boost.BOOST_INCLUDES.insert(0, conf.env.INCLUDES_CONDA_ENV)

@conf
def conda_python(conf):
    conf.env.LIBPATH_PYEMBED= conf.env.LIBPATH_CONDA_ENV
    conf.env.LIBPATH_PYEXT = conf.env.LIBPATH_CONDA_ENV

def configure(conf):
    o = conf.options

    conf.env.USE_CONDA = o.conda or o.conda_global

    if conf.env.USE_CONDA:
        conf.detect_conda()
        conf.conda_boost()
        conf.conda_python()

    if o.conda:
        os.environ['PKG_CONFIG_PATH'] = conf.env.PKG_CONFIG_PATH_ENV
        conf.env.RPATH = conf.env.LIBPATH_CONDA_ENV 

    if o.conda_global:
        conf.env.INCLUDES = conf.env.INCLUDES_CONDA_ENV 
        conf.env.LIBPATH = conf.env.LIBPATH_CONDA_ENV 
        conf.env.RPATH = conf.env.LIBPATH_CONDA_ENV 
