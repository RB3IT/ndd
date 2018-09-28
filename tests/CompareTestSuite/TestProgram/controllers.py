## Builtin
import collections
import copy
import threading
## Builtin: gui
import tkinter as tk, tkinter.ttk as ttk
## Third Party Module
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends import backend_tkagg as tkagg
import mpl_toolkits.mplot3d as plt3d
## Custom Module
from alcustoms import tests
from alcustoms.tkinter import advancedtkinter, smarttkinter
## This Module
from NewDadsDoor.tests.CompareTestSuite.TestProgram import panes
from NewDadsDoor.tests.CompareTestSuite import classes, helpers
## Parent Module
from NewDadsDoor import classes as dadsclasses

class MainController(advancedtkinter.StackingManager):
    """ Primary Controller responsible for managing Root and switching Panes """
    def cleanup(self):
        super().cleanup()
        self.parentpane.destroy()
    def loadmenu(self):
        self.newchild(MenuController)

    def loadtests(self):
        testman = self.newchild(TestManager, eventmanager = None)
        testman.loadrunning()


class MenuController(advancedtkinter.Controller):
    """ Main Menu Controller """
    def __init__(self,pane = panes.MenuPane, **kw):
        super().__init__(pane = pane, **kw)

        p = self.pane
        p.runtestsbutton.configure(command = self.parent.loadtests)
        p.quitbutton.configure(command = self.parent.cleanup)

class TestManager(advancedtkinter.StackingManager):
    """ Manager Controller responsible for switching Panes in the Tests fork """
    def __init__(self,**kw):
        super().__init__(**kw)
        self.eventmanager.bind("<<StackModified>>",self.checkcleanup)
    def checkcleanup(self,*event):
        if not self.stack:
            self.parent.dequeue(self)
    def loadrunning(self):
        """ Loads the RunningPane """
        self.newchild(RunningController)

    def loadresults(self, success, fail):
        """ Loads the ResultsPane """
        self.newchild(ResultsController, success = success, fail = fail)

class RunningController(advancedtkinter.Controller):
    """ Pane Controller which displays current test(s) being run """
    def __init__(self,pane = panes.RunningPane, **kw):
        super().__init__(pane = pane, **kw)
        self.workerthread = None
        self.totaltests = 0
        self.currenttest = 0

        p = self.pane
        p.cancelbutton.configure(command = self.canceltoparent)

    def canceltoparent(self):
        self.parent.dequeue(self)

    def startup(self):
        testmethods = tests.gettests(classes)
        self.totaltests = len(testmethods)
        self.workerthread = threading.Thread(target = runtests, kwargs = dict(testmethods = testmethods, parent = self))
        self.workerthread.start()

    def cleanup(self):
        self.workerthread = None
        return super().cleanup()

    def setcurrent(self,method,stepsize):
        """ Updates the display to show currently running test """
        self.currenttest += 1
        self.pane.currentmessage.configure(text = method)
        self.pane.loadingbar.step(stepsize)

    def completetests(self, success, fail):
        """ Recieves the successes and failures from workerthread and passes them on to parent """
        self.workerthread = None
        self.pane.currentmessage.configure(text = "")
        self.pane.loadingmessage.configure(text = "Complete")
        self.parent.loadresults(success,fail)

def runtests(testmethods, parent = None):
    """ Thread method for running tests, gathering results, and reporting back in """
    successful, failures = list(), list()
    numbertests = len(testmethods)
    testdata = classes.gathertestdata()
    for i,(testname,test) in enumerate(testmethods, start = 1):
        ## Check if program is alive
        if not parent or not parent.workerthread: break
        parent.setcurrent(testname,100 / numbertests)
        results = test(testdata = copy.deepcopy(testdata), fail = False)
        if results:
            failures.append((testname,results))
        else:
            successful.append(testname)
    if parent and parent.workerthread:
        parent.completetests(successful, failures)


