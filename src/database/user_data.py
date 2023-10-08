from src.database.parse_url import parse_hashtags, parse_urls, find_social_media, parse_linkdein_url
from pprint import pprint

def add_update_to_database(data: dict):
    data['Hashtags'] = parse_hashtags(data['Hashtags'])

    data['Social_Media_Links'] = parse_urls(data['Social_Media_Links'])

    data['Media_content'] = {}

    if data['Social_Media_Links']:
        for link in data['Social_Media_Links']:
            media = find_social_media(link)

            data['Media_content'][media] = {}
            data['Media_content'][media] = "No Details"

            if media == 'linkedin':
                media_data = parse_linkdein_url(link)
                data['Media_content']['linkedin'] = media_data


    pprint(data)
