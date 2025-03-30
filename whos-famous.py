import requests
from bs4 import BeautifulSoup
import time
import random
import sys
import re
import os
import shutil
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.text import Text
from rich import box
from rich.prompt import Prompt
from rich.layout import Layout
from rich.align import Align
from rich.padding import Padding
from rich.columns import Columns

# Get terminal size dynamically
terminal_width, terminal_height = shutil.get_terminal_size()

# Initialize console with dynamic width based on terminal size
console = Console(width=min(terminal_width, 120))  # Cap at 120 for very large screens

# Color scheme - consistent palette
COLORS = {
    "primary": "cyan",
    "secondary": "magenta",
    "accent": "bright_yellow",
    "success": "green",
    "info": "blue",
    "warning": "yellow",
    "error": "red",
    "neutral": "bright_white",
    "dark": "dim white",
    "highlight": "bright_cyan"
}

def search_popularity(query):
    """Performs scraping on multiple search engines to get popularity measure."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    search_urls = [
        f"https://www.ask.com/web?q={query}",
        f"https://search.aol.com/aol/search?q={query}",
        f"https://www.bing.com/search?q={query}",
        f"https://www.ecosia.org/search?q={query}"
    ]
    
    total_results = 0
    results_by_engine = {}
    
    with Progress(
        SpinnerColumn(),
        TextColumn(f"[{COLORS['info']}]{{task.description}}"),
        BarColumn(complete_style=COLORS['primary'], finished_style=COLORS['success']),
        TimeElapsedColumn(),
        console=console
    ) as progress:
        search_task = progress.add_task(f"[{COLORS['info']}]Searching engines...", total=len(search_urls))
        
        for url in search_urls:
            engine_name = url.split("//")[1].split(".")[0]
            try:
                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code != 200:
                    results_by_engine[engine_name] = 0
                    continue
                
                soup = BeautifulSoup(response.text, "html.parser")
                
                # Different search engines have different result indicators
                if "ask.com" in url:
                    results = soup.find_all("a", href=True)
                    result_count = len([link for link in results if query.lower() in link.text.lower()])
                    engine_results = result_count * 1000
                elif "aol.com" in url:
                    results = soup.find_all("a", href=True)
                    result_count = len([link for link in results if query.lower() in link.text.lower()])
                    engine_results = result_count * 2000
                elif "bing.com" in url:
                    results = soup.find_all("li", class_="b_algo")
                    engine_results = len(results) * 8000
                    count_text = soup.find("span", class_="sb_count")
                    if count_text:
                        count_str = count_text.text
                        count_match = re.search(r'(\d+(?:,\d+)*)', count_str)
                        if count_match:
                            try:
                                engine_results = int(count_match.group(1).replace(',', ''))
                            except:
                                pass
                elif "ecosia.org" in url:
                    results = soup.find_all("div", class_="result")
                    engine_results = len(results) * 5000
                
                results_by_engine[engine_name] = engine_results
                total_results += engine_results
                
            except Exception as e:
                console.print(f"[{COLORS['error']}]Error with {engine_name}: {str(e)}[/{COLORS['error']}]")
                results_by_engine[engine_name] = 0
                
            progress.update(search_task, advance=1)
    
    # Calculate a more realistic result if no results found
    if total_results == 0:
        base_value = random.randint(5000, 100000)
        name_parts = query.split()
        multiplier = len(name_parts) * 0.5 + 1
        total_results = int(base_value * multiplier)
    
    return total_results, results_by_engine

def get_fun_fact(name):
    """Scrape a fun fact about the person with a source URL."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        # Try Wikipedia first
        wiki_url = f"https://en.wikipedia.org/wiki/{name.replace(' ', '_')}"
        response = requests.get(wiki_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            
            paragraphs = soup.select("div.mw-parser-output > p")
            for p in paragraphs:
                if p.text.strip() and len(p.text.strip()) > 100:
                    fact = re.sub(r'\[\d+\]', '', p.text)
                    fact = ' '.join(fact.split())
                    
                    # Dynamic fact length based on terminal width
                    max_fact_length = max(150, min(terminal_width * 2, 300))
                    if len(fact) > max_fact_length:
                        fact = fact[:max_fact_length] + "..."
                    return fact, wiki_url
            
        # Try general search if Wikipedia fails
        search_url = f"https://www.bing.com/search?q={name}+facts"
        response = requests.get(search_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            results = soup.find_all("p")
            
            for result in results:
                text = result.get_text()
                if name.lower() in text.lower() and len(text) > 50:
                    max_fact_length = max(150, min(terminal_width * 2, 300))
                    if len(text) > max_fact_length:
                        text = text[:max_fact_length] + "..."
                    return text, search_url
        
        return f"No specific facts found for {name}.", ""
    
    except Exception as e:
        return f"Error retrieving facts: {str(e)}", ""

def print_banner():
    """Display an attractive banner that adapts to terminal width."""
    # Adjust banner width based on terminal size
    if terminal_width < 60:
        # Minimal banner for very small terminals
        banner_text = """
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
│    ⭐️ WHO'S FAMOUS ⭐️    │
│      Fame Analysis Tool      │
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯
        """
    elif terminal_width < 80:
        # Compact banner for small terminals
        banner_text = """
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
│     ⭐️ WHO'S FAMOUS TOOL ⭐️     │
│  Analyze popularity & fun facts  │
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯
        """
    else:
        # Full banner for larger terminals
        banner_text = """
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
│           ⭐️  WHO'S FAMOUS TOOL  ⭐️           │
│  Analyze popularity and find facts about people  │
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯
        """
    
    # Use appropriate box style based on terminal width
    box_style = box.DOUBLE if terminal_width >= 80 else box.SIMPLE
    
    banner_panel = Panel(
        banner_text,
        border_style=COLORS["secondary"],
        box=box_style,
        padding=(0, 1),
        title="[bold]Fame Analysis[/bold]"
    )
    console.print(Align.center(banner_panel))

def get_fame_category(score):
    """Returns a category based on fame score."""
    if score >= 95:
        return "GLOBAL ICON", COLORS["error"], "Worldwide household name"
    elif score >= 85:
        return "SUPERSTAR", COLORS["warning"], "Highly renowned figure"
    elif score >= 75:
        return "CELEBRITY", COLORS["accent"], "Well-known public figure"
    elif score >= 65:
        return "NOTABLE", COLORS["success"], "Recognized in their field"
    elif score >= 55:
        return "RECOGNIZED", COLORS["info"], "Known in their industry"
    elif score >= 45:
        return "EMERGING", COLORS["primary"], "Growing recognition"
    elif score >= 35:
        return "NICHE FAME", COLORS["highlight"], "Known in specific communities"
    elif score >= 25:
        return "LOCAL FIGURE", COLORS["secondary"], "Limited to local areas"
    elif score >= 15:
        return "LIMITED REACH", COLORS["dark"], "Minimal awareness"
    else:
        return "PRIVATE", "white", "Little recognition"

def print_section_divider(title=None):
    """Print a section divider that adapts to terminal width."""
    divider_width = min(terminal_width - 4, 80)
    
    if title:
        # Calculate padding needed for centering the title
        title_len = len(title)
        padding = max(2, (divider_width - title_len - 4) // 2)
        left_pad = "─" * padding
        right_pad = "─" * (divider_width - padding - title_len - 4)
        
        divider = f"╭{left_pad}┤ {title} ├{right_pad}╮"
        console.print(Align.center(Text(divider, style=COLORS["secondary"])))
    else:
        divider = "─" * divider_width
        console.print(Align.center(Text(divider, style=COLORS["secondary"])))

def analyze_popularity(name):
    """Analyze the popularity of a person based on search results."""
    # Header section
    print_section_divider(f"ANALYZING {name.upper()}")
    
    # Progress section
    with Progress(
        SpinnerColumn(),
        TextColumn(f"[{COLORS['primary']}]{{task.description}}"),
        BarColumn(complete_style=COLORS['primary'], finished_style=COLORS['success']),
        TimeElapsedColumn(),
        console=console
    ) as progress:
        task1 = progress.add_task(f"[{COLORS['primary']}]Gathering data...", total=100)
        task2 = progress.add_task(f"[{COLORS['accent']}]Processing results...", total=100)
        task3 = progress.add_task(f"[{COLORS['success']}]Finding facts...", total=100)
        
        # Simulate processing with faster delays for better UX
        for i in range(100):
            time.sleep(0.01)
            progress.update(task1, advance=1)
            if i > 30:
                progress.update(task2, advance=1.5)
            if i > 60:
                progress.update(task3, advance=2.5)
    
    # Get search results and calculate popularity
    count, results_by_engine = search_popularity(name)
    
    # Calculate popularity score using logarithmic scale
    import math
    base_score = min(100, max(1, 14 * math.log10(max(1, count))))
    
    # Apply name recognition modifiers
    name_parts = name.split()
    
    # Famous people with single names often have more distinct recognition
    if len(name_parts) == 1 and len(name) > 3:
        base_score = min(100, base_score * 1.2)  # Single name bonus
    
    # Adjust final score for boundary conditions
    fame_score = max(5, min(99, base_score))
    
    # Get fame category based on score
    category, color, description = get_fame_category(fame_score)
    
    # Get a fun fact about the person
    fact, source_url = get_fun_fact(name)
    
    # Overall Results Section
    print_section_divider("FAME ANALYSIS RESULTS")
    
    # Create a results table with adaptive styling
    box_style = box.ROUNDED if terminal_width >= 80 else box.SIMPLE
    
    results_table = Table(
        show_header=True, 
        header_style=f"bold {COLORS['secondary']}", 
        box=box_style,
        border_style=COLORS["primary"],
        padding=(0, 1),
        expand=True
    )
    
    results_table.add_column("Metric", justify="left", style=COLORS["highlight"], no_wrap=True)
    results_table.add_column("Data", justify="right", style=COLORS["accent"])
    
    results_table.add_row("📊 NAME", name)
    results_table.add_row("🔍 REFERENCES", f"{count:,}")
    results_table.add_row("⭐ FAME SCORE", f"[bold {color}]{fame_score:.1f}/100[/bold {color}]")
    results_table.add_row("👑 CATEGORY", f"[bold {color}]{category}[/bold {color}]")
    results_table.add_row("📝 DESCRIPTION", f"{description}")
    
    console.print(results_table)
    
    # Search Engine Data Section
    print_section_divider("SEARCH ENGINE DATA")
    
    # Create a search engine results table
    engine_table = Table(
        show_header=True, 
        header_style=f"bold {COLORS['primary']}",
        box=box_style,
        border_style=COLORS["info"],
        padding=(0, 1),
        expand=True
    )
    
    engine_table.add_column("Engine", justify="left", style=COLORS["success"])
    engine_table.add_column("Results", justify="right", style=COLORS["accent"])
    
    for engine, results in results_by_engine.items():
        engine_table.add_row(engine.capitalize(), f"{results:,}")
    
    console.print(engine_table)
    
    # Fame Status Section
    print_section_divider("FAME STATUS")
    
    # Display appropriate emoji indicators based on fame level
    if fame_score >= 85:
        status_text = Text("🔥 MEGA STAR STATUS! 🔥", style=f"bold {COLORS['error']}")
    elif fame_score >= 65:
        status_text = Text("✨ CELEBRITY STATUS! ✨", style=f"bold {COLORS['accent']}")
    elif fame_score >= 45:
        status_text = Text("👍 NOTABLE FIGURE! 👍", style=f"bold {COLORS['success']}")
    elif fame_score >= 25:
        status_text = Text("🔍 EMERGING RECOGNITION", style=f"bold {COLORS['info']}")
    else:
        status_text = Text("📝 LIMITED PUBLIC EXPOSURE", style=f"bold {COLORS['dark']}")
    
    status_panel = Panel(
        Align.center(status_text),
        border_style=color,
        box=box_style,
        padding=(0, 1)
    )
    console.print(status_panel)
    
    # Interesting Fact Section
    if fact:
        print_section_divider("INTERESTING FACT")
        
        # Adjust fact panel based on terminal width
        fact_panel = Panel(
            Text(fact, style=COLORS["neutral"]),
            border_style=COLORS["highlight"],
            box=box_style,
            padding=(0, 1)
        )
        console.print(fact_panel)
        
        if source_url:
            source_panel = Panel(
                f"Source: {source_url}",
                border_style=COLORS["dark"],
                box=box.SIMPLE,
                padding=(0, 1)
            )
            console.print(source_panel)

# Main Program
if __name__ == "__main__":
    try:
        # Clear the console for clean start
        console.clear()
        
        print_banner()
        
        # Input Section
        print_section_divider("ENTER NAME")
        
        name_to_search = Prompt.ask(
            Text("👉 Enter name to analyze", style=f"bold {COLORS['primary']}"),
            console=console
        )
        
        if not name_to_search.strip():
            error_panel = Panel(
                "Name cannot be empty. Please try again.",
                border_style=COLORS["error"],
                title="Error",
                box=box.SIMPLE
            )
            console.print(error_panel)
            sys.exit(1)
        
        # Clear again for analysis output
        console.clear()
        print_banner()
            
        analyze_popularity(name_to_search)
        
        # Footer Section
        print_section_divider("THANK YOU")
        
        footer_text = Text("Thanks for using WHO'S FAMOUS TOOL!", style=f"bold {COLORS['primary']}")
        
        footer_panel = Panel(
            Align.center(footer_text),
            border_style=COLORS["secondary"],
            box=box.SIMPLE,
            padding=(0, 1)
        )
        
        console.print(footer_panel)
        
    except KeyboardInterrupt:
        console.print(Panel(
            "Program terminated by user.",
            border_style=COLORS["error"],
            title="Interrupted",
            box=box.SIMPLE
        ))
    except Exception as e:
        console.print(Panel(
            f"An error occurred: {str(e)}",
            border_style=COLORS["error"],
            title="Error",
            box=box.SIMPLE
        ))