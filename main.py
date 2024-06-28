import os
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime
import time

def csv_to_xml(csv_file, xml_file, chunk_size=100000):
    print("Iniciando a conversão do CSV para XML...")

    # Verificar se o arquivo CSV existe
    if not os.path.exists(csv_file):
        print(f"Erro: O arquivo {csv_file} não foi encontrado.")
        return

    print(f"Lendo o arquivo CSV em chunks de {chunk_size} linhas...")
    # Inicializar o elemento raiz
    root = ET.Element("portedList")
    root.set("type", "FULL")
    root.set("created", "2024-06-20T12:00:00.000+06:00")

    total_rows = 0
    start_time = time.time()

    # Ler o CSV em chunks
    for chunk in pd.read_csv(csv_file, chunksize=chunk_size):
        total_rows += len(chunk)
        for _, row in chunk.iterrows():
            ported = ET.SubElement(root, "ported")
            number = ET.SubElement(ported, "number")
            number.text = str(row["number"])
            
            portedDate = ET.SubElement(ported, "portedDate")
            # Remover espaços extras e converter a data
            ported_date_str = row["portedDate"].strip()
            portedDate.text = datetime.strptime(ported_date_str, "%d/%m/%Y %H:%M:%S").strftime("%Y-%m-%dT%H:%M:%S.000+06:00")
            
            recipientRC = ET.SubElement(ported, "recipientRC")
            recipientRC.text = str(row["recipientRC"]) if pd.notna(row["recipientRC"]) else ""
            
            donorRC = ET.SubElement(ported, "donorRC")
            donorRC.text = str(row["donorRC"]) if pd.notna(row["donorRC"]) else ""
            
            nrhRC = ET.SubElement(ported, "nrhRC")
            nrhRC.text = str(row["nrhRC"]) if pd.notna(row["nrhRC"]) else ""
            
            numberType = ET.SubElement(ported, "numberType")
            numberType.text = str(row["numberType"])

        # Indicador de progresso
        elapsed_time = time.time() - start_time
        progress = (total_rows / 47000000) * 100  # Supondo 47 milhões de registros
        print(f"Progresso: {progress:.2f}% ({total_rows}/47000000) - Tempo decorrido: {elapsed_time:.2f}s")

    # Definir o atributo "count" com o total de linhas processadas
    root.set("count", str(total_rows))

    print("Criando a árvore XML e escrevendo no arquivo...")
    # Criar a árvore XML e escrever no arquivo
    tree = ET.ElementTree(root)
    tree.write(xml_file, encoding="UTF-8", xml_declaration=True)

    total_time = time.time() - start_time
    print(f"Conversão concluída. Arquivo XML salvo em: {xml_file}")
    print(f"Tempo total de execução: {total_time:.2f}s")

if __name__ == "__main__":
    # Forneça o caminho completo para o arquivo CSV
    csv_file = r"C:\Users\patrick.oliveira\Desktop\BD Ported_Number2\unified_ported_numbers.csv"
    xml_file = "portedListFULL-2024-06-20-12-00.xml"
    
    print("Verificando se o arquivo CSV existe no diretório especificado...")
    # Verificar se o arquivo CSV existe no diretório especificado
    if not os.path.exists(csv_file):
        print(f"Erro: O arquivo {csv_file} não foi encontrado no diretório especificado.")
    else:
        csv_to_xml(csv_file, xml_file)