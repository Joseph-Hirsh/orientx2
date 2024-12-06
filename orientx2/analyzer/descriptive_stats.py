import matplotlib.pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess
from timeline import plot_timeline_events
from utils import load_data, add_day_index, prepare_orientation_data


def apply_lowess_smoothing(df, x_col, y_col, frac=0.05):
    smoothed = lowess(df[y_col], df[x_col], frac=frac, return_sorted=True)
    return smoothed


def get_daily_counts(data):
    daily_counts = data.groupby('day_index')['orientation'].agg(['sum', 'size']).reset_index()
    daily_counts['percentage'] = (daily_counts['sum'] / daily_counts['size']) * 100
    return daily_counts


def get_smoothed_category_data(data):
    daily_counts = get_daily_counts(data)
    smoothed = apply_lowess_smoothing(daily_counts, 'day_index', 'percentage')
    return smoothed


def plot_smoothed_category_data(ax, data, label):
    smoothed = get_smoothed_category_data(data)
    ax.plot(smoothed[:, 0], smoothed[:, 1], label=f"{label} (Percentage)", linewidth=2)


def plot_post_frequency(ax, df):
    post_freq = df.groupby('day_index').size().reset_index(name='post_count')
    ax.plot(post_freq['day_index'], post_freq['post_count'], color='gray', linestyle='--',
            label="Post Frequency", alpha=0.7)


def process_and_plot(csv_file, graph_label):
    df = load_data(csv_file)
    start_date, end_date = df['date'].min(), df['date'].max()

    df = add_day_index(df, start_date)
    df = prepare_orientation_data(df, graph_label)

    categories = [
        ('Conservative', 'Remain'),
        ('Conservative', 'Leave'),
        ('Labour', 'Remain'),
        ('Labour', 'Leave'),
    ]
    category_data = {
        f"{party} {vote}": df[(df['party'] == party) & (df['referendum vote'] == vote)]
        for party, vote in categories
    }

    fig, ax1 = plt.subplots(figsize=(16, 8))
    for label, data in category_data.items():
        plot_smoothed_category_data(ax1, data, label)

    plot_timeline_events(ax1, start_date)
    ax2 = ax1.twinx()
    plot_post_frequency(ax2, df)

    ax1.set_xlim(0, df['day_index'].max())
    ax1.set_xticks([0, df['day_index'].max()])
    ax1.set_xticklabels([start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')])
    ax1.set_title(f"{graph_label} and Post Frequency Over Time")
    ax1.set_xlabel(f"Days Since {start_date.strftime('%B %d, %Y')}")
    ax1.set_ylabel("Percentage of Posts (0-100%)", color='tab:blue')
    ax1.set_ylim(0, 100)
    ax1.grid(True, alpha=0.5)
    ax2.set_ylabel("Post Frequency (Number of Posts)", color='tab:gray')

    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    plt.show()
