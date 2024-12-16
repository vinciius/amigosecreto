"""
Lógica principal do sorteio do amigo secreto
"""
import random

def realizar_sorteio(participantes):
    """
    Realiza o sorteio do amigo secreto entre os participantes
    
    Args:
        participantes (list): Lista com os nomes dos participantes
        
    Returns:
        dict: Dicionário com o resultado do sorteio {participante: amigo}
    """
    if len(participantes) < 2:
        raise ValueError("É necessário pelo menos 2 participantes!")
        
    sorteio = {}
    amigos_disponiveis = participantes.copy()
    
    for participante in participantes:
        while True:
            amigo = random.choice(amigos_disponiveis)
            if amigo != participante:
                sorteio[participante] = amigo
                amigos_disponiveis.remove(amigo)
                break
                
    return sorteio
