<<<<<<< HEAD
"""
Mining Process Flotation Plant Analysis
IND-01: Slag/Residue Generation
Unique Filter: Hour 3 (3 AM) + % Silica Feed between 14.0 and 15.0
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.animation import FuncAnimation
import warnings
warnings.filterwarnings('ignore')

class FlotationPipeline:
    """Complete pipeline for mining flotation process analysis"""
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.raw_data = None
        self.cleaned_data = None
        self.filtered_data = None
        
    def load_data(self):
        """Function 1: Data Ingestion with error handling"""
        try:
            self.raw_data = pd.read_csv(self.filepath)
            print(f"✅ Loaded {len(self.raw_data)} rows")
            return True
        except FileNotFoundError:
            print("❌ Error: File not found. Check path.")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def clean_data(self):
        """Function 2: Cleaning - fix types, handle nulls, duplicates"""
        self.cleaned_data = self.raw_data.copy()
        
        # Convert date
        self.cleaned_data['date'] = pd.to_datetime(self.cleaned_data['date'])
        
        # Convert numeric columns (handle comma decimals)
        numeric_cols = self.cleaned_data.columns.drop('date')
        for col in numeric_cols:
            self.cleaned_data[col] = (self.cleaned_data[col]
                                       .astype(str)
                                       .str.replace(',', '.')
                                       .astype(float))
        
        # Handle missing values
        if self.cleaned_data.isnull().sum().sum() > 0:
            self.cleaned_data = self.cleaned_data.fillna(self.cleaned_data.median())
        
        # Remove duplicates
        self.cleaned_data = self.cleaned_data.drop_duplicates()
        
        print(f"✅ Cleaned data: {len(self.cleaned_data)} rows")
        return True
    
    def apply_filter(self):
        """Function 3: YOUR UNIQUE FILTER - Hour 3 + Silica Feed 14-15%"""
        self.filtered_data = self.cleaned_data[
            (self.cleaned_data['date'].dt.hour == 3) &
            (self.cleaned_data['% Silica Feed'] > 14.0) &
            (self.cleaned_data['% Silica Feed'] < 15.0)
        ].copy()
        
        print(f"✅ Unique filter applied: {len(self.filtered_data)} rows")
        print(f"   (Hour=3, Silica Feed between 14.0-15.0%)")
        return True
    
    def compute_statistics(self):
        """Function 4: NumPy-based statistics"""
        target = self.filtered_data['% Silica Concentrate'].values
        
        stats = {
            'Mean': np.mean(target),
            'Median': np.median(target),
            'Standard Deviation': np.std(target),
            'Variance': np.var(target),
            'Minimum': np.min(target),
            'Maximum': np.max(target),
            'Range': np.max(target) - np.min(target),
            'Skewness': float(((target - np.mean(target))**3).mean() / (np.std(target)**3))
        }
        
        print("\n" + "="*50)
        print("📊 STATISTICS - % Silica Concentrate (Impurity)")
        print("="*50)
        for key, value in stats.items():
            print(f"   {key:20s}: {value:.4f}")
        
        return stats
    
    def analyze_correlations(self):
        """Function 5: Correlation analysis"""
        key_cols = ['% Silica Feed', 'Starch Flow', 'Amina Flow', 
                    'Ore Pulp pH', 'Flotation Column 01 Air Flow',
                    '% Silica Concentrate']
        
        key_cols = [c for c in key_cols if c in self.filtered_data.columns]
        corr_matrix = self.filtered_data[key_cols].corr()
        
        target_corr = corr_matrix['% Silica Concentrate'].drop('% Silica Concentrate')
        strongest = target_corr.abs().idxmax()
        
        print("\n" + "="*50)
        print("🔗 CORRELATION ANALYSIS")
        print("="*50)
        print(f"   Strongest correlate with impurity: {strongest}")
        print(f"   Correlation coefficient: {target_corr[strongest]:.4f}")
        
        return corr_matrix
    
    def create_visualizations(self):
        """Function 6: 3 Static + 2 Animated plots"""
        
        print("\n" + "="*50)
        print("📈 GENERATING VISUALIZATIONS")
        print("="*50)
        
        # Static Plot 1: Histogram
        plt.figure(figsize=(10, 6))
        plt.hist(self.filtered_data['% Silica Concentrate'], bins=30, edgecolor='black', alpha=0.7)
        plt.xlabel('% Silica Concentrate (Impurity)', fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.title('Distribution of Silica Impurity at 3 AM (14-15% Feed)', fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.savefig('outputs/static_histogram.png', dpi=150)
        plt.close()
        print("   ✅ Saved: static_histogram.png")
        
        # Static Plot 2: Boxplot by Month
        self.filtered_data['month'] = self.filtered_data['date'].dt.month
        plt.figure(figsize=(12, 6))
        self.filtered_data.boxplot(column='% Silica Concentrate', by='month')
        plt.title('Monthly Variation of Silica Impurity', fontsize=14)
        plt.suptitle('')
        plt.xlabel('Month', fontsize=12)
        plt.ylabel('% Silica Concentrate', fontsize=12)
        plt.savefig('outputs/static_boxplot.png', dpi=150)
        plt.close()
        print("   ✅ Saved: static_boxplot.png")
        
        # Static Plot 3: Correlation Heatmap
        corr = self.filtered_data.select_dtypes(include=[np.number]).corr()
        top_vars = ['% Silica Feed', '% Silica Concentrate', 'Starch Flow', 
                    'Amina Flow', 'Ore Pulp pH', 'Flotation Column 01 Air Flow']
        top_vars = [v for v in top_vars if v in corr.columns]
        corr_subset = corr.loc[top_vars, top_vars]
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_subset, annot=True, cmap='coolwarm', center=0, fmt='.2f', square=True)
        plt.title('Correlation Matrix - Key Process Variables', fontsize=14)
        plt.tight_layout()
        plt.savefig('outputs/static_heatmap.png', dpi=150)
        plt.close()
        print("   ✅ Saved: static_heatmap.png")
        
        # Animated Plot 1: Time Trend
        try:
            fig, ax = plt.subplots(figsize=(12, 6))
            sorted_data = self.filtered_data.sort_values('date')
            dates = sorted_data['date']
            impurity = sorted_data['% Silica Concentrate']
            
            def animate_trend(frame):
                ax.clear()
                data_up_to = impurity.iloc[:frame+1]
                dates_up_to = dates.iloc[:frame+1]
                ax.plot(dates_up_to, data_up_to, 'b-', linewidth=1.5)
                ax.set_xlabel('Date', fontsize=12)
                ax.set_ylabel('% Silica Concentrate', fontsize=12)
                ax.set_title(f'Impurity Trend Over Time', fontsize=14)
                ax.tick_params(axis='x', rotation=45)
                ax.grid(True, alpha=0.3)
                plt.tight_layout()
            
            n_frames = min(200, len(dates))
            anim = FuncAnimation(fig, animate_trend, frames=n_frames, repeat=False)
            anim.save('outputs/animation_trend.gif', writer='pillow', fps=20)
            plt.close()
            print("   ✅ Saved: animation_trend.gif")
        except Exception as e:
            print(f"   ⚠️ Animation 1 issue: {e}")
        
        # Animated Plot 2: Distribution Shift
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            self.filtered_data['week'] = self.filtered_data['date'].dt.isocalendar().week
            weeks = sorted(self.filtered_data['week'].unique())
            
            def animate_distribution(frame):
                ax.clear()
                week_data = self.filtered_data[self.filtered_data['week'] == weeks[frame]]
                ax.hist(week_data['% Silica Concentrate'], bins=20, alpha=0.7, edgecolor='black', color='steelblue')
                ax.set_xlabel('% Silica Concentrate', fontsize=12)
                ax.set_ylabel('Frequency', fontsize=12)
                ax.set_title(f'Impurity Distribution - Week {weeks[frame]}', fontsize=14)
                ax.grid(True, alpha=0.3)
            
            n_weeks = min(20, len(weeks))
            anim2 = FuncAnimation(fig, animate_distribution, frames=n_weeks, repeat=False)
            anim2.save('outputs/animation_distribution.gif', writer='pillow', fps=5)
            plt.close()
            print("   ✅ Saved: animation_distribution.gif")
        except Exception as e:
            print(f"   ⚠️ Animation 2 issue: {e}")
        
        return True
    
    def comparative_analysis(self):
        """Comparative analysis: High vs Low Starch Flow"""
        median_starch = self.filtered_data['Starch Flow'].median()
        
        high_starch = self.filtered_data[self.filtered_data['Starch Flow'] > median_starch]
        low_starch = self.filtered_data[self.filtered_data['Starch Flow'] <= median_starch]
        
        print("\n" + "="*50)
        print("📊 COMPARATIVE ANALYSIS: High Starch vs Low Starch")
        print("="*50)
        print(f"   High Starch Flow (> {median_starch:.1f}): {len(high_starch)} rows")
        print(f"   Low Starch Flow (≤ {median_starch:.1f}): {len(low_starch)} rows")
        print(f"\n   Mean Impurity (High Starch): {np.mean(high_starch['% Silica Concentrate']):.4f}")
        print(f"   Mean Impurity (Low Starch): {np.mean(low_starch['% Silica Concentrate']):.4f}")
        print(f"   Difference: {np.mean(high_starch['% Silica Concentrate']) - np.mean(low_starch['% Silica Concentrate']):.4f}")
        
        # Save comparison plot
        plt.figure(figsize=(8, 6))
        plt.boxplot([high_starch['% Silica Concentrate'], low_starch['% Silica Concentrate']], 
                    labels=['High Starch', 'Low Starch'])
        plt.ylabel('% Silica Concentrate', fontsize=12)
        plt.title('Impurity Comparison: High vs Low Starch Flow', fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.savefig('outputs/comparison_boxplot.png', dpi=150)
        plt.close()
        print("   ✅ Saved: comparison_boxplot.png")
        
        return {
            'high_starch_mean': np.mean(high_starch['% Silica Concentrate']),
            'low_starch_mean': np.mean(low_starch['% Silica Concentrate']),
            'difference': np.mean(high_starch['% Silica Concentrate']) - np.mean(low_starch['% Silica Concentrate'])
        }
    
    def export_data(self):
        """Save cleaned and filtered data"""
        self.filtered_data.to_csv('data/dataset_cleaned.csv', index=False)
        print(f"\n✅ Cleaned data saved to data/dataset_cleaned.csv")
    
    def run_pipeline(self):
        """Run everything"""
        print("\n" + "="*50)
        print("🏭 MINING PROCESS FLOTATION ANALYSIS")
        print("   IND-01: Slag/Residue Generation")
        print("="*50)
        
        if not self.load_data():
            return
        self.clean_data()
        self.apply_filter()
        
        if len(self.filtered_data) == 0:
            print("❌ Filter returned no data! Check your filter logic.")
            return
        
        self.compute_statistics()
        self.analyze_correlations()
        self.create_visualizations()
        self.comparative_analysis()
        self.export_data()
        
        print("\n" + "="*50)
        print("🎉 PIPELINE COMPLETE!")
        print("="*50)


# ============================================
# RUN THE PIPELINE
# ============================================
if __name__ == "__main__":
    pipeline = FlotationPipeline('data/MiningProcess_Flotation_Plant_Database.csv')
    pipeline.run_pipeline()
=======

>>>>>>> adb9fc5a3738dcde79e8c651952153c45809a6c5
