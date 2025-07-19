import requests
from bs4 import BeautifulSoup
import time
import re
import pandas as pd
from urllib.parse import urljoin, urlparse
import sys

def get_event_match_urls(event_url):
    """
    Scrapes all match URLs from a VLR.gg event page
    Returns: List of match URLs
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        print(f"🌐 Fetching event page: {event_url}")
        r = requests.get(event_url, headers=headers, timeout=15)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        
        match_urls = []
        base_url = "https://www.vlr.gg"
        
        # VLR.gg event page selectors for match links
        match_selectors = [
            'a[href*="/match/"]',  # Direct match links
            'a[href*="/matches/"]',  # Alternative match links
            '.wf-card a[href*="/"]',  # Match cards
            '.match-item a',  # Match items
            'tr a[href*="/"]'  # Table rows with links
        ]
        
        print("🔍 Searching for match links...")
        
        for selector in match_selectors:
            links = soup.select(selector)
            for link in links:
                href = link.get('href')
                if href and isinstance(href, str) and ('/match/' in href or re.search(r'/\d+/', href)):
                    # Skip non-match links
                    if any(skip in href for skip in ['forum', 'ranking', 'team', 'player', 'event', 'stats']):
                        continue
                    
                    full_url = urljoin(base_url, href) if href.startswith('/') else href
                    
                    # Only add unique URLs that look like match pages
                    if full_url not in match_urls and re.search(r'/\d+/', full_url):
                        match_urls.append(full_url)
        
        # Filter and clean URLs - keep only match pages
        filtered_urls = []
        for url in match_urls:
            # Must contain numbers (match IDs) and typical VLR match URL pattern
            if re.search(r'/\d+/', url) and ('vlr.gg' in url):
                # Remove duplicates and query parameters
                clean_url = url.split('?')[0].split('#')[0]
                if clean_url not in filtered_urls:
                    filtered_urls.append(clean_url)
        
        print(f"✅ Found {len(filtered_urls)} match URLs")
        
        # Display first few URLs for verification
        if filtered_urls:
            print("📋 Sample URLs found:")
            for i, url in enumerate(filtered_urls[:5]):
                print(f"  {i+1}. {url}")
            if len(filtered_urls) > 5:
                print(f"  ... and {len(filtered_urls) - 5} more")
        
        return filtered_urls
        
    except Exception as e:
        print(f"❌ Error fetching event page: {e}")
        return []

def get_user_input():
    """Get event details from user via CLI"""
    print("🎮 VLR.gg Match Data Extractor")
    print("=" * 50)
    
    # Get event name
    event_name = input("📝 Enter event name (for file naming): ").strip()
    if not event_name:
        event_name = "vlr_matches"
    
    # Get event URL
    print("\n🌐 Event URL Options:")
    print("1. Enter VLR.gg tournament URL (from matches section)")
    print("2. Use pre-defined individual match URLs")
    
    choice = input("\nSelect option (1 or 2): ").strip()
    
    if choice == "1":
        event_url = input("🔗 Enter VLR.gg tournament URL (must include /matches/): ").strip()
        if not event_url:
            print("❌ No URL provided. Exiting...")
            sys.exit(1)
        
        # Extract match URLs from event page
        match_urls = get_event_match_urls(event_url)
        if not match_urls:
            print("❌ No match URLs found. Please check the event URL.")
            sys.exit(1)
            
    else:
        # Use the pre-defined URLs from the script
        match_urls = get_predefined_urls()
        print(f"📋 Using {len(match_urls)} pre-defined match URLs")
    
    return event_name, match_urls

def get_predefined_urls():
    """Return the pre-defined match URLs"""
    return [
        "https://www.vlr.gg/487985/fut-esports-vs-apeks-esports-world-cup-2025-ubqf",
        "https://www.vlr.gg/487986/team-vitality-vs-giantx-esports-world-cup-2025-ubqf",
        "https://www.vlr.gg/487987/natus-vincere-vs-gentle-mates-esports-world-cup-2025-ubqf",
        "https://www.vlr.gg/487988/karmine-corp-vs-koi-esports-world-cup-2025-ubqf",
        "https://www.vlr.gg/487989/fut-esports-vs-team-vitality-esports-world-cup-2025-ubsf",
        "https://www.vlr.gg/487990/natus-vincere-vs-karmine-corp-esports-world-cup-2025-ubsf",
        "https://www.vlr.gg/487992/apeks-vs-giantx-esports-world-cup-2025-lr1",
        "https://www.vlr.gg/487993/gentle-mates-vs-koi-esports-world-cup-2025-lr1",
        "https://www.vlr.gg/488003/100-thieves-vs-furia-esports-world-cup-2025-ubqf",
        "https://www.vlr.gg/488004/leviat-n-vs-nrg-esports-world-cup-2025-ubqf",
        "https://www.vlr.gg/488005/cloud9-vs-2game-esports-esports-world-cup-2025-ubqf",
        "https://www.vlr.gg/488007/100-thieves-vs-nrg-esports-world-cup-2025-ubsf",
        "https://www.vlr.gg/488008/kr-esports-vs-cloud9-esports-world-cup-2025-ubsf",
        "https://www.vlr.gg/488010/furia-vs-leviat-n-esports-world-cup-2025-lr1",
        "https://www.vlr.gg/487991/fut-esports-vs-karmine-corp-esports-world-cup-2025-ubf",
        "https://www.vlr.gg/487994/natus-vincere-vs-giantx-esports-world-cup-2025-lr2",
        "https://www.vlr.gg/487995/team-vitality-vs-gentle-mates-esports-world-cup-2025-lr2",
        "https://www.vlr.gg/510127/paper-rex-vs-bilibili-gaming-esports-world-cup-2025-opening-a",
        "https://www.vlr.gg/510128/g2-esports-vs-karmine-corp-esports-world-cup-2025-opening-a",
        "https://www.vlr.gg/510133/sentinels-vs-bbl-esports-esports-world-cup-2025-opening-b",
        "https://www.vlr.gg/510134/drx-vs-xi-lai-gaming-esports-world-cup-2025-opening-b",
        "https://www.vlr.gg/510139/rex-regum-qeon-vs-titan-esports-club-esports-world-cup-2025-opening-",
        "https://www.vlr.gg/510138/nrg-vs-team-heretics-esports-world-cup-2025-opening-c",
        "https://www.vlr.gg/510144/gen-g-vs-edward-gaming-esports-world-cup-2025-opening-d",
        "https://www.vlr.gg/510143/100-thieves-vs-fnatic-esports-world-cup-2025-opening-d",
        "https://www.vlr.gg/510129/paper-rex-vs-karmine-corp-esports-world-cup-2025-winners-a",
        "https://www.vlr.gg/510135/bbl-esports-vs-drx-esports-world-cup-2025-winners-b",
        "https://www.vlr.gg/510145/fnatic-vs-gen-g-esports-world-cup-2025-winners-d",
        "https://www.vlr.gg/510140/nrg-vs-rex-regum-qeon-esports-world-cup-2025-winners-c",
        "https://www.vlr.gg/510131/bilibili-gaming-vs-g2-esports-esports-world-cup-2025-elim-a",
        "https://www.vlr.gg/510136/sentinels-vs-xi-lai-gaming-esports-world-cup-2025-elim-b",
        "https://www.vlr.gg/510146/100-thieves-vs-edward-gaming-esports-world-cup-2025-elim-d",
        "https://www.vlr.gg/510141/team-heretics-vs-titan-esports-club-esports-world-cup-2025-elim-c",
        "https://www.vlr.gg/510132/karmine-corp-vs-bilibili-gaming-esports-world-cup-2025-decider-a",
        "https://www.vlr.gg/510137/drx-vs-sentinels-esports-world-cup-2025-decider-b",
        "https://www.vlr.gg/510142/rex-regum-qeon-vs-team-heretics-esports-world-cup-2025-decider-c",
        "https://www.vlr.gg/510147/gen-g-vs-edward-gaming-esports-world-cup-2025-decider-d",
        "https://www.vlr.gg/510149/fnatic-vs-karmine-corp-esports-world-cup-2025-qf",
        "https://www.vlr.gg/510150/paper-rex-vs-sentinels-esports-world-cup-2025-qf",
        "https://www.vlr.gg/510151/nrg-vs-gen-g-esports-world-cup-2025-qf",
        "https://www.vlr.gg/510152/bbl-esports-vs-team-heretics-esports-world-cup-2025-qf",
        "https://www.vlr.gg/510153/fnatic-vs-paper-rex-esports-world-cup-2025-sf",
        "https://www.vlr.gg/510154/gen-g-vs-team-heretics-esports-world-cup-2025-sf",
        "https://www.vlr.gg/510156/paper-rex-vs-gen-g-esports-world-cup-2025-cf",
        "https://www.vlr.gg/510155/fnatic-vs-team-heretics-esports-world-cup-2025-gf",
    ]

def get_vlr_match_maps(url):
    """
    Scrapes all map results from a vlr.gg match URL
    Returns: List of map dictionaries with detailed information
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Extract basic match info
        match_info = extract_match_info(soup, url)
        if not match_info:
            return []
        
        # Extract individual map results
        maps_data = extract_map_results(soup, match_info, url)
        
        return maps_data
        
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return []

