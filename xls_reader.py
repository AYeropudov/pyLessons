import openpyxl as xl

wb = xl.load_workbook(u"/home/alex/spider/xls/price.xlsx")
sheet = wb.get_active_sheet()
x = sheet['F']
for cell in x:
    print cell.value