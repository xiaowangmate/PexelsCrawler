import re
import os
import json
import time
import requests
import cfscrape

scraper = cfscrape.create_scraper()


class PexelsCrawler:
    def __init__(self, output_dir):
        self.index_headers = {
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Cache-Control": "no-cache",
            "Cookie": "_ga=GA1.1.1897440495.1712042147; _fbp=fb.1.1712042152434.1774328176; g_state={\"i_p\":1712137685143,\"i_l\":1}; cf_clearance=EZVhz38TlQSKevWntJFqV_fv8A5gFdwG0PlK7eJTXtE-1712456870-1.0.1.1-bWs3_Wqy.sT1v6dtPXhhWZPAEDlpzrlW1Trh1qUtxbUHqFGFnHve_2r5egHniYKPyRErTLPziqgxLB6c_nm8SA; OptanonConsent=isGpcEnabled=0&datestamp=Sun+Apr+07+2024+10%3A59%3A24+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202301.1.0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0%2CC0004%3A0&AwaitingReconsent=false; __cf_bm=9R2mCimSg3.lYB5em9m7rclHSeBb7.uv6gzvLuirAKA-1712461948-1.0.1.1-wGQUMRGzo1DKQygkg6aA2.j_nig8pU7.Ta4u0Bq_2mthnAiW5mZj9RYIjvy6L.YY7f81pAQ.qorJntM_2gyEIw; _sp_id.9ec1=cced12ff-e652-489f-bbab-51b9b8cf9a3d.1712042147.9.1712462050.1712459040.55398800-1a30-487f-8b27-6785956ed8c0.c299599f-a614-4bce-8887-121a68837b6a.3d238f1e-819c-43b3-b1ea-6f77df8bbe04.1712462050321.1; _sp_ses.9ec1=*; _ga_8JE65Q40S6=GS1.1.1712462051.10.0.1712462051.0.0.0",
            "Pragma": "no-cache",
            "Referer": "https://www.pexels.com/zh-cn/",
            "Sec-Ch-Ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Microsoft Edge\";v=\"120\"",
            "Sec-Ch-Ua-Arch": "\"x86\"",
            "Sec-Ch-Ua-Bitness": "\"64\"",
            "Sec-Ch-Ua-Full-Version": "\"120.0.2210.91\"",
            "Sec-Ch-Ua-Full-Version-List": "\"Not_A Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"120.0.6099.130\", \"Microsoft Edge\";v=\"120.0.2210.91\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Model": "\"\"",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
            "Sec-Ch-Ua-Platform-Version": "\"15.0.0\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
            "X-Nextjs-Data": "1"
        }
        self.headers = {
            "Referer": "https://www.pexels.com/videos/",
            "Secret-Key": "H2jk9uKnhRmL6WPwh89zBezWvr",
            "Cookie": '_ga=GA1.1.1897440495.1712042147; _fbp=fb.1.1712042152434.1774328176; country-code-v2=HK; g_state={"i_p":1712137685143,"i_l":1}; _sp_ses.9ec1=*; __cf_bm=ZR8kyxZECGmX1rZ3CNNWKoQR98ISO.BoM1dae5TzPQ4-1712137983-1.0.1.1-NJRbYLOhMWka0QHKu736aOjl8lctiVZ99a0N0dZtMwVt3hV5zznpY7JRAZIG61ZKfBuR.Q0XVKlFLu0T.FjyOQ; _sp_id.9ec1=cced12ff-e652-489f-bbab-51b9b8cf9a3d.1712042147.7.1712137986.1712133851.92c8e04a-fd66-48f8-a083-a71124ad6dee.00145d2b-afa1-4b1a-a3d7-a131d64139fe.bd54ed3a-69a0-4423-827a-cf8c7ab22884.1712137981625.3; cf_clearance=PWZ.nkDvFTEjyzRQRc4xR9ql4ZMlbOz5MZB83rtteHc-1712137985-1.0.1.1-ypVupUy_0LkFqP0WB0P7eIHKM_iU6FKtfMI0bCwNDCbI_8rcauy7T531GWbPhwVtKT93kACPMGT2wYrvswAlFg; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Apr+03+2024+17%3A53%3A06+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202301.1.0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0%2CC0004%3A0&AwaitingReconsent=false; _ga_8JE65Q40S6=GS1.1.1712137982.7.1.1712137986.0.0.0',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.46"
        }
        self.index_page_url = "https://www.pexels.com/_next/data/HrcChhFmHNOvLJzHC6L0N/zh-CN/home/videos.json"
        self.output_dir = output_dir
        self.downloaded_video_count = self.get_downloaded_video_count()

    def get_downloaded_video_count(self):
        downloaded_video_count = len(
            [f for f in os.listdir(self.output_dir) if os.path.isfile(os.path.join(self.output_dir, f))])
        print(f"downloaded video count: {downloaded_video_count}")
        return downloaded_video_count

    def update_downloaded_video_count(self):
        self.downloaded_video_count += 1
        print(f"downloaded video count: {self.downloaded_video_count}\n{'-' * 100}")

    def crawl_index_page(self):
        response = scraper.get(self.index_page_url, headers=self.index_headers)
        print(response.text)
        response_json = json.loads(response.text)
        initial_data = response_json["pageProps"]["initialData"]
        all_videos = initial_data["data"]
        for video in all_videos:
            download_url = video["attributes"]["video"]["download"]
            print(f"download_url: {download_url}")
            self.download_video(download_url)

        next_seed = initial_data["pagination"]["cursor"]
        more_data = initial_data["pagination"]["more_data"]

        return next_seed, more_data

    def crawl_all(self, last_cursor):
        request_url = f"https://www.pexels.com/en-us/api/v3/videos?seed={last_cursor}&per_page=12&seo_tags=true"
        response = requests.get(request_url, headers=self.headers)
        response_json = json.loads(response.text)

        all_videos = response_json["data"]
        for video in all_videos:
            # download_url = video["attributes"]["video"]["download"]
            # print(f"download_url: {download_url}")
            # self.download_video(download_url)

            self.select_resolution_for_download(video)

        next_seed = response_json["pagination"]["cursor"]
        more_data = response_json["pagination"]["more_data"]

        return next_seed, more_data

    def crawl_recent(self, last_cursor):
        request_url = f"https://www.pexels.com/zh-cn/api/v3/media/recent?seed={last_cursor}&per_page=12&medium_type=Video&seo_tags=true"
        response = requests.get(request_url, headers=self.headers)
        response_json = json.loads(response.text)

        all_videos = response_json["data"]
        for video in all_videos:
            # download_url = video["attributes"]["video"]["download"]
            # print(f"download_url: {download_url}")
            # self.download_video(download_url)

            self.select_resolution_for_download(video)

        next_seed = response_json["pagination"]["cursor"]
        more_data = response_json["pagination"]["more_data"]

        return next_seed, more_data

    def select_resolution_for_download(self, video_json, resolution="1280x720"):
        """
        resolution list(width x height): [426x240, 640x360, 960x540, 1280x720, 1920x1080, 2560x1440, 3840x2160]
        """
        if resolution in ["3840x2160", "2560x1440"]:
            quality = "uhd"
        elif resolution in ["1920x1080", "1280x720"]:
            quality = "hd"
        else:
            quality = "sd"
        video_id = video_json["id"]
        default_download_url = video_json["attributes"]["video"]["src"]
        fps = re.findall("https://videos.pexels.com/video-files/.*?/.*?_(\d{1,2}0)fps.mp4", default_download_url)[0]
        hd_download_url = f"https://videos.pexels.com/video-files/{video_id}/{video_id}-{quality}_{resolution.replace('x', '_')}_{fps}fps.mp4"
        print(f"download_url: {hd_download_url}")
        self.download_video(video_id, hd_download_url)

    def download_video(self, video_id, download_url):
        output_path = f"{self.output_dir}/{video_id}.mp4"
        if not os.path.exists(output_path):
            response = scraper.get(download_url, stream=True, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.46"})
            if response.status_code == 200:
                with open(output_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            file.write(chunk)
                print(f"Video downloaded successfully: {video_id}")
                self.update_downloaded_video_count()
                time.sleep(0.1)
            else:
                print(f"Failed to download video: {download_url}, {response.text}")
                # time.sleep(100)
                # self.download_video(download_url)
        else:
            print(f"Video exist: {video_id}")

    def start_crawl(self):
        seed, more_data = self.crawl_index_page()
        while more_data:
            seed, more_data = self.crawl_all(seed)
            print(f"seed: {seed}, more data: {more_data}")

    def start_crawl_recent(self, seed):
        more_data = True
        while more_data:
            seed, more_data = self.crawl_recent(seed)
            print(f"seed: {seed}, more data: {more_data}")


if __name__ == '__main__':
    pc = PexelsCrawler("G:/Pexels")
    # pc.start_crawl()
    pc.start_crawl_recent("2024-03-29T19%3A00%3A31.784Z")

    # https://videos.pexels.com/video-files/20231457/20231457-hd_1280_720_60fps.mp4
