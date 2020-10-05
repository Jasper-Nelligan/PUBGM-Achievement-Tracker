import json 
  
with open('./Test Files/achievements.json','r') as achievements:
  achievement_dict = json.load(achievements) # only key in achievement_dict is "achievements"
  for achievement in achievement_dict["achievements"]: # achievement is a dictionary containing achievement attributes
      if (achievement['title'] == "Leveled Achievement 2"):  
            print("Category: " + achievement['category'])
            print("Title: " + achievement['title'])
            print("Description: " + achievement["description"])
            is_planned = achievement['levels'][4]['is_planned']
            is_planned = 1
            is_completed = achievement['levels'][4]['is_completed']
            is_completed = 1
            achievement['levels'][4]['is_planned'] = is_planned
            achievement['levels'][4]['is_completed'] = is_completed

with open('./Test Files/achievements.json','w') as achievements:
    json.dump(achievement_dict, achievements, indent=2)
                
  