def extract_match_info(soup, url):
    """Extract basic match information"""
    match_info = {}
    
    # Extract team names - try multiple methods
    team_names = extract_team_names(soup, url)
    if not team_names:
        return None
    
    match_info['team_A'] = team_names[0]
    match_info['team_B'] = team_names[1]
    
    # Extract tournament/event info
    match_info['tournament'] = extract_tournament_name(soup)
    match_info['match_type'] = extract_match_type(soup)
    match_info['date'] = extract_date(soup)
    
    return match_info

def extract_team_names(soup, url):
    """Extract team names using multiple methods"""
    # Method 1: Look for team names in match header
    team_selectors = [
        '.match-header-vs .wf-title-med',
        '.match-header-team .wf-title-med',
        '.team-name',
        '.match-header-vs-team-name'
    ]
    
    for selector in team_selectors:
        elements = soup.select(selector)
        if len(elements) >= 2:
            team_a = elements[0].get_text(strip=True)
            team_b = elements[1].get_text(strip=True)
            if team_a and team_b:
                return [team_a, team_b]
    
    # Method 2: Extract from page title
    title = soup.find('title')
    if title:
        title_text = title.get_text()
        if ' vs ' in title_text:
            parts = title_text.split(' vs ')
            if len(parts) >= 2:
                team_a = parts[0].strip()
                team_b = parts[1].split(' - ')[0].strip()
                return [team_a, team_b]
    
    # Method 3: Extract from URL
    url_parts = url.split('/')
    if len(url_parts) > 1:
        match_slug = url_parts[-1]
        if '-vs-' in match_slug:
            teams = match_slug.split('-vs-')
            if len(teams) >= 2:
                team_a = teams[0].replace('-', ' ').title()
                team_b = teams[1].split('-')[0].replace('-', ' ').title()
                return [team_a, team_b]
    
    return None

