"""
Funções para manipulação de arquivos
"""
import os
import json
from datetime import datetime

def salvar_resultado(sorteio):
    """
    Salva o resultado do sorteio em um arquivo JSON
    
    Args:
        sorteio (dict): Dicionário com o resultado do sorteio
        
    Returns:
        str: Caminho do arquivo salvo
    """
    # Criar diretório se não existir
    if not os.path.exists('resultados'):
        os.makedirs('resultados')
        
    # Nome do arquivo com data e hora
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"resultados/sorteio_{timestamp}.json"
    
    # Salvar resultado
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(sorteio, f, ensure_ascii=False, indent=4)
        
    return filename
