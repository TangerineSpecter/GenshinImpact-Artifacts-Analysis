"""
角色权重字典
health: 生命值
attack：攻击力
defense：防御力
critical_rate：暴击率
critical_damage：暴击伤害
elemental_mastery：元素精通
energy_recharge：元素充能
"""
role_weight_dict = {
    '米卡': {
        'health': 100,
        'attack': 50,
        'defense': 0,
        'critical_rate': 50,
        'critical_damage': 50,
        'elemental_mastery': 0,
        'energy_recharge': 90
    },
    '迪希雅': {
        'health': 75,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 0,
        'energy_recharge': 0
    },
    '艾尔海森': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 75,
        'energy_recharge': 0
    },
    '瑶瑶': {
        'health': 100,
        'attack': 50,
        'defense': 0,
        'critical_rate': 50,
        'critical_damage': 50,
        'elemental_mastery': 0,
        'energy_recharge': 75
    },
    '流浪者': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 0,
        'energy_recharge': 0
    },
    '珐露珊': {
        'health': 0,
        'attack': 55,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 0,
        'energy_recharge': 75
    },
    '纳西妲': {
        'health': 0,
        'attack': 55,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 100,
        'energy_recharge': 0
    },
    '莱依拉': {
        'health': 100,
        'attack': 55,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 0,
        'energy_recharge': 55
    },
    '妮露': {
        'health': 100,
        'attack': 0,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 75,
        'energy_recharge': 0
    },
    '赛诺': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 75,
        'energy_recharge': 0
    },
    '坎蒂丝': {
        'health': 100,
        'attack': 0,
        'defense': 0,
        'critical_rate': 50,
        'critical_damage': 50,
        'elemental_mastery': 0,
        'energy_recharge': 55
    },
    '多莉': {
        'health': 75,
        'attack': 75,
        'defense': 0,
        'critical_rate': 50,
        'critical_damage': 50,
        'elemental_mastery': 0,
        'energy_recharge': 55
    },
    '提纳里': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 75,
        'energy_recharge': 0
    },
    '柯莱': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 75,
        'energy_recharge': 55
    },
    '鹿野院平藏': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 75,
        'energy_recharge': 0
    },
    '久岐忍': {
        'health': 100,
        'attack': 75,
        'defense': 0,
        'critical_rate': 50,
        'critical_damage': 50,
        'elemental_mastery': 100,
        'energy_recharge': 55
    },
    '夜兰': {
        'health': 80,
        'attack': 0,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 0,
        'energy_recharge': 55
    },
    '神里绫人': {
        'health': 50,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 0,
        'energy_recharge': 0
    },
    '八重神子': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 75,
        'energy_recharge': 0
    },
    '申鹤': {
        'health': 0,
        'attack': 100,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 0,
        'energy_recharge': 55
    },
    '云堇': {
        'health': 0,
        'attack': 0,
        'defense': 100,
        'critical_rate': 50,
        'critical_damage': 50,
        'elemental_mastery': 0,
        'energy_recharge': 90
    },
    '荒泷一斗': {
        'health': 0,
        'attack': 50,
        'defense': 100,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 0,
        'energy_recharge': 30
    },
    '五郎': {
        'health': 0,
        'attack': 50,
        'defense': 100,
        'critical_rate': 50,
        'critical_damage': 50,
        'elemental_mastery': 0,
        'energy_recharge': 90
    },
    '班尼特': {
        'health': 100,
        'attack': 50,
        'defense': 0,
        'critical_rate': 50,
        'critical_damage': 50,
        'elemental_mastery': 0,
        'energy_recharge': 55
    },
    '枫原万叶': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 100,
        'energy_recharge': 55
    },
    '雷电将军': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 0,
        'energy_recharge': 75
    },
    '行秋': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 0,
        'energy_recharge': 55
    },
    '钟离': {
        'health': 80,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 0,
        'energy_recharge': 55
    },
    '神里绫华': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 0,
        'energy_recharge': 0
    },
    '香菱': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 75,
        'energy_recharge': 55
    },
    '胡桃': {
        'health': 80,
        'attack': 50,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 75,
        'energy_recharge': 0
    },
    '甘雨': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 75,
        'energy_recharge': 0
    },
    '温迪': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 75,
        'energy_recharge': 55
    },
    '珊瑚宫心海': {
        'health': 100,
        'attack': 50,
        'defense': 0,
        'critical_rate': 0,
        'critical_damage': 0,
        'elemental_mastery': 75,
        'energy_recharge': 55
    },
    '莫娜': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 75,
        'energy_recharge': 75
    },
    '阿贝多': {
        'health': 0,
        'attack': 0,
        'defense': 100,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 0,
        'energy_recharge': 0
    },
    '迪奥娜': {
        'health': 100,
        'attack': 50,
        'defense': 0,
        'critical_rate': 50,
        'critical_damage': 50,
        'elemental_mastery': 0,
        'energy_recharge': 90
    },
    '优菈': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 0,
        'energy_recharge': 30
    },
    '达达利亚': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 75,
        'energy_recharge': 0
    },
    '魈': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 0,
        'energy_recharge': 55
    },
    '宵宫': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 75,
        'energy_recharge': 0
    },
    '九条裟罗': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 0,
        'energy_recharge': 55
    },
    '琴': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 0,
        'energy_recharge': 55
    },
    '菲谢尔': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 75,
        'energy_recharge': 0
    },
    '罗莎莉亚': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 0,
        'energy_recharge': 0
    },
    '可莉': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 75,
        'energy_recharge': 0
    },
    '凝光': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 0,
        'energy_recharge': 0
    },
    '北斗': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 75,
        'energy_recharge': 55
    },
    '刻晴': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 75,
        'energy_recharge': 0
    },
    '托马': {
        'health': 100,
        'attack': 50,
        'defense': 0,
        'critical_rate': 50,
        'critical_damage': 50,
        'elemental_mastery': 0,
        'energy_recharge': 90
    },
    '迪卢克': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 75,
        'energy_recharge': 0
    },
    '芭芭拉': {
        'health': 100,
        'attack': 50,
        'defense': 0,
        'critical_rate': 50,
        'critical_damage': 50,
        'elemental_mastery': 0,
        'energy_recharge': 55
    },
    '诺艾尔': {
        'health': 0,
        'attack': 50,
        'defense': 90,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 0,
        'energy_recharge': 70
    },
    '旅行者草': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 75,
        'energy_recharge': 55
    },
    '旅行者雷': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 75,
        'energy_recharge': 0
    },
    '旅行者岩': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 0,
        'energy_recharge': 0
    },
    '旅行者风': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 75,
        'energy_recharge': 0
    },
    '重云': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 75,
        'energy_recharge': 55
    },
    '七七': {
        'health': 0,
        'attack': 100,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 0,
        'energy_recharge': 55
    },
    '凯亚': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 0,
        'energy_recharge': 0
    },
    '烟绯': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 75,
        'energy_recharge': 0
    },
    '早柚': {
        'health': 0,
        'attack': 50,
        'defense': 0,
        'critical_rate': 50,
        'critical_damage': 50,
        'elemental_mastery': 100,
        'energy_recharge': 55
    },
    '安柏': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 75,
        'energy_recharge': 0
    },
    '丽莎': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 75,
        'energy_recharge': 0
    },
    '埃洛伊': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 0,
        'energy_recharge': 0
    },
    '辛焱': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 0,
        'energy_recharge': 55
    },
    '砂糖': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 100,
        'energy_recharge': 55
    },
    '雷泽': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 0,
        'energy_recharge': 0
    },
    '芙宁娜': {
        'health': 100,
        'attack': 0,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 0,
        'energy_recharge': 30
    },
    '闲云': {
        'health': 0,
        'attack': 100,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 0,
        'energy_recharge': 70
    },
    '林尼': {
        'health': 0,
        'attack': 75,
        'defense': 0,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 0,
        'energy_recharge': 0
    },
    '千织': {
        'health': 0,
        'attack': 70,
        'defense': 100,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 0,
        'energy_recharge': 0
    },
    '嘉明': {
        'health': 0,
        'attack': 75,
        'defense': 100,
        'critical_rate': 100,
        'critical_damage': 100,
        'elemental_mastery': 75,
        'energy_recharge': 0
    }
}
