from descriptive_stats import process_and_plot
from significance_tests import analyze_events

classified_posts = "/Users/josephhirsh/Documents/GitHub/orientx2/assets/classified_posts_for_stats.csv"


# process_and_plot(classified_posts, 0)
# process_and_plot(classified_posts, 1)
# process_and_plot(classified_posts, 2)

print(analyze_events(classified_posts))
