# https://stackoverflow.com/a/1057534
# :verycool:

from os.path import dirname, basename, isfile, join
import glob
modules = glob.glob(join(dirname(__file__), "*.py"))

# add "__" at the start of any module to ignore loading it.
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.startswith('__')]