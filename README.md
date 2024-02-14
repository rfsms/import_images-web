this folder consists of:
1. Python file:
    1. <Pull_Images_From_AOML.py>



* functions in "Pull_Images_From_AOML.py" "script:
    a func. to save downloaded images to s3 <save_to_s3>
    a func. to check if the image exist on S3 side <check_exist_on_s3>
    a func. to download the image locally <download_file>
    a func. to get images url from the provided website link <get_url_folder_content>
    a func. Main function to call other functions when needed  <main>






Main functions Args:
    event: a dict containing:
        - "bucket_name": name of the S3 bucket
        - "links": list of AOML links to download from one for "noaa" and one for "metop
        - "key3": fixed with "value3" can be changed if used for a different site or changed the website structure




Main functions Usage:
        event = {
              "bucket_name": "rfims-prototype",
              "link": ["https://dbps.aoml.noaa.gov/products/noaa/","https://dbps.aoml.noaa.gov/products/metop/"],
              "key3": "value3"
                }

        main(event)




output will be saved to:
                "bucket_name/stand_alone/AOML/"Satellite_name same as in AOML site"/Row_data/"same folder name is in the site"
    example:
                "s3://rfims-prototype/stand_alone/AOML/NOAA19/Row_data/level0/NOAA19.20230627.003945.hrpt"


