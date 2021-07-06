import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

    
def connect_and_get_values(credentials_file, spreadsheet_id, range_):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        credentials_file,
        ['https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=range_,
        majorDimension='ROWS'
    ).execute()

    all_incomes = []
    for val in values['values']:
        if val:
            all_incomes.append(int(val[0]))

    #print(all_incomes, len(all_incomes))
    return all_incomes
