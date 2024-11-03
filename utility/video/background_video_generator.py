import os 
import requests
from utility.utils import log_response,LOG_TYPE_PEXEL

PEXELS_API_KEY = os.environ.get('PEXELS_KEY')

def search_images(query_string, orientation_landscape=True):
    url = "https://api.pexels.com/v1/search"
    headers = {
        "Authorization": PEXELS_API_KEY,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    params = {
        "query": query_string,
        "orientation": "landscape" if orientation_landscape else "portrait",
        "per_page": 15
    }

    response = requests.get(url, headers=headers, params=params)
    json_data = response.json()
    log_response(LOG_TYPE_PEXEL, query_string, response.json())
   
    return json_data


def get_best_image(query_string, orientation_landscape=True, used_images=[]):
    imgs = search_images(query_string, orientation_landscape)
    photos = imgs['photos']  # Extract the photos list from JSON

    # Filter and extract images with width and height as 1920x1080 for landscape or 1080x1920 for portrait
    if orientation_landscape:
        filtered_images = [photo for photo in photos if photo['width'] >= 1920 and photo['height'] >= 1080 and photo['width']/photo['height'] == 16/9]
    else:
        filtered_images = [photo for photo in photos if photo['width'] >= 1080 and photo['height'] >= 1920 and photo['height']/photo['width'] == 9/16]

    # Return the first unused image URL
    for image in filtered_images:
        image_url = image['src']['large']
        if image_url not in used_images:
            return image_url
    print("NO IMAGES found for this round of search with query:", query_string)
    return None


def generate_image_url(timed_image_searches, image_server):
    timed_image_urls = []
    if image_server == "pexel":
        used_links = []
        for (t1, t2), search_terms in timed_image_searches:
            url = ""
            for query in search_terms:
                url = get_best_image(query, orientation_landscape=False, used_images=used_links)
                if url:
                    used_links.append(url)
                    break
            timed_image_urls.append([[t1, t2], url])
    elif image_server == "stable_diffusion":
        timed_image_urls = get_images_for_video(timed_image_searches)

    return timed_image_urls