# -*- coding: utf-8 -*-
import os
import requests
import logging
from datetime import timedelta, datetime as day
from get_data import mainClass
from dateutil.relativedelta import relativedelta
from ResultServices.results import *
from utilities import (
    get_week,get_dates, get_dates_yest, get12months, change, get_two_month_dates, prev_month_last_year,  last_year, credentials_to_dict
)
from flask import Flask, render_template, redirect, session, url_for, jsonify, request
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import smtplib
from email.mime.text import MIMEText
# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"
# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
API_SERVICE_NAME = 'analytics'
API_VERSION = 'v3'
app = Flask(__name__)
app.jinja_env.filters['zip'] = zip
# Note: A secret key is included in the sample so that it works.
# If you use this code in your application, replace this with a truly secret
# key. See http://flask.pocoo.org/docs/0.12/quickstart/#sessions.
app.secret_key = 'sdvnkcklasdhuv.bfvlduvhldfbvbfkvmfnbv'

@app.route('/', methods=["GET", "POST"])
def index():
  if 'credentials' not in session:
    return redirect('authorize')

  credentials = google.oauth2.credentials.Credentials(
      **session['credentials'])

  service = googleapiclient.discovery.build(
      API_SERVICE_NAME, API_VERSION, credentials=credentials)
  try:
      dates = request.form.to_dict()
      # print(dates)
  except:
      dates = {}
  try:
      if dates == {} or dates['option'] == "Week":
          option = 'Last 7 Days'
          dates = get_dates_yest(7)
          print(dates)
          present = mainClass(dates[0]['pre_start'], dates[0]['pre_end'], service)
          previous = mainClass(dates[0]['prv_start'], dates[0]['prv_end'], service)
          sessions = SessionsCategoryResults(present, previous, 'date').main()
          topkeywords = Topkeywords(present, previous).main()
          agents = Agents(present, previous).main()
          sidebutton = SideButton(present, previous).main()
          portfolio = Portfolio(present, previous).main()
          events = Events(present, previous).main()
          devices = Devices(present, previous).main()
          conversions = Conversions(present, previous, 'month').main()
          traffic = WebsiteTrafficResults(present, previous, 'date').main()
          bouncerate = BounceRateResults(present, previous).main()
          avgduration = AvgSessionDuration(present, previous).main()
          result = {
              "sessions": sessions['totalSessions'],
              "session_category": sessions['sessions']['present'],
              'traffic': traffic,
              'conversions': conversions,
              # 'goalconversions': sessions['goalconversions'],
              'session_category_line_data': sessions['session_category_line_data'],
              # 'session_region_line_data': sessions['session_region_line_data'],
              'bouncerate': bouncerate,
              'avgduration': avgduration,
          }
          AllVisitors_pre = (result['session_category'][8].get('Organic Search', 0) +
                             result['session_category'][8].get('Direct', 0) +
                             result['session_category'][8].get('Referral', 0) +
                             result['session_category'][8].get('Social', 0) +
                             result['session_category'][8].get('Paid Search', 0) +
                             result['session_category'][8].get('Email', 0))
          AllVisitors_prev = (sessions['sessions']['present'][9].get('Organic Search', 0) +
                              sessions['sessions']['present'][9].get('Direct', 0) +
                              sessions['sessions']['present'][9].get('Referral', 0) +
                              sessions['sessions']['present'][9].get('Social', 0) +
                              sessions['sessions']['present'][9].get('Paid Search', 0) +
                              sessions['sessions']['present'][9].get('Email', 0))
          MobileTablet_pre = topkeywords['present'][0]['MobileTablet']

          Return_pre, Return_prev = [], []

          for item5, item6 in zip(result['traffic']['returningusers']['present'][0:30],
                                  result['traffic']['returningusers']['previous'][0:30]):
              Return_pre.append(item5['traffic'])
              Return_prev.append(item6['traffic'])
          visitors = {'visits': AllVisitors_pre, 'change_visits': round(
              ((float(AllVisitors_pre) - float(AllVisitors_prev)) / float(
                  AllVisitors_prev)) * 100, 2),
                      'MobileTablet_visits': MobileTablet_pre, 'change_MobileTablet_visits': round(
                  float(topkeywords['change']['mobiletablet_change'][0]), 2),
                      'Return_visits': sum(Return_pre), 'change_Return_visits': round(
                  ((float(sum(Return_pre)) - float(sum(Return_prev))) / float(sum(Return_prev))) * 100, 2)
                      }

          dates = {
              'pre_date': dates[1]['pre_start'] + ' to ' + dates[1]['pre_end'],
              'prev_date': dates[1]['prv_start'] + ' to ' + dates[1]['prv_end']
          }

          keys = (sessions['sessions']['present'][0].keys())
          keys = [x for x in keys if x != 'Country']
          Change = {
              i: change(source=i, result=sessions['sessions']) for i in keys
          }
          Change['Paid Search'][2], Change['Paid Search'][3], Change['Paid Search'][4], Change['Paid Search'][
              5] = 0, 0, 0, 0
          days = [((day.now() - timedelta(days=i)).strftime("%A")) for i in range(1, 8)]

          session['credentials'] = credentials_to_dict(credentials)

          return render_template('last_7_days.html', result=result, dates=dates, Change=Change, option=option,
                                 days=days, visitors=visitors, sessions=sessions, topkeywords=topkeywords,
                                 agents=agents,sidebutton=sidebutton, portfolio=portfolio, events=events, devices=devices)
      elif dates['option'] == "LastMonthPrevYear":
          option = 'Prev. Month of Past Year'
          dates = prev_month_last_year()
          present = mainClass(dates[0]['pre_start'], dates[0]['pre_end'], service)
          previous = mainClass(dates[0]['prv_start'], dates[0]['prv_end'], service)
          sessions = SessionsCategoryResults(present, previous, 'date').main()
          topkeywords = Topkeywords(present, previous).main()
          agents = Agents(present, previous).main()
          sidebutton = SideButton(present, previous).main()
          portfolio = Portfolio(present, previous).main()
          events = Events(present, previous).main()
          devices = Devices(present, previous).main()
          traffic = WebsiteTrafficResults(present, previous, 'date').main()
          conversions = Conversions(present, previous, 'month').main()
          bouncerate = BounceRateResults(present, previous).main()
          avgduration = AvgSessionDuration(present, previous).main()
          result = {
              "sessions": sessions['totalSessions'],
              "session_category": sessions['sessions']['present'],
              'traffic': traffic,
              'conversions': conversions,
              'goalconversions': sessions['goalconversions'],
              'session_category_line_data': sessions['session_category_line_data'],
              'session_region_line_data': sessions['session_region_line_data'],
              'bouncerate': bouncerate,
              'avgduration': avgduration,
          }
          AllVisitors_pre = (result['session_category'][8].get('Organic Search', 0) +
                             result['session_category'][8].get('Direct', 0) +
                             result['session_category'][8].get('Referral', 0) +
                             result['session_category'][8].get('Social', 0) +
                             result['session_category'][8].get('Paid Search', 0) +
                             result['session_category'][8].get('Email', 0))
          AllVisitors_prev = (sessions['sessions']['present'][9].get('Organic Search', 0) +
                              sessions['sessions']['present'][9].get('Direct', 0) +
                              sessions['sessions']['present'][9].get('Referral', 0) +
                              sessions['sessions']['present'][9].get('Social', 0) +
                              sessions['sessions']['present'][9].get('Paid Search', 0) +
                              sessions['sessions']['present'][9].get('Email', 0))
          MobileTablet_pre = topkeywords['present'][0]['MobileTablet']

          Return_pre, Return_prev = [], []

          for item5, item6 in zip(result['traffic']['returningusers']['present'][0:30],
                                  result['traffic']['returningusers']['previous'][0:30]):
              Return_pre.append(item5['traffic'])
              Return_prev.append(item6['traffic'])
          visitors = {'visits': AllVisitors_pre, 'change_visits': round(
              ((float(AllVisitors_pre) - float(AllVisitors_prev)) / float(
                  AllVisitors_prev)) * 100, 2),
                      'MobileTablet_visits': MobileTablet_pre, 'change_MobileTablet_visits': round(
                  float(topkeywords['change']['mobiletablet_change'][0]), 2),
                      'Return_visits': sum(Return_pre), 'change_Return_visits': round(
                  ((float(sum(Return_pre)) - float(sum(Return_prev))) / float(sum(Return_prev))) * 100, 2)
                      }

          dates = {
              'pre_date': dates[1]['pre_start'] + ' to ' + dates[1]['pre_end'],
              'prev_date': dates[1]['prv_start'] + ' to ' + dates[1]['prv_end']
          }
          keys = (sessions['sessions']['present'][0].keys())
          keys = [x for x in keys if x != 'Country']
          Change = {
              i: change(source=i, result=sessions['sessions']) for i in keys
          }
          Change['Paid Search'][2], Change['Paid Search'][3], Change['Paid Search'][4], Change['Paid Search'][
              5] = 0, 0, 0, 0
          session['credentials'] = credentials_to_dict(credentials)
          return render_template('last_month_prev_year.html', result=result, dates=dates, Change=Change,
                                 option=option, visitors=visitors,sessions=sessions,topkeywords=topkeywords,agents=agents,
                                 sidebutton=sidebutton,portfolio=portfolio,events=events,devices=devices)
      elif dates['option'] == "30":
          dates = get_dates(30)
          option = 'This Month (Last 4 Weeks)'
          present = mainClass(dates[0]['pre_start'], dates[0]['pre_end'], service)
          previous = mainClass(dates[0]['prv_start'], dates[0]['prv_end'], service)
          sessions = SessionsCategoryResults(present, previous, 'date').main()
          topkeywords = Topkeywords(present, previous).main()
          agents = Agents(present, previous).main()
          sidebutton = SideButton(present, previous).main()
          portfolio = Portfolio(present, previous).main()
          events = Events(present, previous).main()
          devices = Devices(present, previous).main()
          traffic = WebsiteTrafficResults(present, previous, 'date').main()
          conversions = Conversions(present, previous, 'month').main()
          bouncerate = BounceRateResults(present, previous).main()
          avgduration = AvgSessionDuration(present, previous).main()

          result = {
              "sessions": sessions['totalSessions'],
              "session_category": sessions['sessions']['present'],
              'traffic': traffic,
              'conversions': conversions,
              'goalconversions': sessions['goalconversions'],
              'session_category_line_data': sessions['session_category_line_data'],
              'session_region_line_data': sessions['session_region_line_data'],
              'bouncerate': bouncerate,
              'avgduration': avgduration,
          }
          AllVisitors_pre = (result['session_category'][8].get('Organic Search', 0) +
                             result['session_category'][8].get('Direct', 0) +
                             result['session_category'][8].get('Referral', 0) +
                             result['session_category'][8].get('Social', 0) +
                             result['session_category'][8].get('Paid Search', 0) +
                             result['session_category'][8].get('Email', 0))
          AllVisitors_prev = (sessions['sessions']['present'][9].get('Organic Search', 0) +
                              sessions['sessions']['present'][9].get('Direct', 0) +
                              sessions['sessions']['present'][9].get('Referral', 0) +
                              sessions['sessions']['present'][9].get('Social', 0) +
                              sessions['sessions']['present'][9].get('Paid Search', 0) +
                              sessions['sessions']['present'][9].get('Email', 0))
          MobileTablet_pre = topkeywords['present'][0]['MobileTablet']

          Return_pre, Return_prev = [], []

          for item5, item6 in zip(result['traffic']['returningusers']['present'][0:30],
                                  result['traffic']['returningusers']['previous'][0:30]):
              Return_pre.append(item5['traffic'])
              Return_prev.append(item6['traffic'])
          visitors = {'visits': AllVisitors_pre, 'change_visits': round(
              ((float(AllVisitors_pre) - float(AllVisitors_prev)) / float(
                  AllVisitors_prev)) * 100, 2),
                      'MobileTablet_visits': MobileTablet_pre, 'change_MobileTablet_visits': round(
                  float(topkeywords['change']['mobiletablet_change'][0]), 2),
                      'Return_visits': sum(Return_pre), 'change_Return_visits': round(
                  ((float(sum(Return_pre)) - float(sum(Return_prev))) / float(sum(Return_prev))) * 100, 2)
                      }

          dates = {
              'pre_date': dates[1]['pre_start'] + ' to ' + dates[1]['pre_end'],
              'prev_date': dates[1]['prv_start'] + ' to ' + dates[1]['prv_end']
          }

          keys = (sessions['sessions']['present'][0].keys())
          keys = [x for x in keys if x != 'Country']
          Change = {
              i: change(source=i, result=sessions['sessions']) for i in keys
          }
          Change['Paid Search'][2], Change['Paid Search'][3], Change['Paid Search'][4], Change['Paid Search'][
              5] = 0, 0, 0, 0
          session['credentials'] = credentials_to_dict(credentials)

          return render_template('last_30_days.html', result=result, dates=dates, Change=Change, option=option,
                                 visitors=visitors,sessions=sessions,topkeywords=topkeywords,agents=agents,
                                 sidebutton=sidebutton,portfolio=portfolio,events=events,devices=devices)
      elif dates['option'] == "LastMonth":
          dates = get_two_month_dates()
          # print(dates)
          option = 'Prev. Month'
          present = mainClass(dates[0]['pre_start'], dates[0]['pre_end'], service)
          previous = mainClass(dates[0]['prv_start'], dates[0]['prv_end'], service)
          sessions = SessionsCategoryResults(present, previous, 'date').main()
          topkeywords = Topkeywords(present, previous).main()
          agents = Agents(present, previous).main()
          sidebutton = SideButton(present, previous).main()
          portfolio = Portfolio(present, previous).main()
          events = Events(present, previous).main()
          devices = Devices(present, previous).main()
          traffic = WebsiteTrafficResults(present, previous, 'date').main()
          conversions = Conversions(present, previous, 'month').main()
          bouncerate = BounceRateResults(present, previous).main()
          avgduration = AvgSessionDuration(present, previous).main()

          result = {
              "sessions": sessions['totalSessions'],
              "session_category": sessions['sessions']['present'],
              'traffic': traffic,
              'conversions': conversions,
              'goalconversions': sessions['goalconversions'],
              'session_category_line_data': sessions['session_category_line_data'],
              'session_region_line_data': sessions['session_region_line_data'],
              'bouncerate': bouncerate,
              'avgduration': avgduration,
          }
          AllVisitors_pre = (result['session_category'][8].get('Organic Search', 0) +
                             result['session_category'][8].get('Direct', 0) +
                             result['session_category'][8].get('Referral', 0) +
                             result['session_category'][8].get('Social', 0) +
                             result['session_category'][8].get('Paid Search', 0) +
                             result['session_category'][8].get('Email', 0))
          AllVisitors_prev = (sessions['sessions']['present'][9].get('Organic Search', 0) +
                              sessions['sessions']['present'][9].get('Direct', 0) +
                              sessions['sessions']['present'][9].get('Referral', 0) +
                              sessions['sessions']['present'][9].get('Social', 0) +
                              sessions['sessions']['present'][9].get('Paid Search', 0) +
                              sessions['sessions']['present'][9].get('Email', 0))
          MobileTablet_pre = topkeywords['present'][0]['MobileTablet']

          Return_pre, Return_prev = [], []

          for item5, item6 in zip(result['traffic']['returningusers']['present'][0:30],
                                  result['traffic']['returningusers']['previous'][0:30]):
              Return_pre.append(item5['traffic'])
              Return_prev.append(item6['traffic'])
          visitors = {'visits': AllVisitors_pre, 'change_visits': round(
              ((float(AllVisitors_pre) - float(AllVisitors_prev)) / float(
                  AllVisitors_prev)) * 100, 2),
                      'MobileTablet_visits': MobileTablet_pre, 'change_MobileTablet_visits': round(
                  float(topkeywords['change']['mobiletablet_change'][0]), 2),
                      'Return_visits': sum(Return_pre), 'change_Return_visits': round(
                  ((float(sum(Return_pre)) - float(sum(Return_prev))) / float(sum(Return_prev))) * 100, 2)
                      }

          dates = {
              'pre_date': dates[1]['pre_start'] + ' to ' + dates[1]['pre_end'],
              'prev_date': dates[1]['prv_start'] + ' to ' + dates[1]['prv_end']
          }

          keys = (sessions['sessions']['present'][0].keys())
          keys = [x for x in keys if x != 'Country']
          Change = {
              i: change(source=i, result=sessions['sessions']) for i in keys
          }
          Change['Paid Search'][2], Change['Paid Search'][3], Change['Paid Search'][4], Change['Paid Search'][
              5] = 0, 0, 0, 0
          session['credentials'] = credentials_to_dict(credentials)

          return render_template('last_month.html', result=result, dates=dates, Change=Change, option=option,
                                 visitors=visitors,sessions=sessions,topkeywords=topkeywords,agents=agents,
                                 sidebutton=sidebutton,portfolio=portfolio,events=events,devices=devices)

      elif dates['option'] == "12":
          option = 'Last 12 Months'
          dates = get12months()
          present = mainClass(dates[0]['pre_start'], dates[0]['pre_end'], service)
          previous = mainClass(dates[0]['prv_start'], dates[0]['prv_end'], service)
          sessions = SessionsCategoryResults(present, previous, 'month').main()
          topkeywords = Topkeywords(present, previous).main()
          agents = Agents(present, previous).main()
          sidebutton = SideButton(present, previous).main()
          portfolio = Portfolio(present, previous).main()
          events = Events(present, previous).main()
          devices = Devices(present, previous).main()
          traffic = WebsiteTrafficResults(present, previous, 'month').main()
          conversions = Conversions(present, previous, 'month').main()
          bouncerate = BounceRateResults(present, previous).main()
          avgduration = AvgSessionDuration(present, previous).main()

          result = {
              "sessions": sessions['totalSessions'],
              "session_category": sessions['sessions']['present'],
              'traffic': traffic,
              'conversions': conversions,
              'goalconversions': sessions['goalconversions'],
              'session_category_line_data': sessions['session_category_line_data'],
              'session_region_line_data': sessions['session_region_line_data'],
              'bouncerate': bouncerate,
              'avgduration': avgduration,
          }

          AllVisitors_pre = (result['session_category'][8].get('Organic Search', 0) +
                             result['session_category'][8].get('Direct', 0) +
                             result['session_category'][8].get('Referral', 0) +
                             result['session_category'][8].get('Social', 0) +
                             result['session_category'][8].get('Paid Search', 0) +
                             result['session_category'][8].get('Email', 0))
          AllVisitors_prev = (sessions['sessions']['present'][9].get('Organic Search', 0) +
                              sessions['sessions']['present'][9].get('Direct', 0) +
                              sessions['sessions']['present'][9].get('Referral', 0) +
                              sessions['sessions']['present'][9].get('Social', 0) +
                              sessions['sessions']['present'][9].get('Paid Search', 0) +
                              sessions['sessions']['present'][9].get('Email', 0))
          MobileTablet_pre = topkeywords['present'][0]['MobileTablet']

          Return_pre, Return_prev = [], []

          for item5, item6 in zip(result['traffic']['returningusers']['present'][0:30],
                                  result['traffic']['returningusers']['previous'][0:30]):
              Return_pre.append(item5['traffic'])
              Return_prev.append(item6['traffic'])
          visitors = {'visits': AllVisitors_pre, 'change_visits': round(
              ((float(AllVisitors_pre) - float(AllVisitors_prev)) / float(
                  AllVisitors_prev)) * 100, 2),
                      'MobileTablet_visits': MobileTablet_pre, 'change_MobileTablet_visits': round(
                  float(topkeywords['change']['mobiletablet_change'][0]), 2),
                      'Return_visits': sum(Return_pre), 'change_Return_visits': round(
                  ((float(sum(Return_pre)) - float(sum(Return_prev))) / float(sum(Return_prev))) * 100, 2)
                      }

          dates = {
              'pre_date': dates[1]['pre_start'] + ' to ' + dates[1]['pre_end'],
              'prev_date': dates[1]['prv_start'] + ' to ' + dates[1]['prv_end']
          }

          keys = (sessions['sessions']['present'][0].keys())
          keys = [x for x in keys if x != 'Country']
          Change = {
              i: change(source=i, result=sessions['sessions']) for i in keys
          }
          Change['Paid Search'][2], Change['Paid Search'][3], Change['Paid Search'][4], Change['Paid Search'][
              5] = 0, 0, 0, 0
          months = [(day.today() - relativedelta(months=i)).strftime("%b") for i in range(1, 13)]
          month_num = [(day.today() - relativedelta(months=i)).month for i in range(1, 13)]
          month_num = month_num[::-1]
          session['credentials'] = credentials_to_dict(credentials)

          return render_template('last_12_months.html', result=result, dates=dates, Change=Change, option=option,
                                 months=months,month_num=month_num, visitors=visitors,sessions=sessions,topkeywords=topkeywords,agents=agents,
                                 sidebutton=sidebutton,portfolio=portfolio,events=events,devices=devices)

      elif dates['option'] == "LastYear":
          option = 'Last Year'
          dates = last_year()
          present = mainClass(dates[0]['pre_start'], dates[0]['pre_end'], service)
          previous = mainClass(dates[0]['prv_start'], dates[0]['prv_end'], service)
          sessions = SessionsCategoryResults(present, previous, 'month').main()
          topkeywords = Topkeywords(present, previous).main()
          agents = Agents(present, previous).main()
          sidebutton = SideButton(present, previous).main()
          portfolio = Portfolio(present, previous).main()
          events = Events(present, previous).main()
          devices = Devices(present, previous).main()
          traffic = WebsiteTrafficResults(present, previous, 'month').main()
          conversions = Conversions(present, previous, 'year  ').main()
          bouncerate = BounceRateResults(present, previous).main()
          avgduration = AvgSessionDuration(present, previous).main()

          result = {
              "sessions": sessions['totalSessions'],
              "session_category": sessions['sessions']['present'],
              'traffic': traffic,
              'conversions': conversions,
              'goalconversions': sessions['goalconversions'],
              'session_category_line_data': sessions['session_category_line_data'],
              'session_region_line_data': sessions['session_region_line_data'],
              'bouncerate': bouncerate,
              'avgduration': avgduration,
          }
          AllVisitors_pre = (result['session_category'][8].get('Organic Search', 0) +
                             result['session_category'][8].get('Direct', 0) +
                             result['session_category'][8].get('Referral', 0) +
                             result['session_category'][8].get('Social', 0) +
                             result['session_category'][8].get('Paid Search', 0) +
                             result['session_category'][8].get('Email', 0))
          AllVisitors_prev = (sessions['sessions']['present'][9].get('Organic Search', 0) +
                              sessions['sessions']['present'][9].get('Direct', 0) +
                              sessions['sessions']['present'][9].get('Referral', 0) +
                              sessions['sessions']['present'][9].get('Social', 0) +
                              sessions['sessions']['present'][9].get('Paid Search', 0) +
                              sessions['sessions']['present'][9].get('Email', 0))
          MobileTablet_pre = topkeywords['present'][0]['MobileTablet']

          Return_pre, Return_prev = [], []

          for item5, item6 in zip(result['traffic']['returningusers']['present'][0:30],
                                  result['traffic']['returningusers']['previous'][0:30]):
              Return_pre.append(item5['traffic'])
              Return_prev.append(item6['traffic'])
          visitors = {'visits': AllVisitors_pre, 'change_visits': round(
              ((float(AllVisitors_pre) - float(AllVisitors_prev)) / float(
                  AllVisitors_prev)) * 100, 2),
                      'MobileTablet_visits': MobileTablet_pre, 'change_MobileTablet_visits': round(
                  float(topkeywords['change']['mobiletablet_change'][0]), 2),
                      'Return_visits': sum(Return_pre), 'change_Return_visits': round(
                  ((float(sum(Return_pre)) - float(sum(Return_prev))) / float(sum(Return_prev))) * 100, 2)
                      }

          dates = {
              'pre_date': dates[1]['pre_start'] + ' to ' + dates[1]['pre_end'],
              'prev_date': dates[1]['prv_start'] + ' to ' + dates[1]['prv_end']
          }

          keys = (sessions['sessions']['present'][0].keys())
          keys = [x for x in keys if x != 'Country']
          Change = {
              i: change(source=i, result=sessions['sessions']) for i in keys
          }
          Change['Paid Search'][2], Change['Paid Search'][3], Change['Paid Search'][4], Change['Paid Search'][
              5] = 0, 0, 0, 0
          session['credentials'] = credentials_to_dict(credentials)

          return render_template('last_year.html', result=result, dates=dates, Change=Change, option=option,
                                 visitors=visitors,sessions=sessions,topkeywords=topkeywords,agents=agents,
                                 sidebutton=sidebutton,portfolio=portfolio,events=events,devices=devices)
      elif dates['option'] == "7":
          option = 'Last week'
          dates = get_week()
          # print(dates)
          present = mainClass(dates[0]['pre_start'], dates[0]['pre_end'], service)
          previous = mainClass(dates[0]['prv_start'], dates[0]['prv_end'], service)
          sessions = SessionsCategoryResults(present, previous, 'date').main()
          topkeywords = Topkeywords(present, previous).main()
          agents = Agents(present, previous).main()
          sidebutton = SideButton(present, previous).main()
          portfolio = Portfolio(present, previous).main()
          events = Events(present, previous).main()
          devices = Devices(present, previous).main()
          conversions = Conversions(present, previous, 'month').main()
          traffic = WebsiteTrafficResults(present, previous, 'date').main()
          bouncerate = BounceRateResults(present, previous).main()
          avgduration = AvgSessionDuration(present, previous).main()
          result = {
              "sessions": sessions['totalSessions'],
              "session_category": sessions['sessions']['present'],
              'traffic': traffic,
              'conversions': conversions,
              'goalconversions': sessions['goalconversions'],
              'session_category_line_data': sessions['session_category_line_data'],
              'session_region_line_data': sessions['session_region_line_data'],
              'bouncerate': bouncerate,
              'avgduration': avgduration,
          }
          AllVisitors_pre = (result['session_category'][8].get('Organic Search', 0) +
                             result['session_category'][8].get('Direct', 0) +
                             result['session_category'][8].get('Referral', 0) +
                             result['session_category'][8].get('Social', 0) +
                             result['session_category'][8].get('Paid Search', 0) +
                             result['session_category'][8].get('Email', 0))
          AllVisitors_prev = (sessions['sessions']['present'][9].get('Organic Search', 0) +
                              sessions['sessions']['present'][9].get('Direct', 0) +
                              sessions['sessions']['present'][9].get('Referral', 0) +
                              sessions['sessions']['present'][9].get('Social', 0) +
                              sessions['sessions']['present'][9].get('Paid Search', 0) +
                              sessions['sessions']['present'][9].get('Email', 0))
          MobileTablet_pre = topkeywords['present'][0]['MobileTablet']

          Return_pre, Return_prev = [], []

          for item5, item6 in zip(result['traffic']['returningusers']['present'][0:30],
                                  result['traffic']['returningusers']['previous'][0:30]):
              Return_pre.append(item5['traffic'])
              Return_prev.append(item6['traffic'])
          visitors = {'visits': AllVisitors_pre, 'change_visits': round(
              ((float(AllVisitors_pre) - float(AllVisitors_prev)) / float(
                  AllVisitors_prev)) * 100, 2),
                      'MobileTablet_visits': MobileTablet_pre, 'change_MobileTablet_visits': round(
                  float(topkeywords['change']['mobiletablet_change'][0]), 2),
                      'Return_visits': sum(Return_pre), 'change_Return_visits': round(
                  ((float(sum(Return_pre)) - float(sum(Return_prev))) / float(sum(Return_prev))) * 100, 2)
                      }

          dates = {
              'pre_date': dates[1]['pre_start'] + ' to ' + dates[1]['pre_end'],
              'prev_date': dates[1]['prv_start'] + ' to ' + dates[1]['prv_end']
          }

          keys = (sessions['sessions']['present'][0].keys())
          keys = [x for x in keys if x != 'Country']
          Change = {
              i: change(source=i, result=sessions['sessions']) for i in keys
          }
          Change['Paid Search'][2], Change['Paid Search'][3], Change['Paid Search'][4], Change['Paid Search'][
              5] = 0, 0, 0, 0
          days = [((day.now() - timedelta(days=i)).strftime("%A")) for i in range(1, 8)]

          session['credentials'] = credentials_to_dict(credentials)

          return render_template('last_week.html', result=result, dates=dates, Change=Change, option=option,
                                 days=days, visitors=visitors, sessions=sessions, topkeywords=topkeywords,
                                 agents=agents,
                                 sidebutton=sidebutton, portfolio=portfolio, events=events, devices=devices,
                                 )


  except Exception as e:
      print(e)
      # if e == 'The credentials do not contain the necessary fields need to refresh the access token. You must specify refresh_token, token_uri, client_id, and client_secret.':
      return redirect('authorize')
      # else:
      #     return render_template("page_500.html")


