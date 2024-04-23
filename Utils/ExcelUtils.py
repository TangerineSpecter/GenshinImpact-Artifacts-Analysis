"""
Excel工具类
"""

from openpyxl.styles import Alignment, PatternFill, Border, Side, Font
from openpyxl.workbook import Workbook


def apply_format(cell, is_header):
    font = Font(name="LXGWWenKaiGBScreen", size=14, color="000000", bold=False) if not is_header else Font(
        name="LXGWWenKaiGBScreen", size=18, color="ffffff")
    alignment = Alignment(horizontal='center', vertical='center', text_rotation=0, indent=0)
    fill = PatternFill(patternType="solid", fgColor="ffffcc", bgColor="ff2600") if not is_header else PatternFill(
        patternType="solid", fgColor="5e7ce0", bgColor="9bc2e6")
    side = Side(style="thin", color="000000")
    border = Border(top=side, bottom=side, left=side, right=side, diagonal=side)

    cell.font = font
    cell.alignment = alignment
    cell.fill = fill
    cell.border = border


# 定义表头键值对列表
head = ["部位", "装备角色", "主词条", "主词条属性值", "词条1", "词条2"]

# 定义目标数组列表
targetList = [
    "哈哈哈", "胡桃", "测试1", "测试2", "测试3"
]

# 创建一个工作簿
wb = Workbook()
# 获取当前活动的工作表
ws = wb.active
# 设置工作表的名称
ws.title = u'圣遗物数据'
# 设置表头
ws.append(head)

# 设置表头的列宽
for cell in ws[1]:
    ws.column_dimensions[cell.column_letter].width = max(len(str(cell.value)) + 20, 20)

# 写入数据
ws.append(targetList)

for row in ws:
    for cell in row:
        is_header = cell.row == 1
        apply_format(cell, is_header)

# 将工作簿保存到磁盘
wb.save('王者荣耀战绩.xlsx')
