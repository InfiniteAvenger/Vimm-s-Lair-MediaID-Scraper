#!/usr/bin/env python3
# Script to run vimm_scraper for all platforms available on Vimm's Lair

import subprocess
import time
import logging
import os
import json
import argparse

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scrape_all_platforms.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# List of console platforms on Vimm's Lair with correct case formatting
CONSOLES = [
    "Atari2600", "Atari5200", "NES", "SMS", "Atari7800", 
    "TG16", "Genesis", "TGCD", "SNES", "SegaCD", 
    "Jaguar", "32X", "Saturn", "PS1", "JaguarCD",
    "N64", "Dreamcast", "PS2", "GameCube", "Xbox",
    "Xbox360", "PS3", "Wii", "WiiWare"
]

# List of handheld platforms on Vimm's Lair
HANDHELDS = [
    "GB", "Lynx", "GG", "VB", "GBC", "GBA", "DS", "PSP"
]

# Map of platform codes that need case correction for URLs
# The website URLs are case-sensitive
PLATFORM_URL_MAP = {
    "ATARI2600": "Atari2600",
    "ATARI5200": "Atari5200",
    "ATARI7800": "Atari7800",
    "NES": "NES",
    "SMS": "SMS",
    "TG16": "TG16",
    "GENESIS": "Genesis",
    "TGCD": "TGCD",
    "SNES": "SNES",
    "SEGACD": "SegaCD",
    "JAGUAR": "Jaguar",
    "32X": "32X",
    "SATURN": "Saturn",
    "PS1": "PS1",
    "JAGUARCD": "JaguarCD",
    "N64": "N64",
    "DREAMCAST": "Dreamcast",
    "PS2": "PS2",
    "GAMECUBE": "GameCube",
    "XBOX": "Xbox",
    "XBOX360": "Xbox360",
    "PS3": "PS3",
    "WII": "Wii",
    "WIIWARE": "WiiWare",
    "GB": "GB",
    "LYNX": "Lynx",
    "GG": "GG",
    "VB": "VB",
    "GBC": "GBC",
    "GBA": "GBA",
    "DS": "DS",
    "PSP": "PSP"
}

# Combined list of all platforms
ALL_PLATFORMS = CONSOLES + HANDHELDS

