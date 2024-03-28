import requests
from bs4 import BeautifulSoup
import csv
from pathlib import Path

OUTPUT_CSV_DIR = Path(__file__).resolve().parents[1] / "output_csv"
OUTPUT_CSV_FILE = OUTPUT_CSV_DIR / "output.csv"

base_url = "https://www.tabroom.com/index/tourn/results/round_results.mhtml?tourn_id={tourn_id}&round_id={round_id}"
name_of_rounds = ["Finals", "Semis", "Round 3", "Round 2", "Round 1"]
num_rounds = len(name_of_rounds)
tourn_id = 30030
largest_round_id = 1171709
round_ids = range(largest_round_id, largest_round_id - num_rounds - 1, -1)

def scrape_all_buttons(tourn_id: int, largest_round_id: int, num_rounds: int, base_url: str, name_of_rounds: list[str]) -> None:
    assert num_rounds > 0
    with requests.Session() as session, open('output.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['round_name', 'group_number', 'speaker_number', 'speaker_name', 'school_name'])
        rounds = range(largest_round_id, largest_round_id - num_rounds - 1, -1)
        tourn_url = base_url.replace("{tourn_id}", str(tourn_id))
        
        for curr_round_id, round_name in zip(rounds, name_of_rounds):
            url = tourn_url.replace("{round_id}", str(curr_round_id))

            response = session.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                rows = soup.find_all('tr')
                for row in rows:
                    columns = row.find_all('td')
                    if len(columns) == 0:  # doesn't correspond to a row of speaker rankings
                        continue
                    column_texts = [col.get_text(strip=True) for col in columns]
                    writer.writerow([round_name] + column_texts)

            else:
                print(f"Failed to retrieve data for round_id {curr_round_id}")


if __name__ == "__main__":
    scrape_all_buttons(tourn_id, largest_round_id, num_rounds, base_url, name_of_rounds)
    pass