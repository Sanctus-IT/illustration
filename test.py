

# from datetime import datetime
# start=datetime.now()
# lst = [1,2,54,12,2,1,3,65,2,1,2,5,1,12,2,5,1]
# for i in range(len(lst)):
#     print(lst[i])
# print('---')
# for i in lst:
#     print(i)
# print(datetime.now()-start)

from datetime import timedelta, datetime as day

print day.now().strftime("%d-%b-%y")