@app.route("/metrics" , methods=["GET", "POST"])
def metrics():
    if 'credentials' not in session:
        return redirect('authorize')

    credentials = google.oauth2.credentials.Credentials(
        **session['credentials'])

    service = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)
    try:
        dates = request.form.to_dict()
    except:
        dates = {}
    try:
        if dates == {} or dates['option'] == "Week":
            option = 'Last 7 Days'
            dates = get_dates_yest(7)
            # print(dates)
            present = mainClass(dates[0]['pre_start'], dates[0]['pre_end'], service)
            previous = mainClass(dates[0]['prv_start'], dates[0]['prv_end'], service)
            sessions = SessionsCategoryResults(present, previous, 'date').main()
            topkeywords = Topkeywords(present, previous).main()
            agents = Agents(present, previous).main()
            sidebutton = SideButton(present, previous).main()
            portfolio = Portfolio(present, previous).main()
            events = Events(present, previous).main()
            devices = Devices(present, previous).main()


            dates = {
                'pre_date': dates[1]['pre_start'] + ' to ' + dates[1]['pre_end'],
                'prev_date': dates[1]['prv_start'] + ' to ' + dates[1]['prv_end']
            }


            days = [((day.now() - timedelta(days=i)).strftime("%A")) for i in range(1, 8)]

            session['credentials'] = credentials_to_dict(credentials)

            return render_template('tables.html', dates=dates, option=option,
                                   days=days, sessions=sessions, topkeywords=topkeywords,
                                   agents=agents, sidebutton=sidebutton, portfolio=portfolio, events=events,
                                   devices=devices
                                   )
        elif dates['option'] == "LastMonthPrevYear":
            option = 'Prev. Month of Past Year'
            dates = prev_month_last_year()
            present = mainClass(dates[0]['pre_start'], dates[0]['pre_end'], service)
            previous = mainClass(dates[0]['prv_start'], dates[0]['prv_end'], service)
            sessions = SessionsCategoryResults(present, previous, 'date').main()
            topkeywords = Topkeywords(present, previous).main()
            agents = Agents(present, previous).main()
            sidebutton = SideButton(present, previous).main()
            portfolio = Portfolio(present, previous).main()
            events = Events(present, previous).main()
            devices = Devices(present, previous).main()

            dates = {
                'pre_date': dates[1]['pre_start'] + ' to ' + dates[1]['pre_end'],
                'prev_date': dates[1]['prv_start'] + ' to ' + dates[1]['prv_end']
            }

            session['credentials'] = credentials_to_dict(credentials)
            return render_template('tables.html', dates=dates,
                                   option=option, sessions=sessions, topkeywords=topkeywords,
                                   agents=agents,
                                   sidebutton=sidebutton, portfolio=portfolio, events=events, devices=devices,
                                   )
        elif dates['option'] == "30":
            dates = get_dates(30)
            option = 'This Month (Last 4 Weeks)'
            present = mainClass(dates[0]['pre_start'], dates[0]['pre_end'], service)
            previous = mainClass(dates[0]['prv_start'], dates[0]['prv_end'], service)
            sessions = SessionsCategoryResults(present, previous, 'date').main()
            topkeywords = Topkeywords(present, previous).main()
            agents = Agents(present, previous).main()
            sidebutton = SideButton(present, previous).main()
            portfolio = Portfolio(present, previous).main()
            events = Events(present, previous).main()
            devices = Devices(present, previous).main()

            dates = {
                'pre_date': dates[1]['pre_start'] + ' to ' + dates[1]['pre_end'],
                'prev_date': dates[1]['prv_start'] + ' to ' + dates[1]['prv_end']
            }


            session['credentials'] = credentials_to_dict(credentials)

            return render_template('tables.html', dates=dates, option=option, sessions=sessions, topkeywords=topkeywords, agents=agents,
                                   sidebutton=sidebutton, portfolio=portfolio, events=events, devices=devices,
                                   )
        elif dates['option'] == "LastMonth":
            dates = get_two_month_dates()
            # print(dates)
            option = 'Prev. Month'
            present = mainClass(dates[0]['pre_start'], dates[0]['pre_end'], service)
            previous = mainClass(dates[0]['prv_start'], dates[0]['prv_end'], service)
            sessions = SessionsCategoryResults(present, previous, 'date').main()
            topkeywords = Topkeywords(present, previous).main()
            agents = Agents(present, previous).main()
            sidebutton = SideButton(present, previous).main()
            portfolio = Portfolio(present, previous).main()
            events = Events(present, previous).main()
            devices = Devices(present, previous).main()

            dates = {
                'pre_date': dates[1]['pre_start'] + ' to ' + dates[1]['pre_end'],
                'prev_date': dates[1]['prv_start'] + ' to ' + dates[1]['prv_end']
            }

            session['credentials'] = credentials_to_dict(credentials)

            return render_template('tables.html', dates=dates, option=option,
                                   sessions=sessions, topkeywords=topkeywords, agents=agents,
                                   sidebutton=sidebutton, portfolio=portfolio, events=events, devices=devices,
                                   )

        elif dates['option'] == "12":
            option = 'Last 12 Months'
            dates = get12months()
            present = mainClass(dates[0]['pre_start'], dates[0]['pre_end'], service)
            previous = mainClass(dates[0]['prv_start'], dates[0]['prv_end'], service)
            sessions = SessionsCategoryResults(present, previous, 'month').main()
            topkeywords = Topkeywords(present, previous).main()
            agents = Agents(present, previous).main()
            sidebutton = SideButton(present, previous).main()
            portfolio = Portfolio(present, previous).main()
            events = Events(present, previous).main()
            devices = Devices(present, previous).main()

            dates = {
                'pre_date': dates[1]['pre_start'] + ' to ' + dates[1]['pre_end'],
                'prev_date': dates[1]['prv_start'] + ' to ' + dates[1]['prv_end']
            }

            session['credentials'] = credentials_to_dict(credentials)

            return render_template('tables.html', dates=dates, option=option,
                                   sessions=sessions, topkeywords=topkeywords,
                                   agents=agents,
                                   sidebutton=sidebutton, portfolio=portfolio, events=events, devices=devices,
                                   )

        elif dates['option'] == "LastYear":
            option = 'Last Year'
            dates = last_year()
            present = mainClass(dates[0]['pre_start'], dates[0]['pre_end'], service)
            previous = mainClass(dates[0]['prv_start'], dates[0]['prv_end'], service)
            sessions = SessionsCategoryResults(present, previous, 'month').main()
            topkeywords = Topkeywords(present, previous).main()
            agents = Agents(present, previous).main()
            sidebutton = SideButton(present, previous).main()
            portfolio = Portfolio(present, previous).main()
            events = Events(present, previous).main()
            devices = Devices(present, previous).main()

            dates = {
                'pre_date': dates[1]['pre_start'] + ' to ' + dates[1]['pre_end'],
                'prev_date': dates[1]['prv_start'] + ' to ' + dates[1]['prv_end']
            }


            session['credentials'] = credentials_to_dict(credentials)

            return render_template('tables.html', dates=dates,option=option,
                                   sessions=sessions, topkeywords=topkeywords, agents=agents,
                                   sidebutton=sidebutton, portfolio=portfolio, events=events, devices=devices,
                                   )
        elif dates['option'] == "7":
            option = 'Last week'
            dates = get_week()
            # print(dates)
            present = mainClass(dates[0]['pre_start'], dates[0]['pre_end'], service)
            previous = mainClass(dates[0]['prv_start'], dates[0]['prv_end'], service)
            sessions = SessionsCategoryResults(present, previous, 'date').main()
            topkeywords = Topkeywords(present, previous).main()
            agents = Agents(present, previous).main()
            sidebutton = SideButton(present, previous).main()
            portfolio = Portfolio(present, previous).main()
            events = Events(present, previous).main()
            devices = Devices(present, previous).main()

            dates = {
                'pre_date': dates[1]['pre_start'] + ' to ' + dates[1]['pre_end'],
                'prev_date': dates[1]['prv_start'] + ' to ' + dates[1]['prv_end']
            }

            days = [((day.now() - timedelta(days=i)).strftime("%A")) for i in range(1, 8)]

            session['credentials'] = credentials_to_dict(credentials)

            return render_template('tables.html',dates=dates,option=option,
                                   days=days, sessions=sessions, topkeywords=topkeywords,
                                   agents=agents,
                                   sidebutton=sidebutton, portfolio=portfolio, events=events, devices=devices,
                                   )


    except Exception as e:
        print(e)
        # if e == 'The credentials do not contain the necessary fields need to refresh the access token. You must specify refresh_token, token_uri, client_id, and client_secret.':
        return redirect('authorize')
        # else:
        #     return render_template("page_500.html")

