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
        self.canvas_size = min((self.max_win_size[0]-5,self.max_win_size[1]-70))
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
        self.canvas_frame.grid(row=0, column=0)
        self.canvas_frame.columnconfigure(0, weight=1)
        
        self.the_canvas = Canvas(self.canvas_frame,
                                width=self.canvas_size,
                                height=self.canvas_size,
                                background='black')
        self.the_canvas.grid(row=0, column=0,columnspan=2, sticky="ew")
        self.the_canvas.create_line(0,self.canvas_size/2,self.canvas_size,self.canvas_size/2,fill='#333333')
        self.the_canvas.create_line(self.canvas_size/2,0,self.canvas_size/2,self.canvas_size,fill='#333333')
        
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
        self.masses_count.insert("end", '13')
        self.masses_count.config(font=self.main_font,width=4)
        self.masses_count.grid(row=0,column=4)
    def step(self):
        if self.parent.field.population>1:
            if not self.parent.pause: self.parent.pause = True
            if self.parent.field is None:
                masses_count = int(self.masses_count.get())
                self.parent.field = Field(self,masses_count)
            self.parent.field.step()
            self.parent.field.collisions()
            self.update_canvas()
    def pause(self):
        self.parent.pause = not self.parent.pause
    def play_func(self):
        self.parent.pause = False
        self.parent.main_queue.queue.clear()
        masses_count = int(self.masses_count.get())
        self.parent.field = Field(self,masses_count)
        self.parent.main_queue.put(self.play)
        # self.play()
    def play(self):
        self.pause = False
        while self.parent.field.population>1:
            if not self.parent.pause:
                time.sleep(.02)
                self.parent.field.step()
                self.parent.field.collisions()
                self.update_canvas()
                if self.parent.field.population == 1 or self.parent.field.orbitting:
                    masses_count = int(self.masses_count.get())
                    self.parent.field = Field(self,masses_count)
    def update_canvas(self):
        population = self.parent.field.population
        x_center_of_mass = float(np.sum(self.parent.field.coords[:,0]*self.parent.field.mass.flatten()))/self.parent.field.total_mass
        y_center_of_mass = float(np.sum(self.parent.field.coords[:,1]*self.parent.field.mass.flatten()))/self.parent.field.total_mass
        # print("self.parent.field.coords[:,0]*self.parent.field.mass.flatten():\n" + str(self.parent.field.coords[:,0]*self.parent.field.mass.flatten()))
        # print("self.parent.field.coords:\n" + str(self.parent.field.coords))
        # print("self.parent.field.mass:\n" + str(self.parent.field.mass))
        # print("self.parent.field.total_mass:\n" + str(self.parent.field.total_mass))
        # print("x_center_of_mass: " + str(x_center_of_mass))
        # input("y_center_of_mass: " + str(y_center_of_mass))
        x_offset = .5-x_center_of_mass
        y_offset = .5-y_center_of_mass
        self.the_canvas.delete(self.current_step)
        for i in range(population):
            location = np.copy(self.parent.field.coords[i])
            location[0]=(location[0]+x_offset)*self.canvas_size
            location[1]=(location[1]+y_offset)*self.canvas_size
            mass = self.parent.field.mass[i]
            radius = (3/4 * mass / (3.14159 * self.parent.field.density))**(1/3)
            radius = radius * self.canvas_size
            x0=int(location[0]-radius)
            y0=int(location[1]-radius)
            x1=int(location[0]+radius)
            y1=int(location[1]+radius)
            self.the_canvas.create_oval(x0,y0,x1,y1,fill='white',tags=self.current_step)
        if self.current_step == "odd": self.current_step = "even"
        else: self.current_step = "odd"
        self.the_canvas.delete(self.current_step)