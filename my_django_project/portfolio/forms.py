from django import forms
import pandas as pd
import numpy as np

class PortfolioUploadForm(forms.Form):
    
    csv_file = forms.FileField()
    
    def clean_csv_file(self):
        file = self.cleaned_data['csv_file']
        print('Check form')
        try:
            df = pd.read_csv(file)
            
            required_columns = ['Symbol', 'Purchase Date', 'Volume', 'Purchase Price']
            
            if not np.array(df.columns.values).tolist() == required_columns:
                raise forms.ValidationError("Improper Columns")
            if df.empty or df.iloc[1].isnull().all():
                raise forms.ValidationError("CSV must contain at least one row.")
        except Exception as e:
            raise forms.ValidationError(f"Error reading file: {e}")
        return file
