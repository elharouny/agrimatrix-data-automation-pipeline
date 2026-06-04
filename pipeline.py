import pandas as pd
import json
import logging
from datetime import datetime

# Setup professional logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataAutomationPipeline:
    def __init__(self, config_path):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        logging.info("Pipeline configuration loaded successfully.")

    def extract_data(self, file_path):
        """Extract agricultural batch records from CSV/Excel"""
        logging.info(f"Extracting data from: {file_path}")
        return pd.read_csv(file_path)

    def validate_and_transform(self, df):
        """Clean data and validate export compliance metrics"""
        logging.info("Transforming and validating data metrics...")
        
        # 1. Standardize column formatting
        df.columns = df.columns.str.strip().str.lower()
        
        # 2. Check for missing critical values and fill or drop
        df['pesticide_level_ppm'] = df['pesticide_level_ppm'].fillna(0.0)
        
        # 3. Compliance evaluation logic against dynamic thresholds
        max_allowed_pesticide = self.config['compliance']['max_pesticide_ppm']
        min_required_quality = self.config['compliance']['min_quality_score']
        
        df['export_compliant'] = (df['pesticide_level_ppm'] <= max_allowed_pesticide) & \
                                 (df['quality_score'] >= min_required_quality)
        
        # 4. Data Enrichment: Timestamp the processing event
        df['processed_at'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        return df

    def load_and_report(self, df, output_path):
        """Load compliant batches and export detailed auditing reports"""
        df.to_csv(output_path, index=False)
        
        total_batches = len(df)
        compliant_count = df['export_compliant'].sum()
        failure_rate = ((total_batches - compliant_count) / total_batches) * 100
        
        report_summary = {
            "execution_time": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            "total_processed_batches": int(total_batches),
            "approved_export_batches": int(compliant_count),
            "rejection_rate_percentage": round(failure_rate, 2)
        }
        
        logging.info(f"Pipeline executed. Rejection Rate: {report_summary['rejection_rate_percentage']}%")
        return report_summary

# Quick Execution Example
if __name__ == "__main__":
    # Simulated structure
    pass
