import streamlit as st
import pandas as pd

# Load IPL data from xlsb
@st.cache_data
def load_data():
    return pd.read_excel('ball_by_ball_ipl.xlsb', engine='pyxlsb')

data = load_data()

# Function to calculate stats
def calculate_stats(batter, bowler, data):
    batter_data = data[(data['Batter'] == batter) & (data['Bowler'] == bowler)]
    bowler_data = data[(data['Batter'] == bowler) & (data['Bowler'] == batter)]
    
    # Bowler to Batsman
    balls_bowled = len(batter_data)
    dismissals = batter_data['Wicket'].sum()
    avg_balls_to_dismiss = balls_bowled / dismissals if dismissals > 0 else None
    runs_conceded = batter_data['Runs From Ball'].sum()
    bowling_avg = runs_conceded / dismissals if dismissals > 0 else None

    # Batsman to Bowler
    balls_faced = len(bowler_data)
    singles = len(bowler_data[bowler_data['Batter Runs'] == 1])
    fours = len(bowler_data[bowler_data['Batter Runs'] == 4])
    sixes = len(bowler_data[bowler_data['Batter Runs'] == 6])
    dismissals_against = bowler_data['Wicket'].sum()
    batting_avg = bowler_data['Batter Runs'].sum() / dismissals_against if dismissals_against > 0 else None

    stats = {
        'bowler_to_batter': {
            'balls_bowled': balls_bowled,
            'dismissals': dismissals,
            'avg_balls_to_dismiss': avg_balls_to_dismiss,
            'bowling_avg': bowling_avg
        },
        'batter_to_bowler': {
            'balls_faced': balls_faced,
            'singles': singles,
            'fours': fours,
            'sixes': sixes,
            'dismissals_against': dismissals_against,
            'batting_avg': batting_avg
        }
    }
    
    return stats

# Streamlit App
st.title("IPL Player Comparison")

# Drag and Drop functionality (using selectbox as drag-and-drop alternative)
players = list(data['Batter'].unique())
batter = st.selectbox("Select Batter", players)
bowler = st.selectbox("Select Bowler", players)

if st.button("Compare"):
    stats = calculate_stats(batter, bowler, data)
    
    st.write(f"### {batter} (Batsman) vs {bowler} (Bowler)")
    st.write(f"**{bowler} to {batter}:**")
    st.write(f"- Balls Bowled: {stats['bowler_to_batter']['balls_bowled']}")
    st.write(f"- Times Dismissed: {stats['bowler_to_batter']['dismissals']}")
    st.write(f"- Average Balls to Dismiss: {stats['bowler_to_batter']['avg_balls_to_dismiss']}")
    st.write(f"- Bowling Average: {stats['bowler_to_batter']['bowling_avg']}")
    
    st.write(f"**{batter} to {bowler}:**")
    st.write(f"- Balls Faced: {stats['batter_to_bowler']['balls_faced']}")
    st.write(f"- Singles: {stats['batter_to_bowler']['singles']}")
    st.write(f"- Fours: {stats['batter_to_bowler']['fours']}")
    st.write(f"- Sixes: {stats['batter_to_bowler']['sixes']}")
    st.write(f"- Times Dismissed: {stats['batter_to_bowler']['dismissals_against']}")
    st.write(f"- Batting Average: {stats['batter_to_bowler']['batting_avg']}")

    # Save stats to .xlsb file
    stats_df = pd.DataFrame(stats)
    stats_file_path = "player_comparison_stats.xlsb"
    stats_df.to_excel(stats_file_path, engine="pyxlsb", index=False)
    st.write(f"Statistics saved to {stats_file_path} successfully.")

if __name__ == "__main__":
    st.write("Streamlit app to compare IPL players.")
