if __name__ == "__main__":
    ## Builtin: gui
    import tkinter
    ## This Module
    from gui import controllers

    root = tkinter.Tk()
    main = controllers.MainController(parentpane = root)
    root.mainloop()