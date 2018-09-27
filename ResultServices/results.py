from get_data import get_Month_data, total_sessions

class SessionsCategoryResults:

    def __init__(self, current_results, previous_results, option):
        self.current_results = current_results
        self.previous_results = previous_results
        self.option = option

    @staticmethod
    def fix_change(k, l):
        change = round((((float(k['TotalSessions']) - float(l['TotalSessions']))
                    /float(l['TotalSessions'])) * 100), 2)

        change = 100 if change > 100 else change
        return str(change)+'%'

    @staticmethod
    def mapping(results):
        i = 0
        new_results = []
        length = len(results[0])
        if len(results[0]) == 31:
            length = 30
        while i < length:
            new = [item[i] for item in results]
            new_results.append(new)
            i += 1
        return new_results

    @staticmethod
    def get_totalsessions_total(total_sessions):
        total = 0
        for data in total_sessions:
            total += int(data['TotalSessions'])
        total_sessions.append({'Country': 'Total', 'TotalSessions': total})
        return total_sessions

    @staticmethod
    def total(result, country):
        res_data = {'Country': country, 'Organic Search': 0, 'Direct': 0, 'Paid Search': 0, 'Referral': 0, 'Social': 0, 'Email': 0}
        for item in result:
            res_data['Organic Search'] += int(item.get('Organic Search', 0))
            res_data['Direct'] += int(item.get('Direct', 0))
            res_data['Paid Search'] += int(item.get('Paid Search', 0))
            res_data['Referral'] += int(item.get('Referral', 0))
            res_data['Social'] += int(item.get('Social', 0))
            res_data['Email'] += int(item.get('Email', 0))
        return res_data

    @staticmethod
    def change_cal(total1, total2):
        change_dict = {}
        keys = ['Organic Search', 'Direct', 'Paid Search', 'Referral' 'Social', 'Email']
        change_dict['Country'] = 'Change'
        for key, value in total1.items():
            try:
                if total2.get(key) == 0:
                    change = 100
                else:
                    change = round(((float(total1.get(key, 0))-float(total2.get(key, 0)))/float(total2.get(key,0))) * 100, 2)
                change_dict[key] = str(100 if change > 100 else change) + '%'
            except Exception as e:
                # print e
                pass
        return change_dict

    @staticmethod
    def result(results):
        main_result = [
            {'Country': i.get('Country', 0),
             'Direct': i.get('Direct', 0),
             'Paid Search': i.get('Paid Search', 0),
             'Organic Search': i.get('Organic Search', 0),
             'Referral': i.get('Social', 0),
             'Social': i.get('Referral', 0),
             'Email': i.get('Email', 0)
             }
            for i in results
        ]
        return main_result

    def main(self):
        pre_session_results = self.current_results.sessions(self.option)[0]
        prev_sessions_results = self.previous_results.sessions(self.option)[0]

        pre_conversion_results = self.current_results.sessions(self.option)[1]
        prev_conversion_results = self.previous_results.sessions(self.option)[1]

        keys = ['Country', 'Organic Search', 'Direct', 'Referral', 'Social', 'Paid Search', 'Email']
        pre_total_data = get_Month_data(pre_session_results, keys)
        prev_total_data = get_Month_data(prev_sessions_results, keys)

        pre_TotalSessions_line = total_sessions(pre_session_results)
        prev_TotalSessions_line =total_sessions(prev_sessions_results)

        keys = ['Country', 'TotalSessions']
        pre_TotalSessions = get_Month_data(pre_TotalSessions_line, keys)
        prev_TotalSessions = get_Month_data(prev_TotalSessions_line, keys)
        total_current = self.total(pre_total_data, 'Total')
        total_previous = self.total(prev_total_data, 'Total(Prev)')

        change = self.change_cal(total_current, total_previous)
        pre_total_data.append(total_current)
        pre_total_data.append(total_previous)
        pre_total_data.append(change)

        pre_TotalSessions = self.get_totalsessions_total(pre_TotalSessions)
        prev_TotalSessions = self.get_totalsessions_total(prev_TotalSessions)

        sessions_main_result = [
            {'Country': i[0]['Country'],
             'Current': i[0]['TotalSessions'],
             'Previous': i[1]['TotalSessions'],
             'Change': str(round((((float(i[0]['TotalSessions']) - float(i[1]['TotalSessions']))
                                   / float(i[1]['TotalSessions'])) * 100), 2)) + '%'
             }
            for i in zip(pre_TotalSessions, prev_TotalSessions)
        ]

        new_pre_session_results = self.mapping(pre_session_results)
        new_prev_sessions_results = self.mapping(prev_sessions_results)
        source_change_percentage = []
        for i, j in zip(new_pre_session_results, new_prev_sessions_results):
            total_current = self.total(i, 'Total')
            total_previous = self.total(j, 'Total(Prev)')
            change = self.change_cal(total_current, total_previous)
            source_change_percentage.append([total_current, change])

        total_sessions_line_data = []
        for i, j in zip(pre_TotalSessions_line, prev_TotalSessions_line):
            new = []
            for k, l in zip(i, j):
                change = {
                    'Country': k['Country'],
                    'Total': k['TotalSessions'],
                    'Change': self.fix_change(k, l)
                    }
                new.append(change)
            total_sessions_line_data.append(new)

        return {
            'goalconversions':{'present':pre_conversion_results,'previous':prev_conversion_results},
            'sessions': {'present': pre_total_data, 'previous': prev_total_data},
            'totalSessions': sessions_main_result,
            'session_category_line_data': source_change_percentage,
            'session_region_line_data': total_sessions_line_data
        }

