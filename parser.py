import json
import csv

try:
  file = open('klaytn.json')
  data = json.load(file)

  file2 = open('data.csv', 'w')
  writer = csv.writer(file2)

  header = ['name', 'logo', 'nativePaymentAsset', 'floorPrice', 'numOwners', 'totalSupply', 'sevenDayChange', 'sevenDayVolume', 'oneDayChange', 'oneDayVolume', 'thirtyDayChange', 'totalVolume']
  writer.writerow(header)

  #ranking = 1
  for i in data['props']['relayCache'][0][1]['json']['data']['rankings']['edges']:
    nft = i['node']
    arr = []
    
    arr.extend([nft['name'], nft['logo'], nft['nativePaymentAsset']['symbol']])
    
    for j in range(3, len(header), 1):
      nftStats = i['node']['statsV2'][header[j]]
      
      if nftStats == None:
        nftStats = None
      elif type(nftStats) == dict:
        nftStats = nftStats['unit']
      
      arr.append(nftStats)

    writer.writerow(arr)
    
    #ranking += 1

  file.close()
  file2.close()
except TypeError:
  pass