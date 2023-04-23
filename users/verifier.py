from datetime import date
from calendar import monthrange
import datetime

Total_number_days = monthrange(2020, 2)[1]


# def get_cls_left(cls: float, p_month:int = date.today().month) -> float:
#     reserve = 1.5
#
#     if p_month > 6:
#         # 15 - (12 - p_month)
#         return 3 + p_month - cls
#     else:
#         # 7.5 - (6 - p_month)
#         return 1.5 + p_month - cls

def positive_sum(aList):
    s = 0
    for x in aList:
        if x > 0:
            s = s + x
    return s


def get_cls_left(datelist, h_datelist, p_month):
    reserve = 1.5
    n_leaves = [0 if m < p_month else -1 for m in range(12)]

    for d in datelist:
        n_leaves[d.month - 1] += 1

    for d in h_datelist:
        n_leaves[d.month - 1] += 0.5

    from_reserve = positive_sum(n_leaves)
    left = reserve - from_reserve + p_month + (1.5 if p_month > 6 else 0)

    return left


def generate_range(base_date, no):
    # date_list = [f"{base + datetime.timedelta(days=x):%Y-%m-%d}" for x in range(no)]

    date_list = [base_date + datetime.timedelta(days=x) for x in range(no)]
    return date_list


def generate_leaves(base_date, no, exclude=[]):
    # date_list = [f"{base + datetime.timedelta(days=x):%Y-%m-%d}" for x in range(no)]

    date_list = [base_date + datetime.timedelta(days=x) for x in range(no)]
    date_list = [d for d in date_list if not d.isoweekday() in [7, ] and d not in exclude]
    return date_list


if __name__ == '__main__':
    print(get_cls_left(0))
    print(generate_leaves(datetime.date(2023, 4, 23), 4))
