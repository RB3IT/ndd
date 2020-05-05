## Builtin: gui
import tkinter as tk, tkinter.ttk as ttk
## Custom
from alcustoms.tkinter import smarttkinter

## Current Headers
TESTHEADERS = ["Job Number","Target","Actual","Difference","% Difference"]

class MenuPane(smarttkinter.GMMixin,smarttkinter.ttk.SmartFrame):
    """ Main Menu Pane """
    def __init__(self,parent,**kw):
        super().__init__(parent,**kw)

        ttk.Label(self,text="BRD Services Test Module", style = "Title.TLabel")

        self.runtestsbutton = ttk.Button(self,text="Run Tests", style = 'Main.TButton')

        self.quitbutton = ttk.Button(self,text="Quit", style = 'Main.TButton')

        smarttkinter.masspack(self)

class RunningPane(smarttkinter.GMMixin, smarttkinter.ttk.SmartFrame):
    """ Intermediary Pane to show while tests are running; includes progress bar """
    def __init__(self,parent,**kw):
        super().__init__(parent,**kw)

        f = smarttkinter.ttk.SmartFrame(self)
        self.loadingmessage = ttk.Label(f,text="Running Tests", style = "Subtitle.TLabel")
        self.loadingmessage.pack()
        self.loadingbar = ttk.Progressbar(self)

        ff = smarttkinter.ttk.SmartFrame(self)
        self.currentmessage = ttk.Label(ff,style = "Italics.TLabel", justify = 'right')
        self.currentmessage.pack(side='right')

        self.cancelbutton = ttk.Button(self, text = "Cancel")

        smarttkinter.masspack(self)
        ff.pack_configure(fill='x')

class ResultsPane(smarttkinter.GMMixin, smarttkinter.ttk.SmartFrame):
    """ Results of Tests Pane. Header contains Passes vs Failures. Failures can be show as tabs on Notebook """
    def __init__(self, parent, **kw):
        super().__init__(parent,**kw)

        ttk.Label(self,text="Results", style = "Title.TLabel")
        self.passlabel = ttk.Label(self, style = 'Italics.Subtitle.TLabel')
        self.faillabel = ttk.Label(self, style = 'Italics.Subtitle.TLabel')

        self.resultnotebook = ttk.Notebook(self)

        f = smarttkinter.ttk.SmartFrame(self)
        self.passedbutton = ttk.Button(f,text="Show Passed")
        self.continuebutton = ttk.Button(f,text="Quit")
        smarttkinter.masspack(f, side = 'left', padx=3)
        
        smarttkinter.masspack(self)
        self.resultnotebook.pack_configure(fill='both',expand=True)

class ResultTab(smarttkinter.ttk.SmartFrame):
    """ A Tab to display information on the ResultPane's resultnotebook.
    
    Gives name, failure count, lists failures in table, and has button to display a Chart
    Table default headers are TESTHEADERS
    Show Chart Button should be configured independently.
    """
    def __init__(self,parent, testname = "Test", **kw):
        super().__init__(parent,**kw)
        self.result = None
        self.testname = testname

        self.titlelabel = ttk.Label(self,style = "Subtitle.TLabel")
        self.failurecountlabel = ttk.Label(self,style = "Italics.TLabel")
        self.failurelisttreeview = smarttkinter.ttk.SmartTreeview(self,columns = TESTHEADERS)

        f = smarttkinter.ttk.SmartFrame(self)
        
        ff = smarttkinter.ttk.SmartFrame(f)
        ttk.Label(ff, text = "Door:", style = "Bold.TLabel")
        self.selecteddoor = ttk.Label(ff)
        ff.masspack(side='left')
        
        self.showchartbutton = smarttkinter.ttk.SmartButton(f,text="Show Chart")
        f.masspack(side='left')

        smarttkinter.masspack(self)
        self.failurelisttreeview.pack_configure(fill='both', expand = True)

    def setresult(self,results):
        """ Sets the currently displayed test """
        self.result = results
        self.titlelabel.configure(text = results['title'])
        self.failurecountlabel.configure(text = f"Failures: {len(results['badresults'])} out of {results['trials']}")
        tree = self.failurelisttreeview
        tree.clear()
        ## Flexibility to change headers
        headers = results['headers']
        if headers != tree.get_headings():
            tree.setupcolumns({"name":header} for header in headers)
        for result in results['badresults']:
            values = [f"{float(result[header]):.02%}" if "%" in header else result[header] for header in headers]
            tree.insert("",'end',iid=result["Job Number"].strip(),values = values)

class SuccessWindow(tk.Toplevel):
    def __init__(self, master = None, **kw):
        super().__init__(master, **kw)
        self.transient()
        
        f = self.mainframe = smarttkinter.ttk.SmartFrame(self)
        ttk.Label(f, text="Passed Tests", style = 'Subtitle.TLabel')
        self.treeview = smarttkinter.ttk.SmartTreeview(f, columns = ("Name",))
        self.searchbar = None
        self.quitbutton = ttk.Button(f,text="Close")
        smarttkinter.masspack(f)
        self.treeview.pack_configure(fill='both',expand=True)

        smarttkinter.masspack(self)
        f.pack_configure(fill='both',expand=True)

    def setsearchbar(self,filtermethod):
        """ Creates a new searchbar with the given filtermethod """
        if self.searchbar:
            self.searchbar.destroy()
            self.searchbar = None
        self.searchbar = smarttkinter.ttk.SmartTreeviewSearchbar(self.treeview,filtermethod = filtermethod)

class ChartWindow(tk.Toplevel):
    def __init__(self,master = None, **kw):
        super().__init__(master, **kw)
        self.transient()
        
        f = self.mainframe = smarttkinter.ttk.SmartFrame(self)
        self.titlelabel = ttk.Label(f, style = "Subtitle.TLabel")
        
        ff = smarttkinter.ttk.SmartFrame(f)
        self.goodbadvar = tk.IntVar()
        tk.Radiobutton(ff, text="Invalid", variable = self.goodbadvar, value = 0, indicatoron = False)
        tk.Radiobutton(ff, text="Valid", variable = self.goodbadvar, value = 1, indicatoron = False)
        tk.Radiobutton(ff, text="Both", variable = self.goodbadvar, value = -1, indicatoron = False)
        smarttkinter.masspack(ff, side='left')

        self.chartframe = smarttkinter.ttk.SmartFrame(f)

        ff  = smarttkinter.ttk.SmartFrame(f)
        self.toggleoptionsbutton = ttk.Button(ff, text="Show", command = self.toggleoptions)
        self.toggleoptionsbutton.pack()
        self.optionsframe = smarttkinter.ttk.SmartFrame(ff)

        self.closebutton = ttk.Button(f,text="Close",command = self.destroy)

        smarttkinter.masspack(f)
        f.pack(fill='both',expand=True)

    def show(self):
        self.deiconify()
        self.lift()
        self.focus_force()

    def hide(self):
        self.iconfify()

    def toggleoptions(self):
        try:
            self.optionsframe.pack_info()
            self.optionsframe.pack_forget()
            self.toggleoptionsbutton.configure(text="Show")
        except:
            self.optionsframe.pack(fill='both')
            self.toggleoptionsbutton.configure(text="Hide")
