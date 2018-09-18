# import smtplib
# s = smtplib.SMTP('smtp.gmail.com', 587)
# s.starttls()
#
# s.login("nbveeresh1995@gmail.com", "08521111@A")
#
# msg = "Visits: {}({})-> [Search:{}%, Direct:{}%, Referral:{}%, Social:{}%, Paid:{}%]".format(14578,+5.15,+10.52,+5.16,-14.26,-4.47,-14.61)
# print(msg)
# # msg = 'hellow'
#
# s.sendmail("nbveeresh1995@gmail.com", "nbveeresh1995@gmail.com", msg)
#
# s.quit()
from datetime import datetime as day
from dateutil.relativedelta import relativedelta

# f = {'returningusers': {'present': [{'traffic': 20034, 'option': u'01'}, {'traffic': 18639, 'option': u'02'}, {'traffic': 19640, 'option': u'03'}, {'traffic': 17491, 'option': u'04'}, {'traffic': 17301, 'option': u'05'}, {'traffic': 14933, 'option': u'06'}, {'traffic': 15235, 'option': u'07'}, {'traffic': 15043, 'option': u'08'}, {'traffic': 18171, 'option': u'09'}, {'traffic': 19521, 'option': u'10'}, {'traffic': 18753, 'option': u'11'}, {'traffic': 14637, 'option': u'12'}], 'previous': [{'traffic': 20621, 'option': u'01'}, {'traffic': 20159, 'option': u'02'}, {'traffic': 21716, 'option': u'03'}, {'traffic': 16757, 'option': u'04'}, {'traffic': 17652, 'option': u'05'}, {'traffic': 15010, 'option': u'06'}, {'traffic': 14474, 'option': u'07'}, {'traffic': 14795, 'option': u'08'}, {'traffic': 20375, 'option': u'09'}, {'traffic': 21151, 'option': u'10'}, {'traffic': 21592, 'option': u'11'}, {'traffic': 16110, 'option': u'12'}]}, 'AllTraffic': {'present': [{'option': u'01', 'All Traffic': 68380}, {'option': u'02', 'All Traffic': 64054}, {'option': u'03', 'All Traffic': 69583}, {'option': u'04', 'All Traffic': 62201}, {'option': u'05', 'All Traffic': 62098}, {'option': u'06', 'All Traffic': 55572}, {'option': u'07', 'All Traffic': 57061}, {'option': u'08', 'All Traffic': 63376}, {'option': u'09', 'All Traffic': 64854}, {'option': u'10', 'All Traffic': 67073}, {'option': u'11', 'All Traffic': 62933}, {'option': u'12', 'All Traffic': 47900}], 'previous': [{'option': u'01', 'All Traffic': 72912}, {'option': u'02', 'All Traffic': 68219}, {'option': u'03', 'All Traffic': 72596}, {'option': u'04', 'All Traffic': 57258}, {'option': u'05', 'All Traffic': 60133}, {'option': u'06', 'All Traffic': 52960}, {'option': u'07', 'All Traffic': 49889}, {'option': u'08', 'All Traffic': 51559}, {'option': u'09', 'All Traffic': 73055}, {'option': u'10', 'All Traffic': 73180}, {'option': u'11', 'All Traffic': 73505}, {'option': u'12', 'All Traffic': 57765}]}, 'MobileTabletTraffic': {'present': [{'traffic': 18363, 'option': u'01'}, {'traffic': 17301, 'option': u'02'}, {'traffic': 18779, 'option': u'03'}, {'traffic': 16643, 'option': u'04'}, {'traffic': 16656, 'option': u'05'}, {'traffic': 15080, 'option': u'06'}, {'traffic': 15890, 'option': u'07'}, {'traffic': 18913, 'option': u'08'}, {'traffic': 18646, 'option': u'09'}, {'traffic': 18117, 'option': u'10'}, {'traffic': 16469, 'option': u'11'}, {'traffic': 13662, 'option': u'12'}], 'previous': [{'traffic': 20040, 'option': u'01'}, {'traffic': 18986, 'option': u'02'}, {'traffic': 19380, 'option': u'03'}, {'traffic': 16795, 'option': u'04'}, {'traffic': 16070, 'option': u'05'}, {'traffic': 14712, 'option': u'06'}, {'traffic': 14801, 'option': u'07'}, {'traffic': 15300, 'option': u'08'}, {'traffic': 19999, 'option': u'09'}, {'traffic': 19798, 'option': u'10'}, {'traffic': 20274, 'option': u'11'}, {'traffic': 19317, 'option': u'12'}]}}


month_num = [(day.today() - relativedelta(months=i)).month for i in range(1, 13)]
month_num = month_num[::-1]
print(month_num)
# for i in month_num[0:13]:
#     print(f['AllTraffic']['present'][i-1])
# for i in month_num[0:13]:
#     print(f['returningusers']['present'][i-1])
# for i in month_num[0:13]:
#     print(f['MobileTabletTraffic']['present'][i-1])
# for i in months[::-1]:
#
#     print(f['AllTraffic']['present'][i])



