import re 

def is_valid_phone(phone):
    if re.fullmatch('\d+', phone) != None : 
        return True
    else :
        return False

def is_valid_urls(urls):
    for url in urls :
        if re.fullmatch("https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+/*", url) == None:
            return False
    return True




