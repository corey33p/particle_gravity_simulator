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
        self.max_win_size = (1900,1000)
        self.canvas_size = (1200,900)
        self.im = {}
        self.setup_window()
        self.current_step = "odd"
        self.view_center = [0,0]
        self.crosshair_size = 20
        self.zoom_factor = 1
    def open_images(self):
        pil_img = Image.open('source/play.gif').resize((80,80), Image.ANTIALIAS)
        self.play_photo=ImageTk.PhotoImage(pil_img)
        pil_img = Image.open('source/pause.gif').resize((80,80), Image.ANTIALIAS)
        self.pause_photo=ImageTk.PhotoImage(pil_img)
        pil_img = Image.open('source/zoom_in.gif').resize((80,80), Image.ANTIALIAS)
        self.zoom_in_photo=ImageTk.PhotoImage(pil_img)
        pil_img = Image.open('source/zoom_out.gif').resize((80,80), Image.ANTIALIAS)
        self.zoom_out_photo=ImageTk.PhotoImage(pil_img)
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
        self.primary_window.wm_title("--Gravity--")
        # self.primary_window.geometry('1900x1000-1+0')
        # self.primary_window.geometry('1900x1000-1+0')
        self.primary_window.geometry('1916x1039+3848+1072')
        self.primary_window.minsize(width=100, height=30)
        self.primary_window.maxsize(width=self.max_win_size[0], height=self.max_win_size[1])

        # canvas

        self.canvas_frame = ttk.Frame(self.primary_window)
        self.canvas_frame.grid(row=0, column=1)

        self.the_canvas = Canvas(self.canvas_frame,
                                width=self.canvas_size[0],
                                height=self.canvas_size[1],
                                background='black')
        self.the_canvas.grid(row=0, column=0)

        # bottom buttons
        self.bottom_buttons_frame = ttk.Frame(self.canvas_frame)
        self.bottom_buttons_frame.grid(row=2,column=0)
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
        self.zoom_in_button = Button(self.bottom_buttons_frame,
                                    command= self.zoom_in,
                                    image=self.zoom_in_photo,
                                    width="80",height="80")
        self.zoom_in_button.grid(row=0,column=3)
        #
        self.zoom_out_button = Button(self.bottom_buttons_frame,
                                    command= self.zoom_out,
                                    image=self.zoom_out_photo,
                                    width="80",height="80")
        self.zoom_out_button.grid(row=0,column=4)
        #
        Label(self.bottom_buttons_frame, text="Remaining Masses:",font=self.main_font).grid(row=0, column=5, sticky="e")
        self.current_count = Entry(self.bottom_buttons_frame,justify='right')
        self.current_count.insert("end", '--')
        self.current_count.config(state="disabled",font=self.main_font,width=9)
        self.current_count.grid(row=0,column=6)

        # settings frame
        self.settings_frame = ttk.Frame(self.primary_window)
        self.settings_frame.grid(row=0,column=0)
        #
        Label(self.settings_frame, text="Masses Count:",font=self.main_font).grid(row=0, column=1, sticky="e")
        self.masses_count = Entry(self.settings_frame,justify='right')
        self.masses_count.insert("end", '43')
        self.masses_count.config(font=self.main_font,width=9)
        self.masses_count.grid(row=0,column=2)
        #
        Label(self.settings_frame, text="Gravitational Constant:",font=self.main_font).grid(row=1, column=1, sticky="e")
        self.gravitational_constant = Entry(self.settings_frame,justify='right')
        self.gravitational_constant.insert("end", '10000')
        self.gravitational_constant.config(font=self.main_font,width=9)
        self.gravitational_constant.grid(row=1,column=2)
        #
        Label(self.settings_frame, text="Density:",font=self.main_font).grid(row=2, column=1, sticky="e")
        self.density = Entry(self.settings_frame,justify='right')
        self.density.insert("end", '.0005')
        self.density.config(font=self.main_font,width=9)
        self.density.grid(row=2,column=2)
        #
        Label(self.settings_frame, text="Time Step:",font=self.main_font).grid(row=3, column=1, sticky="e")
        self.time_step = Entry(self.settings_frame,justify='right')
        self.time_step.insert("end", '.05')
        self.time_step.config(font=self.main_font,width=9)
        self.time_step.grid(row=3,column=2)
        #
        Label(self.settings_frame, text="Initial Velocity Stdev:",font=self.main_font).grid(row=4, column=1, sticky="e")
        self.velocity_sigma = Entry(self.settings_frame,justify='right')
        self.velocity_sigma.insert("end", '.02')
        self.velocity_sigma.config(font=self.main_font,width=9)
        self.velocity_sigma.grid(row=4,column=2)
        #
        Label(self.settings_frame, text="Minimum draw size:",font=self.main_font).grid(row=5, column=1, sticky="e")
        self.min_pixel_size = Entry(self.settings_frame,justify='right')
        self.min_pixel_size.insert("end", '2')
        self.min_pixel_size.config(font=self.main_font,width=9)
        self.min_pixel_size.grid(row=5,column=2)
        #
        self.auto_restart_check = IntVar()
        self.auto_restart_check.set(1)
        self.auto_restart_button = Checkbutton(self.settings_frame,
                                               text="Auto Restart When Orbitting",
                                               variable=self.auto_restart_check,
                                               font=self.main_font)
        self.auto_restart_button.grid(row=6,column=1,columnspan=2,sticky="e")
        #
        #
        def follow_com_func(): self.view_behavior.set(0)
        def follow_largest_func(): self.view_behavior.set(1)
        def auto_zoom_func(): self.view_behavior.set(2)
        def remain_static_func(): self.view_behavior.set(3)
        self.view_behavior = IntVar()
        self.view_behavior.set(2)
        self.follow_center_of_mass = Radiobutton(self.settings_frame,
                                                 text="Follow Center Of Mass",
                                                 variable=self.view_behavior,
                                                 value=0,
                                                 command=follow_com_func,
                                                 font=self.main_font)
        self.follow_center_of_mass.grid(row=7,column=1,columnspan=2,sticky="e")
        #
        self.follow_largest_mass = Radiobutton(self.settings_frame,
                                               text="Follow Largest Mass",
                                               variable=self.view_behavior,
                                               value=1,
                                               command=follow_largest_func,
                                               font=self.main_font)
        self.follow_largest_mass.grid(row=8,column=1,columnspan=2,sticky="e")
        #
        self.auto_zoom = Radiobutton(self.settings_frame,
                                     text="Auto Zoom",
                                     variable=self.view_behavior,
                                     value=2,
                                     command=auto_zoom_func,
                                     font=self.main_font)
        self.auto_zoom.grid(row=9,column=1,columnspan=2,sticky="e")
        #
        self.remain_static = Radiobutton(self.settings_frame,
                                              text="Remain Static",
                                              variable=self.view_behavior,
                                              value=3,
                                              command=remain_static_func,
                                              font=self.main_font)
        self.remain_static.grid(row=10,column=1,columnspan=2,sticky="e")
        #
        self.auto_recenter_check = IntVar()
        self.auto_recenter_check.set(1)
        self.auto_recenter_checkbutton = Checkbutton(self.settings_frame,
                                               text="Auto Center When Static",
                                               variable=self.auto_recenter_check,
                                               font=self.main_font)
        self.auto_recenter_checkbutton.grid(row=11,column=1,columnspan=2,sticky="e")
        #
        #
        self.use_colors_check = IntVar()
        self.use_colors_check.set(1)
        self.use_colors_checkbutton = Checkbutton(self.settings_frame,
                                               text="Use Colors",
                                               variable=self.use_colors_check,
                                               font=self.main_font)
        self.use_colors_checkbutton.grid(row=12,column=1,columnspan=2,sticky="e")
        # 
        def weighted_blend_func(): self.color_behavior.set(0)
        def winner_triumph_func(): self.color_behavior.set(1)
        self.color_behavior = IntVar()
        self.color_behavior.set(0)
        self.colors_blend = Radiobutton(self.settings_frame,
                                     text="Blend Colors on Collision",
                                     variable=self.color_behavior,
                                     value=0,
                                     command=weighted_blend_func,
                                     font=self.main_font)
        self.colors_blend.grid(row=13,column=1,columnspan=2,sticky="e")
        #
        self.colors_by_mass = Radiobutton(self.settings_frame,
                             text="Higher Mass Color on Collision",
                             variable=self.color_behavior,
                             value=1,
                             command=winner_triumph_func,
                             font=self.main_font)
        self.colors_by_mass.grid(row=14,column=1,columnspan=2,sticky="e")
    def zoom_in(self):
        self.zoom_factor = self.zoom_factor*2
        x_center_of_mass,y_center_of_mass = self.parent.field.center_of_mass
        self.x_centerOfMass_offset = .5/self.zoom_factor-x_center_of_mass
        self.y_centerOfMass_offset = .5/self.zoom_factor-y_center_of_mass
    def zoom_out(self):
        self.zoom_factor = self.zoom_factor/2
        x_center_of_mass,y_center_of_mass = self.parent.field.center_of_mass
        self.x_centerOfMass_offset = .5/self.zoom_factor-x_center_of_mass
        self.y_centerOfMass_offset = .5/self.zoom_factor-y_center_of_mass
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
                count,g,d,t,vs,dim,c,cb=self.get_settings()
                self.update_count(count)
                self.parent.field = Field(self.parent,
                                          population=count,
                                          gravitational_constant=g,
                                          density=d,
                                          time_step=t,
                                          velocity_std=vs,
                                          field_dimensions=dim,
                                          use_colors=c,
                                          color_handling=cb)
                self.view_center = self.parent.field.center_of_mass
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
        dimensions= self.canvas_size
        c = int(self.use_colors_check.get())
        color_behavior = int(self.color_behavior.get())
        if color_behavior == 0:
            cb = "blend"
        elif color_behavior == 1:
            cb = "biggest mass"
        return pop,g,density,time_step,vel_sigma,dimensions,c,cb
    def play_func(self):
        self.parent.pause = False
        self.parent.main_queue.queue.clear()
        count,g,d,t,vs,dim,c,cb=self.get_settings()
        self.update_count(count)
        self.parent.field = Field(self.parent,
                                  population=count,
                                  gravitational_constant=g,
                                  density=d,
                                  time_step=t,
                                  velocity_std=vs,
                                  field_dimensions=dim,
                                  use_colors=c,
                                  color_handling=cb)
        self.view_center = self.parent.field.center_of_mass
        self.parent.main_queue.put(self.play)
        # self.play() # use for debugging Field class, which is in a separate thread
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
                    count,g,d,t,vs,dim,c,cb=self.get_settings()
                    self.update_count(count)
                    self.parent.field = Field(self.parent,
                                              population=count,
                                              gravitational_constant=g,
                                              density=d,
                                              time_step=t,
                                              velocity_std=vs,
                                              field_dimensions=dim,
                                              use_colors=c,
                                              color_handling=cb)
                    self.view_center = self.parent.field.center_of_mass
    def coordinates_to_pixels(self,x,y):
        canvas_size_after_zoom_x = self.canvas_size[0]/self.zoom_factor
        canvas_size_after_zoom_y = self.canvas_size[1]/self.zoom_factor
        min_x = self.view_center[0] - canvas_size_after_zoom_x/2
        min_y = self.view_center[1] - canvas_size_after_zoom_y/2
        x_scalar = (x - min_x ) / canvas_size_after_zoom_x
        y_scalar = (y - min_y ) / canvas_size_after_zoom_y
        x_pixel = x_scalar * self.canvas_size[0]
        y_pixel = y_scalar * self.canvas_size[1]
        # if self.zoom_factor != 1:
            # print("\nx: " + str(x))
            # print("self.zoom_factor: " + str(self.zoom_factor))
            # print("self.view_center[0]: " + str(self.view_center[0]))
            # print("self.canvas_size[0]: " + str(self.canvas_size[0]))
            # print("canvas_size_after_zoom_x: " + str(canvas_size_after_zoom_x))
            # print("min_x: " + str(min_x))
            # print("x_scalar: " + str(x_scalar))
            # input("x_pixel: " + str(x_pixel))
        return x_pixel,y_pixel
    def update_canvas(self):
        def draw_crosshair(x_coordinate,y_coordinate):
            self.the_canvas.delete("crosshair")
            center_of_cross_coordinates=self.coordinates_to_pixels(x_coordinate,y_coordinate)
            x1 = center_of_cross_coordinates[0] - self.crosshair_size/2
            y1 = center_of_cross_coordinates[1]
            x2 = center_of_cross_coordinates[0] + self.crosshair_size/2
            y2 = center_of_cross_coordinates[1]
            self.the_canvas.create_line(x1,y1,x2,y2,fill='#333333',tags="crosshair")
            # dims = (x1,y1,x2,y2)
            # print("dims: "+str(dims))
            #
            x1 = center_of_cross_coordinates[0]
            y1 = center_of_cross_coordinates[1] - self.crosshair_size/2
            x2 = center_of_cross_coordinates[0]
            y2 = center_of_cross_coordinates[1] + self.crosshair_size/2
            self.the_canvas.create_line(x1,y1,x2,y2,fill='#333333',tags="crosshair")
            # dims = (x1,y1,x2,y2)
            # input("dims: "+str(dims))
        x_center_of_mass,y_center_of_mass = self.parent.field.center_of_mass
        if self.view_behavior.get() == 0: # follow center of mass
            self.view_center = (x_center_of_mass,y_center_of_mass)
        elif self.view_behavior.get() == 1: # follow largest mass
            max_mass = float(np.max(self.parent.field.mass))
            which_mass = int(np.argwhere(self.parent.field.mass == max_mass)[0][0])
            self.view_center = (self.parent.field.coords[which_mass,0],self.parent.field.coords[which_mass,1])
        elif self.view_behavior.get() == 2: # auto zoom
            min_x = np.min(self.parent.field.coords[:,0])
            max_x = np.max(self.parent.field.coords[:,0])
            
            delta_x = max_x-min_x
            min_y = np.min(self.parent.field.coords[:,1])
            max_y = np.max(self.parent.field.coords[:,1])
            delta_y = max_y-min_y
            self.view_center = (min_x+max_x)/2,(min_y+max_y)/2
            
            if self.parent.field.population > 1:
                zoom_factor_x = self.canvas_size[0]/delta_x
                zoom_factor_y = self.canvas_size[1]/delta_y
                self.zoom_factor = min(zoom_factor_x,zoom_factor_y)
            else:
                mass = self.parent.field.mass[0]
                radius = (3/4 * mass / (3.14159 * self.parent.field.density))**(1/3)
                zoom_factor = 2*radius
        else: # remain static
            if self.auto_recenter_check.get(): # nothing to do unless the view needs recentered
                COM_pixel_location = self.coordinates_to_pixels(x_center_of_mass,y_center_of_mass)
                COM_x,COM_y = COM_pixel_location
                if COM_x < 0 or COM_y < 0 or COM_y > self.canvas_size[1] or COM_y > self.canvas_size[0]:
                    self.view_center = (x_center_of_mass,y_center_of_mass)
        draw_crosshair(x_center_of_mass,y_center_of_mass)
        population = self.parent.field.population
        for i in range(population):
            coordinate_location = np.copy(self.parent.field.coords[i])
            pixel_location = self.coordinates_to_pixels(coordinate_location[0],coordinate_location[1])
            mass = self.parent.field.mass[i]
            radius = (3/4 * mass / (3.14159 * self.parent.field.density))**(1/3)
            radius = max(radius*self.zoom_factor,float(self.min_pixel_size.get()))
            color = tuple(self.parent.field.colors[i])
            rgb = "#%02x%02x%02x" % color
            
            x0=int(pixel_location[0]-radius)
            y0=int(pixel_location[1]-radius)
            x1=int(pixel_location[0]+radius)
            y1=int(pixel_location[1]+radius)
            oval_coordinates = (x0,y0,x1,y1)
            self.the_canvas.create_oval(x0,y0,x1,y1,fill=rgb,outline=rgb,tags=self.current_step)
        if self.current_step == "odd": self.current_step = "even"
        else: self.current_step = "odd"
        self.the_canvas.delete(self.current_step)
