from tkinter import *
import PIL.Image, PIL.ImageTk
import renderer
import xml.etree.ElementTree as ET
import camera
from tkinter import filedialog
from PIL import Image,ImageTk

window = Tk()
window.geometry('960x540')
pozicia_x = 0
pozicia_y = 0
pozicia = 0
canvas = Canvas(window,width=960,height=540)
canvas.pack(fill="both", expand=True)
cam = camera.Camera(dimensions = (960,540))
tree = ET.parse("map.osm")
re = renderer.Renderer(cam, tree)
re.center_camera()
vykreslit = re.render()
image = PIL.ImageTk.PhotoImage(vykreslit)
imagesprite = canvas.create_image(480,270,image=image)
#copy_of_image = image.copy()
def mouse_wheel(event):
    global image
    global vykreslit
    global imagesprite
    global re
    if event.delta == 120 or event.num == 4:
        cam.zoom_in((event.x,event.y))
    if event.delta == -120 or event.num == 5:
        cam.zoom_out((event.x, event.y))
    vykreslit = re.render()
    image = PIL.ImageTk.PhotoImage(vykreslit)
    imagesprite = canvas.create_image(480,270,image=image)
def mouse_left_click(event):
    global pozicia_x
    global pozicia_y
    global pozicia
    pozicia_x = event.x
    pozicia_y = event.y
    pozicia = cam.px_to_gps((pozicia_x, pozicia_y))
def mouse_left_move(event):
    global pozicia_x
    global pozicia_y
    global imagesprite
    global cam
    global re
    global vykreslit
    global tree
    global canvas
    global image
    global x
    global y
    cam.move_point_to_pixel(pozicia, (event.x, event.y))
    canvas.delete(imagesprite)
    vykreslit = re.render()
    image = ImageTk.PhotoImage(vykreslit)
    imagesprite = canvas.create_image(int(x/2),int(y/2),image=image)
def on_resize(event):
    global pozicia_x
    global pozicia_y
    global stred_x
    global stred_y
    global imagesprite
    global cam
    global re
    global vykreslit
    global tree
    global canvas
    global image
    global x
    global y
    x = canvas.winfo_reqwidth()
    y = canvas.winfo_reqheight()
    wscale = float(event.width)/x
    hscale = float(event.height)/y
    x = event.width
    y = event.height
    canvas.config(width=x, height=y)
    #canvas.delete(imagesprite)
    x = canvas.winfo_reqwidth()
    y = canvas.winfo_reqheight()
    cam.px_width = x
    cam.px_height = y
    canvas.delete(imagesprite)
    vykreslit = re.render()
    image = ImageTk.PhotoImage(vykreslit)
    imagesprite = canvas.create_image(int(x/2),int(y/2),image=image)
def UploadAction(event=None):
    global filename
    global cam
    global tree
    global re
    global vykreslit
    global canvas
    global image
    global imagesprite
    filename = filedialog.askopenfilename()
    cam = camera.Camera(dimensions = (960,540))
    tree = ET.parse(str(filename))
    re = renderer.Renderer(cam, tree)
    re.center_camera()
    vykreslit = re.render()
    image = PIL.ImageTk.PhotoImage(vykreslit)
    imagesprite = canvas.create_image(480,270,image=image)
canvas.addtag_all("all")
quit_button = Button(window, text = "Open", command=UploadAction)
quit_button_window = canvas.create_window(10, 10, anchor='nw', window=quit_button)
canvas.bind("<MouseWheel>", mouse_wheel)
canvas.bind("<Button-4>", mouse_wheel)
canvas.bind("<Button-5>", mouse_wheel)
canvas.bind("<Button-1>", mouse_left_click)
canvas.bind("<B1-Motion>", mouse_left_move)
canvas.bind("<Configure>", on_resize)
canvas.addtag_all("all")
#frame.pack()
window.mainloop()
