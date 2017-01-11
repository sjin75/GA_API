"""Analytics Reporting API V4 - Print"""

import datetime
import reportingAPI

def main():

  analytics = reportingAPI.initialize_analyticsreporting()

  date_start = datetime.date(2016, 1, 10)
  date_range = 2

  view_ids = ['89357101', '102782120', '88823264', '84826225']

  for view_id in view_ids:
    print(view_id)
    for date in [date_start + datetime.timedelta(days=n) for n in range(0, date_range, 1)]:
      response = reportingAPI.get_report(analytics, view_id, date.isoformat())
      result = reportingAPI.process_response(response)
      print(result)

if __name__ == '__main__':
  main()

