import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import calendar
import plotly.express as px
import networkx as nx
from scipy.stats import ttest_ind

# Create output folder if it doesn't exist
output_folder = "output"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 1) Data loading and initial cleaning
def load_and_preprocess(file_path): 
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
    df['Month_Num'] = df['Date'].dt.month
    df['Year'] = df['Date'].dt.year
    df['Month_Name'] = df['Date'].dt.month_name() 
    return df

# 2) Visualization Functions
def plot_unemployment_trend(df):
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x='Date', y='Estimated Unemployment Rate (%)', color='#2c3e50')
    plt.axvspan(pd.Timestamp('2020-03-25'), pd.Timestamp('2020-06-30'), 
                color='red', alpha=0.1, label='Initial Lockdown Period')
    plt.title('Unemployment Rate Trend: 2020 Analysis')
    plt.legend()
    plt.savefig(os.path.join(output_folder, 'unemployment_trend.png'))
    plt.show()

def plot_area_comparison(df):
    plt.figure(figsize=(10, 5))
    # Fixed FutureWarning by assigning hue
    sns.boxplot(x='Area', y='Estimated Unemployment Rate (%)', hue='Area', data=df, palette='Set2', legend=False)
    plt.title('Unemployment Distribution: Urban vs Rural')
    plt.savefig(os.path.join(output_folder, 'urban_rural_comparison.png'))
    plt.show()

# 4) SNA Analysis: Bipartite and Correlation Networks
def run_sna_analysis(df):
    B = nx.Graph()
    regions = df['Region'].unique()
    months = df['Month_Name'].unique()
    B.add_nodes_from(regions, bipartite=0)
    B.add_nodes_from(months, bipartite=1)
    
    for _, row in df.iterrows():
        B.add_edge(row['Region'], row['Month_Name'], weight=row['Estimated Unemployment Rate (%)'])
    
    pivot_df = df.pivot_table(index='Month_Name', columns='Region', values='Estimated Unemployment Rate (%)')
    corr_matrix = pivot_df.corr()
    
    G_corr = nx.Graph()
    for i in range(len(corr_matrix.columns)):
        for j in range(i):
            if corr_matrix.iloc[i, j] > 0.8:
                G_corr.add_edge(corr_matrix.columns[i], corr_matrix.columns[j], 
                               weight=corr_matrix.iloc[i, j])
    
    betweenness = nx.betweenness_centrality(G_corr)
    print("SNA Analysis Complete.")
    print(f"Top 'Bridge' Region: {max(betweenness, key=betweenness.get)}")
    
    # Visualizing and saving the Correlation Network
    
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G_corr, k=0.5)
    nx.draw(G_corr, pos, with_labels=True, node_color='skyblue', 
            node_size=2000, edge_color='gray', font_size=10)
    plt.title("Regional Correlation Network (Similarity > 0.8)")
    plt.savefig(os.path.join(output_folder, 'sna_correlation_network.png'))
    plt.show()
    return B, G_corr

# 5) Statistical Impact Analysis
def perform_impact_stats(df):
    lockdown = df[(df['Date'] >= '2020-04-01') & (df['Date'] <= '2020-06-30')]
    recovery = df[(df['Date'] >= '2020-07-01') & (df['Date'] <= '2020-11-30')]
    
    t_stat, p_val = ttest_ind(lockdown['Estimated Unemployment Rate (%)'], 
                              recovery['Estimated Unemployment Rate (%)'])
    
    plt.figure(figsize=(8, 5))
    # Fixed FutureWarning by assigning hue
    categories = ['Lockdown (Apr-Jun)', 'Recovery (Jul-Nov)']
    means = [lockdown['Estimated Unemployment Rate (%)'].mean(), 
             recovery['Estimated Unemployment Rate (%)'].mean()]
    sns.barplot(x=categories, y=means, hue=categories, palette='magma', legend=False)
    plt.ylabel('Mean Unemployment Rate (%)')
    plt.title(f'Statistical Comparison (p-value: {p_val:.4f})')
    plt.savefig(os.path.join(output_folder, 'statistical_impact.png'))
    plt.show()
    
    print(f"--- Statistical Analysis ---")
    print(f"T-Statistic: {t_stat:.4f}")
    print(f"P-Value: {p_val:.4f}")


# 6) Geospatial Heatmap Animation
def plot_animated_map(df):
    df = df.copy()
    
    # columns are swapped in the CSV — swapping them back
    df['latitude'], df['longitude'] = df['longitude'].copy(), df['latitude'].copy()
    
    df = df.dropna(subset=['latitude', 'longitude']).sort_values('Date')
    df['Date_Str'] = df['Date'].dt.strftime('%Y-%m')
    df['Date_Label'] = df['Date'].dt.strftime('%B %Y')

    fig = px.scatter_geo(
        df,
        lat='latitude',
        lon='longitude',
        color='Estimated Unemployment Rate (%)',
        hover_name='Region',
        hover_data={'Date_Label': True, 'Date_Str': False},
        size='Estimated Unemployment Rate (%)',
        animation_frame='Date_Str',
        color_continuous_scale='Reds',
        size_max=30,
        scope='asia',
        template='plotly_dark',
        title='India Regional Unemployment Rate (2020)'
    )

    fig.update_geos(
        lataxis_range=[5, 38],
        lonaxis_range=[65, 100],
        showland=True,
        landcolor='#2a2a2a',
        showocean=True,
        oceancolor='#1a1a2e',
        showcoastlines=True,
        coastlinecolor='gray'
    )

    fig.update_layout(
        coloraxis_colorbar=dict(title='Unemployment %'),
        margin=dict(l=0, r=0, t=40, b=0)
    )

    # Save animated map as HTML file 
    fig.write_html(os.path.join(output_folder, 'animated_unemployment_map.html'))
    fig.show(renderer="browser") # This forces it to open in your default browser


# 7) Main Execution Block
if __name__ == "__main__":
    df_covid = load_and_preprocess('Unemployment_Rate_upto_11_2020.csv')
    df_india = load_and_preprocess('Unemployment in India.csv')
    
    plot_unemployment_trend(df_covid)
    plot_area_comparison(df_india)
    perform_impact_stats(df_covid)
    bipartite_g, correlation_g = run_sna_analysis(df_covid)
    plot_animated_map(df_covid)