import pandas as pd

TIMELINE_EVENTS = [
    ("2013-01-23", "David Cameron’s Bloomberg Speech"),
    ("2014-05-22", "UKIP Wins European Parliamentary Elections"),
    ("2014-09-18", "Scottish Independence Referendum"),
    ("2014-11-28", "Cameron’s Immigration Speech"),
    ("2015-05-07", "General Election Victory"),
    ("2015-05-27", "European Union Referendum Bill"),
    ("2015-06-01", "EU Reform Negotiations Begin"),
    ("2016-02-02", "Donald Tusk’s Draft EU Reform Deal"),
    ("2016-02-19", "EU Leaders Approve Renegotiation Deal"),
    ("2016-02-20", "Referendum Date Announced"),
]


def plot_timeline_events(ax, start_date):
    for i, (event_date, event_desc) in enumerate(TIMELINE_EVENTS, start=1):
        day_index = (pd.Timestamp(event_date) - pd.Timestamp(start_date)).days
        ax.axvline(x=day_index, color=f"C{i % 10}", linestyle="--", alpha=1, linewidth=2)