def combine_json_files():
    """Combine all platform-specific JSON files into a single consolidated file"""
    logger.info("Combining all platform JSON files into a single file...")
    
    all_games = {}
    total_game_count = 0
    
    # Look for all vimm_*_media_ids.json files
    for platform in ALL_PLATFORMS:
        file_path = f"vimm_{platform.lower()}_media_ids.json"
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
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
                logger.error(f"Error processing {file_path}: {e}")
    
    # Save the consolidated data
    with open("vimm_all_games_media_ids.json", 'w', encoding='utf-8') as f:
        json.dump(all_games, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Combined JSON file created with {total_game_count} games across {len(all_games)} platforms")
    return total_game_count

def main():
    parser = argparse.ArgumentParser(description="Scrape all platforms from Vimm's Lair")
    parser.add_argument('--test', action='store_true', help='Only scrape one platform (GB) as a test')
    parser.add_argument('--platforms', nargs='+', help='Specify which platforms to scrape (space separated)')
    parser.add_argument('--skip-scraping', action='store_true', help='Skip scraping and only combine existing JSON files')
    args = parser.parse_args()
    
    logger.info("Starting Vimm's Lair platform scraper")
    
    platforms_to_scrape = ALL_PLATFORMS
    
    # If test mode, only scrape Game Boy
    if args.test:
        logger.info("Test mode enabled - only scraping Game Boy (GB)")
        platforms_to_scrape = ["GB"]
    # If specific platforms are requested
    elif args.platforms:
        platforms_to_scrape = []
        for p in args.platforms:
            p_upper = p.upper()
            if p_upper in [plat.upper() for plat in ALL_PLATFORMS]:
                platforms_to_scrape.append(p)
            else:
                logger.warning(f"Unknown platform: {p} - skipping")
        logger.info(f"Scraping {len(platforms_to_scrape)} specific platforms: {', '.join(platforms_to_scrape)}")
    
    # Track successful platforms
    successful_platforms = []
    failed_platforms = []
    
    # Skip scraping if requested
    if not args.skip_scraping:
        # Run the scraper for each platform
        for platform in platforms_to_scrape:
            try:
                logger.info(f"==================================")
                logger.info(f"Starting scraping for platform: {platform}")
                logger.info(f"==================================")
                  # Get the correct URL format for the platform
                platform_for_url = platform
                platform_upper = platform.upper()
                if platform_upper in PLATFORM_URL_MAP:
                    platform_for_url = PLATFORM_URL_MAP[platform_upper]
                else:
                    logger.warning(f"No URL mapping found for {platform} - using as is")
                
                # Run the vimm_scraper.py script with --no-verify-ssl option
                cmd = ["python", "vimm_scraper.py", platform_for_url, "--no-verify-ssl"]
                print(f"\nRunning scraper for {platform} (URL format: {platform_for_url})...")
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                # Print direct output to terminal for real-time feedback
                if result.stdout:
                    print(result.stdout)
                if result.stderr:
                    print(f"Warnings/Errors: {result.stderr}")
                
                # Log the output
                logger.info(f"STDOUT: {result.stdout}")
                if result.stderr:
                    logger.warning(f"STDERR: {result.stderr}")
                  # Check if the scraper was successful
                output_file = f"vimm_{platform.lower()}_media_ids.json"
                if os.path.exists(output_file):
                    with open(output_file, 'r') as f:
                        data = json.load(f)
                        game_count = len(data)
                    
                    logger.info(f"Successfully scraped {game_count} games for {platform}")
                    successful_platforms.append({"platform": platform, "games": game_count})
                else:
                    logger.error(f"Failed to create output file for {platform}")
                    failed_platforms.append(platform)
                
                # Add a delay between platforms to be extra respectful
                if platform != platforms_to_scrape[-1]:  # No need to delay after the last platform
                    delay = 30  # 30 seconds between platforms
                    logger.info(f"Waiting {delay} seconds before starting next platform...")
                    time.sleep(delay)
                    
            except Exception as e:
                logger.error(f"Error processing platform {platform}: {e}")
                failed_platforms.append(platform)
    else:
        logger.info("Skipping scraping phase as requested")
    
    # Combine all JSON files
    total_games = combine_json_files()
    
    # Print a summary of results
    logger.info("\n=========== SUMMARY ===========")
    if not args.skip_scraping:
        logger.info(f"Total platforms attempted: {len(platforms_to_scrape)}")
        logger.info(f"Successfully scraped platforms: {len(successful_platforms)}")
        logger.info(f"Failed platforms: {len(failed_platforms)}")
    logger.info(f"Total games combined: {total_games}")
    
    if successful_platforms:
        logger.info("\nSuccessfully scraped platforms:")
        for p in successful_platforms:
            logger.info(f"  - {p['platform']}: {p['games']} games")
    
    if failed_platforms:
        logger.info("\nFailed platforms:")
        for p in failed_platforms:
            logger.info(f"  - {p}")
    
    # Save summary to a JSON file
    summary = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_platforms_attempted": len(platforms_to_scrape) if not args.skip_scraping else 0,
        "successful_count": len(successful_platforms),
        "failed_count": len(failed_platforms),
        "total_games": total_games,
        "successful_platforms": successful_platforms,
        "failed_platforms": failed_platforms
    }
    
    with open("scraping_summary.json", 'w') as f:
        json.dump(summary, f, indent=2)
    
    logger.info("\nScraping complete! Summary saved to scraping_summary.json")
    logger.info("Consolidated game data saved to vimm_all_games_media_ids.json")
  

if __name__ == "__main__":
    main()
