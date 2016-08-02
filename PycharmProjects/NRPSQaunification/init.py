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


# taken from code.activestate.com/recipes/52549
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


class MyApp:

    def __init__(self, myParent):
        button_width = 7

        button_padx = "2m"
        button_pady = "1m"

        analysis_frame_padx = "3m"
        analysis_frame_pady = "2m"
        analysis_frame_ipadx = "3m"
        analysis_frame_ipady = "1m"

        self.blast_analysis = []
        self.tree_analysis = []
        self.tree_type = []

        root.geometry("600x400")

        self.myParent = root
        self.analysis_container = Frame(root)
        self.analysis_container.pack(ipadx=analysis_frame_ipadx, ipady=analysis_frame_ipady, padx=analysis_frame_padx,
                                         pady=analysis_frame_pady)

        self.top_container = Frame(self.analysis_container)
        self.top_container.pack(side=TOP)

        self.bottom_container = Frame(self.analysis_container, relief=RIDGE, height=100, width=300, bg="green")
        self.bottom_container.pack(side=TOP)

        self.gbk_select_frame = Frame(self.top_container, relief=RIDGE, height=100, width=100, bg="yellow")
        self.gbk_select_frame.pack(side=LEFT, fill=BOTH, expand=YES)

        self.tree_select_frame = Frame(self.top_container, relief=RIDGE, height=100, width=100, bg="cyan")
        self.tree_select_frame.pack(side=LEFT, fill=BOTH, expand=YES)

        self.tree_type_frame = Frame(self.top_container, relief=RIDGE, height = 100, width=100, bg="red")
        self.tree_type_frame.pack(side=LEFT, fill=BOTH, expand=YES)

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

        self.d_var = []
        self.data_files = []
        f = open(os.path.join(ana_dir, os.path.join(nrps_dir, os.path.join(csv_dir, self.csv_files[0]))), 'r')

        z = 0
        s = f.readline()
        for file in s.split("^"):
            self.data_files.append(file)
            self.d_var.append(IntVar())
            Checkbutton(self.tree_type_frame, text=file, variable=self.d_var[z], onvalue=1, offvalue=0, command=curry(
                self.check_click_type, z)).pack(side=TOP)
            z += 1

        self.x_button = Button(self.bottom_container, command=self.x_button_click)
        self.x_button["text"] = "Analyze"
        self.x_button["background"] = "blue"
        self.x_button.focus_force()
        self.x_button.configure(width=button_width, padx=button_padx, pady=button_pady)
        self.x_button.pack(side=TOP)

    def x_button_click(self):
        BlastSequenceSearch.get_sequences()
        csvGenerator.create_csv()
        TreeBuilder.construct_tree()

    def check_click_blast(self, i):
        if self.g_var[i].get() == 1:
            self.blast_analysis.insert(i, self.gbk_files[i])
        else:
            self.blast_analysis.remove(self.gbk_files[i])

    def check_click_tree(self, i):
        if self.c_var[i].get() == 1:
            self.tree_analysis.insert(i, self.csv_files[i])
        else:
            self.tree_analysis.remove(self.csv_files[i])
        print(self.tree_analysis)

    def check_click_type(self, i):
        if self.d_var[i].get() == 1:
            self.tree_type.insert(i, self.data_files[i])
        else:
            self.tree_type.remove(self.data_files[i])
        print(self.tree_type)

root = Tk()
root.wm_title("NRPSAnalysis")
my_app = MyApp(root)
root.mainloop()


