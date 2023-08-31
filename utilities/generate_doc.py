import openpyxl

def generate_doc(table_data):

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    for row_data in table_data:
        sheet.append(row_data)
    return workbook
