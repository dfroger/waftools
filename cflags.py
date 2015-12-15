def remove_isysroot(flags):
    """
    >>> flags =  ['-stdlib=libc++', '-std=c++11',
    ...           '-isysroot', '/Developer/SDKs/MacOSX10.5.sdk',
    ...           '-isysroot', '/Developer/SDKs/MacOSX10.5.sdk']
    >>> remove_isysroot(flags)
    >>> print flags
    ['-stdlib=libstdc++', '-std=c++11' ]
    """
    name = '-isysroot'
    while name in flags:
        idx = flags.index(flag)
        flags.pop(idx)
        flags.pop(idx)

def options(opt):

    group = opt.add_option_group('Compiler flags')

    group.add_option('--cflags', action='store', default="", help='Additional C flags')

    group.add_option('--cxxflags', action='store', default="", help='Additional C++ flags')

    group.add_option('--ldflags', action='store', default="", help='Additional linker flags')

    group.add_option('--remove-isysroot', action='store_true', default=False,
        help='Remove -isysroot C/C++ flag that may come with python-config --cflags')

def configure(conf):

    # WARNING: setting CFLAGS alters conf.load('swig')
    # See: https://github.com/waf-project/waf/issues/1663
    # You may want to load cflags tool AFTER swig tool.
    conf.env.append_value('CFLAGS', conf.options.cflags.split())
    conf.env.append_value('CXXFLAGS', conf.options.cxxflags.split())
    conf.env.append_value('LDFLAGS', conf.options.ldflags.split())

    if conf.options.remove_isysroot:
        remove_isysroot(conf.env.CXXFLAGS)
        remove_isysroot(conf.env.CFLAGS)
        remove_isysroot(conf.env.LDFLAGS)
