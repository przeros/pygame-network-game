from common.Object import Object

class Circle(Object):
    background_color = (255, 255, 255)
    r = None

    def __init__(self, x, y, image_path, r):
        super().__init__(x, y, image_path)
        self.r = r