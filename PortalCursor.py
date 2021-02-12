# -*- coding: utf-8 -*-
# Python 3.6.2 / 3.8.6
# ----------------------------------------------------------------------------

__title__ = "PortalCursor"
__author__ = "Asurix"
__version__ = '0.1.0'
__github__ = "https://github.com/4surix/PortalCursor"


import time
import tkinter as tk

from ctypes import windll, Structure, c_long, byref


class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]


def getCursorPosition():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return pt.x, pt.y


def setCursorPosition(x, y):
    windll.user32.SetCursorPos(x, y)


class Portail:

    def __init__(self, color):

        self.root = root = tk.Toplevel(bg='white')

        root.overrideredirect(1)
        root.lift()
        root.attributes("-topmost", True)
        root.attributes('-alpha', 0.75)
        root.wm_attributes("-transparentcolor", "#012345")

        root.bind("<Button-1>", self.set_coordinates)
        root.bind("<ButtonRelease-1>", self.set_coordinates)
        root.bind("<B1-Motion>", self.move)


        self.x = 1
        self.y = 1
        self.width = 40
        self.height = 55
        self.bord = bord = 5

        canv = tk.Canvas(
            root,
            bg = '#012345',
            bd = 0,
            width = self.width,
            height = self.height,
            selectborderwidth = 0, 
            highlightthickness = 0
        )
        canv.grid()


        # Contour noir

        NO_x = bord
        NO_y = bord
        SE_x = self.width - bord
        SE_y = self.height - bord

        canv.create_oval(
            NO_x, NO_y, SE_x, SE_y,
            fill = '',
            width = bord,
            outline = 'black'
        )


        # Contour couleur

        NO_x += 2
        NO_y += 2
        SE_x -= 2
        SE_y -= 2
        bord -= 2

        canv.create_oval(
            NO_x, NO_y, SE_x, SE_y,
            fill = '',
            width = bord,
            outline = color
        )


        root.geometry(f"{self.width}x{self.height}+1+1")

    def move(self, event):
        x = self.x + event.x_root - self.x__
        y = self.y + event.y_root - self.y__
        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")

    def set_coordinates(self, event):
        self.x = self.root.winfo_rootx()
        self.y = self.root.winfo_rooty()
        self.x__ = event.x_root
        self.y__ = event.y_root


class App(tk.Tk):

    def __init__(self):
        super().__init__()

        self.portail_1 = Portail('#FF6600')
        self.portail_2 = Portail('#28A2FF')

        tk.Label(text='Fermez cette fenêtre pour fermer les portails.').grid()

    @staticmethod
    def in_zone(portail:Portail, x:int, y:int) -> bool: return (
        (
            (
                x
                - (portail.x + portail.width / 2)
            ) 
            / ((portail.width - portail.bord * 4) / 2)
        ) ** 2 
        +
        (
            (
                y
                - (portail.y + portail.height / 2)
            )
            / ((portail.height - portail.bord * 4) / 2)
        ) ** 2
        <= 1
    )

    @staticmethod
    def teleport_to(portail:Portail) -> None: return setCursorPosition(
        portail.x + portail.width // 2,
        portail.y + portail.height // 2
    )

    def run(self):

        teleported_from_1 = teleported_from_2 = False

        while True:

            # Uptate de l'application.
            self.update()


            # Detection si curseur est dans un portail.

            x, y = getCursorPosition()

            if self.in_zone(self.portail_1, x, y):
                if not teleported_from_2:
                    teleported_from_1 = True
                    self.teleport_to(self.portail_2)

            elif self.in_zone(self.portail_2, x, y):
                if not teleported_from_1:
                    teleported_from_2 = True
                    self.teleport_to(self.portail_1)

            else:
                teleported_from_1 = teleported_from_2 = False

App().run()