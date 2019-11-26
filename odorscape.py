import numpy as np
import cv2

def convert_canvas_to_bitmap(canvas):
    label = QLabel()
    pixmap = QPixmap('path_to_your_image')
    label.setPixmap(pixmap)

    height, width, channel = cvImg.shape
    bytesPerLine = 3 * width
    qImg = QImage(cvImg.data, width, height, bytesPerLine, QImage.Format_RGB888)

def load_canvas(canvas_address):
    canvas = np.load(canvas_address)
    return canvas

def save_canvas(canvas, canvas_address):
    np.save(canvas, canvas_address)
    return None


class Canvas(object):
    def __init__(self, w=1000, h=1000, resolution=2):
        self.w = w
        self.h = h
        self.airchannel = np.zeros((h, w), dtype=np.int16)
        self.channel1 = np.zeros((h, w), dtype=np.int16)
        self.channel2 = np.zeros((h, w), dtype=np.int16)

    def build_canvas(self):
        self.canvas = np.zeros((self.h, self.w, 3))
        self.canvas[:,:,0] = self.airchannel
        self.canvas[:,:,1] = self.channel1
        self.canvas[:,:,2] = self.channel2
        self.canvas = self.canvas.astype(np.uint8)
        return self.canvas

    def add_circular_gradient(self, x, y, r, max, min, channel):
        patch = np.zeros((2*r, 2*r))
        center = np.array([r,r])
        for i in range(2*r):
            for j in range(2*r):
                dist = np.linalg.norm(np.array([i,j]) - center)
                if dist <= r:
                    patch[i,j] = (1-(dist/r))*(max - min)
        patch = patch.astype(np.int16)
        if channel=='1':
            self.channel1[(y-r):(y+r), (x-r):(x+r)] += patch[:,:]
        if channel=='2':
            self.channel2[(y-r):(y+r), (x-r):(x+r)] += patch[:,:]


    def add_square_gradient(self, x, y, w, h, max, min, channel, maxat='Top'):

        if maxat=='Top':
            strand = np.linspace(max, min, num=h)
            tup = tuple([strand for i in range(w)])
            layer = np.column_stack(tup)
        if maxat=='Bottom':
            strand = np.linspace(min, max, num=h)
            tup = tuple([strand for i in range(w)])
            layer = np.column_stack(tup)
        if maxat=='Left':
            strand = np.linspace(max, min, num=w)
            tup = tuple([strand for i in range(h)])
            layer = np.row_stack(tup)
        if maxat=='Right':
            strand = np.linspace(min, max, num=w)
            tup = tuple([strand for i in range(h)])
            layer = np.row_stack(tup)

        # Replace canvas patch with gradient
        layer = layer.astype(np.int16)

        if channel=='1':
            self.channel1[y:(y+h), x:(x+w)] += layer[:,:]

        if channel=='2':
            self.channel2[y:(y+h), x:(x+w)] += layer[:,:]


    def check_and_correct_overlap(self):

        composite = np.add(self.channel1, self.channel2)
        problem_row = list(np.where(composite>255)[0])
        problem_col = list(np.where(composite>255)[1])
        problem_coords = [[problem_row[i], problem_col[i]] for i in range(len(problem_row))]

        for point in problem_coords:
            sum = self.channel1[point[0], point[1]]+self.channel2[point[0], point[1]]

            ch1_val = int((self.channel1[point[0], point[1]]/sum)*255)
            ch2_val = int((self.channel2[point[0], point[1]]/sum)*255)

            self.channel1[(point[0]),(point[1])] = ch1_val
            self.channel2[(point[0]),(point[1])] = ch2_val

        self.airchannel = 255*np.ones(self.channel1.shape) - (self.channel1 + self.channel2)

        self.build_canvas()

        # cv2.imshow('g', self.canvas)
        # cv2.waitKey(0)

        return None

if __name__ == "__main__":
    canvas = Canvas(600,600)
    canvas.add_square_gradient(200, 0, 200, 600, 255, 0, 1, maxat='top')
    canvas.add_circular_gradient(400, 400, 100, 255, 0, 2)
    canvas.add_circular_gradient(200, 400, 100, 255, 0, 1)

    canvas.check_and_correct_overlap()
    cv2.imshow('grad1', canvas.canvas)
    cv2.waitKey(0)








#
