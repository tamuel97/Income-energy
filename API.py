import requests
import json
import time
import datetime
import csv
import math

# The time period specified exceeds that allowed for the hour granularity (allowed: 93 days)
# Devices {
#           Castle Hill: DD64108179557                 starting_time: 23/08/2019 10:15
#           Holroyd    : DD54108186977                 starting_time: 23/08/2019 15:05
#           EnergyLab  : D704206224262                 starting_time: 14/02/2019 13:00
#                        D980408552644                 starting_time: 14/02/2019 13:35
# }

# device_name = ['DD64108179557','DD54108186977','D704206224262','D980408552644']
#device_ = device_name[0]
granularity = 'hour'  #'5m' or 'hour'




def choose_file_name(device_):
  if device_ == 'DD64108179557':
    return 'CastleHill.csv'
  elif device_ == 'DD54108186977':
    return 'Holroyd.csv'
  elif device_ == 'D704206224262':
    return 'BT_D704206224262.csv'
  elif device_ == 'D980408552644':
    return 'BT_D980408552644.csv'
  else:
    print('error')

#file_name = choose_file_name(device_)

def StartTime(device_):
  if device_ == 'DD64108179557':
    return '23/08/2019 11:00'
  elif device_ == 'DD54108186977':
    return '23/08/2019 16:00'
  elif device_ == 'D704206224262':
    return '23/08/2019 16:00'
  elif device_ == 'D980408552644':
    return '14/02/2019 14:00'
  else:
    print('error')

#starting_time = StartTime(device_)

def incrementor(granularity):
  if(granularity == '5m'):
    return 604800
  elif(granularity == 'hour'):
    return 8035200

def date2seconds(starting_time):
  return time.mktime(datetime.datetime.strptime(starting_time, "%d/%m/%Y %H:%M").timetuple())

def data(device_,starting_time):
  api_key = 'key_460c536a178082851a40e5292e2af433' # insert your actual key here
  headers = {
    'Authorization': 'Bearer %s' % api_key
  }
  return requests.get('https://api-v3.wattwatchers.com.au/long-energy/'+ device_ +'?fromTs='+ str(int(date2seconds(starting_time))) +'&granularity='+granularity, headers=headers).json()

def writeHeaders(file_name):
  with open(file_name, 'w', newline ='') as f:
    thewriter = csv.writer(f)
    thewriter.writerow(['timestamp','duration','consumptionkWh'])

def writecsv(response, file_name):
  jToKwh = 1/3600000
  with open(file_name, 'a', newline ='') as f:
    thewriter = csv.writer(f)

    for i in range(len(response)):
      thewriter.writerow([time.strftime("%d/%m/%Y %H:%M", time.localtime(response[i]['timestamp'])),response[i]['duration'],sum(response[i]['eReal'][:3])*jToKwh])

def nextweek(starting_time, granularity):
  if((date2seconds(starting_time) + incrementor(granularity)) < int(time.time())):
    return time.strftime("%d/%m/%Y %H:%M", time.localtime(date2seconds(starting_time) + incrementor(granularity)))

def numiterations(starting_time, granularity):
  return math.ceil((time.time() - date2seconds(starting_time))/incrementor(granularity))

def CastleHill():
  device_ = 'DD64108179557'
  starting_time = StartTime(device_)
  file_name = choose_file_name(device_)
  iterations = numiterations(starting_time, granularity)
  writeHeaders(file_name)

  for x in range(iterations):

    response = data(device_,starting_time)
    writecsv(response, file_name)
    starting_time = nextweek(starting_time, granularity)

def Holroyd():
  device_ = 'DD54108186977'
  starting_time = StartTime(device_)
  file_name = choose_file_name(device_)
  iterations = numiterations(starting_time, granularity)
  writeHeaders(file_name)

  for x in range(iterations):

    response = data(device_,starting_time)
    writecsv(response, file_name)
    starting_time = nextweek(starting_time, granularity)
    
def BT_D704206224262():
  device_ = 'D704206224262'
  starting_time = StartTime(device_)
  file_name = choose_file_name(device_)
  iterations = numiterations(starting_time, granularity)
  writeHeaders(file_name)

  for x in range(iterations):

    response = data(device_,starting_time)
    writecsv(response, file_name)
    starting_time = nextweek(starting_time, granularity)

def BT_D980408552644():
  device_ = 'D980408552644'
  starting_time = StartTime(device_)
  file_name = choose_file_name(device_)
  iterations = numiterations(starting_time, granularity)
  writeHeaders(file_name)

  for x in range(iterations):

    response = data(device_,starting_time)
    writecsv(response, file_name)
    starting_time = nextweek(starting_time, granularity)