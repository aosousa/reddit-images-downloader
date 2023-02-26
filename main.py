import os
import requests

from configparser import ConfigParser

parser = ConfigParser()
parser.read('./config.ini')

subreddits = parser.get('main', 'subreddits').split(',')
images_folder = parser.get('main', 'images_folder')

for subreddit in subreddits:
    r = requests.get('https://www.reddit.com/r/{subreddit}.json'.format(subreddit=subreddit), headers = {'User-agent': 'rid-v1'})
    res = r.json()

    # create folder for subreddit images if it doesn't exist
    subreddit_folder = '{folder}/{subreddit}'.format(folder=images_folder, subreddit=subreddit)
    if not os.path.isdir(subreddit_folder):
        os.makedirs(subreddit_folder)

    for post in res['data']['children']:
        if 'post_hint' in post['data'] and post['data']['post_hint'] == 'image':
            filename_split = post['data']['url'].split('/')
            filename = filename_split[len(filename_split) - 1]
            file_path = '{folder}/{filename}'.format(folder=subreddit_folder, filename=filename)
            if not os.path.exists(file_path):
                image_data = requests.get(post['data']['url']).content

                f = open(file_path, 'wb')
                f.write(image_data)
                f.close()

                if os.path.exists(file_path):
                    print('Successfully saved image {filename} from the {subreddit} subreddit'.format(filename=filename, subreddit=subreddit))
            else:
                print('Skipping image {filename} from the {subreddit} subreddit - file already exists'.format(filename=filename, subreddit=subreddit))