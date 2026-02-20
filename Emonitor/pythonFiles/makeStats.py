import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import pandas as pd
import datetime
import numpy as np
import os

statistics_df = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', 'data', 'session_statistics.csv'))

if len(statistics_df) <= 5:
    new_df = pd.DataFrame(columns=['emotion','time','probability'])
    new_df.to_csv(os.path.join(os.path.dirname(__file__), '..', 'data', 'session_statistics.csv'),
                    index=None)
    exit()

emotions = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

emotions_values = []
summary_df = {}

for emotion in emotions:
    emotions_values.append(len(statistics_df[statistics_df['emotion'] == emotion]))
emotions_values = np.array(emotions_values)

for emotion, value in zip(emotions, emotions_values):
    summary_df[emotion] = [round(((value / emotions_values.sum()) * 100), 2)]

dataframes = []
emotions_colors = {'angry': '#224170', 'disgust': '#D88096', 'fear': '#586A79', 'happy': '#d4b8b4', 'neutral': '#82B0D9', 'sad': '#777E9B', 'surprise': '#41A8BF'}
plt.figure(figsize=(13, 7))

for emotion in statistics_df['emotion'].unique():
    emotion_df = statistics_df[statistics_df['emotion'] == emotion]
    plt.bar(emotion_df.index, emotion_df['probability'], label = f'{emotion} {summary_df[emotion][0]}%', color=emotions_colors[emotion])

tick_positions = statistics_df.index[::7]
tick_labels = statistics_df['time'].iloc[::7]

today = datetime.date.today()

folder_path = "plots"
num_files = len([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])

plt.xticks(tick_positions, tick_labels, rotation=90, fontsize=11)
plt.subplots_adjust(left=0.05, right=0.96, top=0.96, bottom=0.15)
plt.xlabel('Time')
plt.ylabel('Confidence')
plt.title(f'Examination of the {today}')
plt.legend()
file_name = f'{num_files}.png'
plt.savefig(os.path.join(os.path.dirname(__file__), '..', 'plots', file_name))


summary_df = {'date': today, **summary_df}
summary_df = pd.DataFrame(summary_df)

summary_df.to_csv(os.path.join(os.path.dirname(__file__), '..', 'data', 'main_statistics.csv'),
                mode='a', header=False, index=False)

new_df = pd.DataFrame(columns=['emotion','time','probability'])
new_df.to_csv(os.path.join(os.path.dirname(__file__), '..', 'data', 'session_statistics.csv'),
                index=None)