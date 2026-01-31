import datetime

def generate_order_number(pk):
    current_date = datetime.datetime.now().strftime('%Y%m%d%H%M%S') # 20260120 + pk
    number = current_date+str(pk)
    print(number)
    return number