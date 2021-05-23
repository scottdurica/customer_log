from db import DBHandler
from gui import GUI


# start and load the UI
db = DBHandler()
gui = GUI(db)
gui.mainloop()
