"""
Efeitos visuais personalizados para a interface
"""
import tkinter as tk
from tkinter import font as tkfont

def hex_to_rgb(hex_color):
    """Converte cor hexadecimal para RGB"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    """Converte RGB para hexadecimal"""
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def interpolate_color(color1, color2, factor):
    """Interpola entre duas cores"""
    rgb1 = hex_to_rgb(color1)
    rgb2 = hex_to_rgb(color2)
    
    return rgb_to_hex(tuple(int(rgb1[i] + (rgb2[i] - rgb1[i]) * factor) for i in range(3)))

class GradientFrame(tk.Canvas):
    """Frame com efeito de gradiente"""
    def __init__(self, parent, color1, color2, height=100, title="", title_font=None, title_color="black", **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self._color1 = color1
        self._color2 = color2
        self._height = height
        self._title = title
        self._title_font = title_font
        self._title_color = title_color
        self.bind('<Configure>', self._draw_gradient)
        
    def _draw_gradient(self, event=None):
        """Desenha o gradiente e o texto"""
        self.delete("all")  # Limpa todo o canvas
        width = self.winfo_width()
        height = self._height
        
        # Número de linhas para o gradiente
        limit = height
        
        # Desenha o gradiente
        for i in range(limit):
            factor = i / float(limit - 1)
            color = interpolate_color(self._color1, self._color2, factor)
            y = i * (height / limit)
            self.create_line(0, y, width, y, fill=color)
            
        # Desenha o texto centralizado
        if self._title and self._title_font:
            font_obj = tkfont.Font(font=self._title_font)
            text_width = font_obj.measure(self._title)
            text_height = font_obj.metrics()["ascent"] + font_obj.metrics()["descent"]
            
            x = width / 2
            y = height * 0.3  # 30% da altura do gradiente
            
            self.create_text(
                x, y,
                text=self._title,
                font=self._title_font,
                fill=self._title_color,
                anchor="center"
            )
            
        self.configure(height=height)