# for item in f['AllTraffic']['present']:
#     print(item)
# for item in f['AllTraffic']['previous'][0:30]:
#     print(item)
# for item1, item2 in zip(f['AllTraffic']['present'][0:30],(f['AllTraffic']['previous'][0:30])):
#     # print(item1,item2)
#     change= ((int(item1['All Traffic'])-int(item2['All Traffic']))/int(item2['All Traffic']))*100
#     print(change)


f = [[{'Country': 'Total', 'Direct': 14479, 'Email': 781, 'Social': 3959, 'Referral': 3157, 'Paid Search': 1603, 'Organic Search': 44401}, {'Country': 'Change', 'Direct': '-40.84%', 'Email': '-0.13%', 'Social': '-23.11%', 'Referral': '-5.2%', 'Paid Search': '100%', 'Organic Search': '14.57%'}], [{'Country': 'Total', 'Direct': 12914, 'Email': 589, 'Social': 4038, 'Referral': 2921, 'Paid Search': 1497, 'Organic Search': 42095}, {'Country': 'Change', 'Direct': '-52.23%', 'Email': '-31.83%', 'Social': '-22.63%', 'Referral': '-16.38%', 'Paid Search': '100%', 'Organic Search': '35.71%'}], [{'Country': 'Total', 'Direct': 13495, 'Email': 797, 'Social': 4937, 'Referral': 3109, 'Paid Search': 1395, 'Organic Search': 45850}, {'Country': 'Change', 'Direct': '-69.57%', 'Email': '-11.35%', 'Social': '49.88%', 'Referral': '38.55%', 'Paid Search': '71.59%', 'Organic Search': '100%'}], [{'Country': 'Total', 'Direct': 12462, 'Email': 756, 'Social': 4849, 'Referral': 2971, 'Paid Search': 1211, 'Organic Search': 39952}, {'Country': 'Change', 'Direct': '-47.63%', 'Email': '22.73%', 'Social': '46.81%', 'Referral': '26.86%', 'Paid Search': '33.81%', 'Organic Search': '51.94%'}], [{'Country': 'Total', 'Direct': 13149, 'Email': 799, 'Social': 5223, 'Referral': 2878, 'Paid Search': 1293, 'Organic Search': 38756}, {'Country': 'Change', 'Direct': '-2.77%', 'Email': '11.75%', 'Social': '26.59%', 'Referral': '-15.15%', 'Paid Search': '100%', 'Organic Search': '2.6%'}], [{'Country': 'Total', 'Direct': 12984, 'Email': 539, 'Social': 4668, 'Referral': 2884, 'Paid Search': 1243, 'Organic Search': 33254}, {'Country': 'Change', 'Direct': '19.36%', 'Email': '-15.25%', 'Social': '19.36%', 'Referral': '-5.87%', 'Paid Search': '96.99%', 'Organic Search': '-1.73%'}], [{'Country': 'Total', 'Direct': 14525, 'Email': 853, 'Social': 4862, 'Referral': 3271, 'Paid Search': 1122, 'Organic Search': 32428}, {'Country': 'Change', 'Direct': '35.71%', 'Email': '15.11%', 'Social': '16.01%', 'Referral': '9.88%', 'Paid Search': '37.0%', 'Organic Search': '6.47%'}], [{'Country': 'Total', 'Direct': 14044, 'Email': 497, 'Social': 4042, 'Referral': 3871, 'Paid Search': 1122, 'Organic Search': 39800}, {'Country': 'Change', 'Direct': '21.87%', 'Email': '7.34%', 'Social': '0.4%', 'Referral': '38.7%', 'Paid Search': '-18.22%', 'Organic Search': '26.82%'}], [{'Country': 'Total', 'Direct': 14122, 'Email': 747, 'Social': 3891, 'Referral': 3042, 'Paid Search': 1405, 'Organic Search': 41647}, {'Country': 'Change', 'Direct': '2.83%', 'Email': '-23.46%', 'Social': '-16.18%', 'Referral': '-23.7%', 'Paid Search': '38.02%', 'Organic Search': '-14.48%'}], [{'Country': 'Total', 'Direct': 14293, 'Email': 851, 'Social': 3924, 'Referral': 3023, 'Paid Search': 1116, 'Organic Search': 43866}, {'Country': 'Change', 'Direct': '-0.72%', 'Email': '1.92%', 'Social': '-25.84%', 'Referral': '-21.48%', 'Paid Search': '35.44%', 'Organic Search': '-8.58%'}], [{'Country': 'Total', 'Direct': 14361, 'Email': 751, 'Social': 3834, 'Referral': 2744, 'Paid Search': 1078, 'Organic Search': 40165}, {'Country': 'Change', 'Direct': '-14.11%', 'Email': '-17.2%', 'Social': '-32.83%', 'Referral': '-47.99%', 'Paid Search': '-6.42%', 'Organic Search': '-8.18%'}], [{'Country': 'Total', 'Direct': 11927, 'Email': 808, 'Social': 3267, 'Referral': 2488, 'Paid Search': 910, 'Organic Search': 28500}, {'Country': 'Change', 'Direct': '-43.78%', 'Email': '-4.38%', 'Social': '-50.55%', 'Referral': '-28.09%', 'Paid Search': '20.21%', 'Organic Search': '14.55%'}]]
for i in month_num[0:13]:
    print(f[i-1])