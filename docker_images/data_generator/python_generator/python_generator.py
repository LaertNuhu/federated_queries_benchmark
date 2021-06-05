#!/usr/bin/python3

import os
import pandas as pd
import random
import string
import time


def random_string(str_size):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(str_size))


def create_users():
    n_users = int(os.getenv("N_USERS"))
    id_length = int(os.getenv("ID_LENGTH"))
    date_length = int(os.getenv("DATE_LENGTH"))
    countries = os.getenv("COUNTRIES").split()
    user_list = []

    for _ in range(n_users):
        user = [
            int(random.random() * 10 ** id_length),
            int(random.random() * 10 ** date_length),
            random.choice(countries)
        ]
        user_list.append(user)
    return pd.DataFrame(user_list, columns=["id", "reg_date", "country"])


def create_photos(users):
    id_length = int(os.getenv("ID_LENGTH"))
    date_length = int(os.getenv("DATE_LENGTH"))
    title_length = int(os.getenv("TITLE_LENGTH"))
    max_photos = int(os.getenv("MAX_PHOTOS_PER_USER"))
    max_views = int(os.getenv("MAX_VIEWS"))
    details_length = int(os.getenv("DETAILS_LENGTH"))
    photo_list = []

    for idx, row in users.iterrows():
        for _ in range(int(random.random() * max_photos)):
            photo = [
                int(random.random() * 10 ** id_length),
                random_string(title_length),
                row["id"],
                int(random.random() * max_views),
                random_string(details_length),
                int(random.random() * 10 ** date_length)
            ]
            photo_list.append(photo)
    return pd.DataFrame(photo_list, columns=["id", "title", "user_id", "views", "details", "date"])


def create_clicks(users):
    date_length = int(os.getenv("DATE_LENGTH"))
    details_length = int(os.getenv("DETAILS_LENGTH"))
    url_length = int(os.getenv("URL_LENGTH"))
    max_clicks = int(os.getenv("MAX_CLICKS_PER_USER"))
    click_list = []

    for idx, row in users.iterrows():
        for _ in range(int(random.random() * max_clicks)):
            click = [
                int(random.random() * 10 ** date_length),
                row["id"],
                random_string(url_length),
                random_string(details_length)
            ]
            click_list.append(click)
    return pd.DataFrame(click_list, columns=["id", "user_id", "url", "details"])


def create_orders(clicks, photos):
    id_length = int(os.getenv("ID_LENGTH"))
    order_chance = float(os.getenv("ORDER_CHANCE_PER_CLICK"))
    n_types = int(os.getenv("N_ORDER_TYPES"))
    max_price = float(os.getenv("MAX_PRICE"))
    countries = os.getenv("COUNTRIES").split()
    order_list = []

    for idx, row in clicks.iterrows():
        if random.random() < order_chance:
            order = [
                int(random.random() * 10 ** id_length),
                int(random.random() * n_types),
                row["url"],
                photos["id"].sample().iloc[0],
                random.random() * max_price,
                random.choice(countries)
            ]
            order_list.append(order)
    return pd.DataFrame(order_list, columns=["id", "type", "source", "photo_id", "price", "country"])


if __name__ == '__main__':
    start_time = time.time()
    checkpoint_time = time.time()
    random.seed(os.getenv("RANDOM_SEED"))

    print("Creating users table...")
    users = create_users()
    print(f"↳ Users creation time: {time.time() - checkpoint_time:.5f} seconds.")
    checkpoint_time = time.time()

    print("Creating photos table...")
    photos = create_photos(users)
    print(f"↳ Photos creation time: {time.time() - checkpoint_time:.5f} seconds.")
    checkpoint_time = time.time()

    print("Creating clicks table...")
    clicks = create_clicks(users)
    print(f"↳ Clicks creation time: {time.time() - checkpoint_time:.5f} seconds.")
    checkpoint_time = time.time()

    print("Creating orders table...")    
    orders = create_orders(clicks, photos)
    print(f"↳ Orders creation time: {time.time() - checkpoint_time:.5f} seconds.")
    checkpoint_time = time.time()

    root_dir = "/data"
    print(f"Writing output to {root_dir}...")
    users.to_csv(os.path.join(root_dir, "users.csv"), index=False, header=False)
    photos.to_csv(os.path.join(root_dir, "photos.csv"), index=False, header=False)
    clicks.to_csv(os.path.join(root_dir, "clicks.csv"), index=False, header=False)
    orders.to_csv(os.path.join(root_dir, "orders.csv"), index=False, header=False)

    print(f"↳ Total time: {time.time() - start_time:.5f} seconds.")
