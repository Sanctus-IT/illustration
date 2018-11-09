

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
<<<<<<< HEAD
dic =[]
present = ({u'Social': u'49', u'Paid Search': u'36', u'Direct': u'161', u'Referral': u'147', u'Organic Search': u'294'}, {u'Visitor_Sent_a_Message': u'0', u'Sign-in': u'2'}, {u'ga:goalCompletionsAll': u'0', u'ga:adClicks': u'34', u'ga:impressions': u'2400', u'ga:adCost': u'34.2', u'ga:CTR': u'1.4166666666666665'}, {u'ga:goalCompletionsAll': u'0'})
for key,value in present[1].items():
    dic.append({str(key):int(value)})
# print dic
for item in dic:
    print item
    if item.keys()=='Visitor_Sent_a_Message':
        print item
=======

# dic ={}
# present = ({u'Social': u'49', u'Paid Search': u'36', u'Direct': u'161', u'Referral': u'147', u'Organic Search': u'294'}, {u'Visitor_Sent_a_Message': u'0', u'Sign-in': u'2',  u'Order': u'3',  u'New Registration': u'5'}, {u'ga:goalCompletionsAll': u'0', u'ga:adClicks': u'34', u'ga:impressions': u'2400', u'ga:adCost': u'34.2', u'ga:CTR': u'1.4166666666666665'}, {u'ga:goalCompletionsAll': u'0'})
# for key,value in present[1].items():
#     dic[str(key)] = int(value)
# new = {}
# dic2 = dic.copy()
# for key in dic2:
#     if key == 'Visitor_Sent_a_Message':
#         new['Chat Conversation']=dic[key]
#         dic.pop(key)
#     elif key =='Order':
#         new['Sales'] = dic[key]
#         dic.pop(key)
# dic.update(new)
# print dic
# lst=[]
# for key,value in dic.items():
#     lst.append('{}: {}'.format(key,value))
#
# print lst
# for item in lst:
#     print item,
# print item

lst =[[[u'(not set)', u'18', u'0', u'0'], [u'Facebook', u'95', u'0', u'0'], [u'Instagram', u'27', u'0', u'1'], [u'LinkedIn', u'12', u'0', u'0'], [u'Pinterest', u'303', u'0', u'0']], [[u'(not set)', u'11', u'0', u'0'], [u'Facebook', u'28', u'0', u'0'], [u'Instagram', u'12', u'0', u'0'], [u'LinkedIn', u'6', u'0', u'0'], [u'Pinterest', u'291', u'0', u'0']], [[u'Instagram', u'1'], [u'LinkedIn', u'1'], [u'Pinterest', u'117']], [[u'Facebook', u'2'], [u'LinkedIn', u'2'], [u'Pinterest', u'5']]]
keys = ['Pinterest', 'Instagram', 'Facebook', 'Twitter', 'LinkedIn', 'Linkedin Groups']
pinterest,instagram,facebook,twitter,linkedin,linkedinGroups=[],[],[],[],[],[]
for item in lst:
    # print(item)
    for item2 in item:
        if item2[0]==keys[0]:
            pinterest.append(item2)
        elif item2[0]==keys[1]:
            instagram.append(item2)
        elif item2[0]==keys[2]:
            facebook.append(item2)
        elif item2[0]==keys[3]:
            twitter.append(item2)
        elif item2[0]==keys[4]:
            linkedin.append(item2)
        elif item2[0]==keys[5]:
            linkedinGroups.append(item2)

print(pinterest)
print(instagram)
print(facebook)
print(twitter)
print(linkedin)
print(linkedinGroups)

def cal(lst):
    result = int(lst[0][1],0)+int(lst[1][1],0)+int(lst[2][1],0)+int(lst[3][1],0)
    return result
print(cal(pinterest))
print(cal(instagram))




>>>>>>> 4a4eb43aeac3268bd238364c2d3dad8a95254534
