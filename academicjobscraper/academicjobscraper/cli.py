import argparse
from .scraper import AcademicJobScraper


def main():
    """Command line interface for AcademicJobScraper."""
    parser = argparse.ArgumentParser(
        description="Scrape and filter academic job listings."
    )
    
    parser.add_argument(
        "url",
        help="Mother URL to scrape job listings from"
    )
    
    parser.add_argument(
        "keywords",
        nargs="+",
        help="Keywords to filter jobs (case-insensitive)"
    )
    
    parser.add_argument(
        "--links-file",
        default="job_links.csv",
        help="Path to save job links CSV (default: job_links.csv)"
    )
    
    parser.add_argument(
        "--data-file",
        default="jobs_data.json",
        help="Path to save job details JSON (default: jobs_data.json)"
    )
    
    parser.add_argument(
        "--results-file",
        default="relevant_jobs.csv",
        help="Path to save filtered results CSV (default: relevant_jobs.csv)"
    )
    
    args = parser.parse_args()
    
    # Initialize and run scraper
    scraper = AcademicJobScraper(
        keywords=args.keywords,
        links_file=args.links_file,
        data_file=args.data_file,
        results_file=args.results_file
    )
    
    try:
        scraper.scrape(args.url)
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
