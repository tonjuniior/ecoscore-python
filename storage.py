import csv
import os

USUARIOS_FILE = 'usuarios.csv'
REGISTROS_FILE = 'registros_habitos.csv'

def carregar_dados_csv(filename):
    """Carrega dados de um arquivo CSV. Retorna uma lista de dicionários."""
    if not os.path.exists(filename) or os.stat(filename).st_size == 0:
        return []
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            dados = list(reader)
            for linha in dados:
                if 'pontuacao' in linha:
                    try:
                        linha['pontuacao'] = int(linha['pontuacao'])
                    except (ValueError, TypeError):
                        linha['pontuacao'] = 0 # Valor padrão em caso de erro
            return dados
    except (IOError, csv.Error) as e:
        print(f"Erro ao carregar o arquivo {filename}: {e}")
        return []

def salvar_dados_csv(data, filename, fieldnames):
    """Salva uma lista de dicionários em um arquivo CSV."""
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    except IOError as e:
        print(f"Erro ao salvar o arquivo {filename}: {e}")

def carregar_usuarios():
    return carregar_dados_csv(USUARIOS_FILE)

def salvar_usuarios(lista_usuarios):
    salvar_dados_csv(lista_usuarios, USUARIOS_FILE, fieldnames=['nome_usuario', 'senha'])

def carregar_registros():
    return carregar_dados_csv(REGISTROS_FILE)

def salvar_registros(lista_registros):
    
    fieldnames = ['nome_usuario', 'data', 'pontuacao', 'transporte', 'residuos', 'energia', 'alimentacao', 'engajamento']
    salvar_dados_csv(lista_registros, REGISTROS_FILE, fieldnames=fieldnames)