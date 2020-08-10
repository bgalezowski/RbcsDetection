import source.comparing_methods as cm
import source.descriptors as d
from source.ImageProcessor import ImageProcessor
from source.Logger import Logger
from collections import UserDict


class Detector:
    def __init__(self, descriptor, comparing_method):
        self.logger = Logger()
        self.ellip = 0
        self.schisto = 0

        self.rbcs = UserDict(
            elliptocyte=0,
            schistocyte=0
        )
        self.choose_descriptor(descriptor)
        self.choose_comparing_method(comparing_method)
        self.load_rbc_distances()

        self.logger.info('Initialization completed')

    def choose_descriptor(self, descriptor):
        if descriptor == 'log-pol':
            self.descriptor = d.log_pol_fourier_transform
        elif descriptor == 'unl':
            self.descriptor = d.unl_fourier_transform
        else:
            self.logger.error('Invalid descriptor')
            exit(1)

    def choose_comparing_method(self, comparing_method):
        if comparing_method == 'canberra':
            self.comparing_method = cm.canberra_distance
        elif comparing_method == 'euclidean':
            self.comparing_method = cm.euclidean_distance
        elif comparing_method == 'correlation':
            self.comparing_method = cm.correlation_coefficient
        elif comparing_method == 'mahalanobis':
            self.comparing_method = cm.mahalanobis_distance
        else:
            self.logger.error('Invalid comparing method')
            exit(1)

    def load_rbc_distances(self):
        ip = ImageProcessor("../samples/elliptocyte.png")
        self.ellip_distances = self.descriptor(ip.contours[0])

        ip = ImageProcessor("../samples/elliptocyte.png")
        self.schis_distances = self.descriptor(ip.contours[0])

        self.logger.info('Rbcs distances loaded')

    def detect(self, parent, child):
        parent_distances = self.descriptor(parent)
        child_distances = self.descriptor(child) if len(child) != 0 else []

        if self.comparing_method(parent_distances, self.ellip_distances):
            self.rbcs['elliptocyte'] += 1
        else:
            pass

        if self.comparing_method(parent_distances, self.schis_distances):
            self.rbcs['schistocyte'] += 1
        else:
            pass

    def print_results(self):
        self.logger.info('Detection completed')
        for rbc in self.rbcs:
            self.logger.ok('Number of ' + rbc + 's: ' + str(self.rbcs[rbc]))