def extract_tournament_name(soup):
    """Extract tournament name"""
    selectors = [
        '.match-header-event .wf-label-med',
        '.match-header-event',
        '.event-name',
        '.tournament-name'
    ]
    
    for selector in selectors:
        element = soup.select_one(selector)
        if element:
            return element.get_text(strip=True)
    
    return "Unknown Tournament"

def extract_match_type(soup):
    """Extract match type (Bo1, Bo3, Bo5)"""
    # Look for match format information
    selectors = [
        '.match-header-vs-note',
        '.match-format',
        '.bo-indicator'
    ]
    
    for selector in selectors:
        element = soup.select_one(selector)
        if element:
            text = element.get_text(strip=True).lower()
            if 'bo5' in text or 'best of 5' in text:
                return 'Bo5'
            elif 'bo3' in text or 'best of 3' in text:
                return 'Bo3'
            elif 'bo1' in text or 'best of 1' in text:
                return 'Bo1'
    
    # Fallback: determine from number of maps
    map_elements = soup.select('.vm-stats-game')
    if len(map_elements) >= 3:
        return 'Bo5' if len(map_elements) >= 4 else 'Bo3'
    
    return 'Bo1'

def extract_date(soup):
    """Extract match date"""
    selectors = [
        '.moment-tz-convert',
        '.match-header-date',
        '.date'
    ]
    
    for selector in selectors:
        element = soup.select_one(selector)
        if element:
            return element.get_text(strip=True)
    
    return "Unknown Date"

