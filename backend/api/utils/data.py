import aiohttp
import asyncio
import os
from aiohttp import ClientSession
from requests.exceptions import HTTPError

import uuid
import pandas as pd


class Process:
    def __init__(self,path_to_csv):
        self.raw_data = pd.read_csv(path_to_csv,error_bad_lines=False,encoding = "ISO-8859-1")
        self.loop = asyncio.get_event_loop()
       
    def initialize_scrapper(self,):
        base_url = 'https://skools.co.za/listings'
        no_emis_names = self.raw_data.loc[self.raw_data.emis == 0].name.tolist()
        self.urls_to_scrape = [[os.path.join(base_url,'-'.join(name.lower().split())),name]  for name in  no_emis_names]

    @staticmethod
    def extract_emis_from_response(response):
        soup = BeautifulSoup(response.content, 'html.parser')
        s = soup.find_all('p')[0].get_text()
        emis_number = re.findall(r"\D(\d{9})\D", " "+s+" ")[0]
        return emis_number

    def generate_fake_emis(self,):
        fake_emis = int(str(uuid.uuid4().int)[:9])
        if fake_emis in self.raw_data.emis.tolist():
            self.generate_fake_emis()
        return fake_emis
            
    @staticmethod
    async def get_emis_page(url, session):
        try:
            response = await session.request(method='GET', url=url)
            response.raise_for_status()
            print(f"Response status ({url}): {response.status}")
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error ocurred: {err}")
        response_content = await response.content
        return response_content


    async def run_program(self,url,name,session):
        """Wrapper for running program in an asynchronous manner"""
        try:
            response = await self.get_emis_page(url, session)
            emis_number = self.extract_emis_from_response(response)
            self.raw_data['emis'].loc[self.raw_data.name == name] = emis_number
    #         print(f"Response: {json.dumps(parsed_response, indent=2)}")
        except Exception as err:
            self.raw_data['emis'].loc[self.raw_data.name == name] = self.generate_fake_emis()
            
    async def scrape(self,):
        async with ClientSession() as session:
            await asyncio.gather(*[self.run_program(url,name,session) for url,name in self.urls_to_scrape])

    def run_scrapper(self):
        self.loop.run_until_complete(self.scrape())

    def enforce_unique(self,val):
        if val in self.raw_data.emis.tolist():
            return self.generate_fake_emis()

    def make_province(self,center_no):
        return self.province_by_centerNo[int(str(center_no)[0])]

    def run_processing_pipeline(self,):
        # scrape emis numbers from skools website
        self.initialize_scrapper()
        self.run_scrapper()
        # ensure all emis numbers are unique 
        self.raw_data['emis'] = self.raw_data.emis.apply(self.enforce_unique)
        # grant emis numbers to records where emis is "AMIS", LOL! 
        self.raw_data['emis'].loc[self.raw_data.emis.isna()] = [self.generate_fake_emis() for _ in self.raw_data['emis'].loc[self.raw_data.emis.isna()]]
        self.raw_data['emis'] = self.raw_data['emis'].astype(int)
        # data mine and add provinces to dataframe based on the first digit of the center number
        self.province_by_centerNo = {4:"EASTERN CAPE",
                                3:"FREE STATE",
                                8:"GAUTENG",
                                5:"KWAZULU-NATAL",
                                7:"LIMPOPO",
                                6:"MPUMALANGA",
                                9:"NORTH WEST",
                                2:"NORTHERN CAPE",
                                1:"WESTERN CAPE"}

        self.raw_data['province'] = self.raw_data.centre_no.apply(self.make_province)
        # generate pass rate using a generic method that can accomodate for new year data

        # rather leave the fancy things
        # wrote_passed_columns = list(filter(lambda x: x.split('_')[-1].isdigit() and x.split('_')[0] in ['wrote','passed'] , self.raw_data.columns))
        # years = set([value.split('_')[1] for value in wrote_passed_columns])
        # for year in years:
        #     self.raw_data[f'pass_rate_{year}']=round(( getattr(self.raw_data,f'passed_{year}') / getattr(self.raw_data,f'wrote_{year}') )*100,2)

        # fill mising
        self.raw_data = self.raw_data.fillna(-1)
        #  numbers to ints
        self.raw_data[self.raw_data.dtypes[self.raw_data.dtypes=='float'].index.tolist()] = self.raw_data[self.raw_data.dtypes[self.raw_data.dtypes=='float'].index.tolist()].astype(int)




    
