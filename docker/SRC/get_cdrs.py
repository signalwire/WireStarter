from datetime import datetime
from signalwire.rest import Client as signalwire_client
import pandas as pd

##
# Code taken from https://developer.signalwire.com/guides/how-to-use-the-list-calls-api-to-get-statistics-python/
##


proj_id = '0fd6cfc3-ac8c-4b6f-9bc3-57048cf6a7f3'
auth_token =  'PTa7de9a82bb8711f22472d05174633af2db1317e2e23298aa'
sig_space_url = 'shane-harrell.signalwire.com'

client = signalwire_client(proj_id, auth_token, signalwire_space_url=sig_space_url)
calls = client.calls.list(start_time_after=datetime(2022, 8, 1), start_time_before=datetime(2022, 9, 10))

#print (calls)

d = []
status = []

for record in calls:
    d.append((record.from_, record.to, record.start_time, record.sid, record.price, record.direction, record.answered_by, 
record.status))
    status.append(record.status)

total_queued=int(status.count("queued"))
total_ringing=int(status.count("ringing"))
total_in_progress=int(status.count("in progress"))
total_canceled=int(status.count("canceled"))
total_completed=int(status.count("completed"))
total_busy=int(status.count("busy"))
total_failed=int(status.count("failed"))

num_outbound_calls = int(calls.count("outbound"))
num_inbound_calls = int(calls.count("inbound"))

df = pd.DataFrame(d, columns=('From', 'To', 'Start Time', 'Call SID',  'Price', 'Call Direction', 'Answered By', 'Call Status'))
print(df)
df.to_csv('Calls.csv', index=False, encoding='utf-8')
print()

totalCalls = len(df)
totalCost = df['Price'].sum()
formattedCost = "${:,.2f}".format(totalCost)

print("You sent " + str(totalCalls) + " total calls during your selected date range.")
print("The total cost of calls in your selected date range is approximately " + formattedCost + " USD.")
print("There are currently " + str(total_queued) + " calls in the queue, with " + str(total_ringing) + " currently ringing and " 
+ str(total_in_progress) + " currently in progress.")
print("There have been " + str(total_canceled) + " calls that have been canceled.")
print("There have been " + str(total_completed) + " completed calls, " + str(total_busy) + " calls marked as busy, and " + 
str(total_failed) + " failed calls.")
print("There were " + str(num_inbound_calls) + " inbound calls and " + str(num_outbound_calls) + " outbound calls.")
