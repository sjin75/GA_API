""" 사용자 추가 (Management API) """

import argparse

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools

def get_service(api_name, api_version, scope, key_file_location,
                service_account_email):
  """Get a service that communicates to a Google API.

  Args:
    api_name: The name of the api to connect to.
    api_version: The api version to connect to.
    scope: A list auth scopes to authorize for the application.
    key_file_location: The path to a valid service account p12 key file.
    service_account_email: The service account email address.

  Returns:
    A service that is connected to the specified API.
  """

  credentials = ServiceAccountCredentials.from_p12_keyfile(
    service_account_email, key_file_location, scopes=scope)

  http = credentials.authorize(httplib2.Http())

  # Build the service object.
  service = build(api_name, api_version, http=http)

  return service

def main():
  # Define the auth scopes to request.
  #scope = ['https://www.googleapis.com/auth/analytics.readonly']
  scope = ['https://www.googleapis.com/auth/analytics.manage.users']

  # Use the developer console and replace the values with your
  # service account email and relative location of your key file.
  service_account_email = '[SERVICE_ACCOUNT_EMAIL]@developer.gserviceaccount.com'
  key_file_location = './client_secrets.p12'

  # Authenticate and construct service.
  service = get_service('analytics', 'v3', scope, key_file_location,
    service_account_email)

  # 권한 부여할 이메일 주소 리스트
  user_list = ['[EMAIL-1]@gmail.com', '[EMAIL-2]@gmail.com']

  try:

    for user in user_list:
      # Mobile Web
      service.management().profileUserLinks().insert(
          accountId='10587421',
          webPropertyId='UA-10587421-2',
          profileId='89357101',
          body={
              'permissions': {
                  'local': [
                      'COLLABORATE',
                      'READ_AND_ANALYZE'
                  ]
              },
              'userRef': {
                  'email': user
              }
          }
      ).execute()

      # Android
      service.management().profileUserLinks().insert(
          accountId='10587421',
          webPropertyId='UA-10587421-2',
          profileId='87855026',
          body={
              'permissions': {
                  'local': [
                      'COLLABORATE',
                      'READ_AND_ANALYZE'
                  ]
              },
              'userRef': {
                  'email': user
              }
          }
      ).execute()

      # iOS
      service.management().profileUserLinks().insert(
          accountId='10587421',
          webPropertyId='UA-10587421-2',
          profileId='88823264',
          body={
              'permissions': {
                  'local': [
                      'COLLABORATE',
                      'READ_AND_ANALYZE'
                  ]
              },
              'userRef': {
                  'email': user
              }
          }
      ).execute()

      # PC Web LONG
      service.management().profileUserLinks().insert(
          accountId='10587421',
          webPropertyId='UA-10587421-2',
          profileId='84826225',
          body={
              'permissions': {
                  'local': [
                      'COLLABORATE',
                      'READ_AND_ANALYZE'
                  ]
              },
              'userRef': {
                  'email': user
              }
          }
      ).execute()

  except TypeError, error:
    # Handle errors in constructing a query.
    print('There was an error in constructing your query : %s' % error)

  except HttpError, error:
    # Handle API errors.
    print('There was an API error : %s : %s' % (error.resp.status, error.resp.reason))

if __name__ == '__main__':
  main()

