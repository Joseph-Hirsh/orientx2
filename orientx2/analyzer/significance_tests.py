import pandas as pd
from statsmodels.stats.proportion import proportions_ztest
from utils import load_data, add_day_index
from timeline import TIMELINE_EVENTS


def test_event_significance(df, label, event_date, window_size=300):
    start_date = df['date'].min()
    event_day = (pd.Timestamp(event_date) - pd.Timestamp(start_date)).days

    before = df[(df['day_index'] >= event_day - window_size) & (df['day_index'] < event_day)]
    after = df[(df['day_index'] > event_day) & (df['day_index'] <= event_day + window_size)]

    before_count = before['orientation'].value_counts().get(label, 0)
    after_count = after['orientation'].value_counts().get(label, 0)

    before_total = len(before)
    after_total = len(after)

    before_ratio = before_count / before_total if before_total > 0 else 0
    after_ratio = after_count / after_total if after_total > 0 else 0

    count = [before_count, after_count]
    nobs = [before_total, after_total]
    z_stat, p_value = proportions_ztest(count, nobs, alternative="two-sided")

    return p_value, before_ratio, after_ratio, before_count, after_count, before_total, after_total


def analyze_events(csv_file, labels=(0, 1, 2), window_size=30):
    df = load_data(csv_file)
    add_day_index(df, df['date'].min())
    results = []

    for event_date, event_desc in TIMELINE_EVENTS:
        for label in labels:
            p_value, before, after, before_count, after_count, before_total, after_total = test_event_significance(
                df, label, event_date, window_size
            )

            if p_value < 0.01:
                significance = "**"
            elif p_value < 0.05:
                significance = "*"
            else:
                significance = ""

            results.append({
                "event": event_desc,
                "label": label,
                "before_percentage": before,
                "before_count": before_count,
                "before_total": before_total,
                "after_percentage": after,
                "after_count": after_count,
                "after_total": after_total,
                "p_value": p_value,
                "significance": significance
            })

    return pd.DataFrame(results)
