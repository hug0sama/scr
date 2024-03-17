import streamlit as st
import requests
import re
from datetime import datetime, timedelta

size = 0
count = 0
killswitch = 0
courts = ['8A', '10A', '10B', '10C', '10D','11A','11B','11C','11D','13A','13B','13C','13D','15A','15B','15C','18A','18B','18C','19A','19B','19C','19D','24A','24B','24C','24D','29A','29B','29C','29D','30A','30B','30C','30D','32A','32B','32C','32D']


today = datetime.today()
end = f"{today.strftime('%Y-%m-%d')}T15:59:00.000Z"
yest = datetime.today() - timedelta(1)
start = f"{yest.strftime('%Y-%m-%d')}T16:00:00.000Z"

when = st.text_input("pm or today or tmr:")
if when == "pm":
	pattern2 = r'\b\d{1,2}:\d{2} PM\b'
elif when == "today":
	pattern2 = r'\b\d{1,2}:\d{2} [AP]M\b'
elif when == "tmr":
	pattern2 = r'\b\d{1,2}:\d{2} [AP]M\b'
	start = f"{today.strftime('%Y-%m-%d')}T16:00:00.000Z"
	tmr = datetime.today() + timedelta(1)
	end = f"{tmr.strftime('%Y-%m-%d')}T15:59:00.000Z"

else:
	st.stop()


st.button("Reset", type="primary")
if st.button("Generate"):
    	for court in courts:
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
		
		#pattern0 = r'title="([^"]*)"'
		#title = re.findall(pattern0, s)
		for i in re.findall(pattern2, content):
			size += 1
		#pattern1 = r'SC\. ([^"]*?)'
		#name = re.findall(pattern1, str(title))
		#print(name.count(''))

		
		#pattern2 = r'\b\d{1,2}:\d{2} [P]M\b'
		if re.search(pattern2, content) != None:
			time = str(re.search(pattern2, content).group())
		else:
			pass

		
		pattern3 = r'Mention'
		pattern4 = r'Trial|Part-Heard'
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
			st.write(court,'-',size,'-',time,'-',hearing)
			
			count += 1
			size = 0
		else:
			pass

		if killswitch == 40:
			break
		else:
			killswitch += 1

	st.write(count)
else:
    st.empty()
	