class WebsiteTrafficResults:

    def __init__(self, current_results, previous_results, option):
        self.current_results = current_results
        self.previous_results = previous_results
        self.option = option

    def main(self):

        pre_Traffic = self.current_results.all_traffic(self.option)
        pre_MobileTabletTraffic = self.current_results.MobileTabletTraffic(self.option)
        pre_returningUsers = self.current_results.returning_users(self.option)

        prev_Traffic = self.previous_results.all_traffic(self.option)
        prev_MobileTabletTraffic = self.previous_results.MobileTabletTraffic(self.option)
        prev_returningUsers = self.previous_results.returning_users(self.option)

        return {
            'AllTraffic': {
                'present':  pre_Traffic,
                'previous': prev_Traffic
            },
            'MobileTabletTraffic': {
                'present': pre_MobileTabletTraffic,
                'previous': prev_MobileTabletTraffic
            },
            'returningusers': {
                'present': pre_returningUsers,
                'previous': prev_returningUsers
            }
        }


class BounceRateResults:

    def __init__(self, current_results, previous_results):
        self.current_results = current_results
        self.previous_results = previous_results

    def main(self):

        pre_bounceRate = self.current_results.bouncerate()
        prev_bounceRate = self.previous_results.bouncerate()

        return {"present": pre_bounceRate, 'previous': prev_bounceRate}

class AvgSessionDuration:

    def __init__(self, current_results, previous_results):
        self.current_results = current_results
        self.previous_results = previous_results

    def main(self):

        pre_AvgSessionDuration = self.current_results.avg_session_duration()
        prev_AvgSessionDuration = self.previous_results.avg_session_duration()
        return {"present": pre_AvgSessionDuration, 'previous': prev_AvgSessionDuration}