def extract_map_results(soup, match_info, url):
    """Extract individual map results"""
    maps_data = []
    
    # Method 1: Look for VLR.gg map stats containers
    map_containers = soup.select('.vm-stats-game')
    
    # Method 2: Look for map navigation tabs (often contains map names)
    if not map_containers:
        map_containers = soup.select('.vm-stats-gamesnav-item')
    
    # Method 3: Look for match header map containers
    if not map_containers:
        map_containers = soup.select('.match-header-vs-score')
    
    # Method 4: Generic map containers
    if not map_containers:
        map_containers = soup.select('.map-item, .game-item, [class*="map-"]')
    
    # Method 5: Try any element with "map" in class name but filter out navigation
    if not map_containers:
        all_map_elements = soup.select('[class*="map"]')
        # Filter out obvious navigation elements
        map_containers = [elem for elem in all_map_elements 
                         if not any(x in str(elem.get('class', [])) for x in ['nav', 'header', 'footer', 'sidebar'])]
    

    
    # Extract data from each container
    temp_maps = []
    for i, map_container in enumerate(map_containers):
        map_data = extract_single_map_data(map_container, match_info, i + 1, url)
        if map_data and map_data.get('map_name') != "Unknown":
            temp_maps.append(map_data)
    
    # Renumber maps sequentially for this match
    for map_num, map_data in enumerate(temp_maps, 1):
        map_data['map_number'] = map_num
        maps_data.append(map_data)
    
    # If no valid maps found, try alternative parsing
    if not temp_maps:
        alt_maps = extract_maps_alternative_method(soup, match_info, url)
        # Renumber alternative maps too
        for map_num, map_data in enumerate(alt_maps, 1):
            map_data['map_number'] = map_num
            maps_data.append(map_data)
    
    return maps_data

def is_valid_valorant_score(score1, score2):
    """
    Validate if scores are realistic Valorant round scores
    Returns True if scores look like actual Valorant map results
    """
    # Basic validation: scores should be between 0 and 30 (theoretical max in OT)
    if not (0 <= score1 <= 30 and 0 <= score2 <= 30):
        return False
    
    # At least one team must have 13+ rounds to win (except for very rare cases)
    if max(score1, score2) < 13:
        return False
    
    # No draws in Valorant
    if score1 == score2:
        return False
    
    # Winner must have at least 2 round advantage unless it's overtime
    winner_score = max(score1, score2)
    loser_score = min(score1, score2)
    
    # Standard game: winner gets 13, loser gets 0-12
    if winner_score == 13:
        return loser_score <= 12
    
    # Overtime: difference should be exactly 2
    if winner_score > 13:
        return winner_score - loser_score == 2
    
    return False

