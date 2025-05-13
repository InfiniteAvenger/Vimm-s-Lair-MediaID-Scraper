
#!/usr/bin/env python3
# Script to combine all platform JSON files into a single consolidated file

import json
import os
import logging
import sys

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("combine_json.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Map of platform codes with correct case formatting 
# This should match the definitions in scrape_all_platforms.py
PLATFORM_CASE_MAP = {
    "atari2600": "Atari2600",
    "atari5200": "Atari5200",
    "atari7800": "Atari7800",
    "nes": "NES",
    "sms": "SMS",
    "tg16": "TG16",
    "genesis": "Genesis",
    "tgcd": "TGCD",
    "snes": "SNES",
    "segacd": "SegaCD",
    "jaguar": "Jaguar",
    "32x": "32X",
    "saturn": "Saturn",
    "ps1": "PS1",
    "jaguarcd": "JaguarCD",
    "n64": "N64",
    "dreamcast": "Dreamcast",
    "ps2": "PS2",
    "gamecube": "GameCube",
    "xbox": "Xbox",
    "xbox360": "Xbox360",
    "ps3": "PS3",
    "wii": "Wii",
    "wiiware": "WiiWare",
    "gb": "GB",
    "lynx": "Lynx",
    "gg": "GG",
    "vb": "VB",
    "gbc": "GBC",
    "gba": "GBA",
    "ds": "DS",
    "psp": "PSP"
}

def combine_json_files():
    """Combine all platform-specific JSON files into a single consolidated file"""
    logger.info("Combining all platform JSON files into a single file...")
    
    all_games = {}
    total_game_count = 0
    
    # Look for all vimm_*_media_ids.json files
    json_files = [f for f in os.listdir('.') if f.startswith('vimm_') and f.endswith('_media_ids.json')]
    
    if not json_files:
        logger.error("No vimm_*_media_ids.json files found in the current directory")
        return 0
    logger.info(f"Found {len(json_files)} platform JSON files")
    
    for file_name in json_files:
        try:
            # Extract platform name from filename (vimm_PLATFORM_media_ids.json)
            platform_lower = file_name.replace('vimm_', '').replace('_media_ids.json', '')
            
            # Get correct case from mapping or use uppercase if not found
            if platform_lower in PLATFORM_CASE_MAP:
                platform = PLATFORM_CASE_MAP[platform_lower]
            else:
                platform = platform_lower.upper()
                logger.warning(f"Platform {platform_lower} not found in case mapping, using uppercase")
            
            with open(file_name, 'r', encoding='utf-8') as f:
                platform_games = json.load(f)
            
            # Add platform information to each game
            for game in platform_games:
                if isinstance(game, dict):  # Ensure it's a valid game object
                    game['platform'] = platform
            
            # Add to the consolidated dictionary
            all_games[platform] = platform_games
            total_game_count += len(platform_games)
            logger.info(f"Added {len(platform_games)} games from {platform}")
        except Exception as e:
            logger.error(f"Error processing {file_name}: {e}")
    
    # Save the consolidated data
    with open("vimm_all_games_media_ids.json", 'w', encoding='utf-8') as f:
        json.dump(all_games, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Combined JSON file created with {total_game_count} games across {len(all_games)} platforms")
    return total_game_count

if __name__ == "__main__":
    total_games = combine_json_files()
    print(f"\nCombining complete! Total games: {total_games}")
    print("Consolidated game data saved to vimm_all_games_media_ids.json")
