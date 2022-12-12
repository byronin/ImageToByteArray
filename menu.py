from tkinter import *
from tkinter import Tk
import tkinter.filedialog
from io import BytesIO
from PIL import Image
import os

UI = Tk()
UI.title('Ronin image2bytearray')
UI.geometry('900x300')
UI.config(bg="grey")
directory_func = tkinter.filedialog
y_scale = StringVar()
x_scale = StringVar()
filename = StringVar()
foldername = StringVar()
bytearray_string = StringVar()

code_str1 = "from machine import Pin, I2C \n"
code_str2 = "from ssd1306 import SSD1306_I2C \n"
code_str3 = "import framebuf \n"
code_str4 = "i2c=I2C(1, scl = Pin(15), sda = Pin(14), freq = 400000) \n"
code_str5 = "oled = SSD1306_I2C(128, 64, i2c) \n"
code_str6 = "buffer = bytearray("
code_str7 = ") \n"
code_str8 = "fb = framebuf.FrameBuffer(buffer,"
code_str9 = ", framebuf.MONO_HLSB) \n"
code_str10 = "oled.blit(fb, "
code_str11 = "oled.show()"

def print_box(Message):
    text_box.insert("end", Message + "\n")
    text_box.see("end")
    UI.update()



scale_x_box = Text(UI,height=1,width=5)
scale_x_box.place(x=100,y=51)

scale_y_box = Text(UI,height=1,width=5)
scale_y_box.place(x=150,y=51)

oled_photo = PhotoImage(file='oled.png')
oled_button = Button(UI, image=oled_photo, borderwidth=0, height=190, width=188, bg="grey")
oled_button.place(x=680, y=8)


test_button = Button(UI, image=oled_photo, borderwidth=0, height=190, width=188, bg="grey")
test_button.place(x=680, y=8)
def select_file():
    Tk().withdraw()
    filename.set(directory_func.askopenfilename())
    file_box.insert("end", filename.get()+ "\n")
    print_box(filename.get())




def export_txt():
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    foldername.set(directory_func.askdirectory())  # show an "Open" dialog box and return the path to the selected file
    completeName = os.path.join(foldername.get(), "byte_array_for_oled.txt")
    file1 = open(completeName, "w")
    x_scale.set(scale_x_box.get(1.0, "end-1c"))
    y_scale.set(scale_y_box.get(1.0, "end-1c"))
    int_yscl = int(y_scale.get())
    int_xscl = int(x_scale.get())
    im = Image.open(filename.get()).convert('1')
    im_resize = im.resize((int_xscl, int_yscl))
    buf = BytesIO()
    im_resize.save(buf, 'ppm')
    byte_im = buf.getvalue()
    temp = len(str(int_xscl) + ' ' + str(int_yscl)) + 4
    expt_byte = byte_im[temp::]
    #print_box(expt_byte)
    #UI.update()
    file1.write(str(expt_byte))
    file1.close()
    print_box(foldername.get()+"byte_array_for_oled.txt")
    UI.update()


def export_pyt():
    x_fdc = 0
    y_fdc = 0
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    foldername.set(directory_func.askdirectory())  # show an "Open" dialog box and return the path to the selected file
    completeName = os.path.join(foldername.get(), "byte_array_for_oled.py")
    file1 = open(completeName, "w")
    x_scale.set(scale_x_box.get(1.0, "end-1c"))
    y_scale.set(scale_y_box.get(1.0, "end-1c"))
    int_yscl = int(y_scale.get())
    int_xscl = int(x_scale.get())
    im = Image.open(filename.get()).convert('1')
    im_resize = im.resize((int_xscl, int_yscl))
    buf = BytesIO()
    im_resize.save(buf, 'ppm')
    byte_im = buf.getvalue()
    temp = len(str(int_xscl) + ' ' + str(int_yscl)) + 4
    expt_byte = byte_im[temp::]
    if int_xscl < 128:
        x_fdc = 128 - int_xscl
        x_fdc = x_fdc / 2
    if int_yscl < 64:
        y_fdc= 64- int_yscl
        y_fdc = y_fdc / 2
    file1.write(code_str1 + code_str2 + code_str3 + code_str4 + code_str5 + code_str6 + str(expt_byte) +code_str7 + code_str8 +str(int(int_xscl)) + ',' + str(int(int_yscl)) + code_str9 + code_str10 + str(int(x_fdc))+","+ str(int(y_fdc))+")\n" + code_str11 )
    file1.close()
    print_box(foldername.get()+"byte_array_for_oled.py")
    UI.update()

def test_array():
    x_place = 0
    y_place = 0
    x_scale.set(scale_x_box.get(1.0, "end-1c"))
    y_scale.set(scale_y_box.get(1.0, "end-1c"))
    int_yscl = int(y_scale.get()) * 1.02518
    int_xscl = int(x_scale.get()) * 1.02518
    int_yscl = int(int_yscl * 1.1718)
    int_xscl = int(int_xscl * 1.1718)
    im = Image.open(filename.get()).convert('1')
    im_resize = im.resize((int_xscl, int_yscl))
    buf = BytesIO()
    im_resize.save(buf, 'ppm')
    byte_im = buf.getvalue()
    temp = len(str(int_xscl) + ' ' + str(int_yscl)) + 4
    print(byte_im[temp::])
    img = Image.frombytes("1", (int_xscl, int_yscl), byte_im[temp::])
    img.save("test.png")
    testing = PhotoImage(file='test.png')
    test_button.config(image = testing, height=int_yscl, width=int_xscl)
    if int_xscl < 151:
        x_place = 151 - int_xscl
        x_place = x_place / 2
    if int_yscl < 75:
        y_place = 75 - int_yscl
        y_place = y_place / 2
    test_button.place(x=int(698+x_place), y=int(51+y_place))
    UI.update()
    #test_button.pack()
    #test_button.pack_forget()




text_box = Text(UI , height=10, width=40)
text_box.pack(side=LEFT,expand=True)

text_box.place(x=330,y=10)
text_box.config(bg='#D9D8D7')
sb_ver = Scrollbar(UI , orient=VERTICAL)
sb_ver.pack(side=RIGHT, fill=Y)
text_box.config(yscrollcommand=sb_ver.set)
sb_ver.config(command=text_box.yview)

file_box = Text(UI,height=1,width=20)
file_box.place(x=32,y=20)

select_button = Button(UI, text="Select File",command=select_file,height=1, width=12)
select_button.place(x=200,y=19)

scale_label = Label(UI, text="XY Scale:", height=1, width=10, bg="grey", font="Candara")
scale_label.place(x=17, y=49)

scale_x_box = Text(UI,height=1,width=5)
scale_x_box.place(x=100,y=51)

scale_y_box = Text(UI,height=1,width=5)
scale_y_box.place(x=150,y=51)

export_test_button = Button(UI, text="Test",command=test_array,height=1, width=12)
export_test_button.place(x=200,y=50)

export_byte_button = Button(UI, text="Get byte[]",command=export_pyt,height=1, width=12)
export_byte_button.place(x=200,y=80)

github_photo = PhotoImage(file='github.png')
github_button = Button(UI, image=github_photo, borderwidth=0, height=78, width=200, bg="grey")
github_button.place(x=10, y=112)

UI.mainloop()