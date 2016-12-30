"""Analytics Reporting API V4 - Print"""

import datetime
import reportingAPI

def store_result(result):
  print(result)

def main():

  analytics = reportingAPI.initialize_analyticsreporting()

  date_start = datetime.date(2016, 12, 23)
  date_range = 10

  view_id = '102782120'

  for date in [date_start + datetime.timedelta(days=n) for n in range(0, date_range, 1)]:
    print(date)
    response = reportingAPI.get_report(analytics, view_id, date.isoformat())
    result = reportingAPI.process_response(response, date.isoformat())
    store_result(result)

if __name__ == '__main__':
  main()

