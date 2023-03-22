from datetime import date
from calendar import monthrange
import datetime

Total_number_days = monthrange(2020, 2)[1]

def get_cls_left(cls: int) -> float:
    p_month = date.today().month
    if p_month > 6:
        # 15 - (12 - p_month)
        return 3 + p_month - cls
    else:
        # 7.5 - (6 - p_month)
        return 1.5 + p_month - cls


def generate_leaves(f_date: str, no: int):
    year, month, date = [int(x) for x in f_date.split('-')]

    base = datetime.date(year, month, date)
    #date_list = [f"{base + datetime.timedelta(days=x):%Y-%m-%d}" for x in range(no)]
    date_list = [base + datetime.timedelta(days=x) for x in range(no)]
    return date_list


if __name__ == '__main__':
    print(get_cls_left(0))
    print(generate_leaves('2023-004-28', 4))
