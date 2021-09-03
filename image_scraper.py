import praw
import requests
import cv2
import os
import time
import numpy as np
from colorama import init, Fore, Style

# initializing colorama
init()

# Put your credentials here
reddit = praw.Reddit(
    client_id='XXXXXXXXXXXXXXX',
    client_secret='XXXXXXXXXXXXXXX',
    user_agent='XXXXXXXXXXXXXXX',
)

def download_images(names, n_posts, p_type, is_user_list):
    """Receive a list of subreddits or a list of users, maximum number of posts to search and type of posts
    PS: Not every post contains a image"""

    dir_name = 'images'
    
    # create a images directory (if not exists)
    if not os.path.exists(dir_name):
        os.mkdir('images')
    
    # path to removed images directory
    removed_images = os.path.abspath('removed_images')

    lst = []  # list who will contain path of each error image
    
    # Getting path to each error image
    for root, dirs, files in os.walk(removed_images):
        for i in files:  # for each file, get the abs path
            lst.append(os.path.join(root, i))

    for name in names:  # for each element in the list
        if is_user_list:
            user = reddit.redditor(name)
        else:
            subreddit = reddit.subreddit(name)

        # path: images/(subreddit-name or username)
        path = os.path.join(os.path.abspath(dir_name), f'{name}')

        # create a directory for each subreddit / user
        if not os.path.exists(path):
            os.mkdir(path)

        print(f'Downloading images from {name}...')

        if is_user_list:  # searching for images posted by users
            # type of posts
            if p_type == 'top':
                submissions = user.submissions.top(limit=n_posts)
            elif p_type == 'hot':
                submissions = user.submissions.hot(limit=n_posts)
            elif p_type == 'new':
                submissions = user.submissions.new(limit=n_posts)
        
        else:  # searching for images in subreddits
            if p_type == 'top':
                submissions = subreddit.top(limit=n_posts)
            elif p_type == 'hot':
                submissions = subreddit.hot(limit=n_posts)
            elif p_type == 'new':
                submissions = subreddit.new(limit=n_posts)
            elif p_type == 'rising':
                submissions = subreddit.rising(limit=n_posts)

        try:
            count = 0
            for submission in submissions:
                
                if 'jpg' in submission.url or 'jpeg' in submission.url or 'png' in submission.url:
                    try:
                        response = requests.get(submission.url, stream=True).raw

                        image = np.asarray(bytearray(response.read()), dtype='uint8')
                        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

                        # Resizing image for comparison
                        resized_image = cv2.resize(image, (280,140))
                        
                        ignore = False  # flag to show if image should or should not be ignored

                        for i in lst:
                            error_img = cv2.imread(i)

                            # Check if the current image (resized_image) is an error image (error_img)
                            diff = cv2.subtract(error_img, resized_image)
                            b,g,r = cv2.split(diff)
                            
                            total_diff = cv2.countNonZero(b) + cv2.countNonZero(g) + cv2.countNonZero(r)
                            
                            if total_diff == 0:
                                ignore = True

                        if not ignore:
                            count += 1
                            cv2.imwrite(f'{path}/{name}-{submission.id}.png', image)
                            
                        
                    except Exception as e:
                        print(f'Error downloading the image: {submission.url}')
                        print(e)
                
                # if post is a gallery (contains more than one image)
                elif 'gallery' in submission.url:
                    try:
                        gallery = []  # list who will contain links for each image in the gallery
                    
                        for i in submission.media_metadata.values():  
                            try:
                                gallery.append(i['s']['u'])  #  append link for each image
                            except:  # handling errors in galleries who contain other type of files
                                continue

                        tag = 0  # tag to distinguish the filename of images in the same gallery
                        
                        for url in gallery:
                            response = requests.get(url, stream=True).raw
                            
                            image = np.asarray(bytearray(response.read()), dtype='uint8')
                            image = cv2.imdecode(image, cv2.IMREAD_COLOR)

                            # Resizing image for comparison
                            resized_image = cv2.resize(image, (280,140))
                            
                            ignore = False  # flag to show if image should or should not be ignored

                            for i in lst:
                                error_img = cv2.imread(i)

                                # Check if the current image (resized_image) is an error image (error_img)
                                diff = cv2.subtract(error_img, resized_image)
                                b,g,r = cv2.split(diff)
                                
                                total_diff = cv2.countNonZero(b) + cv2.countNonZero(g) + cv2.countNonZero(r)
                                
                                if total_diff == 0:
                                    ignore = True

                            if not ignore:
                                count += len(gallery)
                                cv2.imwrite(f'{path}/{name}-{submission.id}{tag}.png', image)

                            tag += 1
                    except:  # error downloading the gallery
                        continue # just go to next post

            # verify if at least one image was downloaded
            if count > 0:
                print(Fore.GREEN + 'Images downloaded successfully!\n' + Style.RESET_ALL)
                time.sleep(0.5)
            else:
                print(Fore.YELLOW + f'Couldn\'t find any images in first {n_posts} posts.\n'  + Style.RESET_ALL)
                time.sleep(0.5)

        except UnboundLocalError:
            if is_user_list:
                print(Fore.RED + 'Error! You should choose one of this post types (top, hot, new)\n' + Style.RESET_ALL)
                os.rmdir(path)
            else:
                print(Fore.RED + 'Error! You should choose one of this post types (top, hot, new, rising)\n' + Style.RESET_ALL)
                os.rmdir(path)
        except:
            if is_user_list:
                print(Fore.RED + 'Error trying to download images from some user! You should check the names and try again\n' + Style.RESET_ALL)
                os.rmdir(path)
            else:
                print(Fore.RED + 'Error trying to download images from some subreddit! You should check the names and try again\n' + Style.RESET_ALL)
                os.rmdir(path)


def display_menu():
    print('1 - Download images from users')
    print('2 - Download images from subreddits')
    print('0 - End Program')
            

if __name__ == '__main__':   
    
    while True:
        
        try:
            # Menu
            display_menu() 
            option = int(input('Please select one option: '))

            if option < 0 or option > 2:
                print(Fore.RED + 'Invalid option, please select a valid option!\n' + Style.RESET_ALL)

        except ValueError:
            print(Fore.RED + 'You need to run the script again and put a number to select an option.' + Style.RESET_ALL)
            exit(0)

        if option == 1:
            try:
                users = input('Reddit usernames: ').lower().split()
                number_of_posts = int(input('Number of posts to search in each account: '))
                post_type = input('Select a post type (hot, new, top): ').strip().lower()

                is_user_list = True  # flag

                download_images(users, number_of_posts, post_type, is_user_list)
            except:
                print(Fore.RED + 'One of the inputs are wrong, try again\n' + Style.RESET_ALL)
        elif option == 2:
            try:
                subred = input('Subreddits names: ').lower().split()
                number_of_posts = int(input('Number of posts to search in each subreddit: '))
                post_type = input('Select a post type (hot, new, top, rising): ').strip().lower()  

                is_user_list = False     
                
                download_images(subred, number_of_posts, post_type, is_user_list)
            except:
                print(Fore.RED + 'One of the inputs are wrong, try again\n' + Style.RESET_ALL)
        elif option == 0:
            exit(0)
