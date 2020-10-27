from extract_emails import EmailExtractor
from extract_emails.browsers import RequestsBrowser
import csv
import os
from googlesearch import search
import pandas as pd


def touch(path):
    with open(path, 'a'):
        os.utime(path, None)

#input_files = os.listdir("input")


files = os.listdir("USA")
for file in files:
    read_path = "USA/" + str(file)
    data = pd.read_csv(read_path)

    print(data.columns)
    names = data.name.tolist()
    page_depth = 2

    for name in names:
        dict1 = {}
        csv_file = "output/usa1.csv"
        # touch(csv_file)
        print(name)
        for url in search(name + str("email id"), stop=1):
            print(url)
        with RequestsBrowser() as browser:
            email_extractor = EmailExtractor(url, browser, depth=page_depth)
            emails = email_extractor.get_emails()
        for email in emails:
            dict1 = {}
            print(email.email)

            dict1 = {name:email.email}
            df = pd.DataFrame.from_dict(dict1,orient='index')
            with open(csv_file,'a') as f: 
                df.to_csv(f,mode='a') 