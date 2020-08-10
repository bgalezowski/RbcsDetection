import argparse as ap

from source.Detector import Detector
from source.ImageProcessor import ImageProcessor
from source.Logger import Logger

logger = Logger()
parser = ap.ArgumentParser(description='RBCs detection')
parser.add_argument('--path', help="Path to file")
parser.add_argument('--descriptor', help='Name of descriptor (log-pol or unl)')
parser.add_argument('--comparing_method', help='Name of comparing method (canberra, euclidean, mahalanobis or correlation')
args = parser.parse_args()

image_processor = ImageProcessor(args.path)

detector = Detector(args.descriptor, args.comparing_method)
image_processor.search_tree(detector)

detector.print_results()

logger.info('Press any key to finish program')
image_processor.show_image()