class Conversions:

    def __init__(self, current_results, previous_results, option):
        self.current_results = current_results
        self.previous_results = previous_results
        self.option = option

    @staticmethod
    def total(result):
        res_data = {'Organic Search': 0, 'Direct': 0, 'Paid Search': 0, 'Referral': 0, 'Social': 0, 'Email': 0}
        for item in result:
            res_data['Organic Search'] += int(item.get('Organic Search', 0))
            res_data['Direct'] += int(item.get('Direct', 0))
            res_data['Paid Search'] += int(item.get('Paid Search', 0))
            res_data['Referral'] += int(item.get('Referral', 0))
            res_data['Social'] += int(item.get('Social', 0))
            res_data['Email'] += int(item.get('Email', 0))
        return res_data

    def main(self):

        pre_conversions_data = self.current_results.totalConversions(self.option)
        prev_conversions_data = self.previous_results.totalConversions(self.option)

        pre_source = self.total(pre_conversions_data['sources'])
        prev_source = self.total(prev_conversions_data['sources'])

        pre_conversions_data['sources'] = pre_source
        prev_conversions_data['sources'] = prev_source

        return {
            'pre_conversions': pre_conversions_data,
            'prev_conversions': prev_conversions_data
        }

class Topkeywords:
    def __init__(self, current_results, previous_results):
        self.current_results = current_results
        self.previous_results = previous_results

    def main(self):
        pre_top_key_words = self.current_results.top_key_words()
        prev_top_key_words = self.previous_results.top_key_words()
        change = {'mobiletablet_change': [((float(pre_top_key_words[0]['MobileTablet']) - float(
                                prev_top_key_words[0]['MobileTablet'])) / float(prev_top_key_words[0]['MobileTablet'])) * 100 if float(
                                prev_top_key_words[0]['MobileTablet']) != 0 else 100],
                  'bouncerate_change': [((float(pre_top_key_words[0]['BounceRate']) - float(
                                  prev_top_key_words[0]['BounceRate'])) / float(prev_top_key_words[0]['BounceRate'])) * 100 if float(
                                  prev_top_key_words[0]['BounceRate']) != 0 else 100],
                  'returnConv_change': [((float(pre_top_key_words[0]['ReturningConversions']) - float(
                                  prev_top_key_words[0]['ReturningConversions'])) / float(prev_top_key_words[0]['ReturningConversions'])) * 100 if float(
                                  prev_top_key_words[0]['ReturningConversions']) != 0 else 100],
                  'unique_change': [((float(pre_top_key_words[0]['UniqueConversions']) - float(prev_top_key_words[0]['UniqueConversions'])) / float(
                                prev_top_key_words[0]['UniqueConversions'])) * 100 if float(prev_top_key_words[0]['UniqueConversions']) != 0 else 100],
                  'avgSession_change': [((float(pre_top_key_words[0]['SessionDuration']) - float(prev_top_key_words[0]['SessionDuration'])) / float(
                                prev_top_key_words[0]['SessionDuration'])) * 100 if float(prev_top_key_words[0]['SessionDuration']) != 0 else 100]
                  }

        return {'present':pre_top_key_words,'previous':prev_top_key_words,'change':change}

class Agents:
    def __init__(self, current_results, previous_results):
        self.current_results = current_results
        self.previous_results = previous_results

    def main(self):
        pre_agents = self.current_results.agents()
        prev_agents = self.previous_results.agents()
        change = {'call_change': [((float(pre_agents[0]['CallClick']) - float(
            prev_agents[0]['CallClick'])) / float(prev_agents[0]['CallClick'])) * 100 if float(
            prev_agents[0]['CallClick']) != 0 else 100],
                  'email_change': [((float(pre_agents[0]['EmailClick']) - float(
                      prev_agents[0]['EmailClick'])) / float(prev_agents[0]['EmailClick'])) * 100 if float(
                      prev_agents[0]['EmailClick']) != 0 else 100],
                  'click_change': [((float(pre_agents[0]['Click']) - float(
                      prev_agents[0]['Click'])) / float(prev_agents[0]['Click'])) * 100 if float(
                      prev_agents[0]['Click']) != 0 else 100]}
        return {'present':pre_agents,'previous':prev_agents,'change':change}

