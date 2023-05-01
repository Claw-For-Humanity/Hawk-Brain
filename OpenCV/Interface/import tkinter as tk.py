import tkinter as tk


root = tk.Tk()

# create a PhotoImage object with your logo image
logo = tk.PhotoImage(file="/Users/changbeankang/Desktop/GitHub/Claw-For-Humanity/Com/logo/Picture2.png")

# set the logo as the icon of the window
root.iconphoto(True, logo)
# root.iconphoto(False, logo)

# set the window title
root.title("My App")
logo_label = tk.Label(root, image=logo)
logo_label.pack()
# set the window size
root.geometry("400x300")

# add widgets to the window
# ...

# start the main loop
root.mainloop()


#/Users/changbeankang/Desktop/GitHub/Claw-For-Humanity/Com/logo