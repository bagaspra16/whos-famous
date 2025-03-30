# Who's Famous Tool

## Overview
Who's Famous Tool is an interactive command-line application that analyzes a person's popularity based on their online presence. The tool uses web scraping to gather data from multiple search engines and provides an analysis of how famous someone is with visually appealing results.

## Features
- 🔍 **Multi-Engine Search**: Fetches data from Ask.com, AOL, Bing, and Ecosia
- 📊 **Fame Score**: Calculates a fame rating on a scale of 1-100
- 🏆 **Categorization**: Groups people into fame categories (like "GLOBAL ICON", "CELEBRITY", "NOTABLE", etc.)
- ℹ️ **Fun Facts**: Finds and displays interesting facts about the person
- 🎨 **Interactive UI**: Beautiful display with progress bars and colored panels
- 📱 **Responsive**: Adapts display based on terminal size

## Prerequisites
To run Who's Famous Tool, you need:
- Python 3.6+
- Active internet connection

## Installation
1. Clone the repository or download the source code:
   ```
   git clone https://github.com/bagaspra16/whos-famous.git
   cd whos-famous
   ```

2. Install the required dependencies:
   ```
   pip install requests beautifulsoup4 rich
   ```

## Usage
1. Run the program:
   ```
   python whos_famous.py
   ```

2. When prompted, enter the name you want to analyze:
   ```
   👉 Enter name to analyze: [person's name]
   ```

3. Wait while the application processes the data and displays the analysis results, which include:
   - Fame score (from 1-100)
   - Fame category
   - Number of references found across search engines
   - Interesting fact about the person

## Example Output
```
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
│           ⭐️  WHO'S FAMOUS TOOL  ⭐️                 │
│  Analyze popularity and find facts about people     │
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

╭───────────────────┤ FAME ANALYSIS RESULTS ├───────────────────╮

┏━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Metric      ┃ Data                       ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 📊 NAME     │ Beyoncé                    │
│ 🔍 REFERENCES│ 5,487,000                 │
│ ⭐ FAME SCORE│ 92.5/100                  │
│ 👑 CATEGORY  │ GLOBAL ICON               │
│ 📝 DESCRIPTION│ Worldwide household name │
└─────────────┴────────────────────-───────┘
```

## How It Works
1. **Data Collection**:
   - Sends queries to various search engines for the specified name
   - Extracts result counts and references from each search engine

2. **Analysis**:
   - Calculates a fame score using a logarithmic scale with adjustments
   - Determines category based on the score
   - Searches for interesting facts from Wikipedia or other sources

3. **Visualization**:
   - Displays results in tables and colored panels
   - Adapts display based on terminal size

## Code Structure
- `print_banner()`: Displays the application banner
- `search_popularity()`: Performs search engine scraping
- `get_fun_fact()`: Finds interesting facts about a person
- `get_fame_category()`: Determines fame category based on score
- `analyze_popularity()`: Main function that performs the analysis
- `print_section_divider()`: Creates responsive section dividers

## Limitations
- Results may not be 100% accurate as they rely on web scraping
- Some search engines may rate-limit or block automated queries
- Facts are extracted from online sources and may not always be available

## License
[Insert license information here]

## Credits
Developed using:
- [requests](https://requests.readthedocs.io/) - HTTP Library
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) - Web Scraping
- [Rich](https://github.com/Textualize/rich) - Terminal Styling

## Contact
https://bagaspra16-portfolio.vercel.app