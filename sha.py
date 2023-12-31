import os
import hashlib
import re

def calcular_sha256(arquivo):
    sha256 = hashlib.sha256()
    with open(arquivo, 'rb') as f:
        while True:
            dados = f.read(8192)
            if not dados:
                break
            sha256.update(dados)
    return sha256.hexdigest()

def procurar_arquivo(nome_arquivo, diretorio):
    # Lista todos os arquivos no diretório
    for root, dirs, arquivos in os.walk(diretorio):
        for arquivo in arquivos:
            if arquivo == nome_arquivo:
                caminho_completo = os.path.join(root, arquivo)
                return caminho_completo
    return None

def comparar_diretorios(diretorio1, diretorio2, differents, not_exist):
    arquivos_origem = os.listdir(diretorio1)

    # for each file in the dir, search on the dir destine
    for arquivo_origem in arquivos_origem:
        caminho_arquivo_origem = os.path.join(diretorio1, arquivo_origem)

        # verify if the archive is one file or dir
        if os.path.isfile(caminho_arquivo_origem):
            # search for the same file in the dir of destine
            caminho_arquivo_destino = procurar_arquivo(arquivo_origem, diretorio2)

            git = re.compile(r'.*git\w*')
            correspondencias1 = git.findall(caminho_arquivo_origem)

            if caminho_arquivo_destino is not None:
                correspondencias2 = git.findall(caminho_arquivo_destino)
                hash1 = calcular_sha256(caminho_arquivo_origem)
                hash2 = calcular_sha256(caminho_arquivo_destino)

                if hash1 != hash2 and not (correspondencias2 or correspondencias1):
                    differents.append(f"Files {caminho_arquivo_origem} and {caminho_arquivo_destino} are different.")
            else:
                if not correspondencias1:
                    not_exist.append(f"File {caminho_arquivo_origem} exists in {diretorio1}, but not in {diretorio2}.")

# example of use
cva_2024 = "/home/raffael/Desktop/Project/cv_2024"
cva_2021 = "/home/raffael/Desktop/Project/cv_2022"

differents = []
not_exist = []

comparar_diretorios(cva_2024, cva_2021, differents, not_exist)

# Print the differences
print("Differents Dir")
for diff in differents:
    print(diff)

# print the file what have in cva_2024 but not in cva_2021
print("\ndon't exist in the cva_2022")
for missing in not_exist:
    print(missing)
