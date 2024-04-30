"""
评分计算模块
"""
from decimal import Decimal


def cal_artifact_grade(role_info, artifact_info):
    """
    评分计算
    """
    total_grade = 0.0
    # 主标签(默认暴击、爆伤 + lv分数)
    main_tag = artifact_info['main_tag']['name']
    level = float(artifact_info['level'])
    if main_tag in ["暴击率", "暴击伤害"]:
        total_grade += level
    # 子标签
    children_tags = artifact_info['children_tag']
    for tag_info in children_tags:
        tag_name = tag_info['name']
        if tag_name in cal_dict:
            value = float(tag_info['value'])
            grade = cal_dict[tag_name](role_info, value)
            total_grade += grade
    return total_grade


def __cal_attack_grade(role_info, value):
    """
    攻击评分计算
    :param role_info 角色配置信息
    :param value 属性值
    """
    if '%' in str(value) or value < 1.0:
        return value * 1.33 * role_info['attack'] / 100
    else:
        return value * 0.398 * 0.5


def __cal_defense_grade(role_info, value):
    """
    防御评分计算
    :param role_info 角色配置信息
    :param value 属性值
    """
    if '%' in str(value) or Decimal(str(value)) < Decimal(1):
        return value * 1.06 * role_info['defense'] / 100
    else:
        return value * 0.335 * 0.66


def __cal_health_grade(role_info, value):
    """
    生命值评分计算
    :param role_info 角色配置信息
    :param value 属性值
    """
    if '%' in str(value) or Decimal(str(value)) < Decimal(1):
        return value * 1.33 * role_info['health'] / 100
    else:
        return value * 0.026 * 0.66


def __cal_elemental_mastery_grade(role_info, value):
    """
    元素精通评分计算
    :param role_info 角色配置信息
    :param value 属性值
    """
    return value * 0.33 * role_info['elemental_mastery'] / 100


def __cal_energy_recharge_grade(role_info, value):
    """
    充能效率评分计算
    :param role_info 角色配置信息
    :param value 属性值
    """
    return value * 1.1979 * role_info['energy_recharge'] / 100


def __cal_critical_rate_grade(role_info, value):
    """
    暴击率评分计算
    :param role_info 角色配置信息
    :param value 属性值
    """
    return value * 2 * role_info['critical_rate'] / 100


def __cal_critical_damage_grade(role_info, value):
    """
    暴击伤害评分计算
    :param role_info 角色配置信息
    :param value 属性值
    """
    return value * 1 * role_info['critical_damage'] / 100


cal_dict = {
    "攻击力": __cal_attack_grade,
    "防御力": __cal_defense_grade,
    "生命值": __cal_health_grade,
    "元素精通": __cal_elemental_mastery_grade,
    "元素充能效率": __cal_energy_recharge_grade,
    "暴击率": __cal_critical_rate_grade,
    "暴击伤害": __cal_critical_damage_grade,
}
