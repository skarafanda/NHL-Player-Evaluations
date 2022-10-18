import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def getP60chart():
    playerName = input("Player Full Name: ")

    df = pd.read_csv('LeagueStats_2022-23.csv')

    #Sorting dataframe by highest P/60 and dropping unnecessary columns.
    df = df.sort_values(by=['PTS/60'], ascending=False)
    df.drop(df.iloc[:, 2:17], inplace=True, axis=1)
    df.drop(df.iloc[:, 3:29], inplace=True, axis=1)

    #Remove players who have not played any minutes.
    df.drop(df[df['timeOnIce'] == "0"].index, inplace = True)

    #Finding the mean and standard deviation for z-score formula
    mean = df['PTS/60'].mean()
    std = np.std(df["PTS/60"])

    values = df['PTS/60']
    z = []

    #Appending z-scores of each player to a list
    for x in values:
        z.append((x-mean)/std)

    #Adding the z-score list to the dataframe
    df["Z-Score"] = z

    #Creating a vertical, bidirectional bar chart
    for i in df['fullName']: 
        if i == playerName:
            fig, ax = plt.subplots()
            
            bar_color = ""
            if df['Z-Score'][df[df['fullName'] == playerName].index[0]] > 0:
                bar_color = "green"
            else:
                bar_color = "red"
            p1 = ax.bar(np.arange(1), df['Z-Score'][df[df['fullName'] == playerName].index[0]], width=.01, color=bar_color)

            ax.axhline(0, color='black', linewidth=0.8)

            plt.ylim(-3, 3)
            ax.set_ylabel('Z-score')
            ax.set_title(i + " | " + df['team'][df[df['fullName'] == playerName].index[0]] + " | TOI: " + df['timeOnIce'][df[df['fullName'] == playerName].index[0]])
            ax.set_xticks(np.arange(1), labels=['P/60'])

            #If you want the exact z-score on the bar (quite unnecessary for this viz)
            #ax.bar_label(p1, label_type='center')

            return plt.show()

getP60chart()