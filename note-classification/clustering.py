from PIL import Image

class Cluster():
    '''Classifies note characters based on a ratio of black to non-black pixels of an RGB image. Each note is
    classified individually. Current classifications consist of: blank space, bar line, quarter note, half note.'''

    def clusterData(self, imageFile):
        '''Takes an RGB image and determines the number of "black" pixels (set by bCutoff threshold),
        the number of total pixels, and the ratio of black to white pixels. clusterData must be called before any
        other Cluster method is invoked.'''
        im = Image.open(imageFile)

        pixels = im.getdata()
        bCutoff = (50, 50, 50)
        self.nBlack = 0
        self.ratio = 0
        self.tPixels = len(pixels)

        for pixel in pixels:
            if (pixel < bCutoff):
                self.nBlack += 1

        self.ratio = self.nBlack/self.tPixels

    def displayData(self):
        '''Displays data on number of black pixels, number of total pixels, and ratio of black-total pixels.'''
        print("----------------------------------------------")
        print("Number of black pixels: " + str(self.nBlack))
        print("Number of total pixels: " + str(self.tPixels))
        print("Ratio of black-total pixels: " + str(self.ratio))
        print("----------------------------------------------\n")

    def classify(self):
        '''Uses data from clusterData to classify character. Returns 3 for bar line, 2 for
        quarter note, 1 for half note, and 0 for blank space.'''
        if self.ratio >= 0.2:
            print("bar line")
            return 3
        if 0.075 <= self.ratio <= 0.11:
            print("quarter note")
            return 2
        elif 0.05 <= self.ratio <= 0.07:
            print("half note")
            return 1
        else:
            print("blank space")
            return 0


if __name__ == "__main__":
    print("Test 1")
    test1 = Cluster()
    test1.clusterData('Characters/hand_drawn_quarter_note.PNG')
    test1.classify()
    test1.displayData()
    test1.clusterData('Characters/hand_drawn_half_note.PNG')
    test1.classify()
    test1.displayData()

    print("Test 2")
    test2 = Cluster()
    test2.clusterData('Characters/hand_drawn_quarter_note2.PNG')
    test2.classify()
    test2.displayData()
    test2.clusterData('Characters/hand_drawn_half_note2.PNG')
    test2.classify()
    test2.displayData()

    print("Test 3")
    test3 = Cluster()
    test3.clusterData('Characters/hand_drawn_quarter_note3.PNG')
    test3.classify()
    test3.displayData()
    test3.clusterData('Characters/hand_drawn_half_note3.PNG')
    test3.classify()
    test3.displayData()

    print("Test 4")
    test4 = Cluster()
    test4.clusterData('Characters/bar_line.PNG')
    test4.classify()
    test4.displayData()
    test4.clusterData('Characters/blank_space.PNG')
    test4.classify()
    test4.displayData()
