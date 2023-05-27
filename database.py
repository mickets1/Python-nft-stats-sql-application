from mysql.connector import connect, Error
import pandas as pd
import numpy as np
import gui

try:
  db = connect(
    host="localhost",
    user="debian-sys-maint",
    password="Ymt634UhHtP8umg7"
  )
  dbName = "Andersson"
  
  cursor = db.cursor(buffered=True)

except Error as e:
  print(e)

def tableNames():
  return ['Ethereum', 'Polygon', 'Klaytn', 'Solana']

# Read csv files and replace all nan values in the dataframe with None, 
# translates to NULL in the database.
def readCsv():
  eth = pd.read_csv('datasets/eth-data.csv')
  poly = pd.read_csv('datasets/poly-data.csv')
  klaytn = pd.read_csv('datasets/klaytn-data.csv')
  solana = pd.read_csv('datasets/solana-data.csv')

  eths = eth.replace(np.nan, None)
  polys = poly.replace(np.nan, None)
  klaytn = klaytn.replace(np.nan, None)
  solana = solana.replace(np.nan, None)

  return [eths, polys, klaytn, solana]

# Create the database if it doesn't exist.
def createDatabase():
  db = showDatabase()
  
  if db == None:
    inputData = readCsv()

    cursor.execute("CREATE DATABASE " + dbName)
    createTables(inputData)
    insertData()
    createView()
    print("Database " + dbName + " created.")
    print("View Created")
  
  gui.gui()

def showDatabase():
  cursor.execute("SHOW DATABASES")

  for db in cursor:
    if db == (dbName):
      return db

#Creating the tables with the attributes from the dataframe.
def createTables(csv):
  tableNamesArray = tableNames()

  i = 0
  for df in csv:
    cursor.execute("CREATE TABLE " + dbName + " . " + tableNamesArray[i] + "(" +
    csv[i].columns[0] + " int PRIMARY KEY," +
    csv[i].columns[1] + " varchar(100)," +
    csv[i].columns[2] + " varchar(400)," +
    csv[i].columns[3] + " varchar(100)," +
    csv[i].columns[4] + " float," +
    csv[i].columns[5] + " int," +
    csv[i].columns[6] + " int," +
    csv[i].columns[7] + " float," +
    csv[i].columns[8] + " float," +
    csv[i].columns[9] + " float," +
    csv[i].columns[10] + " float," +
    csv[i].columns[11] + " float," +
    csv[i].columns[12] + " float)")
    i += 1

  cursor.execute(f"CREATE TABLE {dbName} . User (username varchar(100) PRIMARY KEY, collectionToTrack varchar(100), blockchain varchar(20))")

#Creating attributes and inserting values into respective tables.
def insertData():
  csv = readCsv()
  fieldNamesArray = tableNames()
  
  try:
    attributeIndex = 0
    for i in fieldNamesArray:
      attributes = "`,`".join([str(i) for i in csv[attributeIndex].columns.tolist()])

      # Commit each row in a file(dataframe) to database.
      for j, row in csv[attributeIndex].iterrows():
          sql = "INSERT INTO " + dbName + " . " + i + "(`" + attributes + "`) VALUES (" + "%s," * (len(row)-1) + "%s)"
          cursor.execute(sql, tuple(row))
          db.commit()
      attributeIndex += 1

    # Inserts user data with a name and the collection they want to track.
    sqlUserdata = f"INSERT INTO {dbName} . User (username, collectionToTrack, Blockchain) VALUES ('user1', 'Bored Ape Yacht Club', 'Ethereum'), ('user2', 'Solana Monkey Business', 'Solana'), ('user3', 'Crypto Unicorns Land Market', 'Polygon')"
    cursor.execute(sqlUserdata)
    db.commit()
  except Error as e:
    print(e)

# Aggregation MAX, MIN, AVG from gui input.
def change24h(aggregation, table):
  query = "SELECT "+ aggregation + "(oneDayChange) FROM " + dbName + ' . ' + table
  cursor.execute(query)
  highest = cursor.fetchone()

  # Return procent
  return str(highest[0] * 100) + "%"

# Find partial match of collection name.
def findCollectionName(chain, searchInput):
  query = f"SELECT {chain}.name FROM {dbName} . {chain} WHERE {chain}.name LIKE '%{searchInput}%'"
  cursor.execute(query)
  collectionMatches = cursor.fetchall()

  return chain, collectionMatches

