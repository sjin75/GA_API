"""Analytics Reporting API V4."""

#import argparse

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools

import datetime

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
DISCOVERY_URI = ('https://analyticsreporting.googleapis.com/$discovery/rest')
KEY_FILE_LOCATION = './client_secrets.p12'
SERVICE_ACCOUNT_EMAIL = '699053570093-271jrj42cl3tmdmml308ipglmhoq6bih@developer.gserviceaccount.com'

def initialize_analyticsreporting():
  """Initializes an analyticsreporting service object.

  Returns:
    analytics an authorized analyticsreporting service object.
  """

  credentials = ServiceAccountCredentials.from_p12_keyfile(
    SERVICE_ACCOUNT_EMAIL, KEY_FILE_LOCATION, scopes=SCOPES)

  http = credentials.authorize(httplib2.Http())

  # Build the service object.
  analytics = build('analytics', 'v4', http=http, discoveryServiceUrl=DISCOVERY_URI)

  return analytics


def get_report(analytics, view_id , date):
  # Use the Analytics Service Object to query the Analytics Reporting API V4.
  return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': view_id,
          'dateRanges': [{'startDate': date, 'endDate': date}],
          'dimensions': [{'name': 'ga:date'}],
          'metrics': [{'expression': 'ga:sessions'}, 
                      {'expression': 'ga:users'}, 
                      {'expression': 'ga:newUsers'}, 
                      {'expression': 'ga:avgSessionDuration'}, 
                      {'expression': 'ga:transactions'},
                      {'expression': 'ga:transactionRevenue', 'formattingType': 'INTEGER'}
                     ],
          'samplingLevel':  'LARGE'
        }]
      }
  ).execute()


def process_response(response, date):
  """stores the Analytics Reporting API V4 response"""

  for report in response.get('reports', []):
    columnHeader = report.get('columnHeader', {})
    dimensionHeaders = columnHeader.get('dimensions', [])
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
    rows = report.get('data', {}).get('rows', [])
    samplesReadCounts = report.get('data', {}).get('samplesReadCounts', [])
    metrics = {}

    for row in rows:
      #dimensions = row.get('dimensions', [])
      dateRangeValues = row.get('metrics', [])

      for i, values in enumerate(dateRangeValues):
        for metricHeader, value in zip(metricHeaders, values.get('values')):
          metrics[metricHeader.get('name')] = value

    if len(samplesReadCounts) == 0:
      metrics['sampled'] = 'no'
    else: 
      metrics['sampled'] = 'yes'

    return metrics

def main():

  analytics = initialize_analyticsreporting()

  date_start = datetime.date(2016, 12, 23)
  date_range = 10

  view_id = '102782120'

  for date in [date_start + datetime.timedelta(days=n) for n in range(0, date_range, 1)]:
    print(date)
    response = get_report(analytics, view_id, date.isoformat())
    result = process_response(response, date.isoformat())
    print(result)

if __name__ == '__main__':
  main()

