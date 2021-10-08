
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename

import metrics


class Application(Frame):
    """ GUI application."""
    def __init__(self, master):
        """ Initialize the frame. """
        super(Application, self).__init__(master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        """ Create buttons, text, and. """

        # create submit button
        self.baton = Button(self, text = "Выполнить расчёт", width = 30, height = 2, command = self.calculate,
                            bg = 'aquamarine3', fg = 'purple4', font = 'Arial 14')
        self.baton.grid(row = 1, column = 0, columnspan = 3, sticky = NSEW )

        # create choose button
        self.baton2 = Button(self, text = "Источник...", width = 10, height = 2, command = self.choose,
                            bg = 'aquamarine3', fg = 'purple4', font = 'Arial 14')
        self.baton2.grid(row = 1, column = 3, columnspan = 3, sticky = NSEW )

        # create text widget to input message
        self.notes = Text(self, width = 137, height = 22, wrap = WORD,
                          bg = 'thistle1', fg = 'blue3', font = 'Arial 14')
        self.notes.grid(row = 0, column = 0, columnspan = 5)
        self.notes.insert(1.0, "Enter your code here!")

        # create scrolls for input
        self.scrollsi = Scrollbar(self, orient = VERTICAL,command = self.notes.yview)
        self.scrollsi.grid(row = 0, column = 5, sticky = NS)
        self.notes['yscrollcommand'] = self.scrollsi.set

        #table 1
        self.table1 = ttk.Treeview(self, show = "headings", columns = ('1','2', '3'), height = 13,
                                  selectmode = 'extended')

        self.table1.column('1', width=30, anchor='c')
        self.table1.column('2', width = 570, anchor = 'c')
        self.table1.column('3', width = 150, anchor = 'w')

        self.table1.heading('1', text="№")
        self.table1.heading('2', text = "Operator")
        self.table1.heading('3', text="Amount")
        self.table1.grid(row = 2, column = 0, columnspan = 2)

        # create scrolls for table 1
        self.scroll1 = Scrollbar(self, orient=VERTICAL, command=self.table1.yview)
        self.scroll1.grid(row=2, column=2, sticky=NS)
        self.table1['yscrollcommand'] = self.scroll1.set

        #table 2
        self.table2 = ttk.Treeview(self, show = "headings", columns = ('1','2', '3'), height = 13,
                                  selectmode = 'extended')

        self.table2.column('1', width=30, anchor='c')
        self.table2.column('2', width = 570, anchor = 'c')
        self.table2.column('3', width = 146, anchor = 'w')

        self.table2.heading('1', text="№")
        self.table2.heading('2', text = "Operand")
        self.table2.heading('3', text="Amount")
        self.table2.grid(row = 2, column = 3, columnspan = 2)


        # create scrolls for table 2
        self.scroll2 = Scrollbar(self, orient=VERTICAL, command=self.table2.yview)
        self.scroll2.grid(row=2, column=5, sticky=NS)
        self.table2['yscrollcommand'] = self.scroll2.set

#========================================================================================

    def calculate(self):
        """ Calculate metrics. """
        tstr = self.notes.get(1.0, END)
        hmetr = metrics.HolstedMeasures(tstr)
        i = 1
        st = ''
        for key, value in hmetr.operators.items():
            self.table1.insert("", END, values = (str(i)+'.', key, value))
            i += 1
        i = 1
        for key, value in hmetr.operands.items():
            self.table2.insert("", END, values=(str(i)+'.', key, value))
            i += 1
        self.table1.insert("", END, values=('',"=================================",))
        self.table2.insert("", END, values=('',"=================================",))
        self.table1.insert("", END, values=('',"Total amount of Operators (N1)", hmetr.operators_total))
        self.table2.insert("", END, values=('',"Total amount of Operands (N2)", hmetr.operands_total))
        self.table1.insert("", END, values=('',"Total amount of Unique Operators (n1)", hmetr.operators_vocabulary))
        self.table2.insert("", END, values=('',"Total amount of Unique Operands (n2)", hmetr.operands_vocabulary))
        self.table1.insert("", END, values=('',"=================================", ))
        self.table1.insert("", END, values=('',"Program Vocabulary (n)", hmetr.program_vocabulary))
        self.table1.insert("", END, values=('',"Program Length (N)", hmetr.program_length))
        self.table1.insert("", END, values=('',"Program Volume (V)", hmetr.program_volume))

    def choose(self):
        """ Choose File. """
        filename = askopenfilename(filetypes=(('typescript files', 'ts'),))
        f = open(filename, 'r')
        tstr1 = f.read()
        self.notes.delete(1.0, END)
        self.notes.insert(1.0, tstr1)
        f.close()

#=========================================================================================
# main
root = Tk()
root.title("Holsted")
root.geometry("1000x500+300+120")
root.state('zoomed')
root.resizable(False, False)
app = Application(root)

root.mainloop()