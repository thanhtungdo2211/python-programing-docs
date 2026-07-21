from datetime import date
import calendar

days_in_month = { 'January' : 31, 'February' : 28, 'March' : 31,
'April' : 30, 'May' : 31, 'June' : 30,
'July' : 31, 'August' : 31, 'September' : 30,
'October' : 31, 'November' : 30, 'December' : 31 }
key_array = ['January', 'February', 'March', 'April', 'May', 'June',]
month_length = [31, 28, 31, 30, 31, 30, 31]

def print_month(month, year):
    idx = key_array.index(month)
    day = 1
    wd = date(year,idx + 1,day).weekday()
    wd = (wd + 1) % 7
    end = month_length[idx]
    if calendar.isleap(year) and idx == 1:
        end += 1        
    print('{} {}'.format(month,year).center(20))
    print('Su Mo Tu We Th Fr Sa')
    print(' ' * wd, end='')
    while day <= end:
        print('{:2d} '.format(day), end='')
        wd = (wd + 1) % 7
        day += 1
        if wd == 0: print()
    print()

print_month('February', 2020)
print_month('February', 2021)