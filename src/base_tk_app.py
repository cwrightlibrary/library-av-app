import pandas as pd

def excel_to_csv(excel_path, sheet_name, csv_path):
    df = pd.read_excel(excel_path, sheet_name=sheet_name)
    df.to_csv(csv_path, index=False)

if __name__ == '__main__':
    excel_path = 'src/av_issues.xlsx'
    sheet_name = 'av_issues'
    csv_path = 'src/av_issues.csv'
    
    excel_to_csv(excel_path, sheet_name, csv_path)