""" This is a gui-driven test environment """

if __name__ == "__main__":
    import tkinter
    from alcustoms.tkinter import style
    import controllers

    root = tkinter.Tk()
    style.loadstyle()
    main = controllers.MainController(parentpane = root)
    main.loadmenu()
    root.mainloop()