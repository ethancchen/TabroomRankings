import requests
import re
import numpy as np
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

# TODO: implement searching for url with text fields later
id = "276618" # can change
url = f"https://www.tabroom.com/index/tourn/results/event_results.mhtml?tourn_id=26661&result_id={id}"

# cmp stands for competitor

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

all_elements = soup.find_all('td', class_='rightalign smallish')
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
    if idx % 13 in list(range(6, 13)):
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
less_36 = np.count_nonzero(big_list < 36)
leq_44 = np.count_nonzero(big_list <= 44)
counts = np.unique(big_list, return_counts=True)

print(big_list)
print(f"number of competitors is {len(big_list)}")
print(f"60th highest ranking is {big_list[59]}")
print(f"number of competitors < 36 is {less_36}")
print(f"number of competitors <= 44 is {leq_44}")
print(f"number of competitors >= 36 and <= 44 is {leq_44 - less_36}")
for i, j in zip(counts[0], counts[1]):
    print(int(i), j)
plt.rcParams.update({'figure.figsize':(7,5), 'figure.dpi':200})
plt.hist(big_list, bins=20)
plt.gca().set(title='NSDA OO Prelims Ranking Distribution', ylabel='Count', xlabel='Sum of rankings')
#plt.show()
