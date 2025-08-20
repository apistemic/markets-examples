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
# score  organization.id    organization.name organization.description organization.website_url organization.linkedin_url  organization.employee_count  organization.founded_year
# 1.000            86910                 Uber We are Uber. The ...      http://www.uber.com     https://linkedin....                    122487                         <NA>
# 0.719           247381                 DiDi DiDi Global Inc. ...     http://www.didigl...     https://linkedin....                     25878                         <NA>
# 0.686           177350                 Lyft Whether it’s an e...     https://www.lyft....     https://linkedin....                     25731                         2012
# 0.677           513291                 Bolt At Bolt, we're bu...           http://bolt.eu     https://linkedin....                     12674                         2013
# 0.640           150106                  Ola Ola is India’s la...       http://Olacabs.com     https://linkedin....                     27548                         2010
# 0.616           166825               Careem Careem is buildin...     http://www.careem...     https://linkedin....                      5945                         2012
# 0.585           239295                 Grab Grab is Southeast...     https://grab.careers     https://linkedin....                     49809                         2012
# 0.574           176962                Gojek Gojek is Southeas...     https://www.gojek...     https://linkedin....                         0                         <NA>
# 0.560           347141              inDrive inDrive is a glob...     http://www.inDriv...     https://linkedin....                      8588                         <NA>
# 0.532           213690             DoorDash At DoorDash, our ...     https://careersat...     https://linkedin....                     67148                         <NA>
# ...
```

**Get lookalikes as structured JSON:**
```bash
uv run python cli.py fetch lookalikes linkedin:crunchbase --format json
# [
#  {
#    "organization": {
#      "id": 86910,
#      "name": "Uber",
#      "description": "We are Uber. The go-getters...",
#      "website_url": "http://www.uber.com",
#      "linkedin_url": "https://linkedin.com/company/uber-com",
#      "employee_count": 122487,
#      "founded_year": null
#    },
#    "score": 1.0
#  },
#  {
#    "organization": {
#      "id": 247381,
#      "name": "DiDi",
#      "description": "DiDi Global Inc. is a leading mobility technology platform. ...",
#      "website_url": "http://www.didiglobal.com",
#      "linkedin_url": "https://linkedin.com/company/didiglobal",
#      "employee_count": 25878,
#      "founded_year": null
#    },
#    "score": 0.7185925781557272
#  },
#  {
#    "organization": {
#      "id": 177350,
#      "name": "Lyft",
#      "description": "Whether it\u2019s an everyday commute or a journey that changes everything, ...",
#      "website_url": "https://www.lyft.com/",
#      "linkedin_url": "https://linkedin.com/company/lyft",
#      "employee_count": 25731,
#      "founded_year": 2012
#    },
#    "score": 0.6859793660660187
#  },
#  ...
# ]
```

**Get competitors as CSV for spreadsheet analysis:**
```bash
uv run python cli.py fetch competitors linkedin:uber-com --format csv
# score,organization.id,organization.name,organization.description,organization.website_url,organization.linkedin_url,organization.employee_count,organization.founded_year
# 1.0,86910,Uber,"We ar...",http://www.uber.com,https://linkedin.com/company/uber-com,122487,
# 0.719,247381,DiDi,"DiDi ...",http://www.didiglobal.com,https://linkedin.com/company/didiglobal,25878,
# 0.686,177350,Lyft,"Wheth...",https://www.lyft.com/,https://linkedin.com/company/lyft,25731,2012
# 0.677,513291,Bolt,"At Bo...",http://bolt.eu,https://linkedin.com/company/bolt-eu,12674,2013
# 0.640,150106,Ola,"Ola i...",http://Olacabs.com,https://linkedin.com/company/olacabs-com,27548,2010
# 0.616,166825,Careem,"Caree...",http://www.careem.com,https://linkedin.com/company/careem,5945,2012
# 0.585,239295,Grab,"Grab ...",https://grab.careers,https://linkedin.com/company/grabapp,49809,2012
# 0.574,176962,Gojek,"Gojek...",https://www.gojek.io/careers,https://linkedin.com/company/gojek-gotogroup,0,
# 0.560,347141,inDrive,"inDri...",http://www.inDrive.com,https://linkedin.com/company/indrive,8588,
# 0.532,213690,DoorDash,"At Do...",https://careersatdoordash.com/,https://linkedin.com/company/doordash,67148,
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
# │ *    slug          Company identifier, can be company ID, Linkedin slug or   │
# │                    domain name. For example, to get Uber both                │
# │                    `linkedin:uber-com` and `domain:uber.com` work [required] │
# ╰──────────────────────────────────────────────────────────────────────────────╯
# ╭─ Options ────────────────────────────────────────────────────────────────────╮
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
uv run python cli.py fetch competitors linkedin:uber-com --format csv > competitors.csv

# Get lookalikes in multiple formats (once via domain and once via linkedin slug)
uv run python cli.py fetch lookalikes domain:uber.com --format json > lookalikes.json
uv run python cli.py fetch lookalikes linkedin:uber-com --format parquet > lookalikes.parquet
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
