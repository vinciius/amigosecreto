"""
Definições de estilos e cores para a interface gráfica
"""

COLORS = {
    'primary': '#8e44ad',  # Roxo
    'secondary': '#e74c3c',  # Vermelho
    'bg': '#fff5e6',  # Bege claro
    'header_bg': '#8e44ad',  # Roxo
    'button': '#a569bd',  # Lilás claro
    'button_hover': '#b39ddb',  # Lilás mais claro
    'border': '#d3d3d3',  # Cinza claro
    'text': '#000000',      # Texto preto
    'text_light': '#000000' # Texto preto para todos os elementos
}

# Estilos de fonte
FONTS = {
    'header': ('Roboto', 24, 'bold'),
    'title': ('Roboto', 16, 'bold'),
    'normal': ('Roboto', 12),
    'button': ('Roboto', 11),
    'result': ('Roboto', 14)
}

# Tamanhos de janela
WINDOW_SIZE = "600x650"
RESULT_WINDOW_SIZE = "500x400"

# Estilos de botão
BUTTON_STYLE = {
    'relief': 'flat',
    'borderwidth': 0,
    'padx': 15,
    'pady': 8,
    'cursor': 'hand2'
}

# Estilos de frame
FRAME_STYLE = {
    'padx': 20,
    'pady': 10,
    'relief': 'flat',
    'border': 1
}
