## each cell in puzzle
class Cell:
    def __init__(self,x,y,domain=['w','b'],value='_') :
        self.x=x
        self.y=y
        self.domain = domain
        self.value=value

    def change_color(self):
        if self.value == "w" or self.value == "W":
            self.value = "b"
        else:
            self.value = "w"