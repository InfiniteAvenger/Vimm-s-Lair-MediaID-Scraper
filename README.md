# Vimm's Lair Media ID Scraper

This project provides a set of Python scripts to scrape game information and media IDs from Vimm's Lair, a retro game preservation website.

## Features

- Scrapes game information across multiple console and handheld platforms
- Extracts media IDs for each game
- Generates individual JSON files for each platform
- Combines all platform data into a single consolidated JSON file
- Respects the website by using appropriate delays between requests

## Usage

### Scraping a Single Platform

```bash
python vimm_scraper.py <PLATFORM> --no-verify-ssl
```

Example:
```bash
python vimm_scraper.py GB --no-verify-ssl
```

### Scraping All Platforms

```bash
python scrape_all_platforms.py
```

### Options for Multi-Platform Scraping

- `--test`: Only scrape one platform (GB) as a test
- `--platforms <PLATFORM1> <PLATFORM2> ...`: Specify which platforms to scrape
- `--skip-scraping`: Skip scraping and only combine existing JSON files

Example:
```bash
# Test scraping on Game Boy only
python scrape_all_platforms.py --test

# Scrape specific platforms
python scrape_all_platforms.py --platforms GB SNES N64

# Only combine existing JSON files without scraping
python scrape_all_platforms.py --skip-scraping
```

### Combining JSON Files

If you've already scraped multiple platforms and only want to combine the JSON files:

```bash
python combine_json.py
```

## Supported Platforms

### Consoles
- Atari2600
- Atari5200
- NES
- SMS
- Atari7800
- TG16
- Genesis
- TGCD
- SNES
- SegaCD
- Jaguar
- 32X
- Saturn
- PS1
- JaguarCD
- N64
- Dreamcast
- PS2
- GameCube
- Xbox
- Xbox360
- PS3
- Wii
- WiiWare

### Handhelds
- GB
- Lynx
- GG
- VB
- GBC
- GBA
- DS
- PSP

## Output Files

- Individual platform files: `vimm_<platform>_media_ids.json`
- Combined file: `vimm_all_games_media_ids.json`
- Log files: `vimm_scraper.log`, `scrape_all_platforms.log`, `combine_json.log`
- Summary: `scraping_summary.json`

## Notes

- The `--no-verify-ssl` option is used to bypass SSL certificate verification issues.
- The script includes built-in delays to respect the website's servers.
- Platform names in URLs are case-sensitive. The script handles this automatically.
