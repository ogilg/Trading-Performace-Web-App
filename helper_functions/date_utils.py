from datetime import timedelta


def date_range(start_date, end_date):
    day_lag = 1
    for n in range(int((end_date - start_date).days) + day_lag):
        yield (start_date + timedelta(n)).date()

def remove_day_time(date):
    return date.split('T')[0]
