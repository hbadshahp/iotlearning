
from openpyxl import load_workbook
wb = load_workbook(filename='Book.xlsx',read_only=True)
ws = wb['Sheet1']

for row in ws.rows:
  for cell in row:
    print(cell.value)

# close the workbook after reading
wb.close()
