import requests
import re
import numpy as np
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

url = "https://www.tabroom.com/index/tourn/results/event_results.mhtml?tourn_id=26661&result_id=276436"

# cmp stands for competitor
# with open(url, 'r') as f: # r = read mode
#     doc = BeautifulSoup(f, "html.parser")
# 
# print(doc)

response = requests.get(url)
# print(response.content)
soup = BeautifulSoup(response.content, 'html.parser')

all_elements = soup.find_all('td', class_='rightalign smallish')
# print(soup.get_text()[:100])
# print(len(all_elements))
ptn = r'\n.+(\d)\s(\d)\n'

def get_nums(s):
    s_text = str(s.text)
    if len(s_text) == 1: # empty string
        return 0
    else:
        match_obj = re.match(ptn, s_text)
        # print(f"match_obj is {match_obj}")
        num1, num2 = match_obj.group(1, 2)
        return int(num1) + int(num2)

counter = 0 # for each competitor
big_list = np.array([])
cmp_rankings = np.array([])
for idx, element in enumerate(all_elements):
    if (idx + 1) % 8 == 0 or (idx + 2) % 8 == 0:
        continue
    # print(element.text)
    # print(idx, element)
    # print(get_nums(element))
    curr_ranking = get_nums(element)
    cmp_rankings = np.append(cmp_rankings, curr_ranking)
    if counter == 6: # found one competitor
        cmp_sum = np.sum(cmp_rankings)
        # print(cmp_rankings)
        # print(f"cmp_sum is {cmp_sum}")
        big_list = np.append(big_list, cmp_sum)
        cmp_rankings = np.array([])
        counter = 0
    counter += 1


big_list = np.sort(big_list)
less_35 = np.count_nonzero(big_list <= 35)
less_45 = np.count_nonzero(big_list <= 45)
                           
print(big_list)
print(f"number of competitors is {len(big_list)}")
print(f"60th highest ranking is {big_list[59]}")
print(f"number of competitors <= 35 is {less_35}")
print(f"number of competitors > 35 and <= 45 is {less_45 - less_35}")
plt.rcParams.update({'figure.figsize':(7,5), 'figure.dpi':200})
plt.hist(big_list, bins=20)
plt.gca().set(title='NSDA OO Prelims Ranking Distribution', ylabel='Count', xlabel='Sum of rankings');
plt.show()