class SideButton:
    def __init__(self, current_results, previous_results):
        self.current_results = current_results
        self.previous_results = previous_results

    def main(self):
        pre_side_button = self.current_results.side_button()
        prev_side_button = self.previous_results.side_button()
        change = {'help_change': [((float(pre_side_button[0]['Help']) - float(
            prev_side_button[0]['Help'])) / float(prev_side_button[0]['Help'])) * 100 if float(
            prev_side_button[0]['Help']) != 0 else 100],
                   'recentlyViewed_change': [((float(pre_side_button[0]['RecentlyViewedPortfolios']) - float(
                      prev_side_button[0]['RecentlyViewedPortfolios'])) / float(prev_side_button[0]['RecentlyViewedPortfolios'])) * 100 if float(
                      prev_side_button[0]['RecentlyViewedPortfolios']) != 0 else 100]}
        return {'present':pre_side_button,'previous':prev_side_button,'change':change}

class Portfolio:
    def __init__(self, current_results, previous_results):
        self.current_results = current_results
        self.previous_results = previous_results

    def main(self):
        pre_portfolio = self.current_results.portfolio()
        prev_portfolio = self.previous_results.portfolio()
        change ={'call_change' : [((float(pre_portfolio[0]['CallClick'])-float(prev_portfolio[0]['CallClick']))/float(prev_portfolio[0]['CallClick']))*100 if float(prev_portfolio[0]['CallClick']) !=0 else 100],
                'email_change' : [((float(pre_portfolio[0]['EmailClick'])-float(prev_portfolio[0]['EmailClick']))/float(prev_portfolio[0]['EmailClick']))*100 if float(prev_portfolio[0]['EmailClick']) !=0 else 100] ,
                'video_change' : [((float(pre_portfolio[0]['VideoImgClick'])-float(prev_portfolio[0]['VideoImgClick']))/float(prev_portfolio[0]['VideoImgClick']))*100 if float(prev_portfolio[0]['VideoImgClick']) !=0 else 100],
                'pdf_change' : [((float(pre_portfolio[0]['PDFClick'])-float(prev_portfolio[0]['PDFClick']))/float(prev_portfolio[0]['PDFClick']))*100 if float(prev_portfolio[0]['PDFClick']) !=0 else 100] }

        return {'present':pre_portfolio,'previous':prev_portfolio,'change':change}


class Events:
    def __init__(self, current_results, previous_results):
        self.current_results = current_results
        self.previous_results = previous_results

    def main(self):
        pre_events = self.current_results.events()
        prev_events = self.previous_results.events()
        pre_total = float(pre_events[0]['HelloBar Events'])+float(pre_events[1]['HelloBar Events'])+float(pre_events[2]['HelloBar Events'])+float(pre_events[3]['HelloBar Events'])
        prev_total = float(prev_events[0]['HelloBar Events'])+float(prev_events[1]['HelloBar Events'])+float(prev_events[2]['HelloBar Events'])+float(prev_events[3]['HelloBar Events'])
        change = {'uk_change' : [((float(pre_events[0]['HelloBar Events'])-float(prev_events[0]['HelloBar Events']))/float(prev_events[0]['HelloBar Events']))*100 if float(prev_events[0]['HelloBar Events']) !=0 else 100],
                    'usa_change' : [((float(pre_events[1]['HelloBar Events'])-float(prev_events[1]['HelloBar Events']))/float(prev_events[1]['HelloBar Events']))*100 if float(prev_events[1]['HelloBar Events']) !=0 else 100],
                    'france_change' : [((float(pre_events[2]['HelloBar Events'])-float(prev_events[2]['HelloBar Events']))/float(prev_events[2]['HelloBar Events']))*100 if float(prev_events[2]['HelloBar Events']) !=0 else 100],
                    'china_change' : [((float(pre_events[3]['HelloBar Events'])-float(prev_events[3]['HelloBar Events']))/float(prev_events[3]['HelloBar Events']))*100 if float(prev_events[3]['HelloBar Events']) !=0 else 100],
                    'total_change' : [((pre_total-prev_total)/prev_total)*100 if prev_total !=0 else 100] }
        total = {'pre_total':int(pre_total),'prev_total':int(prev_total)}
        return {'present':pre_events,'previous':prev_events,'total':total,'change':change}

