"""
识别文字坐标
"""

"""
装备坐标
key：字段名
name：描述
left_top：左上角坐标
right_bottom：右下角坐标
replace：需要剔除的字符串，无则不剔除
check_data：校验的数据
"""
entry_position_dict = {

    "children_name": {
        "name": "套装-子名称",
        "left_top": (20, 0),
        "right_bottom": (250, 45)
    },
    "slot": {
        "name": "部位",
        "left_top": (20, 55),
        "right_bottom": (90, 85)
    },
    "main_tag_name": {
        "name": "主属性",
        "left_top": (20, 120),
        "right_bottom": (250, 150),
        "pattern": r'\b0\b'  # 随便写个，无需匹配
    },
    "main_tag_value": {
        "name": "主属性值",
        "left_top": (20, 150),
        "right_bottom": (250, 190),
        "pattern": r'(\d+(\.\d+)?)',
        "replace": ","
    },
    "level": {
        "name": "强化值",
        "left_top": (25, 250),
        "right_bottom": (80, 290),
        "pattern": r'(\d+(\.\d+)?)'
    },
    "children_tag_1": {
        "name": "词条1",
        "left_top": (20, 290),
        "right_bottom": (250, 325),
        "pattern": r'(\d+(\.\d+)?)'
    },
    "children_tag_2": {
        "name": "词条2",
        "left_top": (20, 325),
        "right_bottom": (250, 365),
        "pattern": r'(\d+(\.\d+)?)'
    },
    "children_tag_3": {
        "name": "词条3",
        "left_top": (20, 355),
        "right_bottom": (250, 395),
        "pattern": r'(\d+(\.\d+)?)'
    },
    "children_tag_4": {
        "name": "词条4/套装",
        "left_top": (20, 385),
        "right_bottom": (250, 425),
        "pattern": r'(\d+(\.\d+)?)',
        "replace": "："
    },
    "main_name": {
        "name": "套装/未知",
        "left_top": (20, 425),
        "right_bottom": (250, 455),
        "replace": "：",
        "check_data": "artifact_list"
    },
    "equip_role": {
        "name": "装备角色",
        "left_top": (65, 660),
        "right_bottom": (250, 690),
        "check_data": "role_list"
    }
}

if __name__ == '__main__':
    info = entry_position_dict['equip_role'].get('replace', None)
    if info:
        print(info)
