import BlastSequenceSearch
from tkinter import *
import TreeBuilder
import csvGenerator
import DecisionAnalyze
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
        button_pady = "2m"

        # definition of primary and analysis factor lists
        self.blast_analysis = []
        self.tree_analysis = []
        self.tree_type = []
        self.tree_frame = []
        self.post_analysis = []
        self.titles = []
        self.d_var = []
        self.one_time = 0
        self.one_time_b = 0

        # definition of all primary frames
        self.myParent = root

        self.full_container = Frame(root, relief=RIDGE)
        self.full_container.pack()

        self.title_container = Frame(self.full_container, relief=RIDGE)
        self.title_container.pack(side=TOP, fill=BOTH, expand=YES)

        self.analysis_container = Frame(self.full_container, relief=RIDGE)
        self.analysis_container.pack(side=TOP, fill=BOTH, expand=YES)

        self.analysis_title = Frame(self.analysis_container, relief=RIDGE)
        self.analysis_title.pack(side=TOP, fill=BOTH, expand=YES)

        self.top_container = Frame(self.analysis_container, relief=RIDGE)
        self.top_container.pack(side=TOP, fill=BOTH, expand=YES)

        self.bottom_container = Frame(self.analysis_container, relief=RIDGE)
        self.bottom_container.pack(side=TOP, fill=BOTH, expand=YES)

        self.button_container = Frame(self.bottom_container, relief=RIDGE)
        self.button_container.pack(side=RIGHT, fill=BOTH, expand=YES)

        self.gbk_select_frame = Frame(self.top_container, relief=RIDGE)
        self.gbk_select_frame.pack(side=LEFT, fill=BOTH, expand=YES)

        self.tree_select_frame = Frame(self.top_container, relief=RIDGE)
        self.tree_select_frame.pack(side=LEFT, fill=BOTH, expand=YES)

        self.tree_type_frame = Frame(self.top_container, relief=RIDGE)
        self.tree_type_frame.pack(side=LEFT, fill=BOTH, expand=YES)

        self.type_text_frame = Frame(self.tree_type_frame, relief=RIDGE)
        self.type_text_frame.pack(side=LEFT, fill=BOTH, expand=YES)

        self.hsp_frame = Frame(self.top_container, relief=RIDGE)
        self.hsp_frame.pack(side=LEFT, fill=BOTH, expand=YES)

        # this creates a black line between the post and pre analysis
        self.line = Frame(self.full_container, relief=RIDGE, height=2, bg="black")
        self.line.pack(side=TOP, fill=BOTH, expand=YES)

        self.post_container = Frame(self.full_container, relief=RIDGE)
        self.post_container.pack(side=TOP, fill=BOTH, expand=YES)

        self.post_top = Frame(self.post_container, relief=RIDGE)
        self.post_top.pack(side=TOP, fill=BOTH, expand=YES)

        self.post_bottom = Frame(self.post_container, relief=RIDGE)
        self.post_bottom.pack(side=TOP, fill=BOTH, expand=YES)

        self.post_title_frame = Frame(self.post_top, relief=RIDGE)
        self.post_title_frame.pack(side=TOP, fill=BOTH, expand=YES)

        self.ana_name_frame = Frame(self.post_top, relief=RIDGE)
        self.ana_name_frame.pack(side=LEFT, fill=BOTH, expand=YES)

        self.ana_type_frame = Frame(self.post_top, relief=RIDGE)
        self.ana_type_frame.pack(side=LEFT, fill=BOTH, expand=YES)

        self.ana_sample_frame = Frame(self.post_top, relief=RIDGE)
        self.ana_sample_frame.pack(side=LEFT, fill=BOTH, expand=YES)

        self.post_button_container = Frame(self.post_bottom, relief=RIDGE)
        self.post_button_container.pack(side=RIGHT, fill=BOTH, expand=YES)

        # ---------------------------------------------Title_Container--------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        # creation of the title for the whole things and the analysis section
        Label(self.analysis_title, text="Pre-Decision Tree Analysis", font=("Courier", 15)).pack(side=LEFT)
        Label(self.title_container, text="NRPS Analysis with Decision Trees", font=("Courier", 22)).pack(side=TOP)
        Label(self.post_title_frame, text="Post Decision Tree Analysis", font=("Courier", 15)).pack(side=LEFT)

        # ---------------------------------------------Analysis_Container-----------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        # creation of check buttons: 1 blast buttons

        # title of check buttons below
        Label(self.gbk_select_frame, text="BLAST", font=("Courier", 10)).pack(side=TOP)

        self.g_var = []
        self.gbk_files = []
        for [dirpath, dirname, filename] in os.walk(root_dir):
            self.gbk_files.extend(filename)

        i = 0
        for file in self.gbk_files:
            self.g_var.append(IntVar())
            Checkbutton(self.gbk_select_frame, text=file[0:len(file)-4], variable=self.g_var[i], onvalue=1, offvalue=0,
                            pady=2, command=curry(self.check_click_blast, i)).pack(side=TOP)
            i += 1

        # 2 tree buttons

        # title of check buttons below
        Label(self.tree_select_frame, text="Tree", font=("Courier", 10)).pack(side=TOP)

        self.c_var = []
        self.csv_files = []
        for [dirpath, dirname, filename] in os.walk(os.path.join(ana_dir, os.path.join(nrps_dir, csv_dir))):
            self.csv_files.extend(filename)

        k = 0
        for file in self.csv_files:
            self.c_var.append(IntVar())
            Checkbutton(self.tree_select_frame, text=file[0:len(file) - 4], variable=self.c_var[k], onvalue=1,
                            offvalue=0, pady=2, command=curry(self.check_click_tree, k)).pack(side=TOP)
            k += 1

        self.hsp_files = [IntVar(), IntVar()]
        self.data_files = []

        # creation of analysis button
        self.x_button = Button(self.button_container, command=self.x_button_click, text="Analyze", background="light blue",
                                   activebackground="cyan")
        self.x_button.focus_force()
        self.x_button.configure(width=button_width, padx=button_padx, pady=button_pady, highlightbackground="dark gray",
                                    highlightcolor="dark gray", foreground="dark blue")
        self.x_button.pack(side=RIGHT)

        # ------------------------------------------------Post_Container------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        # creates a title and checkbuttons for set of data you want to do Analysis with
        Label(self.ana_name_frame, text="Data Set", font=("Courier", 10)).pack(side=TOP)

        self.n_var = []
        self.name_files = []
        for [dirpath, dirname, filename] in os.walk(os.path.join(ana_dir, os.path.join(nrps_dir, csv_dir))):
            self.name_files.extend(filename)

        j = 0
        for file in self.name_files:
            self.n_var.append(IntVar())
            Checkbutton(self.ana_name_frame, text=file[0:len(file) - 4], variable=self.n_var[j], onvalue=1, offvalue=0,
                            pady=2, command=curry(self.check_click_name, j)).pack(side=TOP)
            j += 1

        # creates a title and check buttons for the type of post-decision tree analysis you want to do
        Label(self.ana_type_frame, text="Analysis Type", font=("Courier", 10)).pack(side=TOP)

        self.t_var = []
        self.type_files = []
        l = 0
        self.t_var.append(IntVar())
        Checkbutton(self.ana_type_frame, text="Class", variable=self.t_var[0], onvalue=1, offvalue=0, pady=2).pack(
                        side=TOP)
        self.t_var.append(IntVar())
        Checkbutton(self.ana_type_frame, text="Probabilities", variable=self.t_var[1], onvalue=1, offvalue=0, pady=2).pack(side=TOP)

        # Creates a title and input zone for the sample to be analyzed
        Label(self.ana_sample_frame, text="Sample", font=("Courier", 10)).pack(side=TOP)

        self.v = StringVar()
        Entry(self.ana_sample_frame, textvariable=self.v).pack(side=TOP)

        #define the button that is used for post analysis

        self.post_button = Button(self.post_button_container, command=self.post_button_click, text="Analyze",
                                    background="pink", activebackground="red")
        self.post_button.focus_force()
        self.post_button.configure(width=button_width, padx=button_padx, pady=button_pady,
                                       highlightbackground="dark gray", highlightcolor="dark gray",
                                           foreground="dark red")
        self.post_button.pack(side=RIGHT)

    # the action handler for the analysis button; this checks which aspects of analysis should be undertaken
    def x_button_click(self):
        if len(self.blast_analysis) > 0 and self.blast_analysis.count(None) is not len(self.blast_analysis):
            BlastSequenceSearch.get_sequences(self.blast_analysis)
            csvGenerator.create_csv(self.blast_analysis)

        if len(self.tree_analysis) > 0 and self.tree_analysis.count(None) is not len(self.tree_analysis):
            if len(self.tree_type) > 0 and self.tree_type.count(None) is not len(self.tree_type):
                TreeBuilder.construct_tree(self.tree_analysis, self.tree_type, self.hsp_files)

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
            # creates the hsps choice buttons if they have not already been created
            if self.one_time == 0:
                self.one_time = 1
                Label(self.hsp_frame, text="Specificity", font=("Courier", 10)).pack(side=TOP)
                Checkbutton(self.hsp_frame, text="BC-Specific", variable=self.hsp_files[0], onvalue=1, offvalue=0,
                            pady=2).pack(side=TOP)
                Checkbutton(self.hsp_frame, text="Non-Specific", variable=self.hsp_files[1], onvalue=1,
                            offvalue=0, pady=2).pack(side=TOP)

            # while sets to make sure values exsist for all csvs before the choosen one
            while len(self.tree_type)-1 < i:
                self.tree_type.append([])
            while len(self.tree_analysis) - 1 < i:
                self.tree_analysis.append(None)
            self.tree_analysis[i] = self.csv_files[i][0:len(self.csv_files[i])-4]
            while len(self.tree_frame)-1 < i:
                self.tree_frame.append(Frame(self.tree_type_frame, relief=RIDGE))
                self.tree_frame[len(self.tree_frame)-1].pack(side=LEFT, fill=BOTH, expand=YES)
            while len(self.d_var) - 1 < i:
                self.d_var.append([])
            while len(self.titles) - 1 < i:
                self.titles.append(Label())
            self.titles[i] = Label(self.tree_frame[i], text=self.tree_analysis[i])
            self.titles[i].pack(side=TOP)

            if self.one_time_b == 0:
                self.one_time_b = 1
                # creation of labels for tree formatting buttons
                f = open(os.path.join(ana_dir, os.path.join(nrps_dir, os.path.join(csv_dir, self.csv_files[0]))), 'r')
                s = f.readline()

                # title of check buttons in check_click_tree
                Label(self.type_text_frame, text="Type", font=("Courier", 10)).pack(side=TOP)

                for file in s.split("^"):
                    if not file == "description" and not file == "sequence" and not file == "non-specific sequence":
                        self.data_files.append(file)
                        Label(self.type_text_frame, text=file, pady=3).pack(side=TOP)

            # creation of tree formatting buttons
            z = 0
            while len(self.d_var[i]) < len(self.type_text_frame.winfo_children()):
                self.d_var[i].append(IntVar())
            for widget in self.type_text_frame.winfo_children()[0:len(self.type_text_frame.winfo_children())-1]:
                Checkbutton(self.tree_frame[i], variable=self.d_var[i][z], onvalue=1, offvalue=0, pady=2,
                                command=curry(self.check_click_type, i, z, self.d_var[i])).pack(side=TOP)
                z += 1
        else:
            # destroys the tree format choice lables if there are no selected tree choices
            if not any(self.tree_analysis):
                self.type_text_frame.destroy()
                self.type_text_frame = Frame(self.tree_type_frame, relief=RIDGE)
                self.type_text_frame.pack(side=LEFT, fill=BOTH, expand=YES)
                self.one_time = 0
                self.one_time_b = 0
                for widget in self.hsp_frame.winfo_children():
                    widget.destroy()

            # removes all parts of a tree choice
            self.tree_analysis[i] = None
            self.tree_frame[i].destroy()
            self.tree_frame[i] = Frame(self.tree_type_frame, relief=RIDGE)
            self.tree_frame[i].pack(side=LEFT, fill=BOTH, expand=YES)
            self.titles[i].destroy()
            self.titles[i] = Label()

            # destroys the hsp choice buttons if there are no selected tree choices
            if not any(self.tree_analysis):
                self.one_time = 0
                for widget in self.hsp_frame.winfo_children():
                    widget.destroy()

    # the action handler for the check boxes adds and removes their values based on whether the button was turned on or
    # off
    def check_click_type(self, i, z, d_var):
        if d_var[z].get() == 1:
            self.tree_type[i].insert(z, self.data_files[z])
        else:
            self.tree_type[i].remove(self.data_files[z])

    def check_click_name(self, j):
        if self.n_var[j].get() == 1:
            self.post_analysis.insert(j, self.name_files[j])

        else:
            self.post_analysis.remove(self.name_files[j])

    def post_button_click(self):
        DecisionAnalyze.post_analyze(self.post_analysis, self.t_var, self.tree_type, self.v)

# the body which is executed raw
root = Tk()
root.wm_title("NRPSAnalysis")
my_app = MyApp(root)
root.mainloop()
