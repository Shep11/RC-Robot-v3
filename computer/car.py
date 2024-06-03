
HEADER = 64

class car:
    def __init__(self, conn, addr, controler, name):
        self.conn = conn
        self.addr = addr
        self.controler = controler
        self.name = name
    
    def update(self):
        
