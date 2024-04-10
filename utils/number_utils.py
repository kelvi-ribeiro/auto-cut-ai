def get_pretty_minutes(number):
    minutes = int(number)
    decimal_part = number - minutes
    seconds = round(decimal_part * 60, 2)
    return "{:02d}.{:02d}".format(minutes, int(seconds))