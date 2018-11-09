

# from datetime import datetime
# start=datetime.now()
# lst = [1,2,54,12,2,1,3,65,2,1,2,5,1,12,2,5,1]
# for i in range(len(lst)):
#     print(lst[i])
# print('---')
# for i in lst:
#     print(i)
# print(datetime.now()-start)

# from datetime import timedelta, datetime as day
#
# print day.now().strftime("%d-%b-%y")

dic ={}
present = ({u'Social': u'49', u'Paid Search': u'36', u'Direct': u'161', u'Referral': u'147', u'Organic Search': u'294'}, {u'Visitor_Sent_a_Message': u'0', u'Sign-in': u'2',  u'Order': u'3',  u'New Registration': u'5'}, {u'ga:goalCompletionsAll': u'0', u'ga:adClicks': u'34', u'ga:impressions': u'2400', u'ga:adCost': u'34.2', u'ga:CTR': u'1.4166666666666665'}, {u'ga:goalCompletionsAll': u'0'})
for key,value in present[1].items():
    dic[str(key)] = int(value)
new = {}
dic2 = dic.copy()
for key in dic2:
    if key == 'Visitor_Sent_a_Message':
        new['Chat Conversation']=dic[key]
        dic.pop(key)
    elif key =='Order':
        new['Sales'] = dic[key]
        dic.pop(key)
dic.update(new)
print dic
lst=[]
for key,value in dic.items():
    lst.append('{}: {}'.format(key,value))

print lst
for item in lst:
    print item,
print item