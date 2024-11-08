import os
import google.auth
import dotenv
import json
from model.ai.response_format import Factura, CustomerInfo, Category, TableEntry

from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials

dotenv.load_dotenv()

class GoogleSheetsManager():
    def __init__(self) -> None:
        self.service = self.__authenticate__()

    # auth function
    def __authenticate__(self):
        # load creds from .evn file
        service_account_info = json.loads(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON'))
        creds = Credentials.from_service_account_info(service_account_info)

        service = build('sheets', 'v4', credentials=creds)
        return service

    # inserts factura into sheet
    def insert_factura_to_sheet(self,factura: Factura):
        print("Prepare writing to sheets")

        first_empty_row = self.find_first_empty_row()

        rows = []
        for entry in factura.TableSummary:
           
            row = [
                factura.CustomerInfo.Fecha,  # Invoice Date (Fecha)
                "FUE Center Monica Beach",   # Place of Work
                entry.category,              # Type of Service (Category)
                factura.InvoiceNumber,       # Invoice Number
                entry.total,                 # Amount in €
                "",                          # Amount in MAD/TND*
                factura.Payment,             # Type of Payment
                factura.CustomerInfo.Nombre if factura.CustomerInfo.Nombre else "",  # Guest Surname
                "",                          # Guest Name
                factura.CustomerInfo.NrHabt if factura.CustomerInfo.NrHabt else "",  # Guest Room
                factura.CustomerInfo.Hotel,  # Hotel
                ", ".join(entry.details)     # Service/Article (Details)
            ]
            rows.append(row)

        # ToDo: dont overwrite existing data
        range_ = f'Sheet1!A{first_empty_row}:L'
        body = {'values': rows}

        print("Writing to sheets")
        # Call the Sheets API to append rows to the sheet
        request = self.service.spreadsheets().values().update(
            spreadsheetId=os.environ.get('GOOGLE_SHEET_ID'),
            range=range_,
            valueInputOption='RAW',
            body=body
        )
        response = request.execute()

        print(f"Data inserted successfully. {len(rows)} rows added.")
        print(response)

    def find_first_empty_row(self, start_row=7, check_column='D'):
        """Find the first empty row starting from a specified row and column in Google Sheets."""
        range_ = f'Sheet1!{check_column}{start_row}:{check_column}'
        
        # fetch values 
        response = self.service.spreadsheets().values().get(
            spreadsheetId=os.environ.get('GOOGLE_SHEET_ID'),
            range=range_,
            majorDimension='COLUMNS'
        ).execute()
        
        # Get values from response and find the first empty cell
        values = response.get('values', [[]])[0]  # Column D values starting from row 7
        first_empty_row = start_row + len(values) if not values else start_row + values.index('')

        return first_empty_row
