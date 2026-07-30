import xlwings as xw

def update_excel_panel(stock_code: str, ai_data: dict):
    # 连接到当前打开的 Excel 工作簿
    wb = xw.Book('C:/Users/lzw12/Documents/Trading_Dashboard.xlsx')
    sheet = wb.sheets['持仓监控']
    
    # 假设我们要在第一行空白处写入最新决策
    empty_row = sheet.range('A' + str(sheet.cells.last_cell.row)).end('up').row + 1
    
    sheet.range(f'A{empty_row}').value = stock_code
    sheet.range(f'B{empty_row}').value = ai_data.get('entry_price')
    sheet.range(f'C{empty_row}').value = ai_data.get('stop_loss')
    sheet.range(f'D{empty_row}').value = ai_data.get('conclusion')
    
    print(f"✅ {stock_code} 的 1-2 周波段数据已同步至 Excel 面板")