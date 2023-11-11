import requests_with_caching
import json

def get_movies_from_tastedive(movie_or_music_artist):
    base_url = 'https://tastedive.com/api/similar'
    params = dict()
    params['q'] = movie_or_music_artist
    params['type'] = 'movies'
    params['limit'] = 5
    response = requests_with_caching.get(base_url, params=params)
    #print(response.url)
    #print(response.text)
    return json.loads(response.text)
    
    
def extract_movie_titles(dictionary):
    titles = list()
    for result in dictionary['Similar']['Results']:
        titles.append(result['Name'])
    
    return titles


def get_related_titles(lst):
    related_titles = list()
    for title in lst:
        related_titles_results = extract_movie_titles(get_movies_from_tastedive(title))
        #print(related_titles_results)
        
        for related_titles_result in related_titles_results:
            if related_titles_result not in related_titles:
                related_titles.append(related_titles_result)
    
    #print(related_titles)
    return related_titles


def get_movie_data(movie_title):
    base_url = 'http://www.omdbapi.com/'
    params = dict()
    params['t'] = movie_title
    params['r'] = 'json'
    response = requests_with_caching.get(base_url, params=params)
    #print(response.text)
    return json.loads(response.text)



def get_movie_rating(OMDB_dict):
    rating_sources = OMDB_dict['Ratings']
    
    for rating_source in rating_sources:
        if rating_source['Source'] == 'Rotten Tomatoes':
            return int(rating_source['Value'].split('%')[0])
    
    return 0



def get_sorted_recommendations(movie_titles_lst):
    ratings = list()
    related_results = get_related_titles(movie_titles_lst)
    #print(related_results)
    
    for related_result in related_results:
        rating = get_movie_rating(get_movie_data(related_result))
        ratings.append(rating)
        
            
    recommendations = list(zip(ratings, related_results))
    sorted_recommendations = sorted(recommendations, reverse=True)
    
    return [recommendation[1] for recommendation in sorted_recommendations] 