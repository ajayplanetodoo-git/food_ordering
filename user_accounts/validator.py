from django.core.exceptions import ValidationError
import os


'''
This is my customeform validation function for 
'''
def img_field_validation(value):
    ext = os.path.splitext(value.name)[1]
    print(ext)
    ext_list = ['.png','.jpg','.jpeg']
    if ext.lower() not in ext_list:
        raise  ValidationError("Wrong file type! it only allow"+str(ext_list))