class Devices:
    def __init__(self, current_results, previous_results):
        self.current_results = current_results
        self.previous_results = previous_results

    def main(self):
        pre_devices = self.current_results.devices()
        prev_devices = self.previous_results.devices()
        change = {'mobile_change': [((float(pre_devices[0]['mobile']) - float(prev_devices[0]['mobile'])) / float(
            prev_devices[0]['mobile'])) * 100 if prev_devices[0]['mobile'] != 0 else 100],
                  'tablet_change': [((float(pre_devices[0]['tablet']) - float(prev_devices[0]['tablet'])) / float(
                      prev_devices[0]['tablet'])) * 100 if prev_devices[0]['tablet'] != 0 else 100],
                  'desktop_change': [((float(pre_devices[0]['desktop']) - float(prev_devices[0]['desktop'])) / float(
                      prev_devices[0]['desktop'])) * 100 if prev_devices[0]['desktop'] != 0 else 100]}

        return {'present':pre_devices,'previous':prev_devices,'change':change}
class Googleads:

    def __init__(self, current_results, previous_results):
        self.current_results = current_results
        self.previous_results = previous_results

    def main(self):
        pre_portfolio = self.current_results.googleads()
        prev_portfolio = self.previous_results.googleads()
        # print(pre_portfolio)
        # print(prev_portfolio)
        total=pre_portfolio[0]['Animators UK']+pre_portfolio[0]['Animators USA']+pre_portfolio[0]['Competitors']+pre_portfolio[0]['Illustration Search ANZ']+pre_portfolio[0]['Illustration Search UK']+pre_portfolio[0]['Illustration Search USA']
        total_prv=prev_portfolio[0]['Animators UK']+prev_portfolio[0]['Animators USA']+prev_portfolio[0]['Competitors']+prev_portfolio[0]['Illustration Search ANZ']+prev_portfolio[0]['Illustration Search UK']+prev_portfolio[0]['Illustration Search USA']
        total_s=pre_portfolio[0]['Stock UK']+pre_portfolio[0]['Stock USA']
        total_prvs=prev_portfolio[0]['Stock UK']+prev_portfolio[0]['Stock USA']
        change=round(((float(total)-float(total_prv))/float(total_prv))*100,1) if total_prv !=0 else 100
        change_s=round(((float(total_s)-float(total_prvs))/float(total_prvs))*100,1) if total_prvs !=0 else 100
        return {'present':pre_portfolio,'previous':prev_portfolio,'total':total,'total_prv':total_prv,'total_s':total_s,'total_prvs':total_prvs,
                'change':change,'change_s':change_s}
class Googleads_cost:

    def __init__(self, current_results, previous_results):
        self.current_results = current_results
        self.previous_results = previous_results

    def main(self):
        pre_portfolio = self.current_results.googleads_cost()
        prev_portfolio = self.previous_results.googleads_cost()
        # print(pre_portfolio)
        # print(prev_portfolio)
        total=float(pre_portfolio[0]['Animators UK'])+float(pre_portfolio[0]['Animators USA'])+float(pre_portfolio[0]['Competitors'])+float(pre_portfolio[0]['Illustration Search ANZ'])+float(pre_portfolio[0]['Illustration Search UK'])+float(pre_portfolio[0]['Illustration Search USA'])
        total_prv=float(prev_portfolio[0]['Animators UK'])+float(prev_portfolio[0]['Animators USA'])+float(prev_portfolio[0]['Competitors'])+float(prev_portfolio[0]['Illustration Search ANZ'])+float(prev_portfolio[0]['Illustration Search UK'])+float(prev_portfolio[0]['Illustration Search USA'])
        total_s=float(pre_portfolio[0]['Stock UK'])+float(pre_portfolio[0]['Stock USA'])
        total_prvs=float(prev_portfolio[0]['Stock UK'])+float(prev_portfolio[0]['Stock USA'])
        change = round(((float(total)-float(total_prv))/float(total_prv))*100,1) if total_prv != 0 else 100
        change_s = round(((float(total_s)-float(total_prvs))/float(total_prvs))*100,1) if total_prvs != 0 else 100
        return {'present':pre_portfolio,'previous':prev_portfolio,'total':total,'total_prv':total_prv,'total_s':total_s,'total_prvs':total_prvs,
                'change':change,'change_s':change_s}

