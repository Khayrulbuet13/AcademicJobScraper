from bs4 import BeautifulSoup
import requests
import json
import csv
import time
from typing import List, Dict, Optional
from pathlib import Path


class AcademicJobScraper:
    """A class to scrape and filter academic job listings."""

    def __init__(
        self,
        keywords: List[str],
        links_file: str = "job_links.csv",
        data_file: str = "jobs_data.json",
        results_file: str = "relevant_jobs.csv"
    ):
        """
        Initialize the AcademicJobScraper.

        Args:
            keywords: List of keywords to filter jobs (case-insensitive)
            links_file: Path to save job links CSV (optional)
            data_file: Path to save job details JSON (optional)
            results_file: Path to save filtered results CSV (optional)
        """
        if not keywords:
            raise ValueError("Keywords list cannot be empty")
            
        self.keywords = keywords
        self.links_file = links_file
        self.data_file = data_file
        self.results_file = results_file

    def scrape(self, url: str) -> None:
        """
        Main method to scrape jobs from a given URL.

        Args:
            url: The mother URL to scrape job listings from
        """
        print(f"Starting job scraping from: {url}")
        
        # Get the HTML content
        response = requests.get(url)
        response.raise_for_status()
        
        # Extract job links
        links = self._extract_job_links(response.text)
        self._save_links_to_csv(links)
        
        # Process each job
        jobs = self._process_jobs(links)
        self._save_jobs_to_json(jobs)
        
        # Filter relevant jobs
        relevant_jobs = self._filter_jobs(jobs)
        self._save_relevant_jobs_to_csv(relevant_jobs)
        
        print(f"\nFound {len(relevant_jobs)} relevant jobs out of {len(jobs)} total jobs")
        print(f"Results saved to: {self.results_file}")

    def _extract_job_links(self, html_content: str) -> List[str]:
        """Extract job links from HTML content."""
        soup = BeautifulSoup(html_content, 'html.parser')
        job_links = []
        
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if "/ajo/jobs/" in href:
                full_url = (
                    f"https://academicjobsonline.org{href}"
                    if href.startswith("/") else href
                )
                if not full_url.endswith('/apply') and full_url not in job_links:
                    job_links.append(full_url)
        
        print(f"Found {len(job_links)} job links")
        return job_links

    def _save_links_to_csv(self, links: List[str]) -> None:
        """Save job links to CSV file."""
        with open(self.links_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Job Link"])
            for link in links:
                writer.writerow([link])

    def _extract_job_details(self, url: str) -> Optional[Dict]:
        """Extract details from a job page."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Get job title
            title_div = soup.find('b', string='Position Title:')
            title = ''
            if title_div and title_div.parent:
                # Get the next div after the parent div containing "Position Title:"
                title_content_div = title_div.parent.find_next_sibling('div')
                title = title_content_div.text.strip() if title_content_div else ''

            # Get other details
            h2_tag = soup.find('h2')
            desc_section = soup.find(
                'section',
                style=lambda x: x and 'width:96%' in x and 'border:1px solid #cccccc' in x
            )
            canonical_link = soup.find('link', rel='canonical')
            
            return {
                'title': title,
                'institute': h2_tag.text.strip() if h2_tag else '',
                'description': desc_section.text.strip() if desc_section else '',
                'job_link': canonical_link['href'] if canonical_link else url
            }
        except Exception as e:
            print(f"Error processing {url}: {str(e)}")
            return None

    def _process_jobs(self, links: List[str]) -> List[Dict]:
        """Process all job links and extract details."""
        all_jobs = []
        total_jobs = len(links)
        
        print(f"\nProcessing {total_jobs} jobs...")
        for i, url in enumerate(links, 1):
            print(f"Processing job {i}/{total_jobs}: {url}")
            job_details = self._extract_job_details(url)
            if job_details:
                all_jobs.append(job_details)
                print(f"Successfully extracted details for job {i}")
            time.sleep(1)  # Be nice to the server
        
        return all_jobs

    def _save_jobs_to_json(self, jobs: List[Dict]) -> None:
        """Save job details to JSON file."""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(jobs, f, indent=2, ensure_ascii=False)

    def _contains_keywords(self, description: str) -> bool:
        """Check if description contains any keywords."""
        description_lower = description.lower()
        return any(keyword.lower() in description_lower for keyword in self.keywords)

    def _filter_jobs(self, jobs: List[Dict]) -> List[Dict]:
        """Filter jobs based on keywords."""
        matching_jobs = []
        
        for job in jobs:
            if self._contains_keywords(job['description']):
                title = job['title'] if job['title'] else job['institute']
                matching_jobs.append({
                    'title': title,
                    'company': job['institute'],
                    'link': job['job_link']
                })
        
        return matching_jobs

    def _save_relevant_jobs_to_csv(self, matching_jobs: List[Dict]) -> None:
        """Save filtered jobs to CSV file."""
        with open(self.results_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['title', 'company', 'link'])
            writer.writeheader()
            writer.writerows(matching_jobs)
