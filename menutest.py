import requests
import json
import time

class Menu:
    current_page = 1
    previous_page = 0

    def __init__(self, slug_dispo):
        self.api_call = 'https://api-g.weedmaps.com/discovery/v1/listings/dispensaries/' + slug_dispo + '/menu_items?page=' + str(
            self.current_page) + '&page_size=150&limit=150 '
        self.api_response = requests.get(self.api_call)
        self.api_response_parsed = json.loads(self.api_response.text)
        self.menu_count = self.api_response_parsed['meta']['total_menu_items']
        self.slug_dispo = slug_dispo

    def get_menu_data(self, total_menu_items, page_num):
        self.api_call = 'https://api-g.weedmaps.com/discovery/v1/listings/dispensaries/' + self.slug_dispo + '/menu_items?page=' + str(
            self.current_page) + '&page_size=150&limit=150 '
        self.api_response = requests.get(self.api_call)
        self.api_response_parsed = json.loads(self.api_response.text)
        return self.api_response_parsed['data']['menu_items']

    def load_menu_data(self):
        print('Starting on ' + str(self.slug_dispo) + ' processing ...')
        time.sleep(1.5)
        self.menu_item_count = 0
        self.count_max_item_in_page = 150
        while self.current_page > self.previous_page:
            self.dispo_menu_data = self.get_menu_data(self.menu_count, self.current_page)
            for self.menu_item in self.dispo_menu_data:
                self.menu_item_count += 1
                self.menu_price_unit, self.menu_price_unit_price = next(iter(self.menu_item['prices'].items()))
                #if isinstance(self.menu_price_unit_price, (int, float)): print((self.menu_item['name'] + " No Price Online"))
                if isinstance(self.menu_price_unit_price, list):
                    self.tempString = ''
                    for i in self.menu_price_unit_price:
                        self.tempString += str(i['units']) + " " + str(i['price']) + " "
                    print(self.menu_item['name'] + " " + self.menu_price_unit + " " + self.tempString)
                #elif isinstance(v, dict): print(type(v))
                    #print(str(k) + "    " + str(v[0]['price']) + " measurement:" + str(v[0]['units']))
#                else : print(v[0])
#                print(str(self.menu_item['name']) + " " + str(k) + " : " + str(v))
                if self.menu_item_count == self.count_max_item_in_page:
                    self.current_page += 1
                    self.count_max_item_in_page += 150
                    break
            if self.menu_item_count == self.menu_count:
                break
        print(self.menu_count)
        print(self.slug_dispo + ' menu parsing complete!')
        time.sleep(1.5)


caliroots = Menu('cali-roots-3')
caliroots.load_menu_data()

fireleaf = Menu('fire-leaf-dispensary-stockyard')
fireleaf.load_menu_data()
