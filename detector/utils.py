# -*- coding: utf-8 -*-
import os
import sys
execution_path=os.getcwd()

from tkinter import *
import tkinter
from PIL import Image, ImageTk

class Empty_Object:

       def __init(self):
              pass

       def write(self, string):
              pass

       def close(self):
              pass

class Empty_Detector:

       def __init(self, text=False, label=False):
              pass

       def set_preview(self, preview):
              pass

       def set_text(self, text):
              pass


class AnimatedGIF(Label, object):
    def __init__(self, master, path, forever=True):
        self._master = master
        self._loc = 0
        self._forever = forever

        self._is_running = False
        self.empty=Image.open(os.path.join(os.path.join(os.path.join(os.path.join(execution_path,"detector"),"resources"),"empty.png")))
        im = Image.open(path)
        self._frames = []
        i = 0
        try:
            while True:
                photoframe = ImageTk.PhotoImage(im.copy().convert('RGBA'))
                self._frames.append(photoframe)

                i += 1
                im.seek(i)
        except EOFError: pass
        
        self._last_index = len(self._frames) - 1

        try:
            self._delay = im.info['duration']
        except:
            self._delay = 100

        self._callback_id = None

        super(AnimatedGIF, self).__init__(master, image=self._frames[0])


    def set_empty(self):
           self.configure(image=ImageTk.PhotoImage(self.empty))
           self.update()


       
    def start_animation(self, frame=None):
        if self._is_running: return

        if frame is not None:
            self._loc = 0
            self.configure(image=self._frames[frame])

        self._master.after(self._delay, self._animate_GIF)
        self._is_running = True

    def stop_animation(self):
        if not self._is_running: return

        if self._callback_id is not None:
            self.after_cancel(self._callback_id)
            self._callback_id = None

        self.set_empty()
        self._is_running = False


    def _animate_GIF(self):
        self._loc += 1
        self.configure(image=self._frames[self._loc])

        if self._loc == self._last_index:
            if self._forever:
                self._loc = 0
                self._callback_id = self._master.after(self._delay, self._animate_GIF)
            else:
                self._callback_id = None
                self._is_running = False
        else:
            self._callback_id = self._master.after(self._delay, self._animate_GIF)

    def pack(self, start_animation=True, **kwargs):
        if start_animation:
            self.start_animation()

        super(AnimatedGIF, self).pack(**kwargs)

    def grid(self, start_animation=True, **kwargs):
        if start_animation:
            self.start_animation()

        super(AnimatedGIF, self).grid(**kwargs)
        
    def place(self, start_animation=True, **kwargs):
        if start_animation:
            self.start_animation()

        super(AnimatedGIF, self).place(**kwargs)
        
    def pack_forget(self, **kwargs):
        self.stop_animation()

        super(AnimatedGIF, self).pack_forget(**kwargs)

    def grid_forget(self, **kwargs):
        self.stop_animation()

        super(AnimatedGIF, self).grid_forget(**kwargs)
        
    def place_forget(self, **kwargs):
        self.stop_animation()

        super(AnimatedGIF, self).place_forget(**kwargs)


class Preview_Label(Label, object):

       def __init__(self, master):
              self._default_image=ImageTk.PhotoImage(Image.open(os.path.join(os.path.join(os.path.join(os.path.join(execution_path,"detector"),"resources"),"empty.png"))))
              super(Preview_Label, self).__init__(master, image=self._default_image)

       def set_empty(self):
              self.configure(image=self._default_image)
              self.update()
            
