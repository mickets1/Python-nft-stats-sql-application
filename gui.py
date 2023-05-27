import PySimpleGUI as sg
import database

def gui():
  tablesnames = database.tableNames()

  layout = [
          [sg.Text("Aggregation:"), sg.Radio("MAX", "agg", default=False, key="-MAX-"), sg.Radio("MIN", "agg", default=False, key="-MIN-"), sg.Radio("AVG", "agg", default=False, key="-AVG-")],
          [sg.Text("Chain:"), sg.Radio(tablesnames[0], "ALL", default=False, key="-IN1-"), sg.Radio(tablesnames[1], "ALL", default=False, key="-IN2-"), sg.Radio(tablesnames[2], "ALL", default=False, key="-IN3-"), sg.Radio(tablesnames[3], "ALL", default=False, key="-IN4-")],
          [sg.Text("")],
          [sg.Text('Search collection(ex alien, crypto, ape)')],
          [sg.Text('Collection:', size =(10, 1)), sg.InputText()],
          [sg.Text("")],
          [sg.Radio("Show top 10 collections with the most owners", "mostowners", default=False, key="-top10-")],
          [sg.Radio("Find low supply NFT's", "unique", default=False, key="-unique-")],
          [sg.Text("")],
          [sg.Text("No need to select a blockchain for the ones below:")],
          [sg.Text("View floorPrice(Ethereum, Polygon): ")],
          [sg.Text("  Sort order: "), sg.Radio("Cheapest", "ALL", default=False, key="-cheapest-"), sg.Radio("Most expensive", "ALL", default=False, key="-expensive-")],
          [sg.Text("")],
          [sg.Radio("Show the top 5 ranked collections", "ALL", default=False, key="-top5-")],
          [sg.Text("")],
          [sg.Text("Display and compare user tracked collections: ")],
          [sg.Text("User Stats: "), sg.Radio("users", "ALL", default=False, key="-users-")],
          [sg.Text("")],
          [sg.Button("Submit"), sg.Button("Reset"), sg.Button("Clear Textbox")],
          [sg.Output(size=(90, 80), key = 'output')]
          ]

  # Create the window
  window = sg.Window('Opensea NFT Statistics', layout, size=(900,1000))

  # Create an event loop
  while True:
      event, values = window.read()
      # End program if user closes window or
      # presses the OK button
      if event == "OK" or event == sg.WIN_CLOSED:
          break

      if event == 'Reset':
        # Reset chains
        window["-IN1-"].reset_group()
        # Reset aggregations/grouping
        window["-MAX-"].reset_group()
        window["-unique-"].reset_group()
        window["-top10-"].reset_group()
        # No need to further process selections
        continue

      if event == 'Clear Textbox':
        window.FindElement('output').Update("")
        continue
        
    # Single table aggregations:
      elif values["-MAX-"] == True:
        print("Function: change24h()")
        aggregation = "MAX"
        prefix = "Highest 24h: "

        if values["-IN1-"] == True:
          print(prefix + database.change24h(aggregation, tablesnames[0]))
        elif values["-IN2-"] == True:
          print(prefix + database.change24h(aggregation, tablesnames[1]))
        elif values["-IN3-"] == True:
          print(prefix + database.change24h(aggregation, tablesnames[2]))
        elif values["-IN4-"] == True:
          print(prefix + database.change24h(aggregation, tablesnames[3]))
        else:
          print("Select a blockchain")

      elif values["-MIN-"] == True:
        print("Function: change24h()")
        aggregation = "MIN"
        prefix = "Lowest 24h: "

        if values["-IN1-"] == True:
          print(prefix + database.change24h(aggregation, tablesnames[0]))
        elif values["-IN2-"] == True:
          print(prefix + database.change24h(aggregation, tablesnames[1]))
        elif values["-IN3-"] == True:
          print(prefix + database.change24h(aggregation, tablesnames[2]))
        elif values["-IN4-"] == True:
          print(prefix + database.change24h(aggregation, tablesnames[3]))
        else:
          print("Select a blockchain")

      elif values["-AVG-"] == True:
        print("Function: change24h()")
        aggregation = "AVG"
        prefix = "Average 24h: "

        if values["-IN1-"] == True:
          print(prefix + database.change24h(aggregation, tablesnames[0]))
        elif values["-IN2-"] == True:
          print(prefix + database.change24h(aggregation, tablesnames[1]))
        elif values["-IN3-"] == True:
          print(prefix + database.change24h(aggregation, tablesnames[2]))
        elif values["-IN4-"] == True:
          print(prefix + database.change24h(aggregation, tablesnames[3]))
        else:
          print("Select a blockchain")
    # End Single table aggregations.

      # Find collection name.
      if values[0]:
        print("Function: findCollectionName()")
        matches = []

        if values["-IN1-"]  == True:
          matches = database.findCollectionName(tablesnames[0], values[0])
        elif values["-IN2-"] == True:
          matches = database.findCollectionName(tablesnames[1], values[0])
        elif values["-IN3-"] == True:
          matches = database.findCollectionName(tablesnames[2], values[0])
        elif values["-IN4-"] == True:
          matches = database.findCollectionName(tablesnames[3], values[0])
        else:
          print("Select a blockchain")
          continue

        # Print collection matches
        if len(matches[1]) > 0:
          print(matches[0] + ": " )
          for match in matches[1]:
            print(match[0])

        else:
          print("No Matches")
          
      # Display the top 5 collections across all blockchains.
      if values["-top5-"] == True:
        print("Function: top5RankedCollections()")
        collections = database.top5RankedCollections()
        
        for collection in collections:
          print("Rank: " + str(collection[0]))
          print(f" {tablesnames[0]}\n  Name: {collection[1]}\n  Number of owners: {str(collection[2])}\n")
          print(f" {tablesnames[1]}\n  Name: {collection[4]}\n  Number of owners: {str(collection[5])}\n")
          print(f" {tablesnames[2]}\n  Name: {collection[7]}\n  Number of owners: {str(collection[8])}\n")
          print(f" {tablesnames[3]}\n  Name: {collection[10]}\n  Number of owners: {str(collection[11])}\n")

      if values["-top10-"] == True:
        print("Function: findmostOwners()")
        if values["-IN1-"]  == True:
          uniqueNFTs = database.findmostOwners(tablesnames[0])
        elif values["-IN2-"] == True:
          uniqueNFTs = database.findmostOwners(tablesnames[1])
        elif values["-IN3-"] == True:
          uniqueNFTs = database.findmostOwners(tablesnames[2])
        elif values["-IN4-"] == True:
          uniqueNFTs = database.findmostOwners(tablesnames[3])
        else:
          print("Select a blockchain")
          continue

        for nft in uniqueNFTs:
          print(f"Name: {nft[0]}, Owners: {nft[1]}")

      if values["-unique-"] == True:
        print("Function: findLowSupply()")
        if values["-IN1-"]  == True:
          uniqueNFTs = database.findLowSupply(tablesnames[0])
        elif values["-IN2-"] == True:
          uniqueNFTs = database.findLowSupply(tablesnames[1])
        elif values["-IN3-"] == True:
          uniqueNFTs = database.findLowSupply(tablesnames[2])
        elif values["-IN4-"] == True:
          uniqueNFTs = database.findLowSupply(tablesnames[3])
        else:
          print("Select a blockchain")
          continue

        for nft in uniqueNFTs:
          print(f"Name: {nft[0]}, Total supply: {nft[1]}")

      if values["-cheapest-"] == True:
        print("useView()")
        cheapestCollections = database.useView("cheapest")

        for (eth, poly) in zip(cheapestCollections[0], cheapestCollections[1]):
          print(tablesnames[0])
          print("Name: " + eth[0] + " Floor price: " + str(eth[1]))
          print(tablesnames[1])
          print("Name: " + poly[0] + " Floor price: " + str(poly[1]))
          print("")

      elif values["-expensive-"] == True:
        print("useView()")
        expensiveCollections = database.useView("expensive")

        for (eth, poly) in zip(expensiveCollections[0], expensiveCollections[1]):
          print(tablesnames[0])
          print("Name: " + eth[0] + " Floor price: " + str(eth[1]))
          print(tablesnames[1])
          print("Name: " + poly[0] + " Floor price: " + str(poly[1]))
          print("")

      if values["-users-"] == True:
        print("userCollectionStats()")
        userStats = database.userCollectionStats()
        
        for d in userStats:
          print("Username: " + d[0])
          print("Collection: " + d[1])
          print("Blockchain: " + d[2])

          if d[3] is None:
            i = 4

            while d[i] is None:
              i += 1
            print("One day change: ", d[i])

          else:
            print("One day change: ", d[3])

          print("")

      print("")    

       
  window.close()