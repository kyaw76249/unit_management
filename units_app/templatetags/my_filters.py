from django import template

register = template.Library()

@register.filter(name='to_myanmar_num')
def to_myanmar_num(value):
    eng_nums = '0123456789'
    mm_nums = '၀၁၂၃၄၅၆၇၈၉'
    trans = str.maketrans(eng_nums, mm_nums)
    return str(value).translate(trans)