import pandas as pd
import re
import xlsxwriter
from openpyxl import Workbook


def process_informative(text):
    return text

def is_acronym(word):
    return re.match(r'^[A-Z]{2,}$', word) is not None

def process_text(text):
    words = text.split()
    result = []

    for word in words:
        if is_acronym(word):
            result.append(word)
        else:
            result.append(word.capitalize())

    return ' '.join(result)

input_filename = 'conteudo.csv'
output_excel_filename = 'Conteudo.xlsx'
output_csv_filename = 'conteudo_processado.csv'
sheet_name = 'Conteudo'

# Carregar o arquivo CSV com Pandas
data = pd.read_csv(input_filename, encoding='utf-8')

# Processar os dados da coluna "VALOR 01"
data['VALOR 01'] = data['VALOR 01'].apply(lambda x: x.capitalize())

# Criar um arquivo Excel
writer = pd.ExcelWriter(output_excel_filename, engine='xlsxwriter')
data.to_excel(writer, sheet_name=sheet_name, index=False)

# Obter a planilha Excel para ajustar o formato
workbook = writer.book
worksheet = writer.sheets[sheet_name]

# Formato em negrito para a coluna "conteudo informacional"
bold_format = workbook.add_format({'bold': True})
worksheet.set_column('L:L', None, bold_format)
for row_num, value in enumerate(data['VALOR 01'], start=2):
    worksheet.write(row_num - 1, 11, process_informative(value), bold_format)

# Ajustar a largura das colunas na planilha
for i, col in enumerate(data.columns):
    max_len = max(data[col].astype(str).apply(len).max(), len(col))
    worksheet.set_column(i, i, max_len + 2)

writer._save()

# Salvar os dados processados em um novo arquivo CSV
data.to_csv(output_csv_filename, index=False, encoding='utf-8')

print("Processamento concluído. Resultados salvos em", output_excel_filename, "e", output_csv_filename)
