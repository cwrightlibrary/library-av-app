import pandas as pd


class Converter:
    def __init__(self):
        pass

    def excel_to_csv(self, *args, **kwargs):
        excel_path = kwargs.get('excel_path')
        sheet_name = kwargs.get('sheet_name')
        csv_path = kwargs.get('csv_path')
        
        if not excel_path or not sheet_name or not csv_path:
            raise ValueError('Missing requried arguments: "excel_path", "sheet_name", "csv_path"')
        
        df = pd.read_excel(excel_path, sheet_name=sheet_name)
        df.to_csv(csv_path, index=False)
