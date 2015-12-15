"""
Provide helpers to write Waf tool for typical C/C++ package.

Add options for:
    - pkg-config
    - INCLUDE
    - LIBPATH
    - RPATH
    - LIB
"""

def to_list(option, opt, value, parser):
    setattr(parser.values, option.dest, value.split(','))

def options(opt, pkg, lib=None):
    
    if lib == None:
        lib = [pkg,]

    group = opt.add_option_group(
        '{pkg} configure options'.format(pkg=pkg))

    group.add_option(
        '--{pkg}-pkgconfig'.format(pkg=pkg),
        choices=['on','off'],
        default='on',
        help="Try to configure {pkg} with pkgconfig "
             "(on or off, on by default)".format(pkg=pkg),
    )

    group.add_option(
        '--{pkg}-dir'.format(pkg=pkg),
        action='store',
        help='Set {pkg} includes directory to <{PKG}_DIR>/include ' \
             'and {pkg} libaries directory to <{PKG}_DIR>/lib ' \
             '(override pkgconfig)'.format(pkg=pkg, PKG=pkg.upper()),
        )

    group.add_option(
        '--{pkg}-includes'.format(pkg=pkg),
        action='store',
        help='Set {pkg} includes directory (override pkgconfig ' \
             'and --{pkg}-dir)'.format(pkg=pkg),
    )

    group.add_option(
        '--{pkg}-libpath'.format(pkg=pkg),
        action='store',
        help='Set {pkg} libraries directory (override pkgconfig ' \
             'and --{pkg}-dir)'.format(pkg=pkg),
    )

    group.add_option(
        '--{pkg}-lib'.format(pkg=pkg),
        type='string',
        action='callback', callback=to_list,
        help='Comma separated list of {pkg} libraries ' \
             '(or default to {lib} if '\
             'pkg-config is off)'.format(pkg=pkg, lib=','.join(lib)),
    )

    group.add_option(
        '--{pkg}-rpath'.format(pkg=pkg),
        help="{pkg} rpath (by default, set to libpath)".format(pkg=pkg),
    )

def configure(conf, pkg, lib=None):
    
    if lib == None:
        lib = [pkg,]

    def opt(opt):
        """ For example, if pkg='hdf5' and opt='includes', return
        conf.options.hdf5_includes (containing --hdf5-includes=value) """
        key = '{pkg}_{opt}'.format(pkg=pkg.replace('-','_'), opt=opt)
        return getattr(conf.options, key)

    def set_env(opt, value):
        """ For example, if pkg='hdf5' and opt='includes', set
        conv.env['INCLUDE_HDF5'] to value"""
        key = '{opt}_{pkg}'.format(opt=opt, pkg=pkg).upper()
        conf.env[key] = value

    # If not using pkg-config or if pkg-config not available, at least PKG_LIB
    # must be set. PKG_INCLUDES and PKG_LIBPATH may be in the system or set
    # globally with INCLUDES and LIBPATH.
    set_env('lib', lib)

    # Let pkg-config set flags.
    if opt('pkgconfig') == 'on':
        conf.check_cfg(
            package = pkg,
            args='--cflags --libs',
            mandatory = False,
            msg = "Checking for {pkg} with pkg-config".format(pkg=pkg),
            )

    # If user give --pkg-dir, set PKG_INCLUDES and PKG_LIBPATH from it.
    if opt('dir'):
        set_env('includes', join(opt('dir'),'includes'))
        set_env('libpath', join(opt('dir'),'lib'))

    # Set PKG_RPATH from PKG_LIBPATH.
    set_env('rpath', opt('libpath'))

    # Give user a change to override PKG_INCLUDES, PKG_LIBPATH, PKG_LIB
    # and PKG_RPATH with --pkg-includes, --pkg-libpath, --pkg-lib and
    # pkg--rpath.
    for name in ['includes', 'libpath', 'lib', 'rpath']:
        if opt(name):
            set_env(name, opt(name))