# JOIN's tables to retrieve the top5 collections accross all blockchains.
def top5RankedCollections():
  query = (
    f"SELECT Ethereum.ranking, Ethereum.name, Ethereum.numOwners, Polygon.ranking, Polygon.name, Polygon.numOwners, Klaytn.ranking, Klaytn.name, Klaytn.numOwners, Solana.ranking, Solana.name, Solana.numOwners FROM " 
    f"{dbName} . Ethereum "
    f"JOIN {dbName} . Polygon ON Ethereum.ranking = Polygon.ranking "
    f"JOIN {dbName} . Klaytn ON Polygon.ranking = Klaytn.ranking "
    f"JOIN {dbName} . Solana ON Klaytn.ranking = Solana.ranking "
    f"ORDER BY Ethereum.ranking, Polygon.ranking, Klaytn.ranking, Solana.ranking"
  )

  cursor.execute(query)
  top5 = cursor.fetchmany(size=5)

  return top5

# Retrieve collections with a supply of 1 - 10. 
def findLowSupply(chain):
  query = f"SELECT {chain}.name, {chain}.totalSupply FROM {dbName} . {chain} WHERE totalsupply >= 1 AND totalsupply <= 10 GROUP BY name, totalSupply"
  cursor.execute(query)
  totalSupply = cursor.fetchall()

  return totalSupply

# Retrieve collections with most owners
def findmostOwners(chain):
  query = f"SELECT {chain}.name, {chain}.numOwners FROM {dbName} . {chain} GROUP BY name, numOwners ORDER BY {chain}.numOwners DESC LIMIT 10"
  cursor.execute(query)
  mostOwners = cursor.fetchall()

  return mostOwners

# Create a VIEW based on name and floor price, dicarding null values.
def createView():
  query = (
  f"CREATE VIEW {dbName} . DetailsView AS SELECT "
  f"Ethereum.ranking AS EthereumRanking, Ethereum.name AS EthereumName, Ethereum.nativePaymentAsset AS EthereumPayment, Ethereum.floorPrice AS EthereumFloorPrice, " 
  f"Polygon.ranking AS PolygonRanking, Polygon.name AS PolygonName, Polygon.nativePaymentAsset AS PolygonPayment, Polygon.floorPrice AS PolygonFloorPrice "
  f"FROM {dbName} . Ethereum, {dbName} . Polygon "
  f"WHERE Ethereum.ranking = Polygon.ranking AND Ethereum.floorprice IS NOT NULL AND Polygon.floorPrice IS NOT NULL "
  f"ORDER BY Ethereum.ranking, Polygon.ranking"
  )

  cursor.execute(query)

# Statistics for collections that a user might want to track.
def userCollectionStats():
  query = (
    f"SELECT User.username, User.collectionToTrack, User.blockchain, Ethereum.oneDayChange, Polygon.oneDayChange, Klaytn.oneDayChange, Solana.oneDayChange FROM " 
    f"{dbName} . User "
    f"LEFT JOIN {dbName} . Ethereum ON Ethereum.name = User.collectionToTrack "
    f"LEFT JOIN {dbName} . Polygon ON Polygon.name = User.collectionToTrack "
    f"LEFT JOIN {dbName} . Klaytn ON Klaytn.name = User.collectionToTrack "
    f"LEFT JOIN {dbName} . Solana ON Solana.name = User.collectionToTrack "
  )

  cursor.execute(query)
  usertrackedCollectionStats = cursor.fetchall()

  return usertrackedCollectionStats

#Retrieve collection name and lowest/highest floor price from VIEW. 
def useView(order):
  if order == "cheapest":
    sortOrder = "ASC"
  elif order == "expensive":
    sortOrder = "DESC"

  #Ethereum floor price
  query = f"SELECT EthereumName, EthereumFloorPrice FROM {dbName} . DetailsView ORDER BY EthereumFloorPrice {sortOrder} LIMIT 10"
  cursor.execute(query)
  ethFloorPrice = cursor.fetchall()

  # Polygon floor price
  query = f"SELECT PolygonName, PolygonFloorPrice FROM {dbName} . DetailsView ORDER BY PolygonFloorPrice {sortOrder} LIMIT 10"
  cursor.execute(query)
  polygonFloorPrice = cursor.fetchall()

  return ethFloorPrice, polygonFloorPrice

createDatabase()