class ResultsController(advancedtkinter.Controller):
    """ Displays the information on the results

    On Continue, cleans up Parent (TestManager), which clears
    current stack and returns to Main Menu
    """
    def __init__(self, pane = panes.ResultsPane, success = None, fail = None, testdata = None, **kw):
        super().__init__(pane = pane, **kw)
        self.success = success
        self.fail = fail
        if testdata is None: testdata = helpers.testdatabyjobnumber()
        self.testdata = testdata

        self.removedtabs = list()

        p = self.pane
        p.passedbutton.configure(command = self.showpassed)
        p.continuebutton.configure(command = self.parent.cleanup)

    def startup(self):
        p = self.pane
        p.bind("<Double-Escape>", self.reloadtabs)
        p.passlabel.configure(text = f"{len(self.success)} Tests Passed")
        p.faillabel.configure(text = f"{len(self.fail)} Tests Failed")
        self.loadtabs()

    def loadtabs(self):
        p = self.pane
        TRIALS = helpers.importtestdata()

        ## Populate Notebook
        for testname,fails in self.fail:
            ## Convert output to structured dict
            output = dict(title = testname, headers = panes.TESTHEADERS, trials = len(TRIALS))
            ## This is a mostly-superfluous step, but ensures that
            ## the ResultTab will always pull the correct info from each trial
            bads = [dict(zip(panes.TESTHEADERS,trial)) for trial in fails]
            output['badresults'] = bads
            tab = panes.ResultTab(p.resultnotebook, testname = testname)
            tab.setresult(output)
            tab.showchartbutton.configure(command = self.showchart, args = (tab,))
            tab.bind("<Button-2>", lambda *e: self.removetab(tab))
            p.resultnotebook.add(tab,text=testname)

    def removetab(self,tab):
        """ Removes a tab """
        self.pane.resultnotebook.hide(tab)
        self.removedtabs.append(tab)

    def reloadtabs(self,*event):
        """ Reshows hidden tabs """
        for tab in self.removedtabs: self.pane.resultnotebook.add(tab, tab.testname)

    def showpassed(self):
        """ Launces a new window to display a list of Passed Tests """
        con = self.addchildcontroller(SuccessController, eventmanager = None, passed = self.success)
        con.startup()

    def showchart(self,tab):
        """ Launches a new window to display and manage a Results Chart """
        badjobnumbers = [bad["Job Number"] for bad in tab.result['badresults']]
        gooddata = [data for jobnumber,data in self.testdata.items() if jobnumber not in badjobnumbers]
        baddata = [self.testdata[bad] for bad in badjobnumbers]
        con = self.addchildcontroller(ChartController, eventmanager = None, title = tab.result['title'], gooddata = gooddata, baddata = baddata)
        con.startup()

class SuccessController(advancedtkinter.Controller):
    def __init__(self,pane = panes.SuccessWindow, passed = None, **kw):
        super().__init__(pane = pane, **kw)
        if passed is None: passed = list()
        self.passed = passed

        p = self.pane
        p.quitbutton.configure(command = self.cleanup)
        p.setsearchbar(self.filtertreeview)

    def startup(self):
        self.pane.treeview.searchbar.filter()

    def filtertreeview(self,searchvalue):
        """ Filters the Treeview """
        ## If searchvalue is empty string, then it will exist in all functions, so we don't have to check
        return [(func,) for func in self.passed if searchvalue.lower() in func.lower()]

CHARTDICT = dict(figure = None, axes = None, chart = None, toolbar = None, goodseries = None, badseries = None)

