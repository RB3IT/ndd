## Builtin
import math
## Custom module
from NewDadsDoor import classes

#### Gui
## Builtin
import tkinter as tk, tkinter.ttk as ttk
## Custom Module
from alcustoms.tkinter import smarttkinter, advancedtkinter

SmartFrame = smarttkinter.ttk.SmartFrame

class MainPane(smarttkinter.GMMixin,SmartFrame):
    def __init__(self,parent,**kw):
        super().__init__(parent,**kw)
        self.wires = list()
        
        ttk.Label(self, text = "Quick Spring Demo", style = "Title.TLabel")

        f = SmartFrame(self)
        ttk.Label(f, text="Required Torque", style = "Bold.TLabel")
        self.ipptvar = tk.DoubleVar()
        ttk.Entry(f, textvariable = self.ipptvar)
        ttk.Label(f, text="Cycles Rating", style = "Bold.TLabel")
        self.cyclevar = tk.IntVar()
        ttk.Combobox(f, values = list(classes.CYCLES), textvariable = self.cyclevar).state(["readonly",])
        ttk.Label(f, text="Total Turns", style = "Bold.TLabel")
        self.tturnsvar = tk.DoubleVar()
        self.tturnsvar.set(1)
        ttk.Entry(f, textvariable = self.tturnsvar)
        ttk.Label(f, text="OD", style = "Bold.TLabel")
        self.odvar = tk.DoubleVar()
        cb = ttk.Combobox(f, values = list(set(wire['min_od'] for wire in classes.iterwire())), textvariable = self.odvar)
        cb.current(0)
        cb.state(["readonly",])
        smarttkinter.massgrid(f,width = 2)

        f = SmartFrame(self)
        ttk.Label(f, text="Wire", style = "BoldUnderline.TLabel")
        ttk.Label(f, text="Uncoiled length", style = "BoldUnderline.TLabel")
        ttk.Label(f, text="Coiled length", style = "BoldUnderline.TLabel")
        for wire in classes.iterwire():
            ttk.Label(f, text=wire['wirediameter'], style = "Bold.TLabel")
            u = ttk.Label(f)
            c = ttk.Label(f)
            self.wires.append((wire,u,c))
        smarttkinter.massgrid(f, width = 3)

        smarttkinter.masspack(self)

class MainController(advancedtkinter.Controller):
    def __init__(self, pane = MainPane, **kw):
        super().__init__(pane = pane, **kw)

        p = self.pane
        p.cyclevar.set(min(classes.CYCLES))
        for var in [p.ipptvar,p.cyclevar,p.tturnsvar,p.odvar]:
            var.trace("w",self.updatewires)

    def updatewires(self,*event):
        """ Updates the displayed wires """
        p = self.pane
        try: ippt = p.ipptvar.get()
        ## For when ipptentry is empty
        except: ippt = 0
        cycles = p.cyclevar.get()
        try: tturns = p.tturnsvar.get()
        ## For when tturnsentry is empty
        except: tturns = 1
        od = p.odvar.get()

        torquepercentage = classes.CYCLES[cycles]['torquepercentage']
        
        for (wire,ulabel,clabel) in p.wires:
            ulength, clength = "N/A","N/A"
            valid = wire['mp_base'] * torquepercentage > ippt * tturns / 1.015
            if valid:
                if wire['min_od'] <= od:
                    try:
                        ulength = wire['liftrate'] / ippt
                        coillength = math.pi * (od - wire['wirediameter'])
                        clength = ulength / coillength * wire['wirediameter']
                    ## ippt empty or 0
                    except ZeroDivisionError: pass
            ulabel.configure(text = "{:.04}".format(ulength))
            clabel.configure(text = "{:.04}".format(clength))


if __name__ == "__main__":
    root = tk.Tk()
    from alcustoms.tkinter import style
    style.loadstyle()
    main = MainController(parentpane = root)
    main.pane.show()
    root.mainloop()
        
