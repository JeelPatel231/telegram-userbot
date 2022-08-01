# https://stackoverflow.com/a/1057534
# :verycool:

from os.path import dirname, basename, isfile, join
import glob
modules = glob.glob(join(dirname(__file__), "*.py"))

# import EVERYTHING in modules folder
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not basename(f).startswith('__')]

runnable_scripts = [ scripts for scripts in __all__ if basename(scripts).startswith('_') ]