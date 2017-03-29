#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from skyscanner.skyscanner import Flights
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) 

flights_service = Flights('li366941824595940128156908455687')
data = flights_service.get_result(
    cabinclass='Economy',
    country='TH',
    currency='THB',
    locale='th-TH',
    locationSchema='sky',
    originplace='BKKT-sky',
    destinationplace='CNX-sky',
    outbounddate='2017-04-06',
    inbounddate='2017-04-13',
    grouppricing=True,
    adults=2,
    children=0,
    infants=0).parsed

#for c in result['Agents']:
#        if c['Name'] == 'Tripair':
#                print(c['Name']),(c['Id'])

#print json.dumps(result, indent=4, sort_keys=True)

final_output=[]
for c in data['Itineraries']:
	for a in data['Agents']:
		if c['PricingOptions'][0]['Agents'][0] == a['Id']:
			for li in data['Legs']:
				if (c['InboundLegId'] == li['Id']):
					for lo in data['Legs']:
						if (c['OutboundLegId'] == lo['Id']):
							for si in data['Segments']:
								if (li['SegmentIds'][0] == si['Id']):
									for so in data['Segments']:
										if (lo['SegmentIds'][0] == so['Id']):
											for pio in data['Places']:
												if (si['OriginStation'] == pio['Id']):
													for pid in data['Places']:
														if (si['DestinationStation'] == pid['Id']):
															for poo in data['Places']:
																if (so['OriginStation'] == poo['Id']):
																	for pod in data['Places']:
																		if (so['DestinationStation'] == pod['Id']):
																			for ci in data['Carriers']:
																				if (si['OperatingCarrier'] == ci['Id']):
																					for co in data['Carriers']:
																						if (so['OperatingCarrier'] == co['Id']):
																							final_outputs=(so['DepartureDateTime']),(so['ArrivalDateTime']),(poo['Code']),(pod['Code']),(co['Name']).encode('utf-8'),(so['Duration']),(lo['Stops']),(si['DepartureDateTime']),(si['ArrivalDateTime']),(pio['Code']),(pid['Code']),(ci['Name']).encode('utf-8'),(si['Duration']),(li['Stops']),(c['PricingOptions'][0]['Price']),data['Currencies'][0]['Code'],(a['Name']),(c['PricingOptions'][0]['DeeplinkUrl'])
																							final_output.append(final_outputs)
for i in range (3):
        print (final_output[i])