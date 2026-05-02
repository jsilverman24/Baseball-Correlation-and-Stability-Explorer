import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import streamlit as st
import gdown
#load Dataframes for 24 and 25 years
@st.cache_data
def load_pitch_data():
    url = "https://drive.google.com/uc?id=1KDJ5NLOX7Z0zpAxlW3uVCiUTPWw9dLyP"
    gdown.download(url, "pitches_25.csv", quiet=False)
    return pd.read_csv("pitches_25.csv")

@st.cache_data
def load_stat_data():
    df_25 = pd.read_csv("stats-2.csv")
    df_24 = pd.read_csv("stats-3.csv")
    return df_25, df_24

pitch = load_pitch_data()
df_25, df_24 = load_stat_data()
#clean data by only taking numbers and dropping some variables
corrs_df_24 = df_24.select_dtypes('number')
corrs_df_24 = corrs_df_24.drop(['b_rbi', 'b_lob', 'player_age','b_total_bases', 'r_total_caught_stealing', 'r_total_stolen_base', 'b_ab_scoring', 'b_ball', 'b_called_strike', 'b_catcher_interf', 'b_foul', 'b_foul_tip', 'b_game', 'b_gnd_into_dp', 'b_gnd_into_tp', 'b_gnd_rule_double', 'b_hit_by_pitch', 'b_hit_ground', 'b_hit_fly', 'b_hit_into_play', 'b_hit_line_drive', 'b_hit_popup', 'b_out_fly', 'b_out_ground', 'b_out_line_drive', 'b_out_popup','flareburner_percent', 'poorlyunder_percent', 'poorlytopped_percent', 'poorlyweak_percent','pitch_count_offspeed', 'pitch_count_fastball', 'pitch_count_breaking', 'pitch_count','maxeff_arm_2b_3b_sba', 'n_outs_above_average', 'rel_league_reaction_distance', 'rel_league_burst_distance', 'rel_league_routing_distance',
  'swords','solidcontact_percent','popups','groundballs','flyballs','linedrives','batted_ball',
   'out_zone_swing','f_strike_percent','vertical_swing_path','out_zone_swing_miss','in_zone','out_zone', 'out_zone_percent','avg_hyper_speed', 'year','blasts_contact', 'edge','blasts_swing','bacon','xbacon','xbadiff', 'xslgdiff', 'wobadiff','ideal_angle_rate','xobp','xiso']
                               ,axis = 1)
corrs_df_25 = df_25.select_dtypes('number')
corrs_df_25 = corrs_df_25.drop(['b_rbi', 'player_age','b_lob', 'b_total_bases', 'r_total_caught_stealing', 'r_total_stolen_base', 'b_ab_scoring', 'b_ball', 'b_called_strike', 'b_catcher_interf', 'b_foul', 'b_foul_tip', 'b_game', 'b_gnd_into_dp', 'b_gnd_into_tp', 'b_gnd_rule_double', 'b_hit_by_pitch', 'b_hit_ground', 'b_hit_fly', 'b_hit_into_play', 'b_hit_line_drive', 'b_hit_popup', 'b_out_fly', 'b_out_ground', 'b_out_line_drive', 'b_out_popup','flareburner_percent', 'poorlyunder_percent', 'poorlytopped_percent', 'poorlyweak_percent','pitch_count_offspeed', 'pitch_count_fastball', 'pitch_count_breaking', 'pitch_count','maxeff_arm_2b_3b_sba', 'n_outs_above_average', 'rel_league_reaction_distance', 'rel_league_burst_distance', 'rel_league_routing_distance',
  'swords','solidcontact_percent','popups','groundballs','flyballs','linedrives','batted_ball',
   'out_zone_swing','f_strike_percent','vertical_swing_path','year','out_zone_swing_miss','in_zone','out_zone', 'out_zone_percent','avg_hyper_speed', 'blasts_contact', 'edge','blasts_swing','bacon','xbacon','xbadiff', 'xslgdiff', 'wobadiff','ideal_angle_rate','xobp','xiso']
                               ,axis = 1)

# rename columns but keep player_id as is
corrs_df_24.columns = [c if c == 'player_id' else c.replace("percent","%").replace("_"," ").replace("z","zone").replace("avg","Average").replace("slg","Slugging").replace("opposite","Oppo").title() for c in corrs_df_24.columns]
corrs_df_25.columns = [c if c == 'player_id' else c.replace("percent","%").replace("_"," ").replace("z","zone").replace("avg","Average").replace("slg","Slugging").replace("opposite","Oppo").title() for c in corrs_df_25.columns]

# stat columns only (no player_id)
stat_cols_24 = [c for c in corrs_df_24.columns if c not in ('player_id', 'Player Id')]
stat_cols_25 = [c for c in corrs_df_25.columns if c not in ('player_id', 'Player Id')]

#create title
st.title("Correlation Explorer")
#let user pick year for X and Y variables
x_year = st.radio("Select Year for X variable", [2024, 2025])
y_year = st.radio("Select Year for Y variable", [2024, 2025])
#set up dataframes based on the users' year picked
if x_year == 2024:
    x_var = st.selectbox("Choose X variable",stat_cols_24)
    x_df = corrs_df_24
