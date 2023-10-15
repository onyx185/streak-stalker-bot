import datetime

def get_date(date_str:str, separator: str):
    #dd-mm-yyyy
    date_arr = date_str.split(separator)
    return datetime.date(int(date_arr[2]),int(date_arr[1]), int(date_arr[0]))