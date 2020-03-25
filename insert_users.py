""" Insert Users (Management API) """

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

import httplib2

def get_service(api_name, api_version, scopes, key_file_location):
    """Get a service that communicates to a Google API.

    Args:
        api_name: The name of the api to connect to.
        api_version: The api version to connect to.
        scopes: A list auth scopes to authorize for the application.
        key_file_location: The path to a valid service account JSON key file.

    Returns:
        A service that is connected to the specified API.
    """

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
            key_file_location, scopes=scopes)

    # Build the service object.
    service = build(api_name, api_version, credentials=credentials)

    return service

def main():
  # Define the auth scopes to request.
  scope = ['https://www.googleapis.com/auth/analytics.manage.users']

  # key file
  key_file_location = './client_secrets.json'

  # Authenticate and construct service.
  service = get_service('analytics', 'v3', scope, key_file_location)

  # user list
  user_list = [
               '[EMAIL_1]@gmail.com', \
               '[EMAIL_2]@gmail.com'
               ]

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
          profileId='102782120',
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

      # PC Web
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

      # Master
      service.management().profileUserLinks().insert(
          accountId='10587421',
          webPropertyId='UA-10587421-2',
          profileId='163731114',
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

  except error:
    # Handle errors in constructing a query.
    print('There was an error in constructing your query : %s' % error)

if __name__ == '__main__':
  main()