class Googleads_ctr:

    def __init__(self, current_results, previous_results):
        self.current_results = current_results
        self.previous_results = previous_results

    def main(self):
        pre_portfolio = self.current_results.googleads_ctr()
        prev_portfolio = self.previous_results.googleads_ctr()
        # print(pre_portfolio)
        # print(prev_portfolio)
        total=pre_portfolio[0]['Animators UK']+pre_portfolio[0]['Animators USA']+pre_portfolio[0]['Competitors']+pre_portfolio[0]['Illustration Search ANZ']+pre_portfolio[0]['Illustration Search UK']+pre_portfolio[0]['Illustration Search USA']
        total_prv=prev_portfolio[0]['Animators UK']+prev_portfolio[0]['Animators USA']+prev_portfolio[0]['Competitors']+prev_portfolio[0]['Illustration Search ANZ']+prev_portfolio[0]['Illustration Search UK']+prev_portfolio[0]['Illustration Search USA']
        total_s=pre_portfolio[0]['Stock UK']+pre_portfolio[0]['Stock USA']
        total_prvs=prev_portfolio[0]['Stock UK']+prev_portfolio[0]['Stock USA']
        change = round((total - total_prv) / total_prv * 100,1) if total_prv != 0 else 100
        change_s = round((total_s - total_prvs) / total_prvs * 100,1) if total_prvs != 0 else 100
        return {'present':pre_portfolio,'previous':prev_portfolio,'total':total,'total_prv':total_prv,'total_s':total_s,'total_prvs':total_prvs,
                'change':change,'change_s':change_s}
class Googleads_imp:

    def __init__(self, current_results, previous_results):
        self.current_results = current_results
        self.previous_results = previous_results

    def main(self):
        pre_portfolio = self.current_results.googleads_imp()
        prev_portfolio = self.previous_results.googleads_imp()
        # print(pre_portfolio)
        # print(prev_portfolio)
        total=pre_portfolio[0]['Animators UK']+pre_portfolio[0]['Animators USA']+pre_portfolio[0]['Competitors']+pre_portfolio[0]['Illustration Search ANZ']+pre_portfolio[0]['Illustration Search UK']+pre_portfolio[0]['Illustration Search USA']
        total_prv=prev_portfolio[0]['Animators UK']+prev_portfolio[0]['Animators USA']+prev_portfolio[0]['Competitors']+prev_portfolio[0]['Illustration Search ANZ']+prev_portfolio[0]['Illustration Search UK']+prev_portfolio[0]['Illustration Search USA']
        total_s=pre_portfolio[0]['Stock UK']+pre_portfolio[0]['Stock USA']
        total_prvs=prev_portfolio[0]['Stock UK']+prev_portfolio[0]['Stock USA']
        change = round((float(total) - float(total_prv)) / float(total_prv) * 100,1) if total_prv != 0 else 100
        change_s = round((float(total_s) - float(total_prvs)) / float(total_prvs) * 100,1) if total_prvs != 0 else 100
        return {'present':pre_portfolio,'previous':prev_portfolio,'total':total,'total_prv':total_prv,'total_s':total_s,'total_prvs':total_prvs,
                'change':change,'change_s':change_s}
