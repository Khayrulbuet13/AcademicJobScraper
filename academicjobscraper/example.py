from academicjobscraper import AcademicJobScraper

# Example usage of the AcademicJobScraper package

# Initialize the scraper with required keywords and optional file names
scraper = AcademicJobScraper(
    # Required: List of keywords to filter jobs
    keywords=[
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "computer vision"
    ],
    # Optional: Custom file names (these are the default values)
    links_file="job_links.csv",
    data_file="jobs_data.json",
    results_file="relevant_jobs.csv"
)

# Start scraping with a mother URL
# Replace this URL with an actual academicjobsonline.org search URL
url = "https://academicjobsonline.org/ajo/computer_science"
scraper.scrape(url)

# The results will be saved to:
# - job_links.csv: All scraped job URLs
# - jobs_data.json: Detailed information for all jobs
# - relevant_jobs.csv: Filtered jobs matching the keywords
