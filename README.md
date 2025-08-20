# 🚀 Apistemic Markets Examples

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> **Powerful CLI tools and examples for the Apistemic Markets API** 📊

Effortlessly discover competitors and lookalike companies with this feature-rich command-line interface. 
Export data in multiple formats and integrate seamlessly into your business intelligence workflows.

## ✨ Features

- 🔍 **Competitor Discovery** - Find direct competitors for any company
- 🎯 **Lookalike Analysis** - Discover similar companies in your market
- 📊 **Multiple Export Formats** - CSV, JSON, Parquet, and formatted tables
- ⚡ **Fast & Reliable** - Built on the robust Apistemic Markets API
- 🛠️ **Developer Friendly** - Clean Python code with type hints
- 📈 **Business Ready** - Perfect for market research and competitive analysis

## 🚀 Quick Start

```bash
# Discover competitors
uv run python cli.py fetch competitors linkedin:startupradar

# Find lookalikes with CSV export, e.g. for Excel import
uv run python cli.py fetch lookalikes linkedin:crunchbase --format csv > crunchbase.csv

# Export to Parquet for data analysis
uv run python cli.py fetch competitors linkedin:uber-com --format parquet > uber.parquet
```

## 📋 Usage

### Basic Commands

**Get competitors in human-readable table format (default):**
```bash
uv run python cli.py fetch competitors linkedin:startupradar
#         score  organization.id organization.name  ...
# 0    1.000000           721826  startupradar.co  ...
# 1    0.568760           539540         Seedtable  ...
# 2    0.550740           833275            Signal  ...
# ...
```

**Get lookalikes as structured JSON:**
```bash
uv run python cli.py fetch lookalikes linkedin:crunchbase --format json
# [
#   {
#     "organization": {
#       "id": 177620,
#       "name": "Crunchbase",
#       "description": "Crunchbase is a predictive solution...",
#       "website_url": "https://www.crunchbase.com/",
#       "linkedin_url": "https://linkedin.com/company/crunchbase",
#       "employee_count": 262,
#       "founded_year": 2007
#     },
#     "score": 1.0
#   },
#   //...
# ]
```

**Get competitors as CSV for spreadsheet analysis:**
```bash
uv run python cli.py fetch competitors linkedin:startupradar --format csv
# score,organization.id,organization.name,organization.description,organization.website_url,organization.linkedin_url,organization.employee_count,organization.founded_year
# 1.0,721826,startupradar.co,"Discover new startups earlier with our API...",https://startupradar.co,https://linkedin.com/company/startupradar,1,
# 0.568760,539540,Seedtable,"Your go-to source for in-depth insights...",https://seedtable.com,https://linkedin.com/company/seedtable,0,2018.0
# ...
```

**Get help for any command:**
```bash
uv run python cli.py --help
# Usage: cli.py [OPTIONS] COMMAND [ARGS]...
# 
# ╭─ Options ────────────────────────────────────────────────────────────────────╮
# │ --install-completion          Install completion for the current shell.      │
# │ --show-completion             Show completion for the current shell, to copy │
# │                               it or customize the installation.              │
# │ --help                        Show this message and exit.                    │
# ╰──────────────────────────────────────────────────────────────────────────────╯
# ╭─ Commands ───────────────────────────────────────────────────────────────────╮
# │ leadgen                                                                      │
# │ fetch     Fetch competitors or lookalikes for a given company.               │
# ╰──────────────────────────────────────────────────────────────────────────────╯
```

**Get detailed help for the fetch command:**
```bash
uv run python cli.py fetch --help
# Usage: cli.py fetch [OPTIONS] ENDPOINT:{competitors|lookalikes} SLUG
#
# Fetch competitors or lookalikes for a given company.
#
# ╭─ Arguments ──────────────────────────────────────────────────────────────────╮
# │ *    endpoint      Type of data to fetch [required]                          │
# │ *    slug          LinkedIn slug (e.g., 'linkedin:startupradar') [required]  │
# ╰──────────────────────────────────────────────────────────────────────────────╯
# ╭─ Options ────────────────────────────────────────────────────────────────────╮
# │ --limit         INTEGER                   Limit number of results            │
# │ --format        [table|json|csv|parquet]  Output format [default: table]     │
# │ --help                                    Show this message and exit.        │
# ╰──────────────────────────────────────────────────────────────────────────────╯
```

### Export Formats

| Format | Description | Use Case |
|--------|-------------|----------|
| `table` | Human-readable table | Quick analysis |
| `json` | Structured JSON | API integration |
| `csv` | Comma-separated values | Spreadsheet analysis |
| `parquet` | Columnar format | Big data workflows |

## 🔧 Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/markets-examples.git
   cd markets-examples
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Configure API credentials**
   There's a free tier to play around with the API.
   If you don't set up anything, you'll use it automatically.
   [Sign up](https://rapidapi.com/apistemic-com-apistemic-com-default/api/market-intelligence-competitors-lookalikes-and-more)
   to get an API key.
   With an API key, there's two options:
   ```bash
   # add API key to your env
   export RAPIDAPI_API_KEY="your-rapidapi-api-key"

   # or run via uv with env-file
   uv run --env-file=.env python cli.py
   ```


## 💡 Examples

### Market Research Workflow
```bash
# Export competitor data for analysis
uv run python cli.py fetch competitors linkedin:your-company --format csv > competitors.csv

# Get lookalikes in multiple formats
uv run python cli.py fetch lookalikes linkedin:your-company --format json > lookalikes.json
uv run python cli.py fetch lookalikes linkedin:your-company --format parquet > lookalikes.parquet
```

### Integration with Data Science Tools
```python
import pandas as pd

# Load Parquet data directly into pandas
df = pd.read_parquet('competitors.parquet')
print(df.head())
```

## 🛡️ Requirements

- Python 3.13+
- Valid Apistemic Markets API key
- Dependencies managed with `uv`

## 📚 API Reference

The CLI wraps the powerful [Apistemic Markets API](https://markets.apistemic.com), providing:

- **Company Intelligence** - Detailed company profiles and metrics
- **Market Mapping** - Comprehensive competitive landscapes
- **Real-time Data** - Up-to-date company information
- **Global Coverage** - Companies from around the world

See the [API docs](https://competitor-api.apistemic.com/docs) for the full OpenAPI specification and more information.

## 🤝 Contributing

We welcome contributions! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 🌟 Show Your Support

Give a ⭐️ if this project helped you with your market research!

---

**Built with ❤️ by the Apistemic team**
