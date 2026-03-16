import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# Session state storage for dataset
if "df2" not in st.session_state:
    st.session_state.df2 = None

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="T20 Cricket Team Analysis",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>

div.stButton > button {
    background-color: #ff4b4b;
    color: white;
    font-weight: 600;
    border-radius: 8px;
    height: 45px;
    border: none;
}

div.stButton > button:hover {
    background-color: #e63939;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# DATA VALIDATION FUNCTION
# -------------------------------------------------

def data_validation(df):

    bat_stats = (df["Batting_Start_Over"].isnull() &
                (df["Out_Over"].notnull() |
                 df["Balls_Played"].notnull() |
                 df["Runs_Scored"].notnull()))

    bat_stats2 = (df["Batting_Start_Over"].notnull() &
                  (df["Out_Over"].isnull()))

    bowl_stats = ((df["Overs_Bowled"].isnull() | df["Overs_Bowled"] == 0) &
                  (df["Runs_Given"].notnull() | df["Wickets_Taken"].notnull()))

    invalid_player = ((df["Player_Name"].isnull()) &
                     (df["Role"].notnull() |
                      df["Batting_Position"].notnull() |
                      df["Batting_Start_Over"].notnull() |
                      df["Out_Over"].notnull() |
                      df["Balls_Played"].notnull() |
                      df["Runs_Scored"].notnull() |
                      df["Overs_Bowled"].notnull() |
                      df["Runs_Given"].notnull() |
                      df["Wickets_Taken"].notnull()))

    no_match = df["Match_No"].isnull()
    no_position = df["Batting_Position"].isnull()

    if no_match.any():
        raise ValueError("Some players don't have Match Number information")

    elif no_position.any():
        raise ValueError("Some players don't have Batting Position information")

    elif invalid_player.any():
        raise ValueError("Some players don't have their name")

    elif (bat_stats.any()) or (bat_stats2.any()):
        raise ValueError("Invalid data found in batting columns")

    elif bowl_stats.any():
        raise ValueError("Invalid data found in bowling columns")

    return True


# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

with st.sidebar:

    st.markdown(
    """
    <div style='text-align:center; font-size:30px;'>
         Dashboard Menu
    </div>
    """,
    unsafe_allow_html=True
    )

    page = st.radio("",["Analyze your Dataset","About"])

    st.markdown("---")

    st.markdown(
        """
        **Current Version : 2.0**

        **Last Updated On : 16th March 2026**
        """
    )


# -------------------------------------------------
# MAIN PAGE CONTENT
# -------------------------------------------------

left, center, right = st.columns([1,3,1])

with center:

    if page == "Analyze your Dataset":

        st.markdown(
            """
            <h2 style='text-align:center;'>🏏 T20 Cricket Team Performance Analysis Dashboard</h2>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <p style='text-align:center; color:gray; font-size:18px;'>
            Analyze your cricket team's performance using T20 match data
            </p>
            """,
            unsafe_allow_html=True
        )

        st.markdown("")

        dataset_loaded = st.session_state.get("df2") is not None######

        tab1, tab2, tab3, tab4 = st.tabs(
            ["Dataset","Batting Analytics","Bowling Analytics","Summary"]
        )

        # ======================================================
        # DATASET TAB
        # ======================================================

        with tab1:

            st.markdown(
    "<span style='color:gray;'>supports .csv and .xlsx file formats</span>",
    unsafe_allow_html=True
)

            # TEMPLATE DOWNLOAD
            with open("template.csv","rb") as f:
                st.download_button(
                    "Download Template Dataset",
                    f,
                    "template.csv"
                )

            st.markdown(
    "<p style='color:gray; font-size:14px;'>Download the template dataset, fill in your match data, and upload it here</p>",
    unsafe_allow_html=True
)

            st.subheader("Upload your Files")

            st.markdown(
    "<p style='color:#9aa0a6; font-size:14px;'>For testing purpose refer to the example datasets attached below</p>",
    unsafe_allow_html=True
)

            upload_type = st.radio(
                "",
                ["Upload Single Dataset","Upload Multiple Datasets"]
            )

            uploaded_files = None

            if upload_type == "Upload Single Dataset":

                uploaded_files = st.file_uploader(
                    "Upload Single Dataset",
                    type=["csv","xlsx"],
                    accept_multiple_files=False
                )

            else:

                uploaded_files = st.file_uploader(
                    "Upload Multiple Datasets",
                    type=["csv","xlsx"],
                    accept_multiple_files=True
                )

            st.markdown(
    "<p style='color:#9aa0a6; font-size:14px;'>A single dataset may contain data from one match or multiple matches combined.</p>",
    unsafe_allow_html=True
)

            confirm = st.button("Confirm Upload", use_container_width=True)

            # ======================================================
            # PROCESS DATA AFTER CONFIRM
            # ======================================================

            if confirm:

                st.session_state.df2 = None ###

                #if uploaded_files is None:
                #    st.error("Please upload dataset first")

                if uploaded_files is None:###
                    st.error("Please upload dataset first")###
                    st.session_state.df2 = None               ###

                else:

                    all_datasets = []

                    # SINGLE FILE
                    if not isinstance(uploaded_files,list):

                        file = uploaded_files

                        if file.name.endswith(".csv"):
                            df_temp = pd.read_csv(file)
                        else:
                            df_temp = pd.read_excel(file)

                        all_datasets.append(df_temp)

                    # MULTIPLE FILES
                    else:

                        for file in uploaded_files:

                            if file.name.endswith(".csv"):
                                df_temp = pd.read_csv(file)
                            else:
                                df_temp = pd.read_excel(file)

                            all_datasets.append(df_temp)

                    if len(all_datasets)==0:
                        st.error("No dataset loaded")

                    else:

                        df = pd.concat(all_datasets,ignore_index=True)

                        try:

                            data_validation(df)

                            st.success("Dataset passed data validation")

                            # ---------------- CLEANING ----------------

                            df2 = df.copy()

                            df2 = df2.dropna(subset=["Player_Name"])
                            df2["Role"] = df2["Role"].fillna(df2["Role"].mode()[0])
                            df2["Batting_Start_Over"] = df2["Batting_Start_Over"].fillna(0)
                            df2["Out_Over"] = df2["Out_Over"].fillna(0)
                            df2["Balls_Played"] = df2["Balls_Played"].fillna(0)
                            df2["Runs_Scored"] = df2["Runs_Scored"].fillna(0)
                            df2["Overs_Bowled"] = df2["Overs_Bowled"].fillna(0)

                            df2.loc[(df2["Overs_Bowled"]>0)&(df2["Runs_Given"].isnull()),"Runs_Given"]=0
                            df2.loc[(df2["Overs_Bowled"]>0)&(df2["Wickets_Taken"].isnull()),"Wickets_Taken"]=0

                            df2["Runs_Given"]=df2["Runs_Given"].fillna(0)
                            df2["Wickets_Taken"]=df2["Wickets_Taken"].fillna(0)

                            # ---------------- FEATURE ENGINEERING ----------------

                            df2["Was_Out"] = (
                                (df2["Batting_Start_Over"] > 0) &
                                (df2["Out_Over"] != "not-out")
                            )

                            df2["Strike_Rate"] = (
                                (df2["Runs_Scored"] / df2["Balls_Played"]) * 100
                            ).round(2)

                            def economy_calc(df2):

                                over = df2["Overs_Bowled"].astype(int)
                                balls = (df2["Overs_Bowled"] - over) * 10

                                df2["real_over"] = over + (balls/6)
                                df2["Economy_Rate"] = 0.0

                                df2.loc[df2["real_over"]>0,"Economy_Rate"] = \
                                    df2["Runs_Given"]/df2["real_over"]

                                df2.drop(columns=["real_over"],inplace=True)

                                df2["Economy_Rate"] = df2["Economy_Rate"].round(2)

                                return df2

                            df2 = economy_calc(df2)

                            st.success("Data cleaning and feature engineering completed")
                            st.session_state.df2 = df2

                        except Exception as err:

                            st.error(f"Dataset is invalid: {err}")

            # ======================================================
            # DATASET OVERVIEW
            # ======================================================

            st.subheader("Dataset Overview")
            
            def column_info(title, text):
                st.markdown(
                    f"<p style='font-weight:bold;'>{title}</p>",
                    unsafe_allow_html=True
                )
            
                st.markdown(
                    f"<p style='color:#9aa0a6; font-size:14px;'>{text}</p>",
                    unsafe_allow_html=True
                )
            
            
            column_info(
                "Match_No",
                "Enter the match number to which the player’s performance belongs. Null values are NOT allowed because every record must belong to a match. Preferred datatype: Integer."
            )
            
            column_info(
                "Player_Name",
                "Enter the name of the player whose statistics are being recorded. Null values are NOT allowed when other player statistics are present. Preferred datatype: String."
            )
            
            column_info(
                "Role",
                "Enter the player's role such as batsman, bowler, or all-rounder. Null values are allowed but will automatically be filled with the most common role during data cleaning. Preferred datatype: String."
            )
            
            column_info(
                "Batting_Position",
                "Enter the batting order position of the player (1–11). Null values are NOT allowed because batting order is required for analysis. Preferred datatype: Integer."
            )
            
            column_info(
                "Batting_Start_Over",
                "Enter the over number when the player started batting. Null values are allowed only if the player did not bat in the match. Preferred datatype: Numeric."
            )
            
            column_info(
                "Out_Over",
                "Enter the over in which the player got out. If the player remained not-out, you may leave it blank or specify 'not-out'. Null values are allowed for players who did not bat or remained not-out. Preferred datatype: Numeric or String."
            )
            
            column_info(
                "Balls_Played",
                "Enter the total number of balls faced by the player while batting. Null values are allowed only when the player did not bat. Preferred datatype: Integer."
            )
            
            column_info(
                "Runs_Scored",
                "Enter the total runs scored by the player in that match. Null values are allowed only when the player did not bat. Preferred datatype: Integer."
            )
            
            column_info(
                "Overs_Bowled",
                "Enter the total overs bowled by the player (e.g., 2.4 overs). Null values are allowed when the player did not bowl in the match. Preferred datatype: Float."
            )
            
            column_info(
                "Runs_Given",
                "Enter the total runs conceded by the player while bowling. Null values are allowed only if the player did not bowl; otherwise missing values will be filled with 0 during cleaning. Preferred datatype: Integer."
            )
            
            column_info(
                "Wickets_Taken",
                "Enter the number of wickets taken by the bowler in the match. Null values are allowed only if the player did not bowl; otherwise missing values will be filled with 0 during cleaning. Preferred datatype: Integer."
            )


            # ======================================================
            # EXAMPLE DATASETS
            # ======================================================

            st.subheader("Example Datasets")

            with open("RCB_IPL2024_FirstMatch.csv","rb") as f:
                st.download_button("Download Example Dataset 1",f,"RCB_IPL2024_FirstMatch.csv")

            with open("RCB_IPL2024_Match2_vs_PBKS.csv","rb") as f:
                st.download_button("Download Example Dataset 2",f,"RCB_IPL2024_Match2_vs_PBKS.csv")

            with open("RCB_IPL2024_Match3_vs_GT.csv","rb") as f:
                st.download_button("Download Example Dataset 3",f,"RCB_IPL2024_Match3_vs_GT.csv")

        # OTHER TABS

        with tab2:

            if st.session_state.df2 is None:
                #st.warning("Please upload and confirm dataset in Dataset tab first.")
                st.stop()
        
            df2 = st.session_state.df2


        
            # ======================================================
            # Individual Runs Scored by Players
            # ======================================================
        
            st.markdown("### Individual Runs Scored by Players")
        
            done_batting = df2[df2["Balls_Played"] > 0]
        
            runs_difference = (
                done_batting.groupby("Player_Name")
                .agg({"Runs_Scored": "sum", "Balls_Played": "sum"})
                .sort_values(by="Runs_Scored", ascending=False)
                .astype(int)
                .reset_index()
            )
        
            runs_difference.index = runs_difference.index + 1
        
            st.dataframe(
                runs_difference[["Player_Name", "Runs_Scored", "Balls_Played"]],
                use_container_width=True
            )
        
            colors = sns.color_palette("coolwarm", len(runs_difference))
        
            fig, ax = plt.subplots(figsize=(10,5), dpi=120)
        
            sns.barplot(
                y=runs_difference["Player_Name"],
                x=runs_difference["Runs_Scored"],
                palette=colors,
                ax=ax
            )
        
            ax.set_title("Individual Runs Scored by Players", fontsize=16, fontweight="bold")
            ax.set_xlabel("Runs Scored", fontsize=12)
            ax.set_ylabel("Players", fontsize=12)
        
            ax.grid(axis='x', linestyle='--', alpha=0.4)
        
            plt.tight_layout()
        
            st.pyplot(fig)

            st.divider()
        
            # ======================================================
            # Total Runs Contribution
            # ======================================================
        
            st.markdown("### Total Runs Contribution")
        
            top_batters = runs_difference[["Player_Name", "Runs_Scored"]].head()
        
            other_runs = runs_difference["Runs_Scored"].sum().astype(int) - top_batters["Runs_Scored"].sum().astype(int)
        
            batting_data = top_batters.copy()
        
            batting_data.loc[len(batting_data)] = ["Others", int(other_runs)]
        
            batting_data = batting_data[batting_data["Runs_Scored"] > 0]
        
            st.dataframe(
                batting_data,
                use_container_width=True
            )
        
            fig, ax = plt.subplots(figsize=(8,6), dpi=120)
        
            wedges, texts, autotexts = ax.pie(
                batting_data["Runs_Scored"],
                labels=None,
                autopct="%1.1f%%",
                startangle=90,
                wedgeprops={"edgecolor": "black"}
            )
        
            legend_labels = [
                f"{player} - {runs}"
                for player, runs in zip(batting_data["Player_Name"], batting_data["Runs_Scored"])
            ]
        
            ax.legend(
                wedges,
                legend_labels,
                title="Players",
                loc="center left",
                bbox_to_anchor=(1, 0.5)
            )
        
            ax.set_title("Total Runs Contribution", fontsize=16, fontweight="bold")
        
            plt.tight_layout()
        
            st.pyplot(fig)

            st.divider()


            # ======================================================
            # Player's Total Runs in Each Match
            # ======================================================
            
            st.markdown("### Player's Total Runs in Each Match")
            
            if done_batting["Match_No"].nunique() > 1:
            
                players_list = sorted(done_batting["Player_Name"].unique())
            
                selected_player = st.selectbox(
                    "Select Player",
                    players_list
                )
            
                selected_player_df = done_batting[
                    done_batting["Player_Name"] == selected_player
                ]
            
                player_runs = (
                    selected_player_df.groupby("Match_No")["Runs_Scored"]
                    .sum()
                    .reset_index()
                    .sort_values("Match_No")
                )
            
                player_runs["Runs_Scored"] = player_runs["Runs_Scored"].astype(int)
            
                player_runs.index += 1
            
                st.dataframe(player_runs, use_container_width=True)
            
                x_vals = player_runs["Match_No"].astype(int)
                y_vals = player_runs["Runs_Scored"]
            
                fig, ax = plt.subplots(figsize=(8,5), dpi=120)
            
                sns.lineplot(
                    x=x_vals,
                    y=y_vals,
                    marker="o",
                    color="darkblue",
                    ax=ax
                )
            
                ax.set_xticks(range(min(x_vals), max(x_vals)+1))
            
                ax.set_title(
                    f"{selected_player}'s Total Runs in Each Match",
                    fontsize=16,
                    fontweight="bold"
                )
            
                ax.set_xlabel("Match No", fontsize=12)
                ax.set_ylabel("Runs Scored in each match", fontsize=12)
            
                ax.grid(linestyle='--', alpha=0.4)
            
                plt.tight_layout()
            
                st.pyplot(fig)
            
            else:
            
                st.warning(
                    "Player's Total Runs in Each Match is not applicable for single match dataset."
                )
            
            st.divider()


            st.markdown("### Runs Scored Contribution Based on Roles")

            runs_contribution_by_role = done_batting[done_batting["Runs_Scored"] > 0]
            
            runs_contribution_by_role = (
                runs_contribution_by_role.groupby("Role", as_index=False)["Runs_Scored"]
                .sum()
                .sort_values(by="Runs_Scored", ascending=False)
                .reset_index(drop=True)
            )
            
            runs_contribution_by_role["Runs_Scored"] = runs_contribution_by_role["Runs_Scored"].astype(int)
            runs_contribution_by_role.index = runs_contribution_by_role.index + 1
            
            st.dataframe(
                runs_contribution_by_role,
                use_container_width=True
            )
            
            fig, ax = plt.subplots(figsize=(8,6), dpi=120)
            
            wedges, texts, autotexts = ax.pie(
                runs_contribution_by_role["Runs_Scored"],
                labels=None,
                autopct="%1.1f%%",
                startangle=90,
                wedgeprops={"edgecolor": "black"}
            )
            
            legend_labels = [
                f"{role} - {runs}"
                for role, runs in zip(
                    runs_contribution_by_role["Role"],
                    runs_contribution_by_role["Runs_Scored"]
                )
            ]
            
            ax.legend(
                wedges,
                legend_labels,
                title="Roles",
                loc="center left",
                bbox_to_anchor=(1, 0.5)
            )
            
            ax.set_title("Runs Scored Contribution Based on Roles", fontsize=16, fontweight="bold")
            
            plt.tight_layout()
            
            st.pyplot(fig)

            st.divider()


            # ======================================================
            # Strike Rate Comparison
            # ======================================================
        
            st.markdown("### Strike-Rate Comparison between Batsmen and All-Rounders")
        
            batters_allrounders = done_batting[
                (done_batting["Role"] == "batsman") |
                (done_batting["Role"] == "all-rounder")
            ]
        
            strike_rate_diff = (
                batters_allrounders.groupby("Player_Name")
                .agg({
                    "Role": "first",
                    "Strike_Rate": "mean",
                    "Runs_Scored": "sum",
                    "Balls_Played": "sum"
                })
                .sort_values(by="Strike_Rate", ascending=False)
            ).round(2).reset_index()
        
            strike_rate_diff["Runs_Scored"] = strike_rate_diff["Runs_Scored"].astype(int)
            strike_rate_diff["Balls_Played"] = strike_rate_diff["Balls_Played"].astype(int)
        
            strike_rate_diff.index = strike_rate_diff.index + 1
        
            st.dataframe(
                strike_rate_diff[["Player_Name", "Role", "Strike_Rate"]],
                use_container_width=True
            )
        
            colors = {"batsman": "#4C72B0", "all-rounder": "#DD8452"}
        
            fig, ax = plt.subplots(figsize=(10,5), dpi=120)
        
            sns.barplot(
                x=strike_rate_diff["Strike_Rate"],
                y=strike_rate_diff["Player_Name"],
                hue=strike_rate_diff["Role"],
                palette=colors,
                ax=ax
            )
        
            ax.set_title(
                "Strike-Rate Comparison between Batsmen and All-Rounders",
                fontsize=16,
                fontweight="bold"
            )
        
            ax.set_xlabel("Strike Rate", fontsize=12)
            ax.set_ylabel("Players", fontsize=12)
        
            ax.grid(axis='x', linestyle='--', alpha=0.4)
        
            plt.tight_layout()
        
            st.pyplot(fig)

            st.divider()


            st.markdown("### Players Consistency in Batting")

            match_balls_played = df2[df2["Balls_Played"] > 0]
            
            match_runs = (
                match_balls_played.groupby(["Match_No", "Player_Name"])["Runs_Scored"]
                .sum()
                .reset_index()
            )
            
            if match_balls_played["Match_No"].nunique() > 1:
            
                batting_consistency = (
                    match_runs.groupby("Player_Name")["Runs_Scored"]
                    .agg(["mean", "std", "count"])
                    .round(2)
                    .reset_index()
                )
            
                batting_consistency = batting_consistency[batting_consistency["count"] > 1]
            
                batting_consistency["Consistency_Score"] = (
                    batting_consistency["mean"] /
                    (batting_consistency["std"] + 1)
                ).round(2)
            
                batting_consistency = batting_consistency.sort_values(
                    by="Consistency_Score",
                    ascending=False
                ).reset_index(drop=True)
            
                batting_consistency.index += 1
            
                st.dataframe(
                    batting_consistency[["Player_Name", "Consistency_Score"]],
                    use_container_width=True
                )
            
                colors = sns.color_palette("coolwarm", len(batting_consistency))
            
                fig, ax = plt.subplots(figsize=(10,5), dpi=120)
            
                sns.barplot(
                    y=batting_consistency["Player_Name"],
                    x=batting_consistency["Consistency_Score"],
                    palette=colors,
                    ax=ax
                )
            
                ax.set_title("Players Consistency in Batting", fontsize=16, fontweight="bold")
                ax.set_ylabel("Players", fontsize=12)
                ax.set_xlabel("Consistency Score", fontsize=12)
            
                ax.grid(axis='x', linestyle='--', alpha=0.4)
            
                plt.tight_layout()
            
                st.pyplot(fig)
            
            else:
            
                st.warning("Players Consistency in Batting is not applicable for single match dataset")

            st.divider()    

            st.markdown("### Average Runs by Batting Order")

            #if df2["Match_No"].nunique() > 1:            

            df2["Batting_Order"] = pd.cut(
                df2["Batting_Position"],
                bins=[0,3,7,11],
                labels=["top","middle","lower"]
            ).astype(str)
            
            order_runs = (
                df2.groupby("Batting_Order", as_index=False)["Runs_Scored"]
                .sum()
                .sort_values(by="Runs_Scored", ascending=False)
                .reset_index(drop=True)
            )
            
            order_runs["Average_Runs_Scored"] = order_runs["Runs_Scored"]
            
            order_runs = order_runs.drop("Runs_Scored", axis=1)
            
            order_runs.index += 1
            
            st.dataframe(
                order_runs,
                use_container_width=True
            )
        
            fig, ax = plt.subplots(figsize=(8,5), dpi=120)
        
            sns.barplot(
                x=order_runs["Batting_Order"],
                y=order_runs["Average_Runs_Scored"],
                palette="viridis",
                ax=ax
            )
        
            ax.set_title("Average Runs by Batting Order", fontsize=16, fontweight="bold")
            ax.set_xlabel("Batting Order", fontsize=12)
            ax.set_ylabel("Average Runs Scored", fontsize=12)
        
            ax.grid(axis='y', linestyle='--', alpha=0.4)
        
            plt.tight_layout()
        
            st.pyplot(fig)
            
            #else:
            
            #    st.warning("Average Runs by Batting Order is not applicable for single match dataset")

            st.divider() 


            # ======================================================
            # Phase wise Wickets Lost Breakdown
            # ======================================================
            
            st.markdown("### Phase wise Wickets Lost Breakdown")
            
            wickets_df = df2[df2["Was_Out"] == True].copy()
            
            wickets_df["Out_Over"] = pd.to_numeric(wickets_df["Out_Over"], errors="coerce")
            
            def assign_phase(over):
                if over <= 6:
                    return "Powerplay"
                elif over <= 15:
                    return "Middle Overs"
                else:
                    return "Death Overs"
            
            wickets_df["Wicket_Phase"] = wickets_df["Out_Over"].apply(assign_phase)
            
            phase_wickets = (
                wickets_df.groupby("Wicket_Phase")["Player_Name"]
                .size()
                .reindex(["Powerplay", "Middle Overs", "Death Overs"])
                .reset_index(name="Wickets_Lost")
                .sort_values(by="Wickets_Lost", ascending=False)
            )
            
            phase_wickets.index += 1
            
            st.dataframe(phase_wickets, use_container_width=True)
            
            fig, ax = plt.subplots(figsize=(8,5), dpi=120)
            
            sns.barplot(
                x=phase_wickets["Wicket_Phase"],
                y=phase_wickets["Wickets_Lost"],
                palette="viridis",
                ax=ax
            )
            
            ax.set_title("Phase-wise Wickets Lost", fontsize=16, fontweight="bold")
            ax.set_xlabel("Match Phases", fontsize=12)
            ax.set_ylabel("Wickets Lost", fontsize=12)
            
            ax.grid(axis='y', linestyle='--', alpha=0.4)
            
            plt.tight_layout()
            
            st.pyplot(fig)
            
            st.divider()   

        with tab3:

            if st.session_state.get("df2") is None:
        
                st.warning("Please upload and confirm dataset in Dataset tab first.")
        
            else:
        
                df2 = st.session_state.df2


        
                # ======================================================
                # Individual Wickets Taken by Players
                # ======================================================
        
            st.markdown("### Individual Wickets Taken by Players")
            
            done_bowling = df2[df2["Overs_Bowled"] > 0]
            
            bowling_diff = (
                done_bowling.groupby("Player_Name", as_index=False)
                .agg({"Wickets_Taken": "sum", "Overs_Bowled": "sum"})
                .sort_values(by="Wickets_Taken", ascending=False)
                .reset_index(drop=True)
            )
            
            bowling_diff["Wickets_Taken"] = bowling_diff["Wickets_Taken"].astype(int)
            bowling_diff.index = bowling_diff.index + 1
            
            st.dataframe(bowling_diff, use_container_width=True)
            
            colors = sns.color_palette("coolwarm", len(bowling_diff))
            
            fig, ax = plt.subplots(figsize=(10,5), dpi=120)
            
            sns.barplot(
                x=bowling_diff["Wickets_Taken"],
                y=bowling_diff["Player_Name"],
                palette=colors,
                ax=ax
            )
            
            ax.set_title("Individual Wickets Taken by Players", fontsize=16, fontweight="bold")
            ax.set_ylabel("Players", fontsize=12)
            ax.set_xlabel("Wickets Taken", fontsize=12)
            
            ax.grid(axis='x', linestyle='--', alpha=0.4)
            
            plt.tight_layout()
            
            st.pyplot(fig)
            
            st.divider()


            # ======================================================
            # Total Wickets Contribution
            # ======================================================
            
            st.markdown("### Total Wickets Contribution")
            
            top_bowling = bowling_diff[["Player_Name", "Wickets_Taken"]].head()
            
            other_bowlers = (
                bowling_diff["Wickets_Taken"].sum().astype(int)
                - top_bowling["Wickets_Taken"].sum().astype(int)
            )
            
            bowling_data = top_bowling.copy().reset_index(drop=True)
            
            bowling_data.loc[len(bowling_data)] = ["Others", int(other_bowlers)]
            
            bowling_data.index += 1
            
            bowling_data = bowling_data[bowling_data["Wickets_Taken"] > 0]
            
            st.dataframe(bowling_data, use_container_width=True)
            
            fig, ax = plt.subplots(figsize=(8,6), dpi=120)
            
            wedges, texts, autotexts = ax.pie(
                bowling_data["Wickets_Taken"],
                labels=None,
                autopct="%1.1f%%",
                startangle=90,
                wedgeprops={"edgecolor": "black"}
            )
            
            legend_labels = [
                f"{player} - {wickets}"
                for player, wickets in zip(
                    bowling_data["Player_Name"],
                    bowling_data["Wickets_Taken"]
                )
            ]
            
            ax.legend(
                wedges,
                legend_labels,
                title="Players",
                loc="center left",
                bbox_to_anchor=(1, 0.5)
            )
            
            ax.set_title("Total Wickets Contribution", fontsize=16, fontweight="bold")
            
            plt.tight_layout()
            
            st.pyplot(fig)
            
            st.divider()


            # ======================================================
            # Player's Total Wickets in Each Match
            # ======================================================
            
            st.markdown("### Player's Total Wickets in Each Match")
            
            if done_bowling["Match_No"].nunique() > 1:
            
                players_list_bowl = sorted(done_bowling["Player_Name"].unique())
            
                selected_player_bowl = st.selectbox(
                    "Select Player",
                    players_list_bowl
                )
            
                selected_player_bowl_df = done_bowling[
                    done_bowling["Player_Name"] == selected_player_bowl
                ]
            
                player_wickets = (
                    selected_player_bowl_df.groupby("Match_No")["Wickets_Taken"]
                    .sum()
                    .reset_index()
                    .sort_values("Match_No")
                )
            
                player_wickets["Wickets_Taken"] = player_wickets["Wickets_Taken"].astype(int)
            
                player_wickets.index += 1
            
                st.dataframe(player_wickets, use_container_width=True)
            
                x_vals = player_wickets["Match_No"].astype(int)
                y_vals = player_wickets["Wickets_Taken"].astype(int)
            
                fig, ax = plt.subplots(figsize=(8,5), dpi=120)
            
                sns.lineplot(
                    x=x_vals,
                    y=y_vals,
                    marker="o",
                    color="darkblue",
                    ax=ax
                )
            
                ax.set_xticks(range(min(x_vals), max(x_vals)+1))
            
                ax.set_yticks(range(min(y_vals), max(y_vals)+1))
            
                ax.set_title(
                    f"{selected_player_bowl}'s Total Wickets in Each Match",
                    fontsize=16,
                    fontweight="bold"
                )
            
                ax.set_xlabel("Match No", fontsize=12)
                ax.set_ylabel("Wickets Taken in each match", fontsize=12)
            
                ax.grid(linestyle='--', alpha=0.4)
            
                plt.tight_layout()
            
                st.pyplot(fig)
            
            else:
            
                st.warning("Player's Total Wickets in Each Match is not applicable for single match dataset.")
            
            st.divider()

            # ======================================================
            # Wickets Taken Contribution Based on Roles
            # ======================================================
            
            st.markdown("### Wickets Taken Contribution Based on Roles")
            
            wickets_contribution_by_role = done_bowling[done_bowling["Wickets_Taken"] > 0]
            
            wickets_contribution_by_role = (
                wickets_contribution_by_role
                .groupby("Role", as_index=False)["Wickets_Taken"]
                .sum()
                .sort_values(by="Wickets_Taken", ascending=False)
            )
            
            wickets_contribution_by_role["Wickets_Taken"] = wickets_contribution_by_role["Wickets_Taken"].astype(int)
            
            wickets_contribution_by_role.index += 1
            
            st.dataframe(wickets_contribution_by_role, use_container_width=True)
            
            fig, ax = plt.subplots(figsize=(8,6), dpi=120)
            
            wedges, texts, autotexts = ax.pie(
                wickets_contribution_by_role["Wickets_Taken"],
                labels=None,
                autopct="%1.1f%%",
                startangle=90,
                wedgeprops={"edgecolor": "black"}
            )
            
            legend_labels = [
                f"{role} - {wickets}"
                for role, wickets in zip(
                    wickets_contribution_by_role["Role"],
                    wickets_contribution_by_role["Wickets_Taken"]
                )
            ]
            
            ax.legend(
                wedges,
                legend_labels,
                title="Roles",
                loc="center left",
                bbox_to_anchor=(1, 0.5)
            )
            
            ax.set_title("Wickets Taken Contribution Based on Roles", fontsize=16, fontweight="bold")
            
            plt.tight_layout()
            
            st.pyplot(fig)
            
            st.divider()

            # ======================================================
            # Economy-Rate Comparison between Bowlers and All-Rounders
            # ======================================================
            
            st.markdown("### Economy-Rate Comparison between Bowlers and All-Rounders")
            
            bowlers_allrounders = done_bowling[
                (done_bowling["Role"] == "bowler") |
                (done_bowling["Role"] == "all-rounder")
            ]
            
            economy_diff = (
                bowlers_allrounders
                .groupby("Player_Name", as_index=False)
                .agg({
                    "Role": "first",
                    "Economy_Rate": "mean",
                    "Overs_Bowled": "sum",
                    "Runs_Given": "sum"
                })
                .sort_values(by="Economy_Rate")
            ).round(2).reset_index(drop=True)
            
            economy_diff.index += 1
            
            st.dataframe(
                economy_diff[["Player_Name", "Role", "Economy_Rate"]],
                use_container_width=True
            )
            
            colors = {"bowler": "#4C72B0", "all-rounder": "#DD8452"}
            
            fig, ax = plt.subplots(figsize=(10,5), dpi=120)
            
            sns.barplot(
                x=economy_diff["Economy_Rate"],
                y=economy_diff["Player_Name"],
                hue=economy_diff["Role"],
                palette=colors,
                ax=ax
            )
            
            ax.set_title(
                "Economy-Rate Comparison between Bowlers and All-Rounders",
                fontsize=16,
                fontweight="bold"
            )
            
            ax.set_xlabel("Economy Rate", fontsize=12)
            ax.set_ylabel("Players", fontsize=12)
            
            ax.grid(axis='x', linestyle='--', alpha=0.4)
            
            plt.tight_layout()
            
            st.pyplot(fig)
            
            st.divider()

            # ======================================================
            # Players Consistency in Bowling
            # ======================================================
            
            st.markdown("### Players Consistency in Bowling")
            
            match_overs = df2[df2["Overs_Bowled"] > 0]
            
            match_wickets = (
                match_overs
                .groupby(["Match_No", "Player_Name"])["Wickets_Taken"]
                .sum()
                .reset_index()
            )
            
            if match_overs["Match_No"].nunique() > 1:
            
                bowling_consistency = (
                    match_wickets
                    .groupby("Player_Name")["Wickets_Taken"]
                    .agg(["mean", "std", "count"])
                    .round(2)
                    .reset_index()
                )
            
                bowling_consistency = bowling_consistency[bowling_consistency["count"] > 1]
            
                bowling_consistency["Consistency_Score"] = (
                    bowling_consistency["mean"] /
                    (bowling_consistency["std"] + 1)
                ).round(2)
            
                bowling_consistency = bowling_consistency.sort_values(
                    by="Consistency_Score",
                    ascending=False
                ).reset_index(drop=True)
            
                bowling_consistency.index += 1
            
                st.dataframe(
                    bowling_consistency[["Player_Name", "Consistency_Score"]],
                    use_container_width=True
                )
            
                colors = sns.color_palette("coolwarm", len(bowling_consistency))
            
                fig, ax = plt.subplots(figsize=(10,5), dpi=120)
            
                sns.barplot(
                    y=bowling_consistency["Player_Name"],
                    x=bowling_consistency["Consistency_Score"],
                    palette=colors,
                    ax=ax
                )
            
                ax.set_title("Players Consistency in Bowling", fontsize=16, fontweight="bold")
                ax.set_xlabel("Consistency Score", fontsize=12)
                ax.set_ylabel("Players", fontsize=12)
            
                ax.grid(axis='x', linestyle='--', alpha=0.4)
            
                plt.tight_layout()
            
                st.pyplot(fig)
            
            else:
            
                st.warning("Players Consistency in Bowling is not applicable for single match dataset")
            
            st.divider()

        with tab4:
            if st.session_state.get("df2") is None:
        
                st.warning("Please upload and confirm dataset in Dataset tab first.")
        
            else:
        
                df2 = st.session_state.df2

            # ======================================================
            # Summary
            # ======================================================

            # ======================================================
            # Total Runs Scored and Total Wickets Taken in each Match
            # ======================================================
            
            st.markdown("### Total Runs Scored and Total Wickets Taken in each Match")
            
            runs_wickets = (
                df2.groupby("Match_No", as_index=False)
                .agg({"Runs_Scored": "sum", "Wickets_Taken": "sum"})
                .astype(int)
            )
            
            runs_wickets.index += 1
            
            st.dataframe(
                runs_wickets[["Match_No", "Runs_Scored", "Wickets_Taken"]],
                use_container_width=True
            )
            
            fig, ax = plt.subplots(1, 2, figsize=(10,4), dpi=120)
            
            sns.barplot(
                x=runs_wickets["Match_No"],
                y=runs_wickets["Runs_Scored"],
                palette="viridis",
                ax=ax[0]
            )
            
            ax[0].set_xlabel("Match Number", fontsize=12)
            ax[0].set_ylabel("Runs Scored", fontsize=12)
            ax[0].set_title("Runs Scored in each Match", fontsize=10, fontweight="bold")
            ax[0].grid(axis='y', linestyle='--', alpha=0.4)
            
            sns.barplot(
                x=runs_wickets["Match_No"],
                y=runs_wickets["Wickets_Taken"],
                palette="viridis",
                ax=ax[1]
            )
            
            ax[1].set_xlabel("Match Number", fontsize=12)
            ax[1].set_ylabel("Wickets Taken", fontsize=12)
            ax[1].set_title("Wickets Taken in each Match", fontsize=10, fontweight="bold")
            ax[1].grid(axis='y', linestyle='--', alpha=0.4)
            
            plt.tight_layout()
            
            st.pyplot(fig)
            
            st.divider()


            st.markdown("## Team Performance Summary")
            st.markdown(" ")
            
            st.markdown(
            f"""
            **1.** **{runs_difference.iloc[0]["Player_Name"]}** is the highest run scorer with **{runs_difference.iloc[0]["Runs_Scored"]} runs**.
            
            **2.** **{bowling_diff.iloc[0]["Player_Name"]}** is the highest wicket taker with **{bowling_diff.iloc[0]["Wickets_Taken"]} wickets**.
            
            **3.** **{strike_rate_diff.iloc[0]["Player_Name"]}** has the highest strike rate of **{strike_rate_diff.iloc[0]["Strike_Rate"]}**.
            
            **4.** **{economy_diff.iloc[0]["Player_Name"]}** has the best bowling economy rate of **{economy_diff.iloc[0]["Economy_Rate"]}**.
            
            **5.** **{runs_contribution_by_role.iloc[0]["Role"]}** are the highest contributors in scoring total runs with **{runs_contribution_by_role.iloc[0]["Runs_Scored"]} runs**, followed by **{runs_contribution_by_role.iloc[1]["Role"]}** with **{runs_contribution_by_role.iloc[1]["Runs_Scored"]} runs**.
            
            **6.** **{wickets_contribution_by_role.iloc[0]["Role"]}s** are the highest contributors in taking wickets with **{wickets_contribution_by_role.iloc[0]["Wickets_Taken"]} wickets**, followed by **{wickets_contribution_by_role.iloc[1]["Role"]}s** with **{wickets_contribution_by_role.iloc[1]["Wickets_Taken"]} wickets**.
            
            **7.** The **{order_runs.iloc[0]["Batting_Order"]} order** is the strongest batting order followed by the **{order_runs.iloc[1]["Batting_Order"]} order**.
            
            **8.** The team has lost most wickets in the **{phase_wickets.iloc[0]["Wicket_Phase"]}**, losing **{phase_wickets.iloc[0]["Wickets_Lost"]} wickets**.
            """
            )                    


    elif page == "About":

        st.markdown(
            """
            <h3 style='text-align:center;'>About This Dashboard</h3>
            """,
            unsafe_allow_html=True
        )

        # ======================================================
        # About the Creator
        # ======================================================
        
        st.markdown("### About the Creator : Pranay Jha")
        
        st.markdown("""
        Hello! My name is **Pranay Jha**, and I am currently pursuing a **Bachelor of Technology (B.Tech) in Computer Science and Engineering**. 
        I am actively learning and exploring the fields of **Data Science, Data Analytics, and Data Visualization**.
        
        This project, **T20 Cricket Team Performance Analysis Dashboard**, has been developed as part of my learning journey in data analytics. 
        The main goal of this project is to demonstrate how **structured data analysis and interactive dashboards** can be used to evaluate sports performance more effectively.
        
        Through this project, I focused on applying practical data analysis techniques using Python libraries such as **NumPy, Pandas, Matplotlib, Seaborn, and Streamlit**. 
        The dashboard allows users to upload cricket match datasets and instantly generate insights about **batting performance, bowling performance, player consistency, and match-level statistics**.
        
        This project highlights my ability to:
        
        - Work with **real-world structured datasets**
        - Perform **data cleaning and feature engineering**
        - Build **interactive analytical dashboards**
        - Communicate insights through **data visualization**
        - Design **user-friendly analytical tools**
        
        My aim is to continue improving my skills in **data analytics, machine learning, and dashboard development**, and build more practical projects that solve real-world problems using data.
        """)

        st.markdown("""
        ### Connect With Me
                    
        🔗 **GitHub:** [Pranay-256](https://github.com/Pranay-256)
                    
        💼 **LinkedIn:** [Pranay Jha](https://www.linkedin.com/in/pranay-jha-6582a937b/)
        """)
        
        st.divider()
        
        # ======================================================
        # Problem Statement
        # ======================================================
        
        st.markdown("### Problem Statement for this Project")
        
        st.markdown("""
        In many **local cricket matches, school tournaments, inter-college competitions, and small community leagues**, player performance evaluation is usually done **manually or based on personal observation**. 
        This creates several limitations and challenges.
        
        Some common problems include:
        
        - **Player contributions are often judged subjectively** rather than using actual performance statistics.
        - Awards such as **Best Batsman or Best Bowler** may not always be fairly decided.
        - **Batting partnerships and contributions** are rarely analyzed in a structured way.
        - **Bowling performance is usually evaluated only by wickets**, ignoring important factors such as economy rate and consistency.
        - **Match-to-match performance comparison becomes difficult** when proper records are not maintained.
        - In most small tournaments, there is **no structured data system available** to analyze performances across multiple matches.
        
        Because of these issues, it becomes difficult for teams, organizers, and players to **fairly evaluate performance and identify strengths and weaknesses**.
        """)
        
        st.divider()
        
        # ======================================================
        # Objective
        # ======================================================
        
        st.markdown("### Objective")
        
        st.markdown("""
        The main objective of this project is to build a **clear, structured, and unbiased cricket performance analysis system** using match-level data.
        
        Instead of relying on manual judgments, the system uses **data-driven insights** to evaluate team and player performances.
        
        The dashboard focuses on:
        
        - Measuring **individual batting contribution**
        - Evaluating **bowling impact using wickets and economy rate**
        - Measuring **player consistency across multiple matches**
        - Comparing performances between roles such as **batsman, bowler, and all-rounder**
        - Providing **fair statistical summaries** for team performance evaluation
        
        This project is designed to be useful for:
        
        - **Local cricket teams**
        - **Gully cricket players**
        - **School and college tournaments**
        - **Small-scale cricket competitions**
        - Teams that want **simple data-based performance evaluation without advanced analytics tools**
        
        The system helps ensure that decisions and evaluations are **based on actual data rather than opinion**.
        """)
        
        st.divider()
        
        # ======================================================
        # Tech Stack
        # ======================================================
        
        st.markdown("### Tech Stack")
        
        st.markdown("""
        This project has been developed using the **Python data analytics ecosystem** along with an interactive dashboard framework.
        
        **Libraries and tools used in this project:**
        
        - **Python** – Core programming language used for data processing and analytics.
        - **NumPy** – Used for numerical operations and handling structured numeric data efficiently.
        - **Pandas** – Used for data cleaning, data manipulation, grouping, aggregation, and analysis of cricket match datasets.
        - **Matplotlib** – Used to create charts and plots for visualizing cricket performance statistics.
        - **Seaborn** – Used for enhanced statistical visualizations and aesthetically improved charts.
        - **Streamlit** – Used to build the interactive web dashboard that allows users to upload datasets and explore insights dynamically.
        
        Together, these tools allow the project to transform **raw match data into meaningful insights and visual analytics**.
        """)
        
        st.divider()
        
        # ======================================================
        # Analytical Approach and Visualizations
        # ======================================================
        
        st.markdown("### Analytical Approach and Visualizations")
        
        st.markdown("""
        The analysis in this dashboard is divided into two major sections: **Batting Analytics** and **Bowling Analytics**.
        
        **Batting Analysis includes:**
        
        - Individual runs scored by players
        - Total runs contribution by top players
        - Player runs scored across matches            
        - Strike rate comparison between batsmen and all-rounders
        - Role-wise contribution in total runs scored
        - Player batting consistency across matches
        - Batting order strength analysis
        
        **Bowling Analysis includes:**
        
        - Individual wickets taken by bowlers
        - Total wickets contribution by players
        - Wickets taken by players across matches            
        - Wickets contribution based on player roles
        - Economy rate comparison between bowlers and all-rounders
        - Player bowling consistency across matches
        
        **Visualization techniques used:**
        
        - **Bar Charts/Horizontal Bar Charts** – To compare player performances clearly.
        - **Pie Charts** – To show contribution percentages (runs and wickets).
        - **Line Charts** – To analyze player performance trends across matches.
        - **Grouped Bar Charts** – To compare match-level statistics such as runs and wickets.
        
        These visualizations help convert raw numerical data into **clear, interpretable insights** for better performance evaluation.
        """)
        
        st.divider()
        
        # ======================================================
        # Recent Updates
        # ======================================================
        
        st.markdown("### Recent Update")
        
        st.markdown("""
        **Current Version:** 2.0  
        
        **Last Updated On:** 16th March 2026  
        
        **Improvements Made:**
        
        - Improved overall **dashboard user interface**
        - Added support for **.xlsx dataset uploads**
        - Enhanced **data validation and cleaning**
        - Added **more detailed batting and bowling analytics**
        - Improved **visualization clarity and chart styling**
        - Added **interactive player performance analysis**
        - Organized insights into **clear analytical sections**
        """)
