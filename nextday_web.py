import re
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta
import requests
import streamlit as st


today = datetime.today()
start = f"{today.strftime('%Y-%m-%d')}T16:00:00.000Z"
tmr = datetime.today() + timedelta(1)
end = f"{tmr.strftime('%Y-%m-%d')}T15:59:00.000Z"
if today.weekday() == 4:
   sun = datetime.today() + timedelta(2)
   mon = datetime.today() + timedelta(3)
   start = f"{sun.strftime('%Y-%m-%d')}T16:00:00.000Z"
   end = f"{mon.strftime('%Y-%m-%d')}T15:59:00.000Z"

courts = ['8A', '10A', '10B', '10C', '10D','11A','11B','11C','11D','13A','13B','13C','13D','15A','15B','15C','18A','18B','18C','19A','19B','19C','19D','24A','24B','24C','24D','29A','29B','29C','29D','30A','30B','30C','30D','32A','32B','32C','32D']

pattern0 = r'title="([^"]*)"'
pattern2 = r'\b\d{1,2}:\d{2} AM\b'
pattern3 = r'Mention'
pattern4 = r'Trial|Part-Heard'


scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

sheet_id = "1oEvEiKgCk_RXc-TBSv6NJ-9DJFmPPw76A6X1Omg_fzw"
workbook = client.open_by_key(sheet_id)
# sheet = workbook.worksheet("Copy")
# sheet = sheet.duplicate(insert_sheet_index=0, new_sheet_id=3, new_sheet_name=today.strftime('%Y-%m-%d'))
workbook = client.open_by_key(sheet_id)
sheet = workbook.worksheet("Copy of Copy")

count = 0
size = 0



for court in courts:
   cell = sheet.find(court)
   url = 'https://www.judiciary.gov.sg/hearing-list/GetFilteredList/'
   headers = {
   "Content-Type":"application/json; chaset=utf-8",
   "Accept":"*/*",
   "X-Requested-With":"XMLHttpRequest"
   }
   body = {
   "SearchKeywords":court,
   "SelectedStartDate":start,
   "SelectedEndDate":end,
   "SelectedPageSize":"100",
   "SelectedSortBy":"0"
   }
   response = requests.post(url, headers=headers, json=body)
   content = response.text
   s = re.sub('\\\\','', content)
  
   #title = re.findall(pattern0, s)
   for i in re.findall(pattern2, content):
      size += 1

   if re.search(pattern2, content) != None:
      time = str(re.search(pattern2, content).group())
   else:
      pass
   
   if re.search(pattern3, s) != None:
      if re.search(pattern4, s) != None:
         hearing = "MH"
      else:
         hearing = "M"
   elif re.search(pattern4, s) != None:
      hearing = "H"
   else:
      pass
   
   if re.search(pattern2, content) != None:
      result = str(size)+" "+time+" "+hearing
      sheet.update_cell(cell.row, cell.col + 4, result)
      sheet.format(str(cell.row), {"backgroundColor": {"red": 1.0, "green": 1.0, "blue": 0.0}})
      count += 1
      print(court, result)
      size = 0
   else:
      print(court+" "+"NC")
      size = 0

sheet.update_cell(47,3,count)
print("DONE")
input()