def extract_single_map_data(map_container, match_info, map_number, url):
    """Extract data for a single map"""
    map_data = match_info.copy()
    map_data['map_number'] = map_number
    map_data['url'] = url
    
    # Extract map name using improved VLR.gg selectors
    map_name_selectors = [
        '.vm-stats-game-header .map',  # Map header in stats section
        '.vm-stats-game-header span:last-child',  # Last span in header usually contains map name
        '.map-name',
        '.vm-stats-gamesnav-item-name',  # Map navigation item
        '.match-header-vs-score-map',  # Score header map name
        'div[class*="map"] span',  # Generic map containers
        '[data-map-name]',  # Data attribute for map name
    ]
    
    map_name = "Unknown"
    container_text = map_container.get_text()
    
    # First try selectors
    for selector in map_name_selectors:
        element = map_container.select_one(selector)
        if element:
            text = element.get_text(strip=True)
            if text and len(text) > 1 and not text.isdigit():
                map_name = text
                break
    
    # If selectors fail, try to extract Valorant map names from text (clean approach)
    duration = None
    
    if map_name == "Unknown":
        valorant_maps = [
            'Ascent', 'Bind', 'Haven', 'Split', 'Icebox', 'Breeze', 
            'Fracture', 'Pearl', 'Lotus', 'Sunset', 'Abyss'
        ]
        
        for val_map in valorant_maps:
            # Look for map name as a separate word (not part of other text)
            if re.search(r'\b' + val_map.lower() + r'\b', container_text.lower()):
                map_name = val_map
                break
            # Also check if map name appears at start of text (common pattern)
            elif container_text.lower().strip().startswith(val_map.lower()):
                map_name = val_map
                break
    
    # Clean map name and extract additional info
    original_map_text = map_name
    
    # Extract duration (like 50:07, 1:13:23)
    duration_match = re.search(r'(\d{1,2}:\d{2}(?::\d{2})?)', original_map_text)
    if duration_match:
        duration = duration_match.group(1)
        map_name = map_name.replace(duration, '').strip()
    
    # Remove PICK text from map name
    if 'PICK' in original_map_text.upper():
        map_name = re.sub(r'PICK', '', map_name, flags=re.IGNORECASE).strip()
    
    # Clean any remaining non-letter characters from map name
    map_name = re.sub(r'[^A-Za-z]', '', map_name).strip()
    
    # Validate it's still a known map
    valorant_maps = ['Ascent', 'Bind', 'Haven', 'Split', 'Icebox', 'Breeze', 
                     'Fracture', 'Pearl', 'Lotus', 'Sunset', 'Abyss']
    if map_name not in valorant_maps:
        map_name = "Unknown"
    
    map_data['map_name'] = map_name
    map_data['duration'] = duration
    
    # Extract scores with VLR.gg specific selectors and better separation
    scores = []
    
    # Method 1: Look for specific VLR score elements (most reliable)
    vlr_score_selectors = [
        '.vm-stats-game-score div',  # Score divs in game stats
        '.vm-stats-game-score span',  # Score spans in game stats  
        '.match-header-vs-score div',  # Header score divs
        '.score-team',  # Team score elements
        'div[class*="score"]:not([class*="time"]):not([class*="duration"])',  # Score divs but not time
    ]
    
    for selector in vlr_score_selectors:
        elements = map_container.select(selector)
        if len(elements) >= 2:  # Need at least 2 score elements
            try:
                # Try to get scores from first two elements
                score1_text = elements[0].get_text(strip=True)
                score2_text = elements[1].get_text(strip=True)
                
                if score1_text.isdigit() and score2_text.isdigit():
                    score1, score2 = int(score1_text), int(score2_text)
                    if is_valid_valorant_score(score1, score2):
                        scores = [score1, score2]
                        break
            except (ValueError, IndexError):
                continue
    
    # Method 2: Look for score patterns in clean text (avoid timestamps)
    if not scores:
        # Get text but exclude obvious timestamp/duration patterns
        clean_text = re.sub(r'\d{1,2}:\d{2}:\d{2}', '', container_text)  # Remove timestamps like 1:13:23
        clean_text = re.sub(r'\d{2}:\d{2}', '', clean_text)  # Remove durations like 50:07
        
        # Look for Valorant score patterns
        score_patterns = re.findall(r'\b(\d{1,2})\s*[-]\s*(\d{1,2})\b', clean_text)
        for pattern in score_patterns:
            score1, score2 = int(pattern[0]), int(pattern[1])
            if is_valid_valorant_score(score1, score2):
                scores = [score1, score2]
                break
    
    # Method 3: Try to find scores in parent/sibling elements
    if not scores and map_container.parent:
        parent_text = map_container.parent.get_text()
        # Clean parent text from timestamps
        clean_parent = re.sub(r'\d{1,2}:\d{2}(:\d{2})?', '', parent_text)
        
        score_patterns = re.findall(r'\b(\d{1,2})\s*[-]\s*(\d{1,2})\b', clean_parent)
        for pattern in score_patterns:
            score1, score2 = int(pattern[0]), int(pattern[1])
            if is_valid_valorant_score(score1, score2):
                scores = [score1, score2]
                break
    
    # Set scores and determine winner - only if we have valid scores
    if len(scores) >= 2 and is_valid_valorant_score(scores[0], scores[1]):
        map_data['team_A_score'] = scores[0]
        map_data['team_B_score'] = scores[1]
        
        # Determine winner (no draws possible in Valorant)
        if scores[0] > scores[1]:
            map_data['winner'] = match_info['team_A']
            map_data['team_A_won'] = 1
            map_data['team_B_won'] = 0
        else:  # scores[1] > scores[0] (already validated no draws)
            map_data['winner'] = match_info['team_B']
            map_data['team_A_won'] = 0
            map_data['team_B_won'] = 1
        
        return map_data
    else:
        return None