class Googleads_en:

    def __init__(self, current_results, previous_results):
        self.current_results = current_results
        self.previous_results = previous_results

    def main(self):
        pre_portfolio = self.current_results.googleads_en()
        prev_portfolio = self.previous_results.googleads_en()
        # print(pre_portfolio)
        # print(prev_portfolio)
        total=pre_portfolio[0]['Animators UK']+pre_portfolio[0]['Animators USA']+pre_portfolio[0]['Competitors']+pre_portfolio[0]['Illustration Search ANZ']+pre_portfolio[0]['Illustration Search UK']+pre_portfolio[0]['Illustration Search USA']
        total_prv=prev_portfolio[0]['Animators UK']+prev_portfolio[0]['Animators USA']+prev_portfolio[0]['Competitors']+prev_portfolio[0]['Illustration Search ANZ']+prev_portfolio[0]['Illustration Search UK']+prev_portfolio[0]['Illustration Search USA']
        total_s=pre_portfolio[0]['Stock UK']+pre_portfolio[0]['Stock USA']
        total_prvs=prev_portfolio[0]['Stock UK']+prev_portfolio[0]['Stock USA']
        change = round((float(total) - float(total_prv)) / float(total_prv) * 100,1) if total_prv != 0 else 0
        change_s = round((float(total_s) - float(total_prvs)) / float(total_prvs) * 100,1) if total_prvs != 0 else 0
        return {'present':pre_portfolio,'previous':prev_portfolio,'total':total,'total_prv':total_prv,'total_s':total_s,'total_prvs':total_prvs,
                'change':change,'change_s':change_s}
class Googleads_cv:

    def __init__(self, current_results, previous_results):
        self.current_results = current_results
        self.previous_results = previous_results

    def main(self):
        pre_portfolio = self.current_results.googleads_cv()
        prev_portfolio = self.previous_results.googleads_cv()
        # print(pre_portfolio)
        # print(prev_portfolio)
        # total=pre_portfolio[0]['Animators UK']+pre_portfolio[0]['Animators USA']+pre_portfolio[0]['Competitors']+pre_portfolio[0]['Illustration Search ANZ']+pre_portfolio[0]['Illustration Search UK']+pre_portfolio[0]['Illustration Search USA']
        # total_prv=prev_portfolio[0]['Animators UK']+prev_portfolio[0]['Animators USA']+prev_portfolio[0]['Competitors']+prev_portfolio[0]['Illustration Search ANZ']+prev_portfolio[0]['Illustration Search UK']+prev_portfolio[0]['Illustration Search USA']
        # total_s=pre_portfolio[0]['Stock UK']+pre_portfolio[0]['Stock USA']
        # total_prvs=prev_portfolio[0]['Stock UK']+prev_portfolio[0]['Stock USA']
        # change = round((total - total_prv) / total_prv * 100, 1) if total_prv != 0 else 0
        # change_s = round((total_s - total_prvs) / total_prvs * 100, 1) if total_prvs != 0 else 0
        return {'present':pre_portfolio,'previous':prev_portfolio}

class Converted_keywords:
    def __init__(self, current_results, previous_results):
        self.current_results = current_results
        self.previous_results = previous_results

    def main(self):
        pre_keywords = self.current_results.converted_keywords()
        prev_keywords = self.previous_results.converted_keywords()

        pre_agent_pop_ups = self.current_results.agent_pop_ups()
        prev_agent_pop_ups = self.previous_results.agent_pop_ups()
        # print(pre_keywords)
        all_keys = set().union(*(d.keys() for d in pre_keywords))
        pre_keywords = [i.__str__() for i in all_keys]
        # print(prev_keywords)
        # print(pre_agent_pop_ups)
        # print(prev_agent_pop_ups)
        return {'pre_keywords':pre_keywords,'prev_keywords':prev_keywords,
                 'pre_agent_pop_ups':pre_agent_pop_ups,'prev_agent_pop_ups':prev_agent_pop_ups}