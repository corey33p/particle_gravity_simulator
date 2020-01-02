from particles_Field import Field
from PIL import Image, ImageTk, ImageDraw
import tkinter as tk
from tkinter import Canvas,Tk,ttk,Label,Entry,Button,mainloop,Text,Frame,IntVar,Checkbutton,Radiobutton
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
        self.max_win_size = (1335,1440)
        self.canvas_size = int(.8*880/950*self.max_win_size[1])
        self.im = {}
        self.setup_window()
        self.current_step = "odd"
        self.x_offset = self.y_offset = .5
        self.crosshair_size = .02
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
        self.primary_window.geometry('1069x1440-1+0')
        # self.primary_window.geometry('1274x960+3281+1112')
        self.primary_window.minsize(width=100, height=30)
        self.primary_window.maxsize(width=self.max_win_size[0], height=self.max_win_size[1])
        
        # image & canvas
        
        self.im_frame = ttk.Frame(self.primary_window)
        self.im_frame.grid(row=0,column=0,sticky="nsew")
        self.im_frame.columnconfigure(0, weight=1)
        self.im_frame.rowconfigure(0, weight=1)
        self.primary_window.columnconfigure(0, weight=1)
        self.primary_window.rowconfigure(0, weight=1)
        
        self.canvas_frame = ttk.Frame(self.primary_window)
        self.canvas_frame.grid(row=0, column=0)
        
        self.the_canvas = Canvas(self.canvas_frame,
                                width=self.canvas_size,
                                height=self.canvas_size,
                                background='black')
        self.the_canvas.grid(row=0, column=0)
        
        # bottom buttons
        self.bottom_buttons_frame = ttk.Frame(self.primary_window)
        self.bottom_buttons_frame.grid(row=3,column=0)
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
        Label(self.bottom_buttons_frame, text=" Remaining Masses:",font=self.main_font).grid(row=0, column=3)
        self.current_count = Entry(self.bottom_buttons_frame,justify='right')
        self.current_count.insert("end", '--')
        self.current_count.config(state="disabled",font=self.main_font,width=4)
        self.current_count.grid(row=0,column=4)
        
        # settings frame
        self.settings_frame = ttk.Frame(self.primary_window)
        self.settings_frame.grid(row=4,column=0)
        #
        Label(self.settings_frame, text="Masses Count:",font=self.main_font).grid(row=0, column=1)
        self.masses_count = Entry(self.settings_frame,justify='right')
        self.masses_count.insert("end", '43')
        self.masses_count.config(font=self.main_font,width=4)
        self.masses_count.grid(row=0,column=2)
        #
        Label(self.settings_frame, text="Gravitational Constant:",font=self.main_font).grid(row=1, column=1)
        self.gravitational_constant = Entry(self.settings_frame,justify='right')
        self.gravitational_constant.insert("end", '.001')
        self.gravitational_constant.config(font=self.main_font,width=7)
        self.gravitational_constant.grid(row=1,column=2)
        #
        Label(self.settings_frame, text="Density:",font=self.main_font).grid(row=2, column=1)
        self.density = Entry(self.settings_frame,justify='right')
        self.density.insert("end", '9999999')
        self.density.config(font=self.main_font,width=12)
        self.density.grid(row=2,column=2)
        #
        Label(self.settings_frame, text="Time Step:",font=self.main_font).grid(row=3, column=1)
        self.time_step = Entry(self.settings_frame,justify='right')
        self.time_step.insert("end", '.05')
        self.time_step.config(font=self.main_font,width=6)
        self.time_step.grid(row=3,column=2)
        #
        Label(self.settings_frame, text="Initial Velocity Stdev:",font=self.main_font).grid(row=4, column=1)
        self.velocity_sigma = Entry(self.settings_frame,justify='right')
        self.velocity_sigma.insert("end", '.02')
        self.velocity_sigma.config(font=self.main_font,width=5)
        self.velocity_sigma.grid(row=4,column=2)
        #
        self.auto_restart_check = IntVar()
        self.auto_restart_check.set(1)
        self.auto_restart_button = Checkbutton(self.settings_frame, text="Auto Restart When Orbitting", variable=self.auto_restart_check,font=self.main_font)
        self.auto_restart_button.grid(row=5,column=1,columnspan=2)
        #
        #
        def follow_com_func(): self.view_behavior.set(0)
        def follow_largest_func(): self.view_behavior.set(1)
        def remain_static_func(): self.view_behavior.set(2)
        self.view_behavior = IntVar()
        self.view_behavior.set(0)
        self.follow_center_of_mass = Radiobutton(self.settings_frame, 
                                                 text="Follow Center Of Mass", 
                                                 variable=self.view_behavior, 
                                                 value=0, 
                                                 command=follow_com_func,
                                                 font=self.main_font)
        self.follow_center_of_mass.grid(row=6,column=0,columnspan=2)
        self.follow_largest_mass = Radiobutton(self.settings_frame, 
                                               text="Follow Largest Mass", 
                                               variable=self.view_behavior, 
                                               value=1, 
                                               command=follow_largest_func,
                                               font=self.main_font)
        self.follow_largest_mass.grid(row=7,column=0,columnspan=2)
        self.remain_static = Radiobutton(self.settings_frame, 
                                               text="Remain Static", 
                                               variable=self.view_behavior, 
                                               value=2, 
                                               command=remain_static_func,
                                               font=self.main_font)
        self.remain_static.grid(row=8,column=0,columnspan=2)
    def update_count(self,count=None):
            if count is not None: val = str(count)
            elif self.parent.field is not None: 
                val = str(self.parent.field.population)
            else: return
            self.current_count.config(state="normal")
            self.current_count.delete(0,'end')
            self.current_count.insert('end',val)
            self.current_count.config(state='disabled')
    def step(self):
        if self.parent.field.population>1:
            if not self.parent.pause: self.parent.pause = True
            if self.parent.field is None:
                count,g,d,t,vs=self.get_settings()
                self.update_count(count)
                self.parent.field = Field(self.parent,
                                          population=count,
                                          gravitational_constant=g,
                                          density=d,
                                          time_step=t,
                                          velocity_std=vs)
            self.parent.field.step()
            self.parent.field.collisions()
            self.update_canvas()
    def pause(self):
        self.parent.pause = not self.parent.pause
    def get_settings(self):
        pop = int(self.masses_count.get())
        g = float(self.gravitational_constant.get())
        density = float(self.density.get())
        time_step = float(self.time_step.get())
        vel_sigma = float(self.velocity_sigma.get())
        return pop,g,density,time_step,vel_sigma
    def play_func(self):
        self.parent.pause = False
        self.parent.main_queue.queue.clear()
        self.x_offset = self.y_offset = .5
        count,g,d,t,vs=self.get_settings()
        self.update_count(count)
        self.parent.field = Field(self.parent,
                                  population=count,
                                  gravitational_constant=g,
                                  density=d,
                                  time_step=t,
                                  velocity_std=vs)
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
                restart = self.parent.field.population == 1 or self.parent.field.orbitting and self.auto_restart_check.get()
                if self.parent.field.population == 1 or restart:
                    count,g,d,t,vs=self.get_settings()
                    self.update_count(count)
                    self.parent.field = Field(self.parent,
                                              population=count,
                                              gravitational_constant=g,
                                              density=d,
                                              time_step=t,
                                              velocity_std=vs)
    def update_canvas(self):
        def draw_crosshair(x,y):
            self.the_canvas.delete("crosshair")
            x1=(x+self.x_offset-self.crosshair_size)*self.canvas_size
            y1=(y+self.y_offset)*self.canvas_size
            x2=(x+self.x_offset+self.crosshair_size)*self.canvas_size
            y2=(y+self.y_offset)*self.canvas_size
            self.the_canvas.create_line(x1,y1,x2,y2,fill='#333333',tags="crosshair")
            #
            x1=(x+self.x_offset)*self.canvas_size
            y1=(y+self.y_offset-self.crosshair_size)*self.canvas_size
            x2=(x+self.x_offset)*self.canvas_size
            y2=(y+self.y_offset+self.crosshair_size)*self.canvas_size
            self.the_canvas.create_line(x1,y1,x2,y2,fill='#333333',tags="crosshair")
        x_center_of_mass,y_center_of_mass = self.parent.field.center_of_mass
        if self.view_behavior.get() == 0:
            self.x_offset = .5-x_center_of_mass
            self.y_offset = .5-y_center_of_mass
        elif self.view_behavior.get() == 1:
            max_mass = float(np.max(self.parent.field.mass))
            which_mass = int(np.argwhere(self.parent.field.mass == max_mass)[0][0])
            self.x_offset = .5-float(self.parent.field.coords[which_mass][0])
            self.y_offset = .5-float(self.parent.field.coords[which_mass][1])
        draw_crosshair(x_center_of_mass,y_center_of_mass)
        population = self.parent.field.population
        for i in range(population):
            location = np.copy(self.parent.field.coords[i])
            location[0]=(location[0]+self.x_offset)*self.canvas_size
            location[1]=(location[1]+self.y_offset)*self.canvas_size
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
