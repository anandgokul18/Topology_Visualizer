#!/usr/bin/env python

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
               'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('mypkey.json', scope)

gc = gspread.authorize(credentials)

sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1IK-SBOskJnK4aoUI1MohT-QUpTVnS8FCbyKTMsMHLgQ/edit#gid=0')

worksheet = sh.add_worksheet(title="A worksheet", rows="100", cols="20")


