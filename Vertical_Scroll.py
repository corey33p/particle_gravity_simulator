import tkinter as tk
from tkinter import Frame,Canvas,Scrollbar

class VerticalScrollPack(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.canvas = Canvas(root, borderwidth=0)
        self.frame = Frame(self.canvas)
        self.vsb = Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw", tags="self.frame")
        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.frame.bind_all("<MouseWheel>", self.on_mousewheel)
    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    def go_to_top(self, event=None):
        self.canvas.yview_moveto(0)

class VerticalScrollGrid(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.canvas = Canvas(root, borderwidth=0)
        self.frame = Frame(self.canvas)
        self.vsb = Scrollbar(root,orient="vertical",command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.grid(row=0, column=1, sticky='NS')
        self.vsb.configure(command=self.canvas.yview)
        self.canvas.grid(row=0, column=0, sticky='NSEW')
        self.canvas.create_window((4,4), window=self.frame, anchor="nw", tags="self.frame")
        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.frame.bind_all("<MouseWheel>", self.on_mousewheel)
        # self.frame.bind("<Button-4>", self.on_mousewheel_up)
        # self.frame.bind("<Button-5>", self.on_mousewheel_down)
    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    # def on_mousewheel_down(self, event): self.canvas.yview_scroll(1, "units")
    # def on_mousewheel_up(self, event): self.canvas.yview_scroll(-1, "units")
    def on_mousewheel(self, event): self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    def go_to_top(self, event=None):
        self.canvas.yview_moveto(0)
