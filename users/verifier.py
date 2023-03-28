from datetime import date
from calendar import monthrange
import datetime

Total_number_days = monthrange(2020, 2)[1]


def get_cls_left(cls: float, p_month:int = date.today().month) -> float:
    if p_month > 6:
        # 15 - (12 - p_month)
        return 3 + p_month - cls
    else:
        # 7.5 - (6 - p_month)
        return 1.5 + p_month - cls


def generate_range(base_date: date, no: int):
    # date_list = [f"{base + datetime.timedelta(days=x):%Y-%m-%d}" for x in range(no)]

    date_list = [base_date + datetime.timedelta(days=x) for x in range(no)]
    return date_list


def generate_leaves(base_date: date, no: int, exclude: list[date] = []):
    # date_list = [f"{base + datetime.timedelta(days=x):%Y-%m-%d}" for x in range(no)]

    date_list = [base_date + datetime.timedelta(days=x) for x in range(no)]
    date_list = [d for d in date_list if not d.isoweekday() in [7, ] and d not in exclude]
    return date_list


if __name__ == '__main__':
    print(get_cls_left(0))
    print(generate_leaves(datetime.date(2023, 4, 23), 4))
