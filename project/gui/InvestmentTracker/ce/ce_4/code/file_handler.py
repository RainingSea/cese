import os

INVESTMENTS_FILE = 'investments.txt'
REPORTS_FILE = 'reports.txt'

def read_investments():
    investments = []
    if os.path.exists(INVESTMENTS_FILE):
        with open(INVESTMENTS_FILE, 'r') as file:
            for line in file:
                name, type, amount, date, category = line.strip().split(',')
                investments.append((name, type, float(amount), date, category))
    return investments

def write_investment(investment):
    with open(INVESTMENTS_FILE, 'a') as file:
        file.write(f"{investment.name},{investment.type},{investment.amount},{investment.date},{investment.category}\n")

def read_reports():
    reports = []
    if os.path.exists(REPORTS_FILE):
        with open(REPORTS_FILE, 'r') as file:
            for line in file:
                reports.append(line.strip())
    return reports

def write_report(report):
    with open(REPORTS_FILE, 'a') as file:
        file.write(report + '\n')