@app.route("/ads" , methods=["GET", "POST"])
def ads():
    if 'credentials' not in session:
        return redirect('authorize')
    credentials = google.oauth2.credentials.Credentials(
        **session['credentials'])

    service = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)
    try:
        dates = request.form.to_dict()
    except:
        dates = {}
    try:
        if dates == {} or dates['option'] == "Week":
            option = 'Last 7 Days'
            dates = get_dates_yest(7)
            print(dates)
            present = mainClass(dates[0]['pre_start'], dates[0]['pre_end'], service)
            previous = mainClass(dates[0]['prv_start'], dates[0]['prv_end'], service)
            googleads = Googleads(present, previous).main()
            googleads_cost = Googleads_cost(present, previous).main()
            googleads_ctr = Googleads_ctr(present, previous).main()
            googleads_imp = Googleads_imp(present, previous).main()
            googleads_en = Googleads_en(present, previous).main()
            googleads_cv = Googleads_cv(present, previous).main()

            total=googleads_cost['total'] / googleads_en['total'] if googleads_en['total'] else 0
            total_prv =googleads_cost['total_prv']/googleads_en['total_prv'] if googleads_en['total_prv'] else 0
            total_s = googleads_cost['total_s'] / googleads_en['total_s'] if googleads_en['total_s'] else 0
            total_prvs = googleads_cost['total_prvs'] / googleads_en['total_prvs'] if googleads_en['total_prvs'] else 0
            cv = {'total':total,'total_prv': total_prv,
                  'change':((float(total)-float(total_prv))/float(total_prv))*100 if total_prv!=0 else 0,
                  'total_s': total_s, 'total_prvs': total_prvs,
                  'change_s': ((float(total_s) - float(total_prvs)) / float(total_prvs)) * 100 if total_prvs != 0 else 0
                  }

            dates = {
                'pre_date': dates[1]['pre_start'] + ' to ' + dates[1]['pre_end'],
                'prev_date': dates[1]['prv_start'] + ' to ' + dates[1]['prv_end']
            }


            return render_template('ads_tables.html',dates=dates,option=option, googleads=googleads,
                                   googleads_cost=googleads_cost, googleads_ctr=googleads_ctr,
                                   googleads_imp=googleads_imp,cv=cv,
                                   googleads_en=googleads_en, googleads_cv=googleads_cv)
        elif dates['option'] == "LastMonthPrevYear":
            option = 'Prev. Month of Past Year'
            dates = prev_month_last_year()
            present = mainClass(dates[0]['pre_start'], dates[0]['pre_end'], service)
            previous = mainClass(dates[0]['prv_start'], dates[0]['prv_end'], service)
            googleads = Googleads(present, previous).main()
            googleads_cost = Googleads_cost(present, previous).main()
            googleads_ctr = Googleads_ctr(present, previous).main()
            googleads_imp = Googleads_imp(present, previous).main()
            googleads_en = Googleads_en(present, previous).main()
            googleads_cv = Googleads_cv(present, previous).main()
            total = googleads_cost['total'] / googleads_en['total'] if googleads_en['total'] else 0
            total_prv = googleads_cost['total_prv'] / googleads_en['total_prv'] if googleads_en['total_prv'] else 0
            total_s = googleads_cost['total_s'] / googleads_en['total_s'] if googleads_en['total_s'] else 0
            total_prvs = googleads_cost['total_prvs'] / googleads_en['total_prvs'] if googleads_en['total_prvs'] else 0
            cv = {'total': total, 'total_prv': total_prv,
                  'change': ((float(total) - float(total_prv)) / float(total_prv)) * 100 if total_prv != 0 else 0,
                  'total_s': total_s, 'total_prvs': total_prvs,
                  'change_s': ((float(total_s) - float(total_prvs)) / float(total_prvs)) * 100 if total_prvs != 0 else 0
                  }

            dates = {
                'pre_date': dates[1]['pre_start'] + ' to ' + dates[1]['pre_end'],
                'prev_date': dates[1]['prv_start'] + ' to ' + dates[1]['prv_end']
            }

            return render_template('ads_tables.html',dates=dates,option=option,
                                   googleads=googleads,
                                   googleads_cost=googleads_cost, googleads_ctr=googleads_ctr,
                                   googleads_imp=googleads_imp,cv=cv,
                                   googleads_en=googleads_en, googleads_cv=googleads_cv)
        elif dates['option'] == "30":
            dates = get_dates(30)
            option = 'This Month (Last 4 Weeks)'
            present = mainClass(dates[0]['pre_start'], dates[0]['pre_end'], service)
            previous = mainClass(dates[0]['prv_start'], dates[0]['prv_end'], service)
            googleads = Googleads(present, previous).main()
            googleads_cost = Googleads_cost(present, previous).main()
            googleads_ctr = Googleads_ctr(present, previous).main()
            googleads_imp = Googleads_imp(present, previous).main()
            googleads_en = Googleads_en(present, previous).main()
            googleads_cv = Googleads_cv(present, previous).main()
            total = googleads_cost['total'] / googleads_en['total'] if googleads_en['total'] else 0
            total_prv = googleads_cost['total_prv'] / googleads_en['total_prv'] if googleads_en['total_prv'] else 0
            total_s = googleads_cost['total_s'] / googleads_en['total_s'] if googleads_en['total_s'] else 0
            total_prvs = googleads_cost['total_prvs'] / googleads_en['total_prvs'] if googleads_en['total_prvs'] else 0
            cv = {'total': total, 'total_prv': total_prv,
                  'change': ((float(total) - float(total_prv)) / float(total_prv)) * 100 if total_prv != 0 else 0,
                  'total_s': total_s, 'total_prvs': total_prvs,
                  'change_s': ((float(total_s) - float(total_prvs)) / float(total_prvs)) * 100 if total_prvs != 0 else 0
                  }

            dates = {
                'pre_date': dates[1]['pre_start'] + ' to ' + dates[1]['pre_end'],
                'prev_date': dates[1]['prv_start'] + ' to ' + dates[1]['prv_end']
            }


            return render_template('ads_tables.html',dates=dates,option=option,
                                   googleads=googleads,
                                   googleads_cost=googleads_cost, googleads_ctr=googleads_ctr,
                                   googleads_imp=googleads_imp,cv=cv,
                                   googleads_en=googleads_en, googleads_cv=googleads_cv)
        elif dates['option'] == "LastMonth":
            dates = get_two_month_dates()
            # print(dates)
            option = 'Prev. Month'
            present = mainClass(dates[0]['pre_start'], dates[0]['pre_end'], service)
            previous = mainClass(dates[0]['prv_start'], dates[0]['prv_end'], service)
            googleads = Googleads(present, previous).main()
            googleads_cost = Googleads_cost(present, previous).main()
            googleads_ctr = Googleads_ctr(present, previous).main()
            googleads_imp = Googleads_imp(present, previous).main()
            googleads_en = Googleads_en(present, previous).main()
            googleads_cv = Googleads_cv(present, previous).main()
            total = googleads_cost['total'] / googleads_en['total'] if googleads_en['total'] else 0
            total_prv = googleads_cost['total_prv'] / googleads_en['total_prv'] if googleads_en['total_prv'] else 0
            total_s = googleads_cost['total_s'] / googleads_en['total_s'] if googleads_en['total_s'] else 0
            total_prvs = googleads_cost['total_prvs'] / googleads_en['total_prvs'] if googleads_en['total_prvs'] else 0
            cv = {'total': total, 'total_prv': total_prv,
                  'change': ((float(total) - float(total_prv)) / float(total_prv)) * 100 if total_prv != 0 else 0,
                  'total_s': total_s, 'total_prvs': total_prvs,
                  'change_s': ((float(total_s) - float(total_prvs)) / float(total_prvs)) * 100 if total_prvs != 0 else 0
                  }

            dates = {
                'pre_date': dates[1]['pre_start'] + ' to ' + dates[1]['pre_end'],
                'prev_date': dates[1]['prv_start'] + ' to ' + dates[1]['prv_end']
            }


            return render_template('ads_tables.html',dates=dates,option=option,
                                   googleads=googleads,
                                   googleads_cost=googleads_cost, googleads_ctr=googleads_ctr,
                                   googleads_imp=googleads_imp,cv=cv,
                                   googleads_en=googleads_en, googleads_cv=googleads_cv)

        elif dates['option'] == "12":
            option = 'Last 12 Months'
            dates = get12months()
            present = mainClass(dates[0]['pre_start'], dates[0]['pre_end'], service)
            previous = mainClass(dates[0]['prv_start'], dates[0]['prv_end'], service)
            googleads = Googleads(present, previous).main()
            googleads_cost = Googleads_cost(present, previous).main()
            googleads_ctr = Googleads_ctr(present, previous).main()
            googleads_imp = Googleads_imp(present, previous).main()
            googleads_en = Googleads_en(present, previous).main()
            googleads_cv = Googleads_cv(present, previous).main()
            total = googleads_cost['total'] / googleads_en['total'] if googleads_en['total'] else 0
            total_prv = googleads_cost['total_prv'] / googleads_en['total_prv'] if googleads_en['total_prv'] else 0
            total_s = googleads_cost['total_s'] / googleads_en['total_s'] if googleads_en['total_s'] else 0
            total_prvs = googleads_cost['total_prvs'] / googleads_en['total_prvs'] if googleads_en['total_prvs'] else 0
            cv = {'total': total, 'total_prv': total_prv,
                  'change': ((float(total) - float(total_prv)) / float(total_prv)) * 100 if total_prv != 0 else 0,
                  'total_s': total_s, 'total_prvs': total_prvs,
                  'change_s': ((float(total_s) - float(total_prvs)) / float(total_prvs)) * 100 if total_prvs != 0 else 0
                  }

            dates = {
                'pre_date': dates[1]['pre_start'] + ' to ' + dates[1]['pre_end'],
                'prev_date': dates[1]['prv_start'] + ' to ' + dates[1]['prv_end']
            }


            return render_template('ads_tables.html',dates=dates,option=option,
                                   googleads=googleads,
                                   googleads_cost=googleads_cost, googleads_ctr=googleads_ctr,
                                   googleads_imp=googleads_imp,cv=cv,
                                   googleads_en=googleads_en, googleads_cv=googleads_cv)

        elif dates['option'] == "LastYear":
            option = 'Last Year'
            dates = last_year()
            present = mainClass(dates[0]['pre_start'], dates[0]['pre_end'], service)
            previous = mainClass(dates[0]['prv_start'], dates[0]['prv_end'], service)
            googleads = Googleads(present, previous).main()
            googleads_cost = Googleads_cost(present, previous).main()
            googleads_ctr = Googleads_ctr(present, previous).main()
            googleads_imp = Googleads_imp(present, previous).main()
            googleads_en = Googleads_en(present, previous).main()
            googleads_cv = Googleads_cv(present, previous).main()
            total = googleads_cost['total'] / googleads_en['total'] if googleads_en['total'] else 0
            total_prv = googleads_cost['total_prv'] / googleads_en['total_prv'] if googleads_en['total_prv'] else 0
            total_s = googleads_cost['total_s'] / googleads_en['total_s'] if googleads_en['total_s'] else 0
            total_prvs = googleads_cost['total_prvs'] / googleads_en['total_prvs'] if googleads_en['total_prvs'] else 0
            cv = {'total': total, 'total_prv': total_prv,
                  'change': ((float(total) - float(total_prv)) / float(total_prv)) * 100 if total_prv != 0 else 0,
                  'total_s': total_s, 'total_prvs': total_prvs,
                  'change_s': ((float(total_s) - float(total_prvs)) / float(total_prvs)) * 100 if total_prvs != 0 else 0
                  }

            dates = {
                'pre_date': dates[1]['pre_start'] + ' to ' + dates[1]['pre_end'],
                'prev_date': dates[1]['prv_start'] + ' to ' + dates[1]['prv_end']
            }

            return render_template('ads_tables.html',dates=dates,option=option,
                                   googleads=googleads,
                                   googleads_cost=googleads_cost, googleads_ctr=googleads_ctr,
                                   googleads_imp=googleads_imp,cv=cv,
                                   googleads_en=googleads_en, googleads_cv=googleads_cv)
        elif dates['option'] == "7":
            option = 'Last week'
            dates = get_week()
            # print(dates)
            present = mainClass(dates[0]['pre_start'], dates[0]['pre_end'], service)
            previous = mainClass(dates[0]['prv_start'], dates[0]['prv_end'], service)
            googleads = Googleads(present, previous).main()
            googleads_cost = Googleads_cost(present, previous).main()
            googleads_ctr = Googleads_ctr(present, previous).main()
            googleads_imp = Googleads_imp(present, previous).main()
            googleads_en = Googleads_en(present, previous).main()
            googleads_cv = Googleads_cv(present, previous).main()
            total = googleads_cost['total'] / googleads_en['total'] if googleads_en['total'] else 0
            total_prv = googleads_cost['total_prv'] / googleads_en['total_prv'] if googleads_en['total_prv'] else 0
            total_s = googleads_cost['total_s'] / googleads_en['total_s'] if googleads_en['total_s'] else 0
            total_prvs = googleads_cost['total_prvs'] / googleads_en['total_prvs'] if googleads_en['total_prvs'] else 0
            cv = {'total': total, 'total_prv': total_prv,
                  'change': ((float(total) - float(total_prv)) / float(total_prv)) * 100 if total_prv != 0 else 0,
                  'total_s': total_s, 'total_prvs': total_prvs,
                  'change_s': ((float(total_s) - float(total_prvs)) / float(total_prvs)) * 100 if total_prvs != 0 else 0
                  }

            dates = {
                'pre_date': dates[1]['pre_start'] + ' to ' + dates[1]['pre_end'],
                'prev_date': dates[1]['prv_start'] + ' to ' + dates[1]['prv_end']
            }


            return render_template('ads_tables.html',dates=dates,option=option,
                                   googleads=googleads,
                                   googleads_cost=googleads_cost, googleads_ctr=googleads_ctr,
                                   googleads_imp=googleads_imp,cv=cv,
                                   googleads_en=googleads_en, googleads_cv=googleads_cv)


    except Exception as e:
        print(e)
        # if e == 'The credentials do not contain the necessary fields need to refresh the access token. You must specify refresh_token, token_uri, client_id, and client_secret.':
        return redirect('authorize')
        # else:
        #     return render_template("page_500.html")
