# To add a new cell, type ''
# To add a new markdown cell, type ' [markdown]'

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import pairwise_distances
from app.models import db






def find_n_neighbours(df,n):
    order = np.argsort(df.values, axis=1)[:, :n]
    df = df.apply(lambda x: pd.Series(x.sort_values(ascending=False).iloc[:n].index, index=['top{}'.format(i) for i in range(1, n+1)]), axis=1)
    return df

def get_user_similar_restuarants( user1, user2 ):
    common_restuarants = Rating_avg[Rating_avg.username == user1].merge(Rating_avg[Rating_avg.username == user2], on = "rest_id", how = "inner" )
    return common_restuarants.merge( hotel, on = 'rest_id' )

def User_item_score(user,item,sim_user_30_m,final_restuarant,Mean,similarity_with_restuarant):
    a = sim_user_30_m[sim_user_30_m.index==user].values
    b = a.squeeze().tolist()
    c = final_restuarant.loc[:,item]
    d = c[c.index.isin(b)]
    f = d[d.notnull()]
    avg_user = Mean.loc[Mean['username'] == user,'rating'].values[0]
    index = f.index.values.squeeze().tolist()
    corr = similarity_with_restuarant.loc[user,index]
    fin = pd.concat([f, corr], axis=1)
    fin.columns = ['adg_score','correlation']
    fin['score']=fin.apply(lambda x:x['adg_score'] * x['correlation'],axis=1)
    nume = fin['score'].sum()
    deno = fin['correlation'].sum()
    final_score = avg_user + (nume/deno)
    return final_score

def User_item_score1(user, Mean, similarity_with_restuarant, check, sim_user_30_m, restuarant_user, final_restuarant, hotel):
    restuarant_seen_by_user = check.columns[check[check.index==user].notna().any()].tolist()
    a = sim_user_30_m[sim_user_30_m.index==user].values
    b = a.squeeze().tolist()
    d = restuarant_user[restuarant_user.index.isin(b)]
    l = ','.join(d.values)
    restuarant_seen_by_similar_users = l.split(',')
    restuarants_under_consideration = list(set(restuarant_seen_by_similar_users)-set(list(map(str, restuarant_seen_by_user))))
    restuarants_under_consideration = list(map(int, restuarants_under_consideration))
    score = []
    for item in restuarants_under_consideration:
        c = final_restuarant.loc[:,item]
        d = c[c.index.isin(b)]
        f = d[d.notnull()]
        avg_user = Mean.loc[Mean['username'] == user,'rating'].values[0]
        index = f.index.values.squeeze().tolist()
        corr = similarity_with_restuarant.loc[user,index]
        fin = pd.concat([f, corr], axis=1)
        fin.columns = ['adg_score','correlation']
        fin['score']=fin.apply(lambda x:x['adg_score'] * x['correlation'],axis=1)
        nume = fin['score'].sum()
        deno = fin['correlation'].sum()
        final_score = avg_user + (nume/deno)
        score.append(final_score)
    data = pd.DataFrame({'REST_ID':restuarants_under_consideration,'score':score})
    top_5_recommendation = data.sort_values(by='score',ascending=False).head(5)
    
    top_5_recommendation.columns=['rest_id','score']
    restuarant_Name = top_5_recommendation.merge(hotel, how='inner', on='rest_id')
    restuarant_Names = restuarant_Name.name.values.tolist()
    return restuarant_Names



if __name__ == "__main__":
    username = "user_053_abc"
    user= pd.read_sql('rating',db.engine)
    user[user.username==username]
    a= user[user.username==username]
    b= a.rating
    b.tolist()
    df = user.set_index('id', drop = True)
    a1= df.loc[10:20,"rating"]
    a2= list(a1)
    hotel = pd.read_sql("restaurant", db.engine)
    Ratings = pd.read_sql("rating", db.engine)
    Mean = Ratings.groupby(by="username",as_index=False)['rating'].mean()
    Rating_avg = pd.merge(Ratings,Mean,on='username')
    Rating_avg['adg_rating']=Rating_avg['rating_x']-Rating_avg['rating_y']
    Rating_avg.head(15)

    hotel.rename(columns = {'id':'rest_id'}, inplace = True) 

    check = pd.pivot_table(Rating_avg,values='rating_x',index='username',columns='rest_id')
    check.head(15)
    final = pd.pivot_table(Rating_avg,values='adg_rating',index='username',columns='rest_id')

    # Replacing NaN by restuarant Average
    final_restuarant = final.fillna(final.mean(axis=0))

    # Replacing NaN by user Average
    final_user = final.apply(lambda row: row.fillna(row.mean()), axis=1)
    b = cosine_similarity(final_user)
    np.fill_diagonal(b, 0 )
    similarity_with_user = pd.DataFrame(b,index=final_user.index)
    similarity_with_user.columns=final_user.index

    # user similarity on replacing NAN by item(restuarant) avg
    cosine = cosine_similarity(final_restuarant)
    np.fill_diagonal(cosine, 0 )
    similarity_with_restuarant = pd.DataFrame(cosine,index=final_restuarant.index)
    similarity_with_restuarant.columns=final_user.index

    # top 30 neighbours for each user
    sim_user_30_u = find_n_neighbours(similarity_with_user,30)

    # top 30 neighbours for each user
    sim_user_30_m = find_n_neighbours(similarity_with_restuarant,30)
    
    score = User_item_score(username,74385,sim_user_30_m,final_restuarant,Mean,similarity_with_restuarant,)
    print("score (u,i) is",score)

    Rating_avg = Rating_avg.astype({"rest_id": str})
    restuarant_user = Rating_avg.groupby(by = 'username')['rest_id'].apply(lambda x:','.join(x))
    user = "user_01_abc"

    pred_rest = User_item_score1(user,Mean,similarity_with_restuarant,check)

    print(pred_rest)
    












