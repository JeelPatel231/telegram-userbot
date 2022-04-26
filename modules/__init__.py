# https://stackoverflow.com/a/1057534
# :verycool:

from os.path import dirname, basename, isfile, join
import glob
modules = glob.glob(join(dirname(__file__), "*.py"))

# import EVERYTHING in modules folder
# __xxxxxx , ignored
# _xxxx, runnable scripts
# xxx, modules you can use in chat
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not basename(f).startswith('__')]

# add "_" at the start of any module to ignore loading it as module
# it will execute seperately as a runnable
loadable_mods = [ mods for mods in __all__ if not basename(mods).startswith('_') ]

runnable_scripts = [ scripts for scripts in __all__ if basename(scripts).startswith('_') ]