@app.route("/report" , methods=["GET", "POST"])
def report():
    if 'credentials' not in session:
        return redirect('authorize')
    credentials = google.oauth2.credentials.Credentials(
        **session['credentials'])

    service = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)
    try:
        dates = request.form.to_dict()
    except:
        dates = {}
    try:
        if dates == {} or dates['option'] == "7":
            option = 'Last week'
            dates = get_week()
            print(dates)
            present = mainClass(dates[0]['pre_start'], dates[0]['pre_end'], service)
            previous = mainClass(dates[0]['prv_start'], dates[0]['prv_end'], service)
            sessions = SessionsCategoryResults(present, previous, 'date').main()
            keywords = Converted_keywords(present,previous).main()
            session_category = sessions['sessions']['present']
            googleads = Googleads(present, previous).main()
            googleads_cost = Googleads_cost(present, previous).main()
            googleads_ctr = Googleads_ctr(present, previous).main()
            googleads_imp = Googleads_imp(present, previous).main()
            googleads_en = Googleads_en(present, previous).main()
            googleads_cv = Googleads_cv(present, previous).main()
            devices = Devices(present, previous).main()
            events = Events(present, previous).main()
            AllVisitors_pre = (session_category[8].get('Organic Search', 0) +
                               session_category[8].get('Direct', 0) +
                               session_category[8].get('Referral', 0) +
                               session_category[8].get('Social', 0) +
                               session_category[8].get('Paid Search', 0) +
                               session_category[8].get('Email', 0))
            AllVisitors_prev = (sessions['sessions']['present'][9].get('Organic Search', 0) +
                                sessions['sessions']['present'][9].get('Direct', 0) +
                                sessions['sessions']['present'][9].get('Referral', 0) +
                                sessions['sessions']['present'][9].get('Social', 0) +
                                sessions['sessions']['present'][9].get('Paid Search', 0) +
                                sessions['sessions']['present'][9].get('Email', 0))
            change_vists = round((float(AllVisitors_pre)-float(AllVisitors_prev))/float(AllVisitors_prev)*100,2)

            # print(keywords)
            # print(googleads)
            # print(googleads_cost)
            # print(googleads_ctr)
            # print(googleads_imp)
            # print(googleads_en)
            # print(googleads_cv)
            events={'pre_total':events['total']['pre_total'],
                    'change':round(events['change']['total_change'][0], 2)}

            lst = ','.join(keywords['pre_keywords'])
            clicks_on = str(googleads['total'] + googleads['total_s'])
            impr = str(googleads_imp['total'] + googleads_imp['total_s'])
            ctr = str(googleads_ctr['total'] + googleads_ctr['total_s'])
            cost = str(googleads_cost['total'] + googleads_cost['total_s'])
            en = str(googleads_en['total'] + googleads_en['total_s'])
            # c_con = str(googleads_cv['total'] + googleads_cv['total_s'])
            fromx = 'sanctusit.textmail@gmail.com'
            to = 'veeresh@sanctusit.com'
            msg = MIMEText(
                "Hi All   \n\nHere are my weekly metrics \n\n Data for mail" )
            # "\n\n    Illustration Ads     : [Clicks:"+str(googleads['total'])+"; Impr:"+str(googleads_imp['total'])+"; CTR:"+str(googleads_ctr['total'])+"%; Cost:$"+str(googleads_cost['total'])+"; Conv:"+str(googleads_en['total'])+"; Cost/Conv:$"+str(googleads_cv['total'])+";]\n\n    Stock Illustration Ads:[Clicks:"+str(googleads['total_s'])+"; Impr:"+str(googleads_imp['total_s'])+"; CTR:"+str(googleads_ctr['total_s'])+"%; Cost:$"+str(googleads_cost['total_s'])+"; Conv:"+str(googleads_en['total_s'])+"; Cost/Conv:$"+str(googleads_cv['total_s'])+";]\n\n\n\n\n\nThanks and Regards,")
            msg['Subject'] = 'Weekly Metrics report'
            msg['From'] = fromx
            msg['To'] = to

            server = smtplib.SMTP('smtp.gmail.com:587')
            server.starttls()
            server.ehlo()
            server.login('sanctusit.textmail@gmail.com', 'sanctusit.com')
            server.sendmail(fromx, to, msg.as_string())
            server.quit()

            dates = {
                'pre_date': dates[1]['pre_start'] + ' to ' + dates[1]['pre_end'],
                'prev_date': dates[1]['prv_start'] + ' to ' + dates[1]['prv_end']
            }

            return render_template('mail_data.html',dates=dates,option=option, keywords = keywords, sessions=sessions,AllVisitors_pre=AllVisitors_pre,
                                   AllVisitors_prev=AllVisitors_prev,lst=lst,devices=devices,googleads=googleads,
                                       googleads_cost=googleads_cost, googleads_ctr=googleads_ctr,
                                       googleads_imp=googleads_imp,events=events,
                                       googleads_en=googleads_en, googleads_cv=googleads_cv,change_vists=change_vists)

        elif dates['option'] == "LastMonthPrevYear":
            option = 'Prev. Month of Past Year'
            dates = prev_month_last_year()
            present = mainClass(dates[0]['pre_start'], dates[0]['pre_end'], service)
            previous = mainClass(dates[0]['prv_start'], dates[0]['prv_end'], service)
            sessions = SessionsCategoryResults(present, previous, 'date').main()
            keywords = Converted_keywords(present, previous).main()
            session_category = sessions['sessions']['present']
            googleads = Googleads(present, previous).main()
            googleads_cost = Googleads_cost(present, previous).main()
            googleads_ctr = Googleads_ctr(present, previous).main()
            googleads_imp = Googleads_imp(present, previous).main()
            googleads_en = Googleads_en(present, previous).main()
            googleads_cv = Googleads_cv(present, previous).main()
            devices = Devices(present, previous).main()
            events = Events(present, previous).main()
            AllVisitors_pre = (session_category[8].get('Organic Search', 0) +
                               session_category[8].get('Direct', 0) +
                               session_category[8].get('Referral', 0) +
                               session_category[8].get('Social', 0) +
                               session_category[8].get('Paid Search', 0) +
                               session_category[8].get('Email', 0))
            AllVisitors_prev = (sessions['sessions']['present'][9].get('Organic Search', 0) +
                                sessions['sessions']['present'][9].get('Direct', 0) +
                                sessions['sessions']['present'][9].get('Referral', 0) +
                                sessions['sessions']['present'][9].get('Social', 0) +
                                sessions['sessions']['present'][9].get('Paid Search', 0) +
                                sessions['sessions']['present'][9].get('Email', 0))
            change_vists = round((float(AllVisitors_pre) - float(AllVisitors_prev)) / float(AllVisitors_prev) * 100, 2)
            events = {'pre_total': events['total']['pre_total'],
                      'change': round(events['change']['total_change'][0], 2)}
            lst = ','.join(keywords['pre_keywords'])

            dates = {
                'pre_date': dates[1]['pre_start'] + ' to ' + dates[1]['pre_end'],
                'prev_date': dates[1]['prv_start'] + ' to ' + dates[1]['prv_end']
            }
            return render_template('mail_data.html',dates=dates,option=option,
                                   keywords=keywords,sessions=sessions,AllVisitors_pre=AllVisitors_pre,
                                   AllVisitors_prev=AllVisitors_prev,lst=lst,devices=devices,googleads=googleads,
                                       googleads_cost=googleads_cost, googleads_ctr=googleads_ctr,
                                       googleads_imp=googleads_imp,events=events,
                                       googleads_en=googleads_en, googleads_cv=googleads_cv,change_vists=change_vists)

        elif dates['option'] == "30":
            dates = get_dates(30)
            option = 'This Month (Last 4 Weeks)'
            present = mainClass(dates[0]['pre_start'], dates[0]['pre_end'], service)
            previous = mainClass(dates[0]['prv_start'], dates[0]['prv_end'], service)
            sessions = SessionsCategoryResults(present, previous, 'date').main()
            keywords = Converted_keywords(present, previous).main()
            session_category = sessions['sessions']['present']
            googleads = Googleads(present, previous).main()
            googleads_cost = Googleads_cost(present, previous).main()
            googleads_ctr = Googleads_ctr(present, previous).main()
            googleads_imp = Googleads_imp(present, previous).main()
            googleads_en = Googleads_en(present, previous).main()
            googleads_cv = Googleads_cv(present, previous).main()
            devices = Devices(present, previous).main()
            events = Events(present, previous).main()
            AllVisitors_pre = (session_category[8].get('Organic Search', 0) +
                               session_category[8].get('Direct', 0) +
                               session_category[8].get('Referral', 0) +
                               session_category[8].get('Social', 0) +
                               session_category[8].get('Paid Search', 0) +
                               session_category[8].get('Email', 0))
            AllVisitors_prev = (sessions['sessions']['present'][9].get('Organic Search', 0) +
                                sessions['sessions']['present'][9].get('Direct', 0) +
                                sessions['sessions']['present'][9].get('Referral', 0) +
                                sessions['sessions']['present'][9].get('Social', 0) +
                                sessions['sessions']['present'][9].get('Paid Search', 0) +
                                sessions['sessions']['present'][9].get('Email', 0))
            change_vists = round((float(AllVisitors_pre) - float(AllVisitors_prev)) / float(AllVisitors_prev) * 100, 2)
            events = {'pre_total': events['total']['pre_total'],
                      'change': round(events['change']['total_change'][0], 2)}
            lst = ','.join(keywords['pre_keywords'])

            dates = {
                'pre_date': dates[1]['pre_start'] + ' to ' + dates[1]['pre_end'],
                'prev_date': dates[1]['prv_start'] + ' to ' + dates[1]['prv_end']
            }
            return render_template('mail_data.html',dates=dates,option=option,
                                   keywords=keywords,sessions=sessions,AllVisitors_pre=AllVisitors_pre,
                                   AllVisitors_prev=AllVisitors_prev,lst=lst,devices=devices,googleads=googleads,
                                       googleads_cost=googleads_cost, googleads_ctr=googleads_ctr,events=events,
                                       googleads_imp=googleads_imp,change_vists=change_vists,
                                       googleads_en=googleads_en, googleads_cv=googleads_cv)

        elif dates['option'] == "LastMonth":
            dates = get_two_month_dates()
            # print(dates)
            option = 'Prev. Month'
            present = mainClass(dates[0]['pre_start'], dates[0]['pre_end'], service)
            previous = mainClass(dates[0]['prv_start'], dates[0]['prv_end'], service)
            sessions = SessionsCategoryResults(present, previous, 'date').main()
            keywords = Converted_keywords(present, previous).main()
            session_category = sessions['sessions']['present']
            googleads = Googleads(present, previous).main()
            googleads_cost = Googleads_cost(present, previous).main()
            googleads_ctr = Googleads_ctr(present, previous).main()
            googleads_imp = Googleads_imp(present, previous).main()
            googleads_en = Googleads_en(present, previous).main()
            googleads_cv = Googleads_cv(present, previous).main()
            devices = Devices(present, previous).main()
            events = Events(present, previous).main()
            AllVisitors_pre = (session_category[8].get('Organic Search', 0) +
                               session_category[8].get('Direct', 0) +
                               session_category[8].get('Referral', 0) +
                               session_category[8].get('Social', 0) +
                               session_category[8].get('Paid Search', 0) +
                               session_category[8].get('Email', 0))
            AllVisitors_prev = (sessions['sessions']['present'][9].get('Organic Search', 0) +
                                sessions['sessions']['present'][9].get('Direct', 0) +
                                sessions['sessions']['present'][9].get('Referral', 0) +
                                sessions['sessions']['present'][9].get('Social', 0) +
                                sessions['sessions']['present'][9].get('Paid Search', 0) +
                                sessions['sessions']['present'][9].get('Email', 0))
            change_vists = round((float(AllVisitors_pre) - float(AllVisitors_prev)) / float(AllVisitors_prev) * 100, 2)
            events = {'pre_total': events['total']['pre_total'],
                      'change': round(events['change']['total_change'][0], 2)}
            lst = ','.join(keywords['pre_keywords'])

            dates = {
                'pre_date': dates[1]['pre_start'] + ' to ' + dates[1]['pre_end'],
                'prev_date': dates[1]['prv_start'] + ' to ' + dates[1]['prv_end']
            }
            return render_template('mail_data.html',dates=dates,option=option,
                                   keywords=keywords,sessions=sessions,AllVisitors_pre=AllVisitors_pre,
                                   AllVisitors_prev=AllVisitors_prev,lst=lst,devices=devices,googleads=googleads,
                                       googleads_cost=googleads_cost, googleads_ctr=googleads_ctr,events=events,
                                       googleads_imp=googleads_imp,change_vists=change_vists,
                                       googleads_en=googleads_en, googleads_cv=googleads_cv)

        elif dates['option'] == "12":
            option = 'Last 12 Months'
            dates = get12months()
            present = mainClass(dates[0]['pre_start'], dates[0]['pre_end'], service)
            previous = mainClass(dates[0]['prv_start'], dates[0]['prv_end'], service)
            sessions = SessionsCategoryResults(present, previous, 'date').main()
            keywords = Converted_keywords(present, previous).main()
            session_category = sessions['sessions']['present']
            googleads = Googleads(present, previous).main()
            googleads_cost = Googleads_cost(present, previous).main()
            googleads_ctr = Googleads_ctr(present, previous).main()
            googleads_imp = Googleads_imp(present, previous).main()
            googleads_en = Googleads_en(present, previous).main()
            googleads_cv = Googleads_cv(present, previous).main()
            devices = Devices(present, previous).main()
            events = Events(present, previous).main()
            AllVisitors_pre = (session_category[8].get('Organic Search', 0) +
                               session_category[8].get('Direct', 0) +
                               session_category[8].get('Referral', 0) +
                               session_category[8].get('Social', 0) +
                               session_category[8].get('Paid Search', 0) +
                               session_category[8].get('Email', 0))
            AllVisitors_prev = (sessions['sessions']['present'][9].get('Organic Search', 0) +
                                sessions['sessions']['present'][9].get('Direct', 0) +
                                sessions['sessions']['present'][9].get('Referral', 0) +
                                sessions['sessions']['present'][9].get('Social', 0) +
                                sessions['sessions']['present'][9].get('Paid Search', 0) +
                                sessions['sessions']['present'][9].get('Email', 0))
            change_vists = round((float(AllVisitors_pre) - float(AllVisitors_prev)) / float(AllVisitors_prev) * 100, 2)
            events = {'pre_total': events['total']['pre_total'],
                      'change': round(events['change']['total_change'][0], 2)}
            lst = ','.join(keywords['pre_keywords'])

            dates = {
                'pre_date': dates[1]['pre_start'] + ' to ' + dates[1]['pre_end'],
                'prev_date': dates[1]['prv_start'] + ' to ' + dates[1]['prv_end']
            }
            return render_template('mail_data.html',dates=dates,option=option,
                                   keywords=keywords,sessions=sessions,AllVisitors_pre=AllVisitors_pre,
                                   AllVisitors_prev=AllVisitors_prev,lst=lst,devices=devices,googleads=googleads,
                                       googleads_cost=googleads_cost, googleads_ctr=googleads_ctr,events=events,
                                       googleads_imp=googleads_imp,change_vists=change_vists,
                                       googleads_en=googleads_en, googleads_cv=googleads_cv)

        elif dates['option'] == "LastYear":
            option = 'Last Year'
            dates = last_year()
            present = mainClass(dates[0]['pre_start'], dates[0]['pre_end'], service)
            previous = mainClass(dates[0]['prv_start'], dates[0]['prv_end'], service)
            sessions = SessionsCategoryResults(present, previous, 'date').main()
            keywords = Converted_keywords(present, previous).main()
            session_category = sessions['sessions']['present']
            googleads = Googleads(present, previous).main()
            googleads_cost = Googleads_cost(present, previous).main()
            googleads_ctr = Googleads_ctr(present, previous).main()
            googleads_imp = Googleads_imp(present, previous).main()
            googleads_en = Googleads_en(present, previous).main()
            googleads_cv = Googleads_cv(present, previous).main()
            devices = Devices(present, previous).main()
            events = Events(present, previous).main()
            AllVisitors_pre = (session_category[8].get('Organic Search', 0) +
                               session_category[8].get('Direct', 0) +
                               session_category[8].get('Referral', 0) +
                               session_category[8].get('Social', 0) +
                               session_category[8].get('Paid Search', 0) +
                               session_category[8].get('Email', 0))
            AllVisitors_prev = (sessions['sessions']['present'][9].get('Organic Search', 0) +
                                sessions['sessions']['present'][9].get('Direct', 0) +
                                sessions['sessions']['present'][9].get('Referral', 0) +
                                sessions['sessions']['present'][9].get('Social', 0) +
                                sessions['sessions']['present'][9].get('Paid Search', 0) +
                                sessions['sessions']['present'][9].get('Email', 0))
            change_vists = round((float(AllVisitors_pre) - float(AllVisitors_prev)) / float(AllVisitors_prev) * 100, 2)
            events = {'pre_total': events['total']['pre_total'],
                      'change': round(events['change']['total_change'][0], 2)}
            lst = ','.join(keywords['pre_keywords'])

            dates = {
                'pre_date': dates[1]['pre_start'] + ' to ' + dates[1]['pre_end'],
                'prev_date': dates[1]['prv_start'] + ' to ' + dates[1]['prv_end']
            }
            return render_template('mail_data.html',dates=dates,option=option,
                                   keywords=keywords,sessions=sessions,AllVisitors_pre=AllVisitors_pre,
                                   AllVisitors_prev=AllVisitors_prev,lst=lst,devices=devices,googleads=googleads,
                                       googleads_cost=googleads_cost, googleads_ctr=googleads_ctr,events=events,
                                       googleads_imp=googleads_imp,change_vists=change_vists,
                                       googleads_en=googleads_en, googleads_cv=googleads_cv)

        elif dates['option'] == "Week":
            option = 'Last 7 Days'
            dates = get_dates_yest(7)
            print(dates)
            present = mainClass(dates[0]['pre_start'], dates[0]['pre_end'], service)
            previous = mainClass(dates[0]['prv_start'], dates[0]['prv_end'], service)
            sessions = SessionsCategoryResults(present, previous, 'date').main()
            keywords = Converted_keywords(present, previous).main()
            session_category = sessions['sessions']['present']
            googleads = Googleads(present, previous).main()
            googleads_cost = Googleads_cost(present, previous).main()
            googleads_ctr = Googleads_ctr(present, previous).main()
            googleads_imp = Googleads_imp(present, previous).main()
            googleads_en = Googleads_en(present, previous).main()
            googleads_cv = Googleads_cv(present, previous).main()
            devices = Devices(present, previous).main()
            events = Events(present, previous).main()
            AllVisitors_pre = (session_category[8].get('Organic Search', 0) +
                               session_category[8].get('Direct', 0) +
                               session_category[8].get('Referral', 0) +
                               session_category[8].get('Social', 0) +
                               session_category[8].get('Paid Search', 0) +
                               session_category[8].get('Email', 0))
            AllVisitors_prev = (sessions['sessions']['present'][9].get('Organic Search', 0) +
                                sessions['sessions']['present'][9].get('Direct', 0) +
                                sessions['sessions']['present'][9].get('Referral', 0) +
                                sessions['sessions']['present'][9].get('Social', 0) +
                                sessions['sessions']['present'][9].get('Paid Search', 0) +
                                sessions['sessions']['present'][9].get('Email', 0))
            lst = ','.join(keywords['pre_keywords'])
            events = {'pre_total': events['total']['pre_total'],
                      'change': round(events['change']['total_change'][0], 2)}
            change_vists = round((float(AllVisitors_pre) - float(AllVisitors_prev)) / float(AllVisitors_prev) * 100, 2)

            dates = {
                'pre_date': dates[1]['pre_start'] + ' to ' + dates[1]['pre_end'],
                'prev_date': dates[1]['prv_start'] + ' to ' + dates[1]['prv_end']
            }
            return render_template('mail_data.html', dates=dates, option=option, keywords=keywords,sessions=sessions,AllVisitors_pre=AllVisitors_pre,
                                   AllVisitors_prev=AllVisitors_prev,lst=lst,devices=devices,googleads=googleads,
                                       googleads_cost=googleads_cost, googleads_ctr=googleads_ctr,events=events,
                                       googleads_imp=googleads_imp,change_vists=change_vists,
                                       googleads_en=googleads_en, googleads_cv=googleads_cv)

    except Exception as e:
        print(e)
        # if e == 'The credentials do not contain the necessary fields need to refresh the access token. You must specify refresh_token, token_uri, client_id, and client_secret.':
        return redirect('authorize')
        # else:
        #     return render_template("page_500.html")

