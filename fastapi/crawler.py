import requests
from bs4 import BeautifulSoup

users = [
    "강성우", "강성원", "고예준", "권보연", "김기연(13기)", "김동영(13기)", "김송희", "김은지", "김지윤", "김태양",
    "김택우", "김현석", "문경태", "문성준", "박정식", "박철준", "박현준", "변정희", "송희원", "신예지", "심수민",
    "안승현", "양준헌", "오원영", "오지훈", "윤태호", "이새나", "이승대", "이승현(13기)", "이재준", "이창현(13기)",
    "이한선", "임영서", "임학수", "전성현", "정민규(13기)", "차원제", "최유정", "하진우", "함준형"
]

base_url = "https://kitribob.wiki/wiki/"

def get_user_info(user_name):
    if user_name not in users:
        return {"error": "User not found in the list."}
    

    user_url = base_url + requests.utils.quote(user_name)
    
    try:
        response = requests.get(user_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
    
        table = soup.find('table', {'class': 'wikitable'})
        if not table:
            return {"error": "No data table found for the user."}
        
        user_info = {'name': user_name}
        rows = table.find_all('tr')

        for row in rows:
            cells = row.find_all(['th', 'td'])
            if len(cells) == 2:
                key = cells[0].get_text(strip=True)
                value = cells[1].get_text(strip=True)
                user_info[key] = value
            elif len(cells) == 1: 
                key = cells[0].get_text(strip=True)
                user_info[key] = None 
        
        return user_info
    
    except requests.exceptions.HTTPError as errh:
        return {"error": f"HTTP Error: {errh}"}
    except requests.exceptions.ConnectionError as errc:
        return {"error": f"Error Connecting: {errc}"}
    except requests.exceptions.Timeout as errt:
        return {"error": f"Timeout Error: {errt}"}
    except requests.exceptions.RequestException as err:
        return {"error": f"An error occurred: {err}"}
