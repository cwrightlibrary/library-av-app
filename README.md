# 📀 AV App

Using CSV files and python to keep track of and analyze AV problems at the library.

## 💡 Progress

* [ ] Add `main.py` and move the code from `base_tk_app.py`, refactoring it to work better
* [ ] When showing the csv information, only show:
  * [ ] **active**
  * [ ] **item-name**
  * [ ] **item-type**
  * [ ] **customer-name**
  * [ ] **item-todo** *(if enough space)*
* [ ] Create a theme for all `tkinter` widgets that works in light and dark mode
* [x] Create a new icon that's more *mac-like*
* [ ] 

## ✨ Features

- Data processing with `pandas` and `csv`
- A modern, responsive GUI with `tkinter` to edit and create CSV files
- Deadline and update driven to increase productivity and flow

## 🔨 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/cwrightlibrary/library-av-app.git
   cd library-av-app
   ```
2. Install the dependencies by running
   ```
   pip3 install -r requirements.txt
   ```
   - (Optional) Start a virtual environment before installing:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
3. Add a **CSV** file to `/resources` or create one by running `/src/app.py`
