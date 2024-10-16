#coding part
from datetime import datetime

#function to create full inventory
def creat_full(invent):
    sorte = list(invent.keys())

    for i in range(len(sorte)):
        for j in range(i + 1, len(sorte)):
            if invent[sorte[i]]['company'] > invent[sorte[j]]['company']:
                temp = sorte[i]
                sorte[i] = sorte[j]
                sorte[j] = temp

            elif invent[sorte[i]]['company'] == invent[sorte[j]]['company']:
                if invent[sorte[i]]['item'] > invent[sorte[j]]['item']:
                    temp = sorte[i]
                    sorte[i] = sorte[j]
                    sorte[j] = temp
                
                elif invent[sorte[i]]['item'] == invent[sorte[j]]['item']:
                    if int(sorte[i]) > int(sorte[j]):
                        temp = sorte[i]
                        sorte[i] = sorte[j]
                        sorte[j] = temp

    with open('FullInventory.txt', 'w') as ffile: #open in write mode
        for k in sorte: #loop through sorted
            price = invent[k].get('price', '') #retrieve price, if missing, return empty
            serv = invent[k].get('service_date','') #retrieve service date, if missing, return empty
            line = f"{k},{invent[k]['company']},{invent[k]['item']},{price},{serv}" # create line
            if invent[k]['damage']: #check if damaged
                line += ',damaged' #if damaged, add "damaged"
            print("Writing line to file: ", line)
            
            ffile.write(line + '\n') #write the line to the file


def create_itemtype(invent):
    item_types = {} #create dictionary to hold item types

    for item_id in invent: #iterate over ID's
        item_info = invent[item_id] #access details of current item
        item_type = item_info['item'] #details of item
        if item_type not in item_types: #if item type not yet in dictionary
            item_types[item_type] = [] #make empty list for type
        item_types[item_type].append(item_id) #add item id to type
        
    for item_type in item_types: #loop through each item
        item = item_types[item_type] #get list of items for current type
        item.sort() #sort items by ID
        with open(f"{item_type}Inventory.txt", 'w') as ifile: #create file for current type
            for item_id in item: #loop through id in list
                item_info = invent[item_id] #details of current
                price = item_info.get('price', '') #retrieve price, empty if null
                serv = item_info.get('service_date','') #retrieve service date, empty if null
                line = f"{item_id},{item_info['company']},{price},{serv}" #make line
                if item_info['damage']: #check if damaged
                    line += ',damaged' #appened damage 
                ifile.write(line + '\n') #write to file



def create_pastserv(invent): #this part highkey kinda confused me, 
                                                  #it says the date that the program is executed in the instructions so 
                                                  #i hope im doing this right
    past_serv_item = [] #list to store past service dates

    today = datetime.today().strftime('%m/%d/%Y')

    today_split = today.split('/') #split by '/' seperating the numbers
    today_month = int(today_split[0]) #convert month, day, and year into integers
    today_day = int(today_split[1])
    today_year = int(today_split[2])

    for o in invent: #loop over inventory
        if 'service_date' in invent[o]: #if item has a service date
            service_date = invent[o]['service_date'] #get the service date
            serv_split = service_date.split('/') #split serv date by '/'
            serv_month = int(serv_split[0]) #turn service dates into integers
            serv_day = int(serv_split[1])
            serv_year = int(serv_split[2])

        if serv_year < today_year: #if service year before today
            past_serv_item.append(o) #add to list
        elif serv_year == today_year: #if year is the same
            if serv_month < today_month: #if service month is before today
                past_serv_item.append(o) #add to list
            elif serv_month == today_month: #if month is same
                if serv_day < today_day: #if service day is before today
                    past_serv_item.append(o) #add to list

    for i in range(len(past_serv_item)): #sort by date
        for j in range(i + 1, len(past_serv_item)):
            serv_datei = invent[past_serv_item[i]]['service_date'].split('/')
            serv_monthi = int(serv_datei[0])
            serv_dayi = int(serv_datei[1])
            serv_yeari = int(serv_datei[2])

            serv_datej = invent[past_serv_item[j]]['service_date'].split('/')
            serv_monthj = int(serv_datej[0])
            serv_dayj = int(serv_datej[1])
            serv_yearj = int(serv_datej[2])

            if (serv_yeari > serv_yearj) or (serv_yeari == serv_yearj and serv_monthi > serv_monthj) or (serv_yeari == serv_yearj and serv_monthi == serv_monthj and serv_dayi > serv_dayj):
                temp = past_serv_item[i]
                past_serv_item[i] = past_serv_item[j]
                past_serv_item[j] = temp


    with open('PastServiceDateInventory.txt', 'w') as pfile: #open file in write mode
        for o in past_serv_item: #loop through sorted
            price = invent[o].get('price', '') #get price, if empty none
            service_date = invent[o]['service_date'] #get service date
            line = f"{o},{invent[o]['company']},{invent[o]['item']},{price},{service_date}" #create line
            if invent[o]['damage']: #check if damaged
                line += ',damaged' #if damaged, appened
            pfile.write(line + '\n') #write line to file


def create_damaged(invent):
    d_items = [] #list to store damaged

    for o in invent: #loop through each item
        if invent[o]['damage']: #if item is damaged
            d_items.append(o) #add to list 
#sort highest to lowest
    for i in range(len(d_items)): 
        for j in range(i + 1, len(d_items)):
            price_i = float(invent[d_items[i]].get('price', 0)) #get price of current
            price_j = float(invent[d_items[j]].get('price', 0)) #get price of next
            if price_i < price_j: # if current is cheaper, swap
                temp = d_items[i] 
                d_items[i] = d_items[j]
                d_items[j] = temp

    with open('DamagedInventory.txt', 'w') as dfile:
        for o in d_items:
            price = invent[o].get('price', '')
            serv = invent[o].get('service_date', '')
            line = f"{o},{invent[o]['company']},{invent[o]['item']},{price},{serv}"
            dfile.write(line + '\n')







def readmanufacturer():
    invent = {} #dictionary to store inventory

    with open('ManufacturerList.txt', 'r') as mfile: #read mode manufacturer list
        for line in mfile: #over each line
            split = line.strip().split(',') #split line (comma)
            id = split[0] #first is item id
            company = split[1] #second is company name
            item = split[2] #third is item having

            damage = len(split) > 3 and split[3] == 'damaged'


            #item id is key in dictionary 
            invent[id] = {
                'company': company, 'item' : item, 'damage' : damage
            }
    return invent #return inventory dictionary after reading all lines


def readprice(invent):
    with open('priceList.txt', 'r') as pfile: #open price text file on read
        for line in pfile: #loop over file
            split = line.strip().split(',') #strip and split by comma
            id = split[0] #first is id
            price = split[1] # second is item price

            if id in invent: #if item id exists in inventory
                invent[id]['price'] = price # add price to dictionary under price

def readservice(invent):
    with open('ServiceDatesList.txt', 'r') as sfile: #open servicedatelist in read mode
        for line in sfile: #loop over lines in file
            split = line.strip().split(',') #strip and split by comma
            o = split[0] #item id
            serv = split[1] #service date

            if o in invent: #if item in inventory
                invent[o]['service_date'] = serv #add service date to item in inventory


def main():
    invent = readmanufacturer()
    readprice(invent)
    readservice(invent)
    creat_full(invent)
    create_itemtype(invent)
    create_pastserv(invent)
    create_damaged(invent)

if __name__ == "__main__":
    main()




