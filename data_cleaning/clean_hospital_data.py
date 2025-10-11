#!/usr/bin/env python3
"""
Hospital Dataset Cleaning Script
================================

This script performs comprehensive data cleaning on the hospital dataset including:
- Name formatting standardization
- Gender consistency checks
- Date validation and formatting
- Missing value handling
- Data type corrections
- Outlier detection and handling
- Data validation

Author: ML Data Cleaning Expert
Date: October 2025
"""

import pandas as pd
import numpy as np
import re
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class HospitalDataCleaner:
    def __init__(self, input_file):
        """Initialize the data cleaner with input file path."""
        self.input_file = input_file
        self.df = None
        self.cleaning_report = {
            'original_rows': 0,
            'final_rows': 0,
            'issues_fixed': []
        }
    
    def load_data(self):
        """Load the dataset and perform initial inspection."""
        print("Loading hospital dataset...")
        self.df = pd.read_csv(self.input_file, index_col=0)
        self.cleaning_report['original_rows'] = len(self.df)
        
        print(f"Dataset loaded: {len(self.df)} rows, {len(self.df.columns)} columns")
        print("\nColumns:", list(self.df.columns))
        print("\nFirst few rows:")
        print(self.df.head())
        
        return self.df
    
    def clean_names(self):
        """Clean and standardize name formatting."""
        print("\n=== Cleaning Names ===")
        
        # Count names with formatting issues
        irregular_names = self.df['Name'].str.contains(r'[a-z][A-Z]|[A-Z][a-z][A-Z]', na=False).sum()
        print(f"Found {irregular_names} names with irregular capitalization")
        
        # Standardize name formatting
        def fix_name_formatting(name):
            if pd.isna(name):
                return name
            
            # Remove extra spaces and normalize
            name = re.sub(r'\s+', ' ', str(name).strip())
            
            # Handle titles (Mr., Mrs., Dr., Ms.)
            title_pattern = r'^(mr\.|mrs\.|dr\.|ms\.)\s*'
            title_match = re.match(title_pattern, name.lower())
            title = ""
            if title_match:
                title = title_match.group(1).title() + " "
                name = re.sub(title_pattern, '', name, flags=re.IGNORECASE)
            
            # Split name into parts and capitalize properly
            name_parts = name.split()
            cleaned_parts = []
            
            for part in name_parts:
                # Handle hyphenated names
                if '-' in part:
                    hyphen_parts = [p.capitalize() for p in part.split('-')]
                    cleaned_parts.append('-'.join(hyphen_parts))
                else:
                    cleaned_parts.append(part.capitalize())
            
            return title + ' '.join(cleaned_parts)
        
        self.df['Name'] = self.df['Name'].apply(fix_name_formatting)
        self.cleaning_report['issues_fixed'].append(f"Fixed {irregular_names} irregularly formatted names")
        print("Name formatting standardized")
    
    def clean_gender_data(self):
        """Clean and validate gender data."""
        print("\n=== Cleaning Gender Data ===")
        
        # First, check if there are actual literal "Nan" strings (not pandas NaN)
        # We need to be more careful here - pandas NaN will show up as 'nan' when converted to string
        if self.df['Gender'].dtype == 'object':
            # Check for literal string "Nan", "NaN", "nan" etc. (but not pandas NaN)
            literal_nan_mask = (self.df['Gender'].astype(str).str.match(r'^[Nn]a[Nn]$', na=False) & 
                              self.df['Gender'].notna())
            nan_strings = literal_nan_mask.sum()
            
            if nan_strings > 0:
                print(f"Found {nan_strings} rows with literal 'Nan' strings in Gender")
                self.df.loc[literal_nan_mask, 'Gender'] = np.nan
                self.cleaning_report['issues_fixed'].append(f"Fixed {nan_strings} literal 'Nan' strings to proper null values")
            else:
                print("No literal 'Nan' strings found in Gender column")
        
        # Check for invalid gender values (excluding proper nulls)
        valid_genders = ['Male', 'Female']
        invalid_mask = (~self.df['Gender'].isin(valid_genders) & self.df['Gender'].notna())
        invalid_genders = self.df[invalid_mask]
        
        if len(invalid_genders) > 0:
            print(f"Found {len(invalid_genders)} rows with invalid gender values:")
            print(invalid_genders['Gender'].unique())
            # Convert invalid values to proper nulls
            self.df.loc[invalid_mask, 'Gender'] = np.nan
            self.cleaning_report['issues_fixed'].append(f"Converted {len(invalid_genders)} invalid gender entries to null values")
        
        print(f"Gender distribution:\n{self.df['Gender'].value_counts(dropna=False)}")
    
    def clean_blood_types(self):
        """Validate and clean blood type data."""
        print("\n=== Cleaning Blood Types ===")
        
        valid_blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        invalid_blood = self.df[~self.df['Blood Type'].isin(valid_blood_types)]
        
        if len(invalid_blood) > 0:
            print(f"Found {len(invalid_blood)} rows with invalid blood types")
            # Mark invalid blood types for review
            self.df.loc[~self.df['Blood Type'].isin(valid_blood_types), 'Blood Type'] = 'Unknown'
            self.cleaning_report['issues_fixed'].append(f"Marked {len(invalid_blood)} invalid blood type entries")
        
        print(f"Blood type distribution:\n{self.df['Blood Type'].value_counts()}")
    
    def clean_dates(self):
        """Clean and validate date columns."""
        print("\n=== Cleaning Dates ===")
        
        date_columns = ['Date of Admission', 'Discharge Date']
        
        for col in date_columns:
            print(f"Processing {col}...")
            
            # Convert to datetime
            original_invalid = self.df[col].isna().sum()
            self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
            new_invalid = self.df[col].isna().sum()
            
            if new_invalid > original_invalid:
                invalid_dates = new_invalid - original_invalid
                print(f"Found {invalid_dates} invalid date formats in {col}")
                self.cleaning_report['issues_fixed'].append(f"Converted {invalid_dates} invalid dates to NaT in {col}")
        
        # Check for logical date inconsistencies
        if 'Date of Admission' in self.df.columns and 'Discharge Date' in self.df.columns:
            invalid_date_logic = (self.df['Discharge Date'] < self.df['Date of Admission']).sum()
            if invalid_date_logic > 0:
                print(f"Found {invalid_date_logic} records where discharge date is before admission date")
                # Mark these for manual review
                mask = self.df['Discharge Date'] < self.df['Date of Admission']
                self.df.loc[mask, 'Discharge Date'] = pd.NaT
                self.cleaning_report['issues_fixed'].append(f"Fixed {invalid_date_logic} illogical date sequences")
    
    def clean_hospital_names(self):
        """Clean hospital names by removing trailing punctuation and standardizing format."""
        print("\n=== Cleaning Hospital Names ===")
        
        # Count hospitals with trailing commas
        trailing_comma = self.df['Hospital'].str.endswith(',', na=False).sum()
        print(f"Found {trailing_comma} hospital names with trailing commas")
        
        def clean_hospital_name(name):
            if pd.isna(name):
                return name
            
            # Remove trailing commas and extra spaces
            name = str(name).strip().rstrip(',').strip()
            
            # Standardize common abbreviations
            name = re.sub(r'\bLLC\b', 'LLC', name, flags=re.IGNORECASE)
            name = re.sub(r'\bPLC\b', 'PLC', name, flags=re.IGNORECASE)
            name = re.sub(r'\bInc\b', 'Inc', name, flags=re.IGNORECASE)
            name = re.sub(r'\bLtd\b', 'Ltd', name, flags=re.IGNORECASE)
            
            return name
        
        self.df['Hospital'] = self.df['Hospital'].apply(clean_hospital_name)
        self.cleaning_report['issues_fixed'].append(f"Cleaned {trailing_comma} hospital names with formatting issues")
    
    def clean_numerical_data(self):
        """Clean and validate numerical columns."""
        print("\n=== Cleaning Numerical Data ===")
        
        # Clean Age column
        print("Processing Age column...")
        age_issues = 0
        
        # Check for unrealistic ages
        unrealistic_age = ((self.df['Age'] < 0) | (self.df['Age'] > 120)).sum()
        if unrealistic_age > 0:
            print(f"Found {unrealistic_age} unrealistic age values")
            self.df.loc[(self.df['Age'] < 0) | (self.df['Age'] > 120), 'Age'] = np.nan
            age_issues += unrealistic_age
        
        # Clean Billing Amount
        print("Processing Billing Amount...")
        billing_issues = 0
        
        # Check for negative billing amounts
        negative_billing = (self.df['Billing Amount'] < 0).sum()
        if negative_billing > 0:
            print(f"Found {negative_billing} negative billing amounts")
            self.df.loc[self.df['Billing Amount'] < 0, 'Billing Amount'] = np.abs(self.df.loc[self.df['Billing Amount'] < 0, 'Billing Amount'])
            billing_issues += negative_billing
        
        # Check for unrealistic billing amounts (e.g., less than $1 or more than $1M)
        unrealistic_billing = ((self.df['Billing Amount'] < 1) | (self.df['Billing Amount'] > 1000000)).sum()
        if unrealistic_billing > 0:
            print(f"Found {unrealistic_billing} potentially unrealistic billing amounts")
            # Cap extreme values
            self.df.loc[self.df['Billing Amount'] > 1000000, 'Billing Amount'] = 1000000
            self.df.loc[self.df['Billing Amount'] < 1, 'Billing Amount'] = np.nan
            billing_issues += unrealistic_billing
        
        # Clean Room Number
        print("Processing Room Number...")
        room_issues = 0
        
        # Check for unrealistic room numbers
        unrealistic_rooms = ((self.df['Room Number'] < 1) | (self.df['Room Number'] > 9999)).sum()
        if unrealistic_rooms > 0:
            print(f"Found {unrealistic_rooms} unrealistic room numbers")
            self.df.loc[(self.df['Room Number'] < 1) | (self.df['Room Number'] > 9999), 'Room Number'] = np.nan
            room_issues += unrealistic_rooms
        
        if age_issues > 0:
            self.cleaning_report['issues_fixed'].append(f"Fixed {age_issues} age-related issues")
        if billing_issues > 0:
            self.cleaning_report['issues_fixed'].append(f"Fixed {billing_issues} billing amount issues")
        if room_issues > 0:
            self.cleaning_report['issues_fixed'].append(f"Fixed {room_issues} room number issues")
    
    def clean_categorical_data(self):
        """Clean and standardize categorical columns."""
        print("\n=== Cleaning Categorical Data ===")
        
        # Clean Medical Condition
        medical_conditions = self.df['Medical Condition'].value_counts()
        print(f"Medical conditions found: {list(medical_conditions.index)}")
        
        # Clean Admission Type
        admission_types = self.df['Admission Type'].value_counts()
        print(f"Admission types: {list(admission_types.index)}")
        
        # Clean Test Results
        test_results = self.df['Test Results'].value_counts()
        print(f"Test results: {list(test_results.index)}")
        
        # Standardize Insurance Provider names
        def clean_insurance_name(name):
            if pd.isna(name):
                return name
            return str(name).strip().title()
        
        self.df['Insurance Provider'] = self.df['Insurance Provider'].apply(clean_insurance_name)
        
        # Standardize medication names
        def clean_medication_name(name):
            if pd.isna(name):
                return name
            return str(name).strip().title()
        
        self.df['Medication'] = self.df['Medication'].apply(clean_medication_name)
        
        self.cleaning_report['issues_fixed'].append("Standardized categorical data formatting")
    
    def remove_duplicates(self):
        """Remove duplicate rows from the dataset."""
        print("\n=== Removing Duplicate Rows ===")
        
        initial_count = len(self.df)
        
        # Check for exact duplicates
        duplicates = self.df.duplicated()
        duplicate_count = duplicates.sum()
        
        if duplicate_count > 0:
            print(f"Found {duplicate_count} exact duplicate rows")
            self.df = self.df.drop_duplicates()
            self.cleaning_report['issues_fixed'].append(f"Removed {duplicate_count} duplicate rows")
        else:
            print("No duplicate rows found")
        
        final_count = len(self.df)
        rows_removed = initial_count - final_count
        print(f"Rows removed: {rows_removed}")
        
        return self.df
    
    def handle_missing_values(self):
        """Handle missing values in the dataset with ML-appropriate policies."""
        print("\n=== Handling Missing Values ===")
        
        missing_summary = self.df.isnull().sum()
        missing_summary = missing_summary[missing_summary > 0]
        
        if len(missing_summary) > 0:
            print("Missing values per column:")
            print(missing_summary)
            
            # ML-appropriate missing value policies:
            
            # 1. Name: Drop for ML (PII/leakage concerns)
            if 'Name' in missing_summary.index:
                print(f"Name column has {missing_summary['Name']} missing values")
                print("Recommendation: Consider dropping Name column for ML (PII/leakage risk)")
                # Keep nulls as-is for now, let user decide
            
            # 2. Age: fill with median (common practice)
            if 'Age' in missing_summary.index:
                median_age = self.df['Age'].median()
                self.df['Age'].fillna(median_age, inplace=True)
                print(f"Filled missing ages with median value: {median_age}")
                self.cleaning_report['issues_fixed'].append(f"Filled {missing_summary['Age']} missing ages with median")
            
            # 3. Insurance Provider: Keep as null or encode as "Unknown" - both valid for ML
            if 'Insurance Provider' in missing_summary.index:
                print(f"Insurance Provider has {missing_summary['Insurance Provider']} missing values")
                print("Recommendation: Keep as null or encode as 'Unknown' category")
                # Option to encode as "Unknown" for categorical encoding
                # self.df['Insurance Provider'].fillna('Unknown', inplace=True)
            
            # 4. Medication: Keep as null - missing medication is meaningful information
            if 'Medication' in missing_summary.index:
                print(f"Medication has {missing_summary['Medication']} missing values")
                print("Recommendation: Keep as null (missing medication is meaningful)")
            
            # 5. Other fields: keep as missing for manual review
            remaining_missing = [col for col in missing_summary.index 
                               if col not in ['Age', 'Name', 'Insurance Provider', 'Medication']]
            if remaining_missing:
                print(f"Other columns with missing values: {remaining_missing}")
                print("Keeping as null for manual review")
            
            self.cleaning_report['issues_fixed'].append("Applied ML-appropriate missing value policies")
        else:
            print("No missing values found")
    
    def detect_outliers(self):
        """Detect and report potential outliers."""
        print("\n=== Outlier Detection ===")
        
        numerical_columns = ['Age', 'Billing Amount', 'Room Number']
        
        for col in numerical_columns:
            if col in self.df.columns:
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers = self.df[(self.df[col] < lower_bound) | (self.df[col] > upper_bound)]
                
                if len(outliers) > 0:
                    print(f"Found {len(outliers)} potential outliers in {col}")
                    print(f"  Range: {self.df[col].min():.2f} - {self.df[col].max():.2f}")
                    print(f"  Normal range (IQR): {lower_bound:.2f} - {upper_bound:.2f}")
    
    def generate_data_quality_report(self):
        """Generate a comprehensive data quality report."""
        print("\n" + "="*50)
        print("DATA QUALITY REPORT")
        print("="*50)
        
        print(f"Original dataset size: {self.cleaning_report['original_rows']} rows")
        print(f"Final dataset size: {len(self.df)} rows")
        print(f"Rows removed: {self.cleaning_report['original_rows'] - len(self.df)}")
        
        print("\nIssues fixed:")
        for issue in self.cleaning_report['issues_fixed']:
            print(f"  • {issue}")
        
        print(f"\nFinal data types:")
        print(self.df.dtypes)
        
        print(f"\nFinal missing values:")
        missing = self.df.isnull().sum()
        missing = missing[missing > 0]
        if len(missing) > 0:
            print(missing)
        else:
            print("No missing values")
        
        print(f"\nDataset summary:")
        print(self.df.describe(include='all'))
    
    def save_cleaned_data(self, output_file):
        """Save the cleaned dataset with proper data types."""
        print(f"\nSaving cleaned dataset to {output_file}...")
        
        # Ensure dates are properly formatted before saving
        date_columns = ['Date of Admission', 'Discharge Date']
        for col in date_columns:
            if col in self.df.columns and self.df[col].dtype == 'datetime64[ns]':
                print(f"Maintaining {col} as datetime64[ns] (will be saved as text in CSV)")
        
        # Save with proper index handling
        self.df.to_csv(output_file, index=False)
        print("Dataset saved successfully!")
        
        # Verify the save
        print(f"Saved dataset shape: {self.df.shape}")
        print(f"Data types maintained:")
        for col in ['Date of Admission', 'Discharge Date']:
            if col in self.df.columns:
                print(f"  {col}: {self.df[col].dtype}")
    
    def run_full_cleaning(self, output_file=None):
        """Run the complete data cleaning pipeline."""
        print("Starting Hospital Dataset Cleaning Pipeline")
        print("="*50)
        
        # Load data
        self.load_data()
        
        # Run all cleaning steps in logical order
        self.remove_duplicates()  # Remove duplicates first
        self.clean_names()
        self.clean_gender_data()  # Now properly handles "Nan" strings
        self.clean_blood_types()
        self.clean_dates()
        self.clean_hospital_names()
        self.clean_numerical_data()
        self.clean_categorical_data()
        self.handle_missing_values()  # Updated with ML-appropriate policies
        self.detect_outliers()
        
        # Generate report
        self.generate_data_quality_report()
        
        # Save cleaned data
        if output_file:
            self.save_cleaned_data(output_file)
        
        return self.df

def main():
    """Main function to run the data cleaning pipeline."""
    input_file = "Hospital_dataset.csv"
    output_file = "Hospital_dataset_final_cleaned.csv"
    
    # Initialize cleaner
    cleaner = HospitalDataCleaner(input_file)
    
    # Run cleaning pipeline
    cleaned_data = cleaner.run_full_cleaning(output_file)
    
    print("\n" + "="*50)
    print("DATA CLEANING COMPLETED SUCCESSFULLY!")
    print("="*50)
    print(f"Cleaned dataset saved as: {output_file}")
    print(f"Original size: {cleaner.cleaning_report['original_rows']} rows")
    print(f"Final size: {len(cleaned_data)} rows")
    
    # Additional ML-ready recommendations
    print("\n" + "="*50)
    print("ML READINESS RECOMMENDATIONS")
    print("="*50)
    print("1. Consider dropping 'Name' column (PII/leakage risk)")
    print("2. Handle remaining nulls in 'Insurance Provider' and 'Medication' as needed")
    print("3. Encode categorical variables for ML algorithms")
    print("4. Split dates into separate features if needed (year, month, day)")
    print("5. Consider feature engineering (e.g., length of stay = discharge - admission)")

if __name__ == "__main__":
    main()
