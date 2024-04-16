from argparse import ArgumentParser
from crawl_pexels import PexelsCrawler

parser = ArgumentParser()

parser.add_argument(
    '--download_dir'
)

args = parser.parse_args()

pc = PexelsCrawler(args.download_dir)
pc.start_crawl_recent(pc.read_last_seed())
