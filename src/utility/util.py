import calendar
import os


def getWeekendDate(year, month):
    """
    Get the weekend date of a month
    :param year: int
    :param month: int
    :return: list
    """
    calendar_matrix = calendar.monthcalendar(year, month)
    weekend_date = []
    weekends = []
    # complexity: number of weekend_date
    for week in calendar_matrix:  # 4~5
        weekend_date = week[-2:]
        for date in weekend_date:  # 2
            if date > 0:
                weekends.append(date - 1)

    return weekends


def getFileName(path):
    basename = os.path.basename(path)
    filename = basename.split(".")[0]

    return filename