def extract_maps_alternative_method(soup, match_info, url):
    """Alternative method to extract maps when primary method fails"""
    maps_data = []
    
    # Look for any text patterns that might indicate maps and scores
    text_content = soup.get_text()
    
    # Common Valorant map names
    valorant_maps = [
        'Ascent', 'Bind', 'Haven', 'Split', 'Icebox', 'Breeze', 
        'Fracture', 'Pearl', 'Lotus', 'Sunset', 'Abyss'
    ]
    
    # Try to find map information in structured text
    lines = text_content.split('\n')
    map_number = 1
    found_maps = set()  # To avoid duplicates
    
    # Method 1: Look for lines containing map names and scores
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
            
        for map_name in valorant_maps:
            if map_name.lower() in line.lower() and map_name not in found_maps:
                # Look for scores in current line or next few lines
                score_match = None
                score1, score2 = 0, 0
                search_lines = lines[i:i+3]  # Current line and next 2
                
                for search_line in search_lines:
                    score_match = re.search(r'\b(\d{1,2})\s*[-:]\s*(\d{1,2})\b', search_line)
                    if score_match:
                        score1, score2 = int(score_match.group(1)), int(score_match.group(2))
                        if is_valid_valorant_score(score1, score2):
                            break
                    score_match = None
                
                if score_match and is_valid_valorant_score(score1, score2):
                    map_data = match_info.copy()
                    map_data['map_number'] = map_number
                    map_data['map_name'] = map_name
                    map_data['duration'] = None
                    map_data['team_A_score'] = score1
                    map_data['team_B_score'] = score2
                    map_data['url'] = url
                    
                    # Determine winner
                    if score1 > score2:
                        map_data['winner'] = match_info['team_A']
                        map_data['team_A_won'] = 1
                        map_data['team_B_won'] = 0
                    elif score2 > score1:
                        map_data['winner'] = match_info['team_B']
                        map_data['team_A_won'] = 0
                        map_data['team_B_won'] = 1
                    else:
                        map_data['winner'] = "Draw"
                        map_data['team_A_won'] = 0
                        map_data['team_B_won'] = 0
                    
                    maps_data.append(map_data)
                    found_maps.add(map_name)
                    map_number += 1
                    break
    
    # Method 2: If still no maps, look for numbered sections (1 Lotus, 2 Bind, etc.)
    if not maps_data:
        pattern = r'(\d+)\s+([A-Z][a-z]+)\s+.*?(\d{1,2})\s*[-:]\s*(\d{1,2})'
        matches = re.findall(pattern, text_content)
        
        for match in matches:
            map_num, potential_map, score1, score2 = match
            if potential_map in valorant_maps:
                score1, score2 = int(score1), int(score2)
                if is_valid_valorant_score(score1, score2):
                    map_data = match_info.copy()
                    map_data['map_number'] = int(map_num)
                    map_data['map_name'] = potential_map
                    map_data['duration'] = None
                    map_data['team_A_score'] = score1
                    map_data['team_B_score'] = score2
                    map_data['url'] = url
                    
                    # Determine winner
                    if score1 > score2:
                        map_data['winner'] = match_info['team_A']
                        map_data['team_A_won'] = 1
                        map_data['team_B_won'] = 0
                    elif score2 > score1:
                        map_data['winner'] = match_info['team_B']
                        map_data['team_A_won'] = 0
                        map_data['team_B_won'] = 1
                    else:
                        map_data['winner'] = "Draw"
                        map_data['team_A_won'] = 0
                        map_data['team_B_won'] = 0
                    
                    maps_data.append(map_data)
    
    return maps_data

