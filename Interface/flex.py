import tkinter as tk


def launcher():
    root = tk.Tk()
    root.title("Project Claw For Humanity")

    logo = tk.PhotoImage(file="/Users/changbeankang/Desktop/GitHub/Claw-For-Humanity/Com/logo/Picture2.png")
    root.iconphoto(True, logo)
    logo = logo.subsample(2)
    logo_label = tk.Label(root, image=logo)
    logo_label.pack()
    
    # logo.subsample(2)


    root.geometry("300x300")  
    root.mainloop()
    
launcher()