
import requests
from bs4 import BeautifulSoup
import urllib.request
import os
import botocore
import boto3




######################################################################################################################################################
# S3 related
######################################################################################################################################################


def save_to_s3(file_path, bucket_name, s3_save_path):
    print('Starting Saving to S3 bucket ' + file_path)
    client = boto3.client('s3')
    client.upload_file(file_path, bucket_name, s3_save_path)
    print('Saving to S3 Bucket Ended successfully ' + s3_save_path + file_path)



def check_exist_on_s3(bucket_name, Prefix):
    s3 = boto3.resource('s3')
    try:
        s3.Object(bucket_name, Prefix).load()
    except botocore.exceptions.ClientError as e:
        print(Prefix + " doesn.t exist")
        return False
    else:
        print(Prefix + " exist")
        return True






######################################################################################################################################################
# Requests and BeautifulSoup
#####################################################################################################################################################


def get_url_folder_content(web_url):
    grab = requests.get(web_url)
    soup = BeautifulSoup(grab.text, 'html.parser')
    links = []
    # traverse paragraphs from soup

    for link in soup.find_all("a"):
        data = link.get('href')
        if ("?") not in data.lower() and data not in web_url:
            links.append(data)

    return links


def download_file(src ,dst):
    print("Downloading " + src)
    urllib.request.urlretrieve(src, dst)


######################################################################################################################################################


def main(event):
    """Main functions

    Args:
            event (int): dict containing:
            - "bucket_name": name of the S# bucket
            - "links": list of AOML links to download from one for "noaa" and one for "metop
            - "key3": fixed with "value3" can be changed if used for a different site or changed the website structure

    Usage:
            event = {
                  "bucket_name": "rfims-prototype",
                  "link": [
                    "https://dbps.aoml.noaa.gov/products/noaa/",
                    "https://dbps.aoml.noaa.gov/products/metop/"
                  ],
                  "key3": "value3"
                }

            main(event)

    output will be saved to:
                "bucket_name/stand_alone/AOML/"Satellite_name same as in AOML site"/Row_data/"same folder name is in the site"
    example:
                "s3://rfims-prototype/stand_alone/AOML/NOAA19/Row_data/level0/NOAA19.20230627.003945.hrpt"

    """


    print("starting")


    bucket_name = event["bucket_name"]

    web_links = event["link"]



    list_of_links = web_links

    flag = True
    while flag:
        new_list = []
        # print(list_of_links)
        lists_len = len(list_of_links)
        counter = 0
        for web_link in list_of_links:
            folders = get_url_folder_content(web_link)

            if len(folders) > 0:
                for folder in folders:
                    if "." not in folder:

                        new_list.append(web_link + folder)
                    else:
                        counter +=1
                        searchword = web_link.split("products/")[-1].split("/")[0].lower()
                        sat_name = None
                        if searchword in folder.lower():
                            part2_name = folder.lower().split(searchword)[-1][0:3]
                            if "19" in part2_name:
                                sat_name = searchword + "19"
                            elif "18" in part2_name:
                                sat_name = searchword + "18"
                            elif "c" in part2_name:
                                sat_name = searchword + "c"
                            elif "b" in part2_name:
                                sat_name = searchword + "b"
                        if sat_name:
                            Prefix = "stand_alone/AOML/"+sat_name.upper() + "/Row_data/"+web_link.split("/")[-2] + "/" + folder
                            # exist_list = list_s3_files_v2(bucket_name, Prefix)

                            s3_save_path = Prefix
                            # if folder not in exist_list:
                            if not check_exist_on_s3(bucket_name,s3_save_path):
                                file_local_path = "/tmp/" + folder
                                download_file(web_link+ folder, file_local_path)
                                print("Downloading " + web_link+ folder)

                                save_to_s3(file_local_path, bucket_name, s3_save_path)
                                os.remove(file_local_path)
                            else:
                                print(s3_save_path + " already exists")
                        else:
                            print(folder + "has No satellite name")
            else:
                counter +=1

        if counter == lists_len:
            flag = False
        else:
            list_of_links = new_list




    return {
        'body': 'All files are downloaded'
    }


event = {
  "bucket_name": "rfims-prototype",
  "link": [
    "https://dbps.aoml.noaa.gov/products/noaa/",
    "https://dbps.aoml.noaa.gov/products/metop/"
  ],
  "key3": "value3"
}


main(event)



