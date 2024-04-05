import streamlit as st
import requests
import re
from datetime import datetime, timedelta

size = 0
count = 0
killswitch = 0
times = []
hearings = []
result = []
courts = ['8A', '10A', '10B', '10C', '10D','11A','11B','11C','11D','13A','13B','13C','13D','15A','15B','15C','18A','18B','18C','19A','19B','19C','19D','24A','24B','24C','24D','29A','29B','29C','29D','30A','30B','30C','30D','32A','32B','32C','32D']


today = datetime.today()
if datetime.today().weekday() == 4:
		sun = datetime.today() + timedelta(2)
		start = f"{sun.strftime('%Y-%m-%d')}T16:00:00.000Z"
		mon = datetime.today() + timedelta(3)
		end = f"{mon.strftime('%Y-%m-%d')}T15:59:00.000Z"
elif datetime.today().weekday() == 5:
		sun = datetime.today() + timedelta(1)
		start = f"{sun.strftime('%Y-%m-%d')}T16:00:00.000Z"
		mon = datetime.today() + timedelta(2)
		end = f"{mon.strftime('%Y-%m-%d')}T15:59:00.000Z"
else:
	end = f"{today.strftime('%Y-%m-%d')}T15:59:00.000Z"
	yest = datetime.today() - timedelta(1)
	start = f"{yest.strftime('%Y-%m-%d')}T16:00:00.000Z"


when = st.text_input("pm/tmr/today:")
if when == "pm":
	pattern2 = r'\b\d{1,2}:\d{2} PM\b'
elif when == "today":
	pattern2 = r'\b\d{1,2}:\d{2} [AP]M\b'
elif when == "tmr":
	pattern2 = r'\b\d{1,2}:\d{2} AM\b'
	
else:
	st.stop()

st.button("Clear", type="primary")
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
		
		for i in re.findall(pattern2, content):
			size += 1

		if re.search(pattern2, content) != None:
			#time = str(re.search(pattern2, content).group())
			times = re.findall(pattern2, content)
		else:
			pass

		pattern4 = r'hearing-type"u003e(.*?)u003c'
		#pattern4 = r'For Mention|Trial|Part-Heard|For Hearing|Hearing(Newton)|For Further Mention'
		if re.search(pattern4, s) != None:
			hearings = re.findall(pattern4, s)
		else:
			st.write(hearings)
			st.write(times)


		if size != 0:
			for i in range(size):
				temp = times[i] + " " + hearings[i]
				result.append(temp)
			st.write(court, "\n", ", ".join(result), "\n")
			count += 1
			size = 0
			times = []
			hearings = []
			result = []
		else:
			pass

		if killswitch == 40:
			break
		else:
			killswitch += 1

	st.write(count)
    
else:
    st.empty()
