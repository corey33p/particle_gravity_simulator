from particles_Field import Field
from PIL import Image, ImageTk, ImageDraw
import tkinter as tk
from tkinter import Canvas,Tk,ttk,Label,Entry,Button,mainloop,Text,Frame,IntVar,Checkbutton
import os
import numpy as np
from tkinter import filedialog
import math
import random
import time

class Display:
    def __init__(self, parent):
        self.parent = parent
        self.main_font = ("Courier", 22, "bold")
        self.max_win_size = (1335,950)
        self.canvas_size = ((self.max_win_size[0]-5,self.max_win_size[1]-70))
        self.im = {}
        self.setup_window()
        self.current_step = "odd"
    def open_images(self):
        pil_img = Image.open('source/play.gif').resize((80,80), Image.ANTIALIAS)
        self.play_photo=ImageTk.PhotoImage(pil_img)
        pil_img = Image.open('source/pause.gif').resize((80,80), Image.ANTIALIAS)
        self.pause_photo=ImageTk.PhotoImage(pil_img)
        # pil_img = Image.open('source/close.gif').resize((80,80), Image.ANTIALIAS)
        # self.close_photo=ImageTk.PhotoImage(pil_img)
        # pil_img = Image.open('source/accept.gif').resize((80,80), Image.ANTIALIAS)
        # self.accept_photo=ImageTk.PhotoImage(pil_img)
        # pil_img = Image.open('source/refresh.gif').resize((80,80), Image.ANTIALIAS)
        # self.refresh_photo=ImageTk.PhotoImage(pil_img)
        # pil_img = Image.open('source/random.gif').resize((80,80), Image.ANTIALIAS)
        # self.random_photo=ImageTk.PhotoImage(pil_img)
        pil_img = Image.open('source/next.gif').resize((80,80), Image.ANTIALIAS)
        self.next_photo=ImageTk.PhotoImage(pil_img)
        # pil_img = Image.open('source/trash.gif').resize((80,80), Image.ANTIALIAS)
        # self.clear_photo=ImageTk.PhotoImage(pil_img)
    def setup_window(self):
        # initial setup
        self.primary_window = Tk()
        self.open_images()
        self.primary_window.wm_title("Gravity")
        # self.primary_window.geometry('1274x960-1+0')
        self.primary_window.geometry('1274x960+3281+1112')
        self.primary_window.minsize(width=100, height=30)
        self.primary_window.maxsize(width=self.max_win_size[0], height=self.max_win_size[1])
        
        # image & canvas
        
        self.im_frame = ttk.Frame(self.primary_window)
        self.im_frame.grid(row=0,column=0,columnspan=2,sticky="nsew")
        self.im_frame.columnconfigure(0, weight=1)
        self.im_frame.rowconfigure(0, weight=1)
        self.primary_window.columnconfigure(0, weight=1)
        self.primary_window.rowconfigure(0, weight=1)
        
        self.canvas_frame = ttk.Frame(self.primary_window)
        self.canvas_frame.grid(row=0, column=0, sticky="nsew")
        self.canvas_frame.columnconfigure(0, weight=1)
        
        self.the_canvas = Canvas(self.canvas_frame,
                                width=self.canvas_size[0],
                                height=self.canvas_size[1],
                                background='black')
        self.the_canvas.grid(row=0, column=0,columnspan=2, sticky="ew")
        
        # bottom buttons
        self.bottom_buttons_frame = ttk.Frame(self.primary_window)
        self.bottom_buttons_frame.grid(row=3,column=0,columnspan=2)
        #
        self.play_button = Button(self.bottom_buttons_frame,
                                    command= self.play_func,
                                    image=self.play_photo,
                                    width="80",height="80")
        self.play_button.grid(row=0,column=0)
        #
        self.pause_button = Button(self.bottom_buttons_frame,
                                    command= self.pause,
                                    image=self.pause_photo,
                                    width="80",height="80")
        self.pause_button.grid(row=0,column=1)
        #
        self.step_button = Button(self.bottom_buttons_frame,
                                    command= self.step,
                                    image=self.next_photo,
                                    width="80",height="80")
        self.step_button.grid(row=0,column=2)
        #
        Label(self.bottom_buttons_frame, text=" Masses Count:",font=self.main_font).grid(row=0, column=3)
        self.masses_count = Entry(self.bottom_buttons_frame,justify='right')
        self.masses_count.insert("end", '3')
        self.masses_count.config(font=self.main_font,width=4)
        self.masses_count.grid(row=0,column=4)
    def step(self):
        if not self.parent.pause: self.parent.pause = True
        if self.parent.field is None:
            masses_count = int(self.masses_count.get())
            self.parent.field = Field(self,masses_count)
        self.parent.field.step()
        self.update_canvas()
    def pause(self):
        self.parent.pause = not self.parent.pause
    def play_func(self):
        self.parent.pause = False
        self.parent.main_queue.queue.clear()
        masses_count = int(self.masses_count.get())
        self.parent.field = Field(self,masses_count)
        # self.parent.main_queue.put(self.play)
        self.play()
    def play(self):
        self.pause = False
        while True:
            if not self.parent.pause:
                time.sleep(.04)
                self.parent.field.step()
                self.parent.field.collisions()
                self.update_canvas()
    def update_canvas(self):
        population = self.parent.field.population
        for i in range(population):
            location = np.copy(self.parent.field.coords[i])
            location[0]=location[0]*self.canvas_size[0]
            location[1]=location[1]*self.canvas_size[1]
            mass = self.parent.field.mass[i]
            # diameter = mass*40
            # radius = diameter / 2
            radius = (.75/3.14159*mass*self.parent.field.density)**(1/3)
            x0=int(location[0]-radius)
            y0=int(location[1]-radius)
            x1=int(location[0]+radius)
            y1=int(location[1]+radius)
            self.the_canvas.create_oval(x0,y0,x1,y1,fill='white',tags=self.current_step)
        if self.current_step == "odd": self.current_step = "even"
        else: self.current_step = "odd"
        self.the_canvas.delete(self.current_step)