"""Analytics Reporting API V4."""

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

import datetime

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = './client_secrets.json'


def initialize_analyticsreporting():
    """Initializes an Analytics Reporting API V4 service object.

    Returns:
      An authorized Analytics Reporting API V4 service object.
    """
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        KEY_FILE_LOCATION, SCOPES)

    # Build the service object.
    analytics = build('analyticsreporting', 'v4', credentials=credentials)

    return analytics


def get_report(analytics, view_id, date):
    """Queries the Analytics Reporting API V4.

    Args:
      analytics: An authorized Analytics Reporting API V4 service object.
    Returns:
      The Analytics Reporting API V4 response.
    """
    return analytics.reports().batchGet(
        body={
            'reportRequests': [
            {
              'viewId': view_id,
              'dateRanges': [{'startDate': date, 'endDate': date}],
              'metrics': [{'expression': 'ga:sessions'},
                          {'expression': 'ga:users'},
                          {'expression': 'ga:newUsers'},
                          {'expression': 'ga:avgSessionDuration'},
                          {'expression': 'ga:transactions'},
                          {'expression': 'ga:transactionRevenue', 'formattingType': 'INTEGER'}
                         ],
              'dimensions': [{'name': 'ga:date'}],
              'samplingLevel':  'LARGE'
            }]
        }
    ).execute()


def process_response(response):
    """Parses and prints the Analytics Reporting API V4 response.

    Args:
      response: An Analytics Reporting API V4 response.
    """
    for report in response.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
        samplesReadCounts = report.get('data', {}).get('samplesReadCounts', [])
        result = {}

        for row in report.get('data', {}).get('rows', []):
            dimensions = row.get('dimensions', [])
            dateRangeValues = row.get('metrics', [])

            for header, dimension in zip(dimensionHeaders, dimensions):
                result[header] = dimension

            for i, values in enumerate(dateRangeValues):
                for metricHeader, value in zip(metricHeaders, values.get('values')):
                    result[metricHeader.get('name')] = value

        if len(samplesReadCounts) == 0:
            result['sampled'] = 'no'
        else:
            result['sampled'] = 'yes'

    return result


def main():
    analytics = initialize_analyticsreporting()

    date_start = datetime.date(2020, 3, 1)
    date_range = 2

    view_ids = ['89357101', '102782120', '88823264', '84826225']

    for view_id in view_ids:
        print(view_id)
        for date in [date_start + datetime.timedelta(days=n) for n in range(0, date_range, 1)]:
            response = get_report(analytics, view_id, date.isoformat())
            result = process_response(response)
            print(result)


if __name__ == '__main__':
    main()
