# 🎁 Amigo Secreto

Uma aplicação simples para realizar sorteios de amigo secreto com interface gráfica.

## 📁 Estrutura do Projeto

```
amigosecreto/
├── src/                    # Código fonte
│   ├── gui/               # Interface gráfica
│   │   ├── app.py        # Classe principal da interface
│   │   └── styles.py     # Definições de estilos
│   ├── core/             # Lógica principal
│   │   └── sorteio.py    # Funções do sorteio
│   └── utils/            # Utilitários
│       └── file_handler.py # Manipulação de arquivos
├── resultados/            # Pasta para salvar resultados
├── main.py               # Ponto de entrada
└── README.md             # Este arquivo
```

## 🚀 Como Executar

1. Certifique-se de ter Python 3.6 ou superior instalado
2. Execute o arquivo principal:
   ```
   python main.py
   ```

## 💡 Funcionalidades

- Adicionar e remover participantes
- Realizar sorteio automático
- Interface amigável e intuitiva
- Salvar resultado do sorteio em arquivo JSON
- Visualização individual do amigo secreto

## 🎨 Interface

A interface foi desenvolvida com tkinter e possui um design moderno com cores suaves e agradáveis.

## 📝 Notas

- Os resultados são salvos na pasta `resultados/` com data e hora
- Cada participante pode ver apenas seu próprio amigo secreto
- É necessário pelo menos 2 participantes para realizar o sorteio
