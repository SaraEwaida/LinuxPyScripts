from optparse import OptionParser

def get_parser():
    parser = OptionParser(usage="usage: %prog [options] filename", version="%prog 1.0")

    parser.add_option("-f", "--file",
                      action="store",
                      dest="filename",
                      help="Write report to FILE", metavar="FILE")

    parser.add_option("-o", "--output",
                      action="store",
                      dest="output",
                      help="Output directory or file name", metavar="OUTPUT")

    return parser
