import os
from datetime import date, datetime

PATH = r'/Users/darrenpaul/Documents/Development/learning-selenium/modules/configs/following.txt'

followers = []
with open(PATH) as doc:
    for line in doc.readlines():
        followers.append(line.strip())

aaa = []
for i in followers:
    new = '{0}  {1}'.format(i, date.today())
    aaa.append(new)
for a in aaa:
    with open(PATH, 'a') as doc:
        doc.write('{0}\n'.format(a))