def main():
    # Get user input for event name and URLs
    event_name, match_urls = get_user_input()
    
    print(f"\n🎮 Processing {len(match_urls)} matches for event: {event_name}")
    print("=" * 60)
    
    all_maps_data = []
    successful_matches = 0
    total_maps = 0
    
    for i, url in enumerate(match_urls, 1):
        print(f"\n[{i}/{len(match_urls)}] Processing: {url.split('/')[-1]}")
        
        maps_data = get_vlr_match_maps(url)
        
        if maps_data:
            successful_matches += 1
            total_maps += len(maps_data)
            all_maps_data.extend(maps_data)
            
            print(f"  ✅ Found {len(maps_data)} valid maps:")
            for map_data in maps_data:
                print(f"    Map {map_data['map_number']}: {map_data['map_name']} - "
                      f"{map_data['team_A']} {map_data['team_A_score']}-{map_data['team_B_score']} {map_data['team_B']} "
                      f"(Winner: {map_data['winner']})")
            
            # Validate series completeness
            validate_series_completeness(maps_data, url)
        else:
            print("  ❌ No valid maps found")
        
        # Be respectful with requests
        time.sleep(2)
    
    print("\n" + "=" * 60)
    print(f"✅ Successfully processed {successful_matches}/{len(match_urls)} matches")
    print(f"📊 Total maps extracted: {total_maps}")
    
    if all_maps_data:
        # Create DataFrame
        df = pd.DataFrame(all_maps_data)
        
        # Reorder columns for better readability
        column_order = [
            'tournament', 'match_type', 'date', 'team_A', 'team_B', 
            'map_number', 'map_name', 'duration',
            'team_A_score', 'team_B_score', 'winner', 'team_A_won', 'team_B_won', 'url'
        ]
        
        # Only include columns that exist in the dataframe
        available_columns = [col for col in column_order if col in df.columns]
        df = df[available_columns]
        
        # Generate filenames with event name
        safe_event_name = "".join(c for c in event_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_event_name = safe_event_name.replace(' ', '_')
        
        csv_filename = f'{safe_event_name}_match_maps.csv'
        excel_filename = f'{safe_event_name}_match_maps.xlsx'
        
        # Save to CSV
        df.to_csv(csv_filename, index=False)
        print(f"💾 Saved to {csv_filename}")
        
        # Save to Excel
        with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='All Maps', index=False)
            
            # Create summary sheet
            summary_df = create_summary_stats(df)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        print(f"📊 Saved to {excel_filename}")
        
        # Print sample of the data
        print(f"\n📋 Sample of extracted data:")
        print(df.head().to_string())
        
        return df
    else:
        print("❌ No data extracted!")
        return None

def validate_series_completeness(maps_data, url):
    """Validate if a series has the expected number of maps"""
    if not maps_data:
        return
    
    num_maps = len(maps_data)
    match_type = maps_data[0].get('match_type', '').lower()
    
    # Count wins for each team
    team_a = maps_data[0]['team_A']
    team_b = maps_data[0]['team_B']
    team_a_wins = sum(1 for m in maps_data if m['winner'] == team_a)
    team_b_wins = sum(1 for m in maps_data if m['winner'] == team_b)
    
    # Validate based on series format
    if num_maps == 1:
        # Bo1 is always complete
        return
    elif num_maps == 2:
        # Bo3 that ended 2-0
        if team_a_wins == 2 or team_b_wins == 2:
            print(f"    ✅ Complete Bo3 series (2-0)")
        else:
            print(f"    ⚠️ Incomplete Bo3: Found 2 maps but neither team won 2")
    elif num_maps == 3:
        # Bo3 that went full distance
        if (team_a_wins == 2 and team_b_wins == 1) or (team_a_wins == 1 and team_b_wins == 2):
            print(f"    ✅ Complete Bo3 series (2-1)")
        else:
            print(f"    ⚠️ Unexpected Bo3 result: {team_a_wins}-{team_b_wins}")
    elif num_maps == 4:
        # Bo5 that ended 3-1
        if team_a_wins == 3 or team_b_wins == 3:
            print(f"    ✅ Complete Bo5 series (3-1)")
        else:
            print(f"    ⚠️ Incomplete Bo5: Found 4 maps but no team won 3")
    elif num_maps == 5:
        # Bo5 that went full distance
        if (team_a_wins == 3 and team_b_wins == 2) or (team_a_wins == 2 and team_b_wins == 3):
            print(f"    ✅ Complete Bo5 series (3-2)")
        else:
            print(f"    ⚠️ Unexpected Bo5 result: {team_a_wins}-{team_b_wins}")
    else:
        print(f"    ⚠️ Unusual series length: {num_maps} maps")

def create_summary_stats(df):
    """Create summary statistics"""
    summary_data = []
    
    # Team statistics
    teams = set(df['team_A'].unique()) | set(df['team_B'].unique())
    
    for team in teams:
        team_maps = df[(df['team_A'] == team) | (df['team_B'] == team)]
        wins = len(team_maps[team_maps['winner'] == team])
        losses = len(team_maps[team_maps['winner'] != team]) - len(team_maps[team_maps['winner'] == 'Draw'])
        
        summary_data.append({
            'Team': team,
            'Maps Played': len(team_maps),
            'Maps Won': wins,
            'Maps Lost': losses,
            'Win Rate': f"{(wins / len(team_maps) * 100):.1f}%" if len(team_maps) > 0 else "0.0%"
        })
    
    return pd.DataFrame(summary_data).sort_values('Maps Won', ascending=False)

if __name__ == "__main__":
    main() 
