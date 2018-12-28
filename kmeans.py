"""
Kmeans clustering algorithm for colour detection in images

Initialise a kmeans object and then use the run() method.
Several debugging methods are available which can help to
show you the results of the algorithm.
"""

from PIL import Image
import random
import numpy

class Cluster(object):

    def __init__(self):
        self.pixels = []
        self.centroid = None

    def addPoint(self, pixel):
        self.pixels.append(pixel)

    def setNewCentroid(self):

        R = [colour[0] for colour in self.pixels]
        G = [colour[1] for colour in self.pixels]
        B = [colour[2] for colour in self.pixels]

        R = sum(R) / len(R)
        G = sum(G) / len(G)
        B = sum(B) / len(B)

        self.centroid = (R, G, B)
        self.pixels = []

        return self.centroid


class Kmeans(object):

    def __init__(self, image, size=200):
        self.image = image.resize((size, size))
        self.pixels = self.image.getdata()
        #print(type(self.pixels))

    def run(self, k):
        self.clusters = [None for i in range(k)]
        
        randomPixel = random.sample(list(self.pixels), k)

        for idx in range(k):
            self.clusters[idx] = Cluster()
            self.clusters[idx].centroid = randomPixel[idx]

        # oldClusters = None
        iterations = 0

        while iterations < 4:
            print(iterations)

            for pixel in self.pixels:
                shortest = float('Inf')
                for cluster in self.clusters:
                    distance = self.calcDistance(cluster.centroid, pixel)
                    if distance < shortest:
                        shortest = distance
                        nearest = cluster

                nearest.addPoint(pixel)

            for cluster in self.clusters:
                cluster.setNewCentroid()
            iterations += 1

        return [cluster.centroid for cluster in self.clusters]

    def assignClusters(self, clusters, points):

        for point in points:
            shortest = float('Inf')
            for cluster in clusters:
                distance = self.calcDistance(cluster.centroid, point)
                if distance < shortest:
                    shortest = distance
                    nearest = cluster

            nearest.addPoint(point)

    def showImage(self):
        self.image.show()

    def showCentroidColours(self):
        for cluster in self.clusters:
            r,g,b = cluster.centroid
            ri, gi, bi = int(r), int(g), int(b)
            image = Image.new("RGB", (200, 200), (ri,gi,bi) )
            image.show()

    def showClustering(self):
        localPixels = [None] * len(self.image.getdata())

        for idx, pixel in enumerate(self.image.getdata()):
                shortest = float('Inf')
                for cluster in self.clusters:
                    distance = self.calcDistance(cluster.centroid, pixel)
                    if distance < shortest:
                        shortest = distance
                        nearest = cluster

                localPixels[idx] = nearest.centroid

        localPixels = numpy.asarray(localPixels).astype('uint8').reshape((200, 200, 3))
        colourMap = Image.fromarray(localPixels)
        colourMap.show()


    def calcDistance(self, in_a, in_b):

        row_a = numpy.array(in_a)
        row_b = numpy.array(in_b)
        try:
            result = numpy.sqrt(sum((row_a - row_b) ** 2))
        except:
            import pdb; pdb.set_trace()
        return result


def main():

    image = Image.open("images/Lenna.png")

    k = Kmeans(image, size=200)
    result = k.run(3)
    print(result)

    k.showImage()
    k.showCentroidColours()
    k.showClustering()

if __name__ == "__main__":
    main()
    
