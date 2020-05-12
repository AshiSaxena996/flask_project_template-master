import pandas as pd
from app import db
import os
from app.models import Restaurant, Rating, User, Locality, Cuisine


def seed_ratings(filepath="../csv_data/user_ratings.csv"):
    if os.path.exists(filepath):
        df = pd.read_csv(filepath, index_col=0)
        for index, row in df.iterrows():
            # access data using column names which are required, print is not neccessary
            # USERNAME,REST_ID,RESTAURANT,RATING
            print(index, row['USERNAME'], row['REST_ID'], row['RATING'])
            record = Rating(rest_id=row['REST_ID'], rating=row['RATING'], username=row['USERNAME'])
            db.session.add(record)
        # save every thing
        db.session.commit()


def seed_users(filepath="../csv_data/user_data_01.csv"):
    if os.path.exists(filepath):
        df = pd.read_csv(filepath, index_col=0)
        for index, row in df.iterrows():
            # access data using column names which are required, print is not neccessary
            # print(index, row['USERNAME'], row['EMAIL'], row['PASSWORD'],row['NAME'],row['AGE'], row['PHONE'], row['CITY'])
            user = User(username=row['USERNAME'],
                        email=row['EMAIL'],
                        name=row['NAME'],
                        age=row['AGE'],
                        phone=row['PHONE'],
                        city=row['CITY'])
            user.set_password(password=row['PASSWORD'])
            db.session.add(user)
        db.session.commit()


def seed_restuarants(filepath="../csv_data/lko_final_01.csv"):
    if os.path.exists(filepath):
        df = pd.read_csv(filepath)
        for index, r in df.iterrows():
            # rest_id,zomato_url,name,city,area,rating,rating_count,telephone,
            # cuisine,cost_for_two,address,online_order,table_reservation,delivery_only,
            # famous_food,longitude,latitude

            record = Restaurant(id=r['rest_id'],
                                zomato_url=r['zomato_url'],
                                name=r['name'],
                                city=r['city'],
                                area=r['area'],
                                rating=r['rating'],
                                rating_count=r['rating_count'],
                                telephone=r['telephone'],
                                cuisine=r['cusine'],
                                cost_for_two=r['cost_for_two'],
                                address=r['address'],
                                online_order=r['online_order'],
                                table_reservation=r['table_reservation'],
                                delivery_only=r['delivery_only'],
                                famous_food=r['famous_food'],
                                longitude=r['longitude'],
                                latitude=r['latitude'], )
            db.session.add(record)
        db.session.commit()


def seed_locality(filepath="../csv_data/lko_final_01.csv"):
    if os.path.exists(filepath):
        df = pd.read_csv(filepath, index_col=0)
        df_local = df[['area', 'city']].copy()
        df_local.drop_duplicates(keep='first', inplace=True)
        for index, row in df_local.iterrows():
            record = Locality(name=row['area'], city=row['city'])
            db.session.add(record)
        db.session.commit()


def seed_cuisine(filepath="../csv_data/lko_final_01.csv"):
    if os.path.exists(filepath):
        df = pd.read_csv(filepath, index_col=0)
        df_local = df[['cusine']].copy()
        df_local.drop_duplicates(keep='first', inplace=True)
        for index, row in df_local.iterrows():
            record = Cuisine(name=row['cusine'])
            db.session.add(record)
        db.session.commit()


if __name__ == '__main__':
    seed_locality()
    seed_cuisine()
    print("done")
