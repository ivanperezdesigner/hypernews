from datetime import datetime
import random

def assign_new_link(links_list):
    new_link = random.randint(1, 99999999)
    while new_link in links_list:
        new_link = random.randint(1, 99999999)
    return new_link

print(assign_new_link())