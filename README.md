# SSD Assignments

Assignments for the Software Systems Development course at IIIT Hyderabad (Monsoon 2021): Bash shell programming, an interactive Python bill splitter, and its Flask + MySQL client-server version.

![Bash](https://img.shields.io/badge/Bash-4EAA25?style=flat-square&logo=gnubash&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white)

## Overview

This repository holds my individual submissions for two of the course assignments. Each folder includes the original problem statement (PDF) and notes on my approach and assumptions.

- **Assignment 1: Shell programming.** Five Bash scripts covering directory listing, text processing, command lookup, Roman numeral conversion and batch file operations.
- **Assignment 3A: Python programming.** A command-line restaurant bill calculator with tips, bill splitting and a "Test your luck" lucky draw, using only the standard library.
- **Assignment 3B: Flask and SQLAlchemy.** The same bill calculator rebuilt as a CLI client talking to a Flask REST API, with users, roles, a MySQL-backed menu and transaction history.

## Assignments

### Assignment 1: Shell programming

| Question | Summary |
|---|---|
| [q1.sh](./2021201064_A1/q1.sh) | Lists only the directories in the current directory with human-readable sizes, sorted by size (largest first), tab separated. Handles names that contain spaces. |
| [q2.sh](./2021201064_A1/q2.sh) | Takes an input and an output file and writes every word ending in "ing" to the output file in lowercase, one per line. |
| [q3.sh](./2021201064_A1/q3.sh) | Takes a word and checks whether any permutation of its letters is a command on the system (looked up with `compgen -c`). Prints `YES` with the matching commands, or `NO`. |
| [q4.sh](./2021201064_A1/q4.sh) | Roman numeral tool. With one argument it converts an integer (1-3999) to Roman or a Roman numeral to an integer. With two arguments it adds two integers (shown in Roman) or two Roman numerals (shown as an integer). Validates input and prints error messages. |
| [q5.sh](./2021201064_A1/q5.sh) | Creates `temp_activity/` with 50 files, renames the first 25 to `.md`, appends `_modified` to every name, and zips the `.txt` files into `txt_compressed.zip`. |

Problem statement: [Assignment_1.pdf](./2021201064_A1/Assignment_1.pdf). Notes on each question: [README](./2021201064_A1/README.md).

### Assignment 3: Python and Flask

| Part | Summary |
|---|---|
| [3A: bill.py](./2021201064_A3/2021201064_3A/bill.py) | Interactive CLI. Shows the menu from `Menu.csv` (half and full plate prices), takes orders as `item_id plate_type quantity`, applies a 0/10/20% tip, splits the bill between a number of people, and runs an optional "Test your luck" draw (50%, 25%, 10% or 0% discount, or a 20% surcharge) with an ASCII face shown for the result. It then prints an itemised final bill. |
| [3B: server.py + client.py](./2021201064_A3/2021201064_3B/) | Rebuilds 3A as a client-server app. The Flask-RESTful server (port 8000) uses SQLAlchemy over MySQL to store users, the menu, transactions and transaction line items. The CLI client handles sign-up, login and logout, ordering and billing (same logic as 3A), and viewing past bills. A user flagged as chef can also add items to the menu. |

Problem statements: [Assignment_3A.pdf](./2021201064_A3/2021201064_3A/Assignment_3A.pdf), [Assignment_3B.pdf](./2021201064_A3/2021201064_3B/Assignment_3B.pdf).

#### 3B REST endpoints

| Endpoint | Purpose |
|---|---|
| `POST /add_user` | Register a customer |
| `POST /login_user` | Authenticate and return the user's role |
| `GET /menu_display` | Fetch the current menu |
| `POST /add_new_menu_item` | Add menu items (chef) |
| `POST /trans`, `POST /trans_detail` | Save a completed bill and its line items |
| `/get_trans`, `/get_trans_detail` | Fetch a user's past bills and the items in a bill |

## Tech stack

- **Assignment 1:** Bash, `du`, `grep`, `awk`, `tr`, `sort`, `compgen`, `zip`
- **Assignment 3A:** Python 3 standard library (`csv`, `random`)
- **Assignment 3B:** Python 3, Flask, Flask-RESTful, Flask-SQLAlchemy, Flask-Login, MySQL, `requests`

## Project structure

```
SSD-Assignment/
├── 2021201064_A1/
│   ├── q1.sh ... q5.sh
│   ├── Assignment_1.pdf
│   └── README.md
└── 2021201064_A3/
    ├── 2021201064_3A/
    │   ├── bill.py
    │   ├── Menu.csv
    │   ├── Assignment_3A.pdf
    │   └── README.md
    └── 2021201064_3B/
        ├── server.py
        ├── client.py
        ├── Assignment_3B.pdf
        └── README.md
```

## Getting started

### Assignment 1

Requires Bash (Linux, macOS, WSL or Git Bash). `q3.sh` uses `compgen`, a Bash builtin.

```bash
cd 2021201064_A1
bash q1.sh
bash q2.sh input.txt output.txt
bash q3.sh <word>
bash q4.sh 1994          # -> MCMXCIV
bash q4.sh XIV XX        # -> 34
bash q5.sh
```

### Assignment 3A

Requires Python 3. Run it from its own folder so the menu file is found:

```bash
cd 2021201064_A3/2021201064_3A
python bill.py
```

`bill.py` opens `menu.csv` (lowercase) while the file in the repository is `Menu.csv`. That works on Windows and macOS, but on a case-sensitive file system (Linux) rename the file or the path in the code.

Enter one order per line as `item_id plate_type quantity` and press Enter on an empty line to finish. Then follow the prompts for tip, number of people and the lucky draw.

### Assignment 3B

Requires Python 3 and a running MySQL server.

1. Create a database named `bill`:

   ```sql
   CREATE DATABASE bill;
   ```

2. Set `SQLALCHEMY_DATABASE_URI` in `server.py` to your own MySQL user and password (`mysql://<user>:<password>@localhost/bill`). The tables are created automatically on first run.

3. Install the dependencies and start the server, then run the client in a second terminal:

   ```bash
   pip install flask flask-restful flask-sqlalchemy flask-login mysqlclient requests

   cd 2021201064_A3/2021201064_3B
   python server.py      # serves on http://127.0.0.1:8000
   python client.py
   ```

New sign-ups are customers. To get the chef menu (adding menu items), set `chef = 1` for that user in the `register` table.

## Context

Built as part of the Software Systems Development course in the M.Tech programme at IIIT Hyderabad (Monsoon 2021).

---

Made by [Mukul Kumar](https://mkk96.github.io) · [GitHub](https://github.com/mkk96) · [LinkedIn](https://www.linkedin.com/in/mukul-kumar-60322616b/)
