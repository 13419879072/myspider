from datetime import datetime


detail_time = '2008-9-22 15:25'
detail_time2 = datetime.strptime(detail_time, '%Y-%m-%d %H:%M')

print(detail_time2)
print(type(detail_time2))