else:
    x_var = st.selectbox("Choose X variable", stat_cols_25)
    x_df = corrs_df_25
if y_year == 2024:
    y_var = st.selectbox("Choose Y variable",stat_cols_25)
    y_df = corrs_df_24
else:
    y_var = st.selectbox("Choose Y variable", stat_cols_24)
    y_df = corrs_df_25

#run graph function
if x_var and y_var:

    #filter for player id and variable, rename the column n
    x_col = x_df[['player_id', x_var]].rename(columns={x_var: 'x_val'})
    y_col = y_df[['player_id', y_var]].rename(columns={y_var: 'y_val'})

    #merge these two on player id
    graph_df = pd.merge(x_col, y_col, on='player_id', how='inner')
    #create correlation
    corr = graph_df['x_val'].corr(graph_df['y_val'])
    st.write(f"Correlation: {corr}")
    #create graph
    fig, ax = plt.subplots()
    ax.set_xlabel(x_var)
    ax.set_ylabel(y_var)
    sns.scatterplot(data=graph_df, x='x_val', y='y_val', ax=ax)
    st.pyplot(fig)

st.title("Stability Explorer")

#create definitions for the variables within the pitch by pitch dataset
stat_definitions = {
    'Hard Hit Percentage': lambda df: (df['launch_speed'] >= 95).astype(float),
    'Sweet Spot Percentage': lambda df: (df['launch_angle'].between(8, 32)).astype(float),
    'Barrel': lambda df: (df['launch_speed_angle'] == 6).astype(float),
    'Bat Speed': lambda df: df['bat_speed'],
    'strikeout': lambda df: (df['events'] == 'strikeout').astype(float),
    'Walk': lambda df: (df['events'] == 'walk').astype(float),
    'Xwoba': lambda df: df['estimated_woba_using_speedangle'],
    'Xba': lambda df: df['estimated_ba_using_speedangle'],
    'Xslugging': lambda df: df['estimated_slg_using_speedangle'],
    'Swing Length': lambda df: df['swing_length'],
    'Attack Angle': lambda df: df['attack_angle'],
    'Woba': lambda df: df['woba_value'],
}

#get variable from the user based on the stats provided
x_var = st.selectbox("Choose variable",stat_definitions)
#run stability
if x_var:

    #filter to only end of plate appearances, not pitch by pitch
    pa_level = pitch[pitch['events'].notna()].copy()
    if x_var in ['Hard Hit Percentage', 'Sweet Spot Percentage', 'Barrel', 'xba', 'Xwoba', 'Xslugging', 'Woba']:
        #these need launch speeds to be non-0
        pa_level = pa_level[pa_level['launch_speed'].notna()]
    # create stat value column which takes the pa level and applies conditions of the x var
    pa_level['stat_value'] = stat_definitions[x_var](pa_level)

    # get the plate appearance number for each batter and descend the order in the pa_num column
    pa_level['pa_num'] = pa_level.groupby('batter')['at_bat_number'].rank(method='first')

    # get max pa from all the batters and take the 90th percentile. make it an int so it can be in range
    max_pa = int(pa_level.groupby('batter')['pa_num'].max().quantile(0.9))
    # create thresholds
    min_pa = 0
    thresholds = range(min_pa, max_pa, 10)
    results = []
    #run for each threshold
    for threshold in thresholds:
        # get each players plate appearance number
        player_counts = pa_level.groupby('batter')['pa_num'].max()
        # see if they are qualified and grab their index number
        qualified = player_counts[player_counts >= min_pa].index
        # makes sure a player is qualified and below the thrsehold
        subset = pa_level[
            (pa_level['batter'].isin(qualified)) & (pa_level['pa_num'] <= threshold)
            ]

        # splitting the plate appearnaces into even and odds to run correlaitons
        odd = subset[subset['pa_num'] % 2 == 1].groupby('batter')['stat_value'].mean()
        even = subset[subset['pa_num'] % 2 == 0].groupby('batter')['stat_value'].mean()
        # combine into one dataframe
        combined = pd.concat([odd, even], axis=1).dropna()
        combined.columns = ['odd', 'even']

        if len(combined) < 10:
            continue

        # get pearsons
        r, p_value = stats.pearsonr(combined['odd'], combined['even'])

        # get spearman-browns
        sb = (2 * r) / (1 + r)
        #add results back
        results.append({"pa": threshold, "correlation": sb})

    results_df = pd.DataFrame(results)

    # create stabilized dataframe for when its above .707 at each threshold
    stabilized = results_df[results_df['correlation'] >= .707]
    if len(stabilized) > 0:
        #finds the minimum of those stabilized and prints it
        st.write(f"Stabilized at: {stabilized['pa'].min()} PA's")
    else:
        st.write("Never stabilized")
    #plot it
    fig,ax = plt.subplots()
    sns.lineplot(data = results_df, x = 'pa', y = 'correlation', ax = ax)
    plt.axhline(y = .707,color='red',linestyle='--')
    st.write("Stabilizes at Spearman-Brown of.707, where R^2 is 0.50 and 50% of the variance is explained")
    st.pyplot(fig)
