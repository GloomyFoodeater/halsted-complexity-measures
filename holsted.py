from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename

import metrics

class Application(Frame):
    """ GUI application."""
    def __init__(self, master):
        super(Application, self).__init__(master)
        self.grid()
        self.create_widgets()

    # Intitalize components
    def create_widgets(self):

        # Create submit button
        self.submit_button = Button(self, text = "Выполнить расчёт", width = 30, height = 2, command = self.calculate,
                            bg = 'aquamarine3', fg = 'purple4', font = 'Arial 14')
        self.submit_button.grid(row = 1, column = 0, columnspan = 3, sticky = NSEW )

        # Create choose button
        self.submit_button2 = Button(self, text = "Источник...", width = 10, height = 2, command = self.choose,
                            bg = 'aquamarine3', fg = 'purple4', font = 'Arial 14')
        self.submit_button2.grid(row = 1, column = 3, columnspan = 3, sticky = NSEW )

        # Create text widget to input message
        self.notes = Text(self, width = 137, height = 22, wrap = WORD,
                          bg = 'thistle1', fg = 'blue3', font = 'Arial 14')
        self.notes.grid(row = 0, column = 0, columnspan = 5)
        self.notes.insert(1.0, "Enter your code here!")

        # Create scrolls for input
        self.scrolls_input = Scrollbar(self, orient = VERTICAL,command = self.notes.yview)
        self.scrolls_input.grid(row = 0, column = 5, sticky = NS)
        self.notes['yscrollcommand'] = self.scrolls_input.set

        # Operators' table
        self.operators_table = ttk.Treeview(self, show = "headings", columns = ('1','2', '3'), height = 13,
                                  selectmode = 'extended')

        self.operators_table.column('1', width=30, anchor='c')
        self.operators_table.column('2', width = 570, anchor = 'c')
        self.operators_table.column('3', width = 150, anchor = 'w')

        self.operators_table.heading('1', text="№")
        self.operators_table.heading('2', text = "Operator")
        self.operators_table.heading('3', text="Amount")
        self.operators_table.grid(row = 2, column = 0, columnspan = 2)

        # Create scrolls
        self.scrolls_operators = Scrollbar(self, orient=VERTICAL, command=self.operators_table.yview)
        self.scrolls_operators.grid(row=2, column=2, sticky=NS)
        self.operators_table['yscrollcommand'] = self.scrolls_operators.set

        # Operands' table
        self.operands_table = ttk.Treeview(self, show = "headings", columns = ('1','2', '3'), height = 13,
                                  selectmode = 'extended')

        self.operands_table.column('1', width=30, anchor='c')
        self.operands_table.column('2', width = 570, anchor = 'c')
        self.operands_table.column('3', width = 146, anchor = 'w')

        self.operands_table.heading('1', text="№")
        self.operands_table.heading('2', text = "Operand")
        self.operands_table.heading('3', text="Amount")
        self.operands_table.grid(row = 2, column = 3, columnspan = 2)

        # Create scrolls
        self.scrolls_operands = Scrollbar(self, orient=VERTICAL, command=self.operands_table.yview)
        self.scrolls_operands.grid(row=2, column=5, sticky=NS)
        self.operands_table['yscrollcommand'] = self.scrolls_operands.set

    # Calculate measures
    def calculate(self):
        for i in self.operators_table.get_children():
            self.operators_table.delete(i)
        for i in self.operands_table.get_children():
            self.operands_table.delete(i)
        tstr = self.notes.get(1.0, END)
        hmetr = metrics.HolstedMeasures(tstr)
        i = 1
        st = ''
        for key, value in hmetr.operators.items():
            self.operators_table.insert("", END, values = (str(i)+'.', key, value))
            i += 1
        i = 1
        for key, value in hmetr.operands.items():
            self.operands_table.insert("", END, values=(str(i)+'.', key, value))
            i += 1
        self.operators_table.insert("", END, values=('',"=================================",))
        self.operands_table.insert("", END, values=('',"=================================",))
        self.operators_table.insert("", END, values=('',"Total amount of Operators (N1)", hmetr.operators_total))
        self.operands_table.insert("", END, values=('',"Total amount of Operands (N2)", hmetr.operands_total))
        self.operators_table.insert("", END, values=('',"Total amount of Unique Operators (n1)", hmetr.operators_vocabulary))
        self.operands_table.insert("", END, values=('',"Total amount of Unique Operands (n2)", hmetr.operands_vocabulary))
        self.operators_table.insert("", END, values=('',"=================================", ))
        self.operators_table.insert("", END, values=('',"Program Vocabulary (n)", hmetr.program_vocabulary))
        self.operators_table.insert("", END, values=('',"Program Length (N)", hmetr.program_length))
        self.operators_table.insert("", END, values=('',"Program Volume (V)", hmetr.program_volume))

    def choose(self):
        filename = askopenfilename(filetypes=(('typescript files', 'ts'),))
        f = open(filename, 'r')
        tstr1 = f.read()
        self.notes.delete(1.0, END)
        self.notes.insert(1.0, tstr1)
        f.close()

root = Tk()
root.title("Holsted")
root.geometry("1000x500+300+120")
root.state('zoomed')
root.resizable(False, False)
app = Application(root)

root.mainloop()