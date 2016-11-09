""" Update User Permissions """
""" Target: users from Ticketmonster TI property """
""" Permissions: COLLABORATE for TM/ MOBILE/ ANDROID APP (Push Events Included) View """

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

  # Note: This code assumes you have an authorized Analytics service object.
  # See the User Permissions Developer Guide for details.

  # Requests a list of user links for a given property
  try:
    property_links = service.management().webpropertyUserLinks().list(
        accountId='10587421',
        webPropertyId='UA-10587421-2'
    ).execute()

  except TypeError, error:
    # Handle errors in constructing a query.
    print('There was an error in constructing your query : %s' % error)

  except HttpError, error:
    # Handle API errors.
    print('There was an API error : %s : %s' % (error.resp.status, error.resp.reason))

  for propertyUserLink in property_links.get('items', []):
    entity = propertyUserLink.get('entity', {})
    propertyRef = entity.get('webPropertyRef', {})
    userRef = propertyUserLink.get('userRef', {})
    permissions = propertyUserLink.get('permissions', {})

    print('Property User Link Id   = %s' % propertyUserLink.get('id'))
    print('Property User Link kind = %s' % propertyUserLink.get('kind'))
    print('User Email             = %s' % userRef.get('email'))
    print('Permissions effective  = %s' % permissions.get('effective'))
    print('Permissions local      = %s' % permissions.get('local'))
    print('Property Id             = %s' % propertyRef.get('id'))
    print('Property kind           = %s' % propertyRef.get('kind'))
    print('Property Name           = %s' % propertyRef.get('name'))

    userLinkId = '102782120' + ':' + propertyUserLink.get('id').split(':')[1]

    try:
      service.management().profileUserLinks().update(
          accountId='10587421',
          webPropertyId='UA-10587421-2',
          profileId='102782120',  # push event included
          linkId=userLinkId,
          body={
              'permissions': {
                  'local': [
                      'COLLABORATE',
                      'READ_AND_ANALYZE'
                  ]
              }
          }
      ).execute()

    except TypeError, error:
      # Handle errors in constructing a query.
      print('There was an error in constructing your query : %s' % error)

if __name__ == '__main__':
  main()

