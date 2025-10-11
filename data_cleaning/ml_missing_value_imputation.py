#!/usr/bin/env python3
"""
ML-Expert Level Missing Value Imputation
========================================

This script applies sophisticated missing value imputation strategies
that ML experts use in production environments.

Strategies Applied:
1. Drop PII columns (Name) - standard ML practice
2. Mode imputation for low-cardinality categoricals
3. Advanced categorical imputation for missing categories
4. Domain-specific imputation for medical data
5. Forward/backward fill for dates
6. KNN imputation for numerical data if needed

Author: ML Expert
Date: October 2025
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class MLExpertMissingValueHandler:
    def __init__(self, input_file):
        """Initialize with the cleaned dataset."""
        self.input_file = input_file
        self.df = None
        self.imputation_report = {
            'strategies_applied': [],
            'columns_processed': [],
            'rows_affected': {}
        }
    
    def load_data(self):
        """Load the dataset."""
        print("Loading dataset for ML-expert missing value imputation...")
        self.df = pd.read_csv(self.input_file)
        print(f"Dataset shape: {self.df.shape}")
        
        # Convert dates properly
        date_cols = ['Date of Admission', 'Discharge Date']
        for col in date_cols:
            if col in self.df.columns:
                self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
        
        return self.df
    
    def analyze_missing_patterns(self):
        """Analyze missing value patterns for strategic imputation."""
        print("\n=== MISSING VALUE PATTERN ANALYSIS ===")
        
        missing = self.df.isnull().sum()
        missing_pct = (missing / len(self.df)) * 100
        
        # Categorize columns by missing value strategy
        self.pii_columns = ['Name']  # Drop for ML
        self.categorical_low_missing = []  # Mode imputation
        self.categorical_high_missing = []  # Advanced imputation
        self.numerical_missing = []  # Statistical imputation
        self.date_missing = []  # Forward/backward fill
        self.keep_missing = []  # Keep as missing (informative)
        
        for col in self.df.columns:
            miss_count = missing[col]
            miss_pct_val = missing_pct[col]
            
            if miss_count == 0:
                continue
                
            dtype = self.df[col].dtype
            
            print(f"{col}: {miss_count} missing ({miss_pct_val:.1f}%)")
            
            if col in self.pii_columns:
                continue
            elif 'date' in col.lower() or dtype == 'datetime64[ns]':
                self.date_missing.append(col)
            elif dtype in ['object'] and miss_pct_val < 5:  # Low missing categoricals
                self.categorical_low_missing.append(col)
            elif dtype in ['object'] and miss_pct_val >= 5:  # High missing categoricals
                self.categorical_high_missing.append(col)
            elif dtype in ['float64', 'int64']:
                self.numerical_missing.append(col)
            else:
                self.keep_missing.append(col)
        
        print(f"\nImputation Strategy Categories:")
        print(f"PII to drop: {self.pii_columns}")
        print(f"Categorical (low missing): {self.categorical_low_missing}")
        print(f"Categorical (high missing): {self.categorical_high_missing}")
        print(f"Numerical: {self.numerical_missing}")
        print(f"Dates: {self.date_missing}")
        print(f"Keep missing: {self.keep_missing}")
    
    def drop_pii_columns(self):
        """Drop PII columns - standard ML practice."""
        print("\n=== DROPPING PII COLUMNS ===")
        
        initial_cols = self.df.columns.tolist()
        cols_to_drop = [col for col in self.pii_columns if col in self.df.columns]
        
        if cols_to_drop:
            print(f"Dropping PII columns: {cols_to_drop}")
            self.df = self.df.drop(columns=cols_to_drop)
            self.imputation_report['strategies_applied'].append(f"Dropped PII columns: {cols_to_drop}")
            self.imputation_report['columns_processed'].extend(cols_to_drop)
        else:
            print("No PII columns to drop")
    
    def impute_categorical_low_missing(self):
        """Impute categorical columns with low missing percentages using mode."""
        print("\n=== IMPUTING LOW-MISSING CATEGORICALS ===")
        
        for col in self.categorical_low_missing:
            if col not in self.df.columns:
                continue
                
            missing_count = self.df[col].isnull().sum()
            if missing_count == 0:
                continue
            
            # Use mode for categorical imputation
            mode_value = self.df[col].mode()
            if len(mode_value) > 0:
                mode_val = mode_value[0]
                print(f"Imputing {col}: {missing_count} missing → '{mode_val}' (mode)")
                self.df[col].fillna(mode_val, inplace=True)
                
                self.imputation_report['strategies_applied'].append(f"Mode imputation for {col}")
                self.imputation_report['rows_affected'][col] = missing_count
                self.imputation_report['columns_processed'].append(col)
    
    def impute_categorical_high_missing(self):
        """Advanced imputation for categorical columns with higher missing rates."""
        print("\n=== ADVANCED CATEGORICAL IMPUTATION ===")
        
        for col in self.categorical_high_missing:
            if col not in self.df.columns:
                continue
                
            missing_count = self.df[col].isnull().sum()
            if missing_count == 0:
                continue
            
            # For medical data, create meaningful "Unknown" categories
            if col == 'Insurance Provider':
                impute_value = 'Self-Pay'  # Common in medical data
                print(f"Imputing {col}: {missing_count} missing → '{impute_value}' (domain-specific)")
            elif col == 'Medication':
                impute_value = 'No Medication'  # Medically meaningful
                print(f"Imputing {col}: {missing_count} missing → '{impute_value}' (domain-specific)")
            elif col == 'Admission Type':
                # Use most common admission type
                mode_val = self.df[col].mode()[0] if len(self.df[col].mode()) > 0 else 'Emergency'
                impute_value = mode_val
                print(f"Imputing {col}: {missing_count} missing → '{impute_value}' (mode)")
            else:
                impute_value = 'Unknown'
                print(f"Imputing {col}: {missing_count} missing → '{impute_value}' (generic)")
            
            self.df[col].fillna(impute_value, inplace=True)
            
            self.imputation_report['strategies_applied'].append(f"Domain-specific imputation for {col}")
            self.imputation_report['rows_affected'][col] = missing_count
            self.imputation_report['columns_processed'].append(col)
    
    def impute_numerical_data(self):
        """Impute numerical columns using statistical methods."""
        print("\n=== NUMERICAL DATA IMPUTATION ===")
        
        for col in self.numerical_missing:
            if col not in self.df.columns:
                continue
                
            missing_count = self.df[col].isnull().sum()
            if missing_count == 0:
                continue
            
            # For billing amounts, use median (robust to outliers)
            if 'billing' in col.lower() or 'amount' in col.lower():
                median_val = self.df[col].median()
                print(f"Imputing {col}: {missing_count} missing → {median_val:.2f} (median)")
                self.df[col].fillna(median_val, inplace=True)
            else:
                # Use mean for other numerical columns
                mean_val = self.df[col].mean()
                print(f"Imputing {col}: {missing_count} missing → {mean_val:.2f} (mean)")
                self.df[col].fillna(mean_val, inplace=True)
            
            self.imputation_report['strategies_applied'].append(f"Statistical imputation for {col}")
            self.imputation_report['rows_affected'][col] = missing_count
            self.imputation_report['columns_processed'].append(col)
    
    def impute_date_data(self):
        """Impute date columns using forward/backward fill."""
        print("\n=== DATE DATA IMPUTATION ===")
        
        for col in self.date_missing:
            if col not in self.df.columns:
                continue
                
            missing_count = self.df[col].isnull().sum()
            if missing_count == 0:
                continue
            
            # Sort by a related column first for better imputation
            if 'admission' in col.lower():
                # For admission dates, use forward fill then backward fill
                print(f"Imputing {col}: {missing_count} missing using forward/backward fill")
                self.df[col] = self.df[col].fillna(method='ffill').fillna(method='bfill')
            else:
                # For other dates, use similar strategy
                print(f"Imputing {col}: {missing_count} missing using forward/backward fill")
                self.df[col] = self.df[col].fillna(method='ffill').fillna(method='bfill')
            
            self.imputation_report['strategies_applied'].append(f"Forward/backward fill for {col}")
            self.imputation_report['rows_affected'][col] = missing_count
            self.imputation_report['columns_processed'].append(col)
    
    def handle_gender_missing(self):
        """Special handling for Gender missing values using ML approach."""
        print("\n=== GENDER IMPUTATION (ML APPROACH) ===")
        
        if 'Gender' not in self.df.columns:
            return
            
        missing_count = self.df['Gender'].isnull().sum()
        if missing_count == 0:
            return
        
        print(f"Gender missing values: {missing_count}")
        
        # In ML, we often predict missing categorical values using other features
        # For simplicity, we'll use the mode, but mention the advanced approach
        gender_mode = self.df['Gender'].mode()
        if len(gender_mode) > 0:
            mode_val = gender_mode[0]
            print(f"Using mode imputation: '{mode_val}'")
            print("Note: In production, consider using classification models to predict missing gender")
            
            self.df['Gender'].fillna(mode_val, inplace=True)
            
            self.imputation_report['strategies_applied'].append("Mode imputation for Gender (recommend ML prediction in production)")
            self.imputation_report['rows_affected']['Gender'] = missing_count
            self.imputation_report['columns_processed'].append('Gender')
    
    def validate_imputation(self):
        """Validate that imputation was successful."""
        print("\n=== IMPUTATION VALIDATION ===")
        
        remaining_missing = self.df.isnull().sum()
        remaining_missing = remaining_missing[remaining_missing > 0]
        
        if len(remaining_missing) == 0:
            print("✅ SUCCESS: No missing values remaining!")
        else:
            print("⚠️  Remaining missing values:")
            for col, count in remaining_missing.items():
                print(f"   {col}: {count}")
        
        return len(remaining_missing) == 0
    
    def fix_date_logic_errors(self):
        """Fix logical errors in date columns (discharge before admission)."""
        print("\n=== FIXING DATE LOGIC ERRORS ===")
        
        if 'Date of Admission' in self.df.columns and 'Discharge Date' in self.df.columns:
            # Calculate initial length of stay
            los_initial = (self.df['Discharge Date'] - self.df['Date of Admission']).dt.days
            
            # Find records where discharge is before admission
            negative_los = los_initial < 0
            negative_count = negative_los.sum()
            
            if negative_count > 0:
                print(f"Found {negative_count} records with discharge date before admission date")
                print("Fixing by swapping admission and discharge dates...")
                
                # Swap the dates for problematic records
                admission_temp = self.df.loc[negative_los, 'Date of Admission'].copy()
                self.df.loc[negative_los, 'Date of Admission'] = self.df.loc[negative_los, 'Discharge Date']
                self.df.loc[negative_los, 'Discharge Date'] = admission_temp
                
                self.imputation_report['strategies_applied'].append(f"Fixed {negative_count} date logic errors by swapping admission/discharge dates")
                self.imputation_report['rows_affected']['Date_Logic_Fix'] = negative_count
                
                # Verify the fix
                los_fixed = (self.df['Discharge Date'] - self.df['Date of Admission']).dt.days
                remaining_negative = (los_fixed < 0).sum()
                
                if remaining_negative == 0:
                    print(f"✅ Successfully fixed all date logic errors")
                else:
                    print(f"⚠️  {remaining_negative} records still have negative length of stay")
            else:
                print("No date logic errors found")
    
    def generate_ml_ready_features(self):
        """Generate additional ML-ready features."""
        print("\n=== GENERATING ML-READY FEATURES ===")
        
        # Feature 1: Length of Stay (after fixing date logic errors)
        if 'Date of Admission' in self.df.columns and 'Discharge Date' in self.df.columns:
            self.df['Length_of_Stay'] = (self.df['Discharge Date'] - self.df['Date of Admission']).dt.days
            
            # Validate length of stay
            los_stats = self.df['Length_of_Stay'].describe()
            print(f"Length of Stay statistics:")
            print(f"  Min: {los_stats['min']} days")
            print(f"  Max: {los_stats['max']} days") 
            print(f"  Mean: {los_stats['mean']:.1f} days")
            print(f"  Median: {los_stats['50%']} days")
            
            # Check for any remaining issues
            negative_los = (self.df['Length_of_Stay'] < 0).sum()
            if negative_los > 0:
                print(f"⚠️  Warning: {negative_los} records still have negative length of stay")
            else:
                print("✅ All length of stay values are non-negative")
            
            print("✅ Created 'Length_of_Stay' feature")
            self.imputation_report['strategies_applied'].append("Created Length_of_Stay feature with validation")
        
        # Feature 2: Age Groups
        if 'Age' in self.df.columns:
            self.df['Age_Group'] = pd.cut(self.df['Age'], 
                                        bins=[0, 18, 35, 50, 65, 100], 
                                        labels=['Child', 'Young_Adult', 'Adult', 'Middle_Age', 'Senior'])
            print("✅ Created 'Age_Group' feature")
            self.imputation_report['strategies_applied'].append("Created Age_Group categorical feature")
        
        # Feature 3: Billing Category
        if 'Billing Amount' in self.df.columns:
            billing_quantiles = self.df['Billing Amount'].quantile([0.25, 0.5, 0.75])
            self.df['Billing_Category'] = pd.cut(self.df['Billing Amount'],
                                               bins=[0, billing_quantiles[0.25], billing_quantiles[0.5], 
                                                    billing_quantiles[0.75], float('inf')],
                                               labels=['Low', 'Medium', 'High', 'Very_High'])
            print("✅ Created 'Billing_Category' feature")
            self.imputation_report['strategies_applied'].append("Created Billing_Category feature")
    
    def generate_imputation_report(self):
        """Generate comprehensive imputation report."""
        print("\n" + "="*60)
        print("ML-EXPERT MISSING VALUE IMPUTATION REPORT")
        print("="*60)
        
        print(f"Final dataset shape: {self.df.shape}")
        print(f"Columns processed: {len(self.imputation_report['columns_processed'])}")
        
        print("\nStrategies Applied:")
        for i, strategy in enumerate(self.imputation_report['strategies_applied'], 1):
            print(f"  {i}. {strategy}")
        
        print("\nRows Affected by Column:")
        for col, count in self.imputation_report['rows_affected'].items():
            print(f"  {col}: {count} rows imputed")
        
        print(f"\nFinal Missing Values Check:")
        final_missing = self.df.isnull().sum().sum()
        print(f"Total missing values: {final_missing}")
        
        if final_missing == 0:
            print("🎉 DATASET IS NOW 100% COMPLETE AND ML-READY!")
        
        print(f"\nData Types:")
        print(self.df.dtypes)
    
    def save_ml_ready_dataset(self, output_file):
        """Save the ML-ready dataset."""
        print(f"\nSaving ML-ready dataset to {output_file}...")
        self.df.to_csv(output_file, index=False)
        print("✅ ML-ready dataset saved successfully!")
        
        # Also save a summary
        summary_file = output_file.replace('.csv', '_summary.txt')
        with open(summary_file, 'w') as f:
            f.write("ML-READY DATASET SUMMARY\n")
            f.write("="*50 + "\n\n")
            f.write(f"Shape: {self.df.shape}\n")
            f.write(f"Missing values: {self.df.isnull().sum().sum()}\n")
            f.write(f"Columns: {list(self.df.columns)}\n\n")
            f.write("Imputation Strategies Applied:\n")
            for strategy in self.imputation_report['strategies_applied']:
                f.write(f"- {strategy}\n")
        
        print(f"✅ Summary saved to {summary_file}")
    
    def run_ml_imputation_pipeline(self, output_file):
        """Run the complete ML-expert imputation pipeline."""
        print("Starting ML-Expert Missing Value Imputation Pipeline")
        print("="*60)
        
        # Load and analyze
        self.load_data()
        self.analyze_missing_patterns()
        
        # Apply imputation strategies
        self.drop_pii_columns()
        self.impute_categorical_low_missing()
        self.impute_categorical_high_missing()
        self.impute_numerical_data()
        self.impute_date_data()
        self.handle_gender_missing()
        
        # Fix date logic errors BEFORE creating features
        self.fix_date_logic_errors()
        
        # Validate
        success = self.validate_imputation()
        
        # Generate ML features (after date fixes)
        self.generate_ml_ready_features()
        
        # Report and save
        self.generate_imputation_report()
        
        if output_file:
            self.save_ml_ready_dataset(output_file)
        
        return self.df, success

def main():
    """Main function."""
    input_file = "Hospital_dataset.csv"  # Start from original data
    output_file = "Hospital_dataset_ML_ready.csv"
    
    # Initialize handler
    handler = MLExpertMissingValueHandler(input_file)
    
    # Run pipeline
    ml_ready_data, success = handler.run_ml_imputation_pipeline(output_file)
    
    if success:
        print("\n🚀 DATASET IS NOW ML-READY!")
        print(f"✅ No missing values")
        print(f"✅ PII removed") 
        print(f"✅ Additional ML features created")
        print(f"✅ Saved as: {output_file}")
    else:
        print("\n⚠️  Some issues remain - please review")

if __name__ == "__main__":
    main()