class ChartController(advancedtkinter.Controller):
    """ Controller for a popup window which displays a chart related to the errors in question """
    MAXFIELDS = 3
    def __init__(self, pane = panes.ChartWindow, title = "Chart", gooddata = None, baddata = None, defaults = None, **kw):
        """ Creates a new ChartController which creates a Chart Window by default.

        data should be values to chart.
        defaults are the default axis values for the chart.
        If more than 3 defaults are specified, only the last 3 elements are used.
        """
        super().__init__(pane = pane, **kw)
        self.chart = dict(CHARTDICT)
        
        self.data = dict()
        if gooddata is None: gooddata = dict()
        if baddata is None: baddata = dict()
        if defaults is None: defaults = ['width','stopheight']
        self.data['good'] = gooddata
        self.data['bad'] = baddata
        self.data['goodcolor'] = "blue"
        self.data['badcolor'] = "red"
        self.data['defaultheaders'] = defaults
        
        self.attrs = collections.deque(maxlen=self.MAXFIELDS)
        self.fields = dict()

        p = self.pane
        p.protocol("WM_DELETE_WINDOW", self.cleanup)
        p.titlelabel.configure(text=title)
        p.goodbadvar.trace('w',self.toggledata)

    def startup(self):
        for header in helpers.getvalidationfields():
            box = tk.Checkbutton(self.pane.optionsframe, text = header, command = lambda header = header: self.addattr(header))
            self.fields[header] = box
            box.bind("<ButtonPress-3>",self.deselectall)
            if header in self.data['defaultheaders']: box.invoke()

        smarttkinter.massgrid(self.pane.optionsframe)

        self.displaychart()

        return super().startup()

    def deselectall(self, event = None):
        """ Deselects all fields """
        for field in self.fields.values():
            field.deselect()
        self.attrs.clear()
        if event:
            event.widget.select()
            ## Note I'm being lazy here!
            self.addattr(event.widget.cget('text'))

    def toggledata(self,*event):
        """ Updates the displayed data """
        value = self.pane.goodbadvar.get()
        ## Both
        if value == -1: good, bad = True, True
        ## Valid
        elif value: good, bad = True, False
        ## Invalid
        else: good, bad = False, True
        self.chart['goodseries'].set_visible(good)
        self.chart['badseries'].set_visible(bad)
        self.chart['canvas'].draw()

    def addattr(self, attr):
        """ Triggers when Checkbutton is pressed. Updates Chart Fields and checkbuttons """
        if attr in self.attrs:
            self.attrs.remove(attr)
        else:
            ## Clumsy way of doing it, but there is no way to hook into deque automatically popping values
            if len(self.attrs) == self.MAXFIELDS:
                ## Untoggle value that's about to be popped
                self.fields[self.attrs[0]].toggle()
            self.attrs.append(attr)
        self.displaychart()

    def displaychart(self):
        """ Clears the chart area and displays a new chart (or a label if missing required items) """
        self.clearchart()
        attrs = len(self.attrs)
        if attrs == 3: projection = "3d"
        else: projection = None
        self.chart['figure'],self.chart['axes'] = newchart(projection = projection)
        self.chart['canvas'],self.chart['chart'], self.chart['charttoolbar'] = displaychart(self.chart['figure'],self.pane.chartframe)

        if not self.attrs:
            self.setchartlabel("No Axis to Display")
        elif not self.data:
            self.setchartlabel("No Data to Display")
        else:
            if attrs == 1:
                self._linechart()
            elif attrs == 2:
                self._xychart()
            elif attrs == 3:
                self._3dchart()
            else:
                self.setchartlabel("Too Many Variables to Display")
        self.toggledata()

    def clearchart(self):
        """ Removes all elements from the chart Frame """
        if self.chart['chart']: self.chart['chart'].destroy()
        if self.chart['toolbar']: self.chart['toolbar'].destroy()
        smarttkinter.clearwidget(self.pane.chartframe)
        self.chart = dict(CHARTDICT)

    def setchartlabel(self,label):
        """ Displays a label centered in the chart area """
        cf = self.pane.chartframe
        smarttkinter.ttk.SmartFrame(cf).pack(fill = 'both', expand = True)
        ttk.Label(cf, text = label, style = "Subtitle.TLabel", anchor = "center", justify = "center").pack()
        smarttkinter.ttk.SmartFrame(cf).pack(fill = 'both',expand = True)

    def getseries(self,attr):
        """ Helper function for pulling a good and bad series for the given attr """
        return [data[attr] for data in self.data['good']],[data[attr] for data in self.data['bad']]

    def _plotvalues(self, goodvalues = None, badvalues = None, **kw):
        """ Helper function to draw good and bad series (regardless of length) """
        self.chart['goodseries'] = self.chart['axes'].scatter(*goodvalues, c = self.data['goodcolor'])
        self.chart['badseries'] = self.chart['axes'].scatter(*badvalues, c = self.data['badcolor'])

    def _linechart(self):
        """ Displays a single-axis chart """
        ## x axis attribute
        xattr = self.attrs[0]
        ## x axis values
        good_x_axis,bad_x_axis = self.getseries(xattr)
        ## Have to use a 2d chart as the base
        good_y_axis,bad_y_axis = [0 for data in self.data['good']],[0 for data in self.data['bad']]

        ## Fix obtuse values
        good_x_axis,bad_x_axis = parsedata(xattr,good_x_axis), parsedata(xattr,bad_x_axis)

        self._plotvalues(goodvalues = (good_x_axis,good_y_axis), badvalues = (bad_x_axis,bad_y_axis))

        self.chart['axes'].set_xlabel(xattr)

        ## Turn off y_axis
        self.chart['axes'].get_yaxis().set_visible(False)

    def _xychart(self):
        """ Displays a 2-axis chart """
        xattr, yattr = list(self.attrs)[:2]
        ## Get x values
        good_x_axis,bad_x_axis = self.getseries(xattr)
        ## Get y values
        good_y_axis,bad_y_axis = self.getseries(yattr)

        ## Fix obtuse values
        good_x_axis,bad_x_axis = parsedata(xattr,good_x_axis), parsedata(xattr,bad_x_axis)
        good_y_axis,bad_y_axis = parsedata(yattr,good_y_axis), parsedata(yattr,bad_y_axis)

        ## Builder Function
        self._plotvalues(goodvalues = (good_x_axis,good_y_axis), badvalues = (bad_x_axis,bad_y_axis))

        self.chart['axes'].set_xlabel(xattr)
        self.chart['axes'].set_ylabel(yattr)

    def _3dchart(self):
        """ Displays a 3d Chart """
        ## Get values
        xattr, yattr, zattr = list(self.attrs)[:3]
        ## Get x values
        good_x_axis,bad_x_axis = self.getseries(xattr)
        ## Get y values
        good_y_axis,bad_y_axis = self.getseries(yattr)
        ## Get z values
        good_z_axis,bad_z_axis = self.getseries(zattr)

        ## Fix obtuse values
        good_x_axis,bad_x_axis = parsedata(xattr,good_x_axis), parsedata(xattr,bad_x_axis)
        good_y_axis,bad_y_axis = parsedata(yattr,good_y_axis), parsedata(yattr,bad_y_axis)
        good_z_axis,bad_z_axis = parsedata(zattr,good_z_axis), parsedata(zattr,bad_z_axis)

        ## Builder Function
        self._plotvalues(goodvalues = (good_x_axis,good_y_axis, good_z_axis), badvalues = (bad_x_axis,bad_y_axis, bad_z_axis))

        self.chart['axes'].set_xlabel(xattr)
        self.chart['axes'].set_ylabel(yattr)
        self.chart['axes'].set_zlabel(zattr)

        plt3d.Axes3D.mouse_init(self.chart['axes'])

def parsedata(attr,values):
    """ Converts obtuse data to graph-able values """
    if attr == "Hand":
        out = []
        for v in values:
            if v.lower() == "rh": out.append(0)
            elif v.lower() == 'lh': out.append(1)
            else: out.append(-1)
        return out
    if attr == "pipe":
        return [dadsclasses.PIPELOOKUP[v]['radius'] for v in values]
    return values

def newchart(projection = False):
    """ Creates a new figure and subplot """
    ## Figure is the base
    figure = tkagg.Figure()
    ## Actual chart
    if projection:
        axes = figure.add_subplot(111, projection = projection)
    else:
        axes = figure.add_subplot(111)
    return figure,axes

def displaychart(plot, chartframe):
    """ Helper function for creating the tk widgets """
    canvas = tkagg.FigureCanvasTkAgg(plot,chartframe)
    chart = canvas.get_tk_widget()
    chart.pack(fill = 'both')
    charttoolbar = tkagg.NavigationToolbar2TkAgg(canvas,chartframe)
    return canvas, chart, charttoolbar