from openpyxl import Workbook

# # 假设有一个字段映射，将字段名与表头对应起来
# field_mapping = {
#     'name': 'Name1',
#     'city': 'City1',
#     'age': 'Age1'
# }
#
# # 假设有一个数据集
# data = [
#     {'name': 'Alice', 'age': 25, 'city': 'London'},
#     {'name': 'Bob', 'age': 30, 'city': 'Paris'},
#     {'name': 'Charlie', 'age': 35, 'city': 'Berlin'}
# ]
#
# # 创建一个新的Excel工作簿
# wb = Workbook()
# ws = wb.active
#
# # 添加表头
# for col, header in enumerate(field_mapping.values(), start=1):
#     cell = ws.cell(row=1, column=col)
#     cell.value = header
#
# # 根据字段映射将数据插入到相应的单元格中
# for row, row_data in enumerate(data, start=2):
#     for field, col in field_mapping.items():
#         cell = ws.cell(row=row, column=list(field_mapping.keys()).index(field) + 1)
#         cell.value = row_data[field]
#
# # 保存Excel文件
# wb.save("data.xlsx")
