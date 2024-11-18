import requests
import re
from bs4 import BeautifulSoup

def player_transfer_response(player_id : int):
    response = {
        "name" : get_player_name(player_id), 
        "transfers" : get_player_transfers(player_id)
    }
    
    return response


def get_player_transfers(player_id : int):
    headers = {"User-Agent": 
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/113.0.0.0 "
                        "Safari/537.36"
    }  
    
    res = requests.get(f"https://www.transfermarkt.co.uk/ceapi/transferHistory/list/{player_id}" , headers=headers)
    
    json_res = res.json()
    
    transfer_list = json_res["transfers"]
    
    transfers = []
    
    for transfer in transfer_list:
        current_club = transfer["from"]["clubName"]
        current_club_badge = transfer["from"]["href"]
        new_club = transfer["to"]["clubName"]
        new_club_badge = transfer["to"]["href"]
        
        if valid_transfer(current_club, new_club):
            transfers.append({
                "to" : {
                    "club" : new_club,
                    "badge" : get_badge(new_club_badge)
                },
                "from" : {
                    "club" : current_club,
                    "badge" : get_badge(current_club_badge)
                },
                "fee" : transfer["fee"]
            })
            
    
    return transfers

def get_badge(url : str):   
    url_array = url.split("/")
    for i in range(len(url_array)):
        if url_array[i] == "verein":
            return f"https://tmssl.akamaized.net//images/wappen/head/{url_array[i+1]}.png"
    
    return None
           
def get_player_name(player_id : int):
    headers = {
         "User-Agent": 
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/113.0.0.0 "
                    "Safari/537.36"
    }
    
    res = requests.get(f'https://www.transfermarkt.co.uk/-/profil/spieler/{player_id}', headers=headers)
    
    soup = BeautifulSoup(res.text, "html.parser")
    
    tree = soup.find(attrs={
        "class" : "data-header__headline-wrapper"
    })
    
    text_arr = tree.text.strip().split(" ")
    
    filtered_text = [] 
    
    for text in text_arr:
        cleaned_text = text.replace("\n", "")
        if re.match(r'^([A-Z]|[a-z])+', cleaned_text):
            filtered_text.append(cleaned_text)

    res_text = ' '.join(filtered_text)
    
    return res_text
    
def valid_transfer(currentClub, newClub):
    youth_abr = set(("Youth", "Yth"))
    currentClub_set = set(currentClub.split())
    newClub_set = set(newClub.split())

    if currentClub_set & newClub_set:
        return False
    
    if youth_abr & (currentClub_set | newClub_set):
        return False 
    
    else:
        if any(re.search(r'^U[0-9]+', val) for val in currentClub_set | newClub_set):
            return False
        
    return True
