import json
from django.shortcuts import render
from django.http import JsonResponse
from aima3.logic import FolKB, expr, fol_fc_ask

# Define global agenda and working memory
agenda = []
working_memory = {}

def add_to_agenda(task):
    agenda.append(task)

def update_working_memory(key, value):
    working_memory[key] = value

def process_preferences(preferences, kb):
    global working_memory
    # Initialize an empty list for recommended restaurants
    recommended_restaurants = []

    # Update working memory with user preferences
    for key, value in preferences.items():
        update_working_memory(key, value)

    # Process agenda tasks
    while agenda:
        task = agenda.pop(0)
        if task == 'recommend_restaurants':
            recommended_restaurants.extend(restaurant_recommendation.generate_recommendations(preferences))
        # Add more tasks as needed

    return recommended_restaurants

def restaurant_recommendation(request):
    if request.method == 'POST':
        # Process the user's preferences
        body_unicode = request.body.decode('utf-8')
        preferences = json.loads(body_unicode)
        print(preferences)

        # Create an empty knowledge base
        kb = FolKB()

        # Add rules to the knowledge base
        expr1_possibility_1 = expr("cuisine('algerian') and prefers('algerian_cuisine')")
        expr1_possibility_2 = expr("not cuisine('algerian') or prefers('algerian_cuisine')")
        expr2_possibility_1 = expr("budget('friendly') and prefers('budget_friendly')")
        expr2_possibility_2 = expr("not budget('friendly') or prefers('budget_friendly')")
        expr3_possibility_1 = expr("atmosphere('cozy') and prefers('cozy_atmosphere')")
        expr3_possibility_2 = expr("not atmosphere('cozy') or prefers('cozy_atmosphere')")
        expr4_possibility_1 = expr("location('downtown') and prefers('downtown_location')")
        expr4_possibility_2 = expr("not location('downtown') or prefers('downtown_location')")
        expr5_possibility_1 = expr("location('uptown') and prefers('uptown_location')")
        expr5_possibility_2 = expr("not location('uptown') or prefers('uptown_location')")
        expr6_possibility_1 = expr("location('suburb') and prefers('suburb_location')")
        expr6_possibility_2 = expr("not location('suburb') or prefers('suburb_location')")
        expr7_possibility_1 = expr("traditional_dishes('yes') and prefers('traditional_dishes')")
        expr7_possibility_2 = expr("not traditional_dishes('yes') or prefers('traditional_dishes')")

        # Add expressions to knowledge base
        kb.tell(expr1_possibility_1)
        kb.tell(expr1_possibility_2)
        kb.tell(expr2_possibility_1)
        kb.tell(expr2_possibility_2)
        kb.tell(expr3_possibility_1)
        kb.tell(expr3_possibility_2)
        kb.tell(expr4_possibility_1)
        kb.tell(expr4_possibility_2)
        kb.tell(expr5_possibility_1)
        kb.tell(expr5_possibility_2)
        kb.tell(expr6_possibility_1)
        kb.tell(expr6_possibility_2)
        kb.tell(expr7_possibility_1)
        kb.tell(expr7_possibility_2)

        # Function to process user responses and recommend restaurants
        def recommend_restaurants(preferences):
            activated = fol_fc_ask(kb, preferences.items())
            print(activated)
                
            # Recommendations based on activated preferences
            recommended_restaurants = []

            # Example recommendations (replace with your logic)
            # Get user preferences
            algerian_pref = preferences.get('algerian', '')
            budget_pref = preferences.get('budget_friendly', '')
            cozy_pref = preferences.get('cozy', '')
            location_pref = preferences.get('location', '')
            traditional_dishes_pref = preferences.get('traditional_dishes', '')

            # Check all combinations of preferences
            if algerian_pref == 'yes':
                if budget_pref == 'yes':
                    recommended_restaurants.append({'name': 'Algiers Budget Bites', 'city': 'Algiers'})
                else:
                    recommended_restaurants.append({'name': 'Algiers Fine Dining', 'city': 'Algiers'})

            if budget_pref == 'yes':
                recommended_restaurants.append({'name': 'Algiers Budget Bites', 'city': 'Algiers'})

            if cozy_pref == 'yes':
                if location_pref == 'downtown':
                    recommended_restaurants.append({'name': 'Downtown Cozy Corner', 'city': 'Algiers'})
                    recommended_restaurants.append({'name': 'Oran Oasis', 'city': 'Oran'})
                    recommended_restaurants.append({'name': 'Bejaia Bistro', 'city': 'Bejaia'})
                    recommended_restaurants.append({'name': 'Tizi Ouzo Tavern', 'city': 'Tizi Ouzo'})
                elif location_pref == 'uptown':
                    recommended_restaurants.append({'name': 'Uptown Cozy Cafe', 'city': 'Algiers'})
                elif location_pref == 'suburb':
                    recommended_restaurants.append({'name': 'Suburban Comfort Eats', 'city': 'Algiers'})

            if location_pref == 'downtown':
                recommended_restaurants.append({'name': 'Downtown Dining', 'city': 'Algiers'})
            elif location_pref == 'uptown':
                recommended_restaurants.append({'name': 'Uptown Eats', 'city': 'Algiers'})
            elif location_pref == 'suburb':
                recommended_restaurants.append({'name': 'Suburban Grill', 'city': 'Algiers'})

            if traditional_dishes_pref == 'yes':
                recommended_restaurants.append({'name': 'Traditional Tastes', 'city': 'Algiers'})

            return recommended_restaurants

        # Get restaurant recommendations based on user preferences
        recommendations = recommend_restaurants(preferences)

        # Prepare response data
        response_data = {'recommended_restaurants': recommendations}

        return JsonResponse(response_data)

    return render(request, 'home.html')
