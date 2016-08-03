import BlastSequenceSearch
from tkinter import *
import TreeBuilder
import csvGenerator
import os
# base script that runs the two primary parts of the program
ana_dir = "Analysis"
nrps_dir = "NRPS"
dot_dir = "TreeDot"
Sraw_dir = "BLASTStandardRaw"
bla_dir = "BLAST"
root_dir = "NRPSRoot"
xml_dir = "BLASTXML"
csv_dir = "NRPSCSV"


# taken from code.activestate.com/recipes/52549 this is not mine
class curry:
    def __init__(self, fun, *args, **kwargs):
        self.fun = fun
        self.pending = args[:]
        self.kwargs = kwargs.copy()

    def __call__(self, *args, **kwargs):
        if kwargs and self.kwargs:
            kw = self.kwargs.copy()
            kw.update(kwargs)
        else:
            kw = kwargs or self.kwargs

        return self.fun(*(self.pending + args), **kw)


# a pocket class to allow me to use instance variable for various frames and other GUI related objects
class MyApp:

    # the initialization method where most of my GUI is built besides for action based parts
    def __init__(self, myParent):
        button_width = 7

        button_padx = "2m"
        button_pady = "1m"

        analysis_frame_padx = "3m"
        analysis_frame_pady = "2m"
        analysis_frame_ipadx = "3m"
        analysis_frame_ipady = "1m"

        # definition of primary and analysis factor lists
        self.blast_analysis = []
        self.tree_analysis = []
        self.tree_type = []
        self.tree_frame = []
        self.titles = []
        self.d_var = []

        # definition of all primary frames
        self.myParent = root
        self.analysis_container = Frame(root)
        self.analysis_container.pack(ipadx=analysis_frame_ipadx, ipady=analysis_frame_ipady, padx=analysis_frame_padx,
                                         pady=analysis_frame_pady)
        self.top_container = Frame(self.analysis_container, relief=RIDGE)
        self.top_container.pack(side=TOP)

        self.bottom_container = Frame(self.analysis_container, relief=RIDGE)
        self.bottom_container.pack(side=TOP)

        self.button_container = Frame(self.bottom_container, relief=RIDGE)
        self.button_container.pack(side=RIGHT)

        self.gbk_select_frame = Frame(self.top_container, relief=RIDGE)
        self.gbk_select_frame.pack(side=LEFT, fill=BOTH, expand=YES)

        self.tree_select_frame = Frame(self.top_container, relief=RIDGE)
        self.tree_select_frame.pack(side=LEFT, fill=BOTH, expand=YES)

        self.tree_type_frame = Frame(self.top_container, relief=RIDGE)
        self.tree_type_frame.pack(side=LEFT, fill=BOTH, expand=YES)

        self.type_text_frame = Frame(self.tree_type_frame, relief=RIDGE)
        self.type_text_frame.pack(side=LEFT, fill=BOTH, expand=YES)

        # creation of check buttons: 1 blast buttons
        self.g_var = []
        self.gbk_files = []
        for [dirpath, dirname, filename] in os.walk(root_dir):
            self.gbk_files.extend(filename)
        i = 0
        for file in self.gbk_files:
            self.g_var.append(IntVar())
            Checkbutton(self.gbk_select_frame, text=file, variable=self.g_var[i], onvalue=1, offvalue=0, command=curry(
                self.check_click_blast, i)).pack(side=TOP)
            i += 1

        # 2 tree buttons
        self.c_var = []
        self.csv_files = []
        for [dirpath, dirname, filename] in os.walk(os.path.join(ana_dir, os.path.join(nrps_dir, csv_dir))):
            self.csv_files.extend(filename)
        k = 0
        for file in self.csv_files:
            self.c_var.append(IntVar())
            Checkbutton(self.tree_select_frame, text=file, variable=self.c_var[k], onvalue=1, offvalue=0, command=curry(
                self.check_click_tree, k)).pack(side=TOP)
            k += 1

        # creation of labels for tree formatting buttons
        self.data_files = []
        f = open(os.path.join(ana_dir, os.path.join(nrps_dir, os.path.join(csv_dir, self.csv_files[0]))), 'r')
        s = f.readline()
        space = ""
        for file in s.split("^"):
            while len(file) > len(space):
                space += " "
        Label(self.type_text_frame, text=space + "                         ").pack(side=TOP)
        for file in s.split("^"):
            self.data_files.append(file)
            Label(self.type_text_frame, text=file).pack(side=TOP)

        # creation of analysis button
        self.x_button = Button(self.button_container, command=self.x_button_click, text="Analyse", background="cyan")
        self.x_button.focus_force()
        self.x_button.configure(width=button_width, padx=button_padx, pady=button_pady)
        self.x_button.pack(side=RIGHT)

    # the action handler for the analysis button; this checks which aspects of analysis should be undertaken
    def x_button_click(self):
        if len(self.blast_analysis) > 0 and self.blast_analysis.count(None) is not len(self.blast_analysis):
            BlastSequenceSearch.get_sequences(self.blast_analysis)
        if len(self.tree_analysis) > 0 and self.tree_analysis.count(None) is not len(self.tree_analysis):
            csvGenerator.create_csv(self.tree_analysis)
            if len(self.tree_type) > 0 and self.tree_type.count(None) is not len(self.tree_type):
                TreeBuilder.construct_tree(self.tree_analysis, self.tree_type)

    # the action handler for the Blast check boxes; adds and removes their values based on whether the button was turned
    # on or off
    def check_click_blast(self, i):
        if self.g_var[i].get() == 1:
            self.blast_analysis.insert(i, self.gbk_files[i][0:len(self.gbk_files[i])-4])
        else:
            self.blast_analysis.remove(self.gbk_files[i][0:len(self.gbk_files[i])-4])

    # the action handler for the csv check boxes; adds and removes their values based on whether the button was turned
    # on or off and then creates tree formatting buttons for further fine tuning
    def check_click_tree(self, i):
        if self.c_var[i].get() == 1:
            # while sets to make sure values exsist for all csvs before the choosen one
            while len(self.tree_type)-1 < i:
                self.tree_type.append([])
            while len(self.tree_analysis) - 1 < i:
                self.tree_analysis.append(None)
            self.tree_analysis[i] = self.csv_files[i][0:len(self.csv_files)-4]
            while len(self.tree_frame) - 1 < i:
                self.tree_frame.append(Frame(self.tree_type_frame, relief=RIDGE))
                self.tree_frame[len(self.tree_frame)-1].pack(side=LEFT, fill=BOTH, expand=YES)
            while len(self.d_var) - 1 < i:
                self.d_var.append([])
            while len(self.titles) - 1 < i:
                self.titles.append(Label())
            self.titles[i] = Label(self.tree_frame[i], text=self.tree_analysis[i])
            self.titles[i].pack(side=TOP)

            # creation of tree formatting buttons
            z = 0
            while len(self.d_var[i]) < len(self.type_text_frame.winfo_children()):
                self.d_var[i].append(IntVar())
            for widget in self.type_text_frame.winfo_children()[0:len(self.type_text_frame.winfo_children())-2]:
                Checkbutton(self.tree_frame[i], variable=self.d_var[i][z], onvalue=1, offvalue=0, command=curry(
                    self.check_click_type, i, z, self.d_var[i])).pack(side=TOP)
                z += 1
        else:
            # removes all parts of a tree choice
            self.tree_analysis[i] = None
            self.tree_frame[i].destroy()
            self.tree_frame[i] = Frame(self.tree_type_frame, relief=RIDGE)
            self.tree_frame[i].pack(side=LEFT, fill=BOTH, expand=YES)
            self.titles[i].destroy()
            self.titles[i] = Label()

    # the action handler for the check boxes adds and removes their values based on whether the button was turned on or
    # off
    def check_click_type(self, i, z, d_var):
        if d_var[z].get() == 1:
            self.tree_type[i].insert(z, self.data_files[z])
        else:
            self.tree_type[i].remove(self.data_files[z])


# the body which is executed raw
root = Tk()
root.wm_title("NRPSAnalysis")
my_app = MyApp(root)
root.mainloop()