@app.route("/region" , methods=["GET", "POST"])
def region():
    if 'credentials' not in session:
        return redirect('authorize')

    credentials = google.oauth2.credentials.Credentials(
        **session['credentials'])

    service = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)
    try:
        dates = request.form.to_dict()
    except:
        dates = {}
    try:
        if dates == {} or dates['option'] == "Week":
            option = 'Last 7 Days'
            dates = get_dates_yest(7)
            # print(dates)
            present = mainClass(dates[0]['pre_start'], dates[0]['pre_end'], service)
            previous = mainClass(dates[0]['prv_start'], dates[0]['prv_end'], service)
            sessions = SessionsCategoryResults(present, previous, 'date').main()
            result = {
                "sessions": sessions['totalSessions'],
                'goalconversions': sessions['goalconversions'],
                'session_region_line_data': sessions['session_region_line_data'],
            }

            dates = {
                'pre_date': dates[1]['pre_start'] + ' to ' + dates[1]['pre_end'],
                'prev_date': dates[1]['prv_start'] + ' to ' + dates[1]['prv_end']
            }


            days = [((day.now() - timedelta(days=i)).strftime("%A")) for i in range(1, 8)]

            session['credentials'] = credentials_to_dict(credentials)

            return render_template('region.html', dates=dates, option=option,
                                   days=days, sessions=sessions,result=result)
    except Exception as e:
        print(e)
        # if e == 'The credentials do not contain the necessary fields need to refresh the access token. You must specify refresh_token, token_uri, client_id, and client_secret.':
        return redirect('authorize')
        # else:
        #     return render_template("page_500.html")



