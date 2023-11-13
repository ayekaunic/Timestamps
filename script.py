# imports
import os
import pandas as pd
from PIL import Image
from datetime import datetime

# functions
def get_image_date_time(filename):
    try:
        with Image.open(filename) as img:
            exif_data = img._getexif()
            if exif_data:
                # 0x9003 represents the DateTimeOriginal field in EXIF data
                if 0x9003 in exif_data:
                    date_time = exif_data[0x9003]
                    return date_time
    except (AttributeError, KeyError, IndexError):
        pass
    return None



def format_date_time(date_time):
    try:
        date_time_obj = datetime.strptime(date_time, '%Y:%m:%d %H:%M:%S')
        formatted_date_time = date_time_obj.strftime('%I:%M %p, %d %B %Y')
        return formatted_date_time
    except ValueError:
        return None



def create_image_dataframe(folder_path):
    image_data = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        date_time = get_image_date_time(file_path)
        if date_time:
            formatted_date_time = format_date_time(date_time)
            if formatted_date_time:
                image_data.append({'Filename': filename, 'Date_Time': formatted_date_time})
        else:
            image_data.append({'Filename': filename, 'Date_Time': 'Not found'})

    df = pd.DataFrame(image_data)
    return df



# extracting timestamps and saving to csv
folder_path = "./images/"
image_dataframe = create_image_dataframe(folder_path)
image_dataframe.to_csv('timestamps.csv', index=False)