@app.route('/authorize')
def authorize():
  # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES)

  flow.redirect_uri = url_for('oauth2callback', _external=True)

  authorization_url, state = flow.authorization_url(
      # Enable offline access so that you can refresh an access token without
      # re-prompting the user for permission. Recommended for web server apps.
      access_type='offline',
      # Enable incremental authorization. Recommended as a best practice.
      include_granted_scopes='true')

  # Store the state so the callback can verify the auth server response.
  session['state'] = state

  return redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
  # Specify the state when creating the flow in the callback so that it can
  # verified in the authorization server response.
  state = session['state']
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
  flow.redirect_uri = url_for('oauth2callback', _external=True)
  # Use the authorization server's response to fetch the OAuth 2.0 tokens.
  authorization_response = request.url
  authorization_response=authorization_response.replace('http', 'https')
  flow.fetch_token(authorization_response=authorization_response)
  # Store credentials in the session.
  # ACTION ITEM: In a production app, you likely want to save these
  #              credentials in a persistent database instead.
  credentials = flow.credentials
  session['credentials'] = credentials_to_dict(credentials)
  return redirect(url_for('index'))
@app.route('/revoke')
def revoke():
  if 'credentials' not in session:
    return ('You need to <a href="/authorize">authorize</a> before ' +
            'testing the code to revoke credentials.')
  credentials = google.oauth2.credentials.Credentials(
    **session['credentials'])
  revoke = requests.post('https://accounts.google.com/o/oauth2/revoke',
      params={'token': credentials.token},
      headers = {'content-type': 'application/x-www-form-urlencoded'})
  status_code = getattr(revoke, 'status_code')
  if status_code == 200:
    return jsonify({"status": 'Success'})
@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500
if __name__ == '__main__':
  # When running locally, disable OAuthlib's HTTPs verification.
  # ACTION ITEM for developers:
  #     When running in production *do not* leave this option enabled.
  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
  # Specify a hostname and port that are set as a valid redirect URI
  # for your API project in the Google API Console.
  port = int(os.environ.get("PORT", 8080))
  # app.run(host="0.0.0.0", debug=True, port=port)
  app.run(host="localhost", debug=True, port=port)
