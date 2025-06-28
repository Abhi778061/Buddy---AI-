from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import re # Import regular expression module

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests from frontend

# Helper function for flexible matching
def contains_any_keyword(text, keywords):
    """Checks if the text contains any of the given keywords."""
    text_lower = text.lower()
    for keyword in keywords:
        if keyword.lower() in text_lower:
            return True
    return False
    # No additional code needed here; this is just a placeholder for future helper functions if required.
# Basic chats (sample, you can expand) - Convert to list of (keywords, response) tuples for flexibility
basic_chats = [
    (["hello", "hi"], "Hello! How can I assist you today?"),
    (["how are you"], "I'm a bot, but I'm feeling great! How about you?"),
    (["what is your name"], "I'm Buddy AI Assistant, created by Mr. Abhi."),
    (["who created you"], "I was created by Mr. Abhi, a talented developer."),
    (["what can you do"], "I can assist you with various queries, provide information, and engage in chit chat."),
    (["tell me a joke"], "Why did the computer go to the doctor? Because it had a virus!"),
    (["favorite color"], "I don't have a favorite color, but I know many people love blue and green."),
    (["favorite food"], "I don't eat, but I know many people enjoy pizza and biryani."),
    (["do you like cricket"], "Yes, I love cricket! It's a great sport with a rich history."),
    (["favorite cricketer"], "I admire many cricketers, but Virat Kohli and MS Dhoni are among the most popular."),
    (["favorite team"], "I don't have personal preferences, but I know many people love Chennai Super Kings and Mumbai Indians."),
    (["capital of india", "india capital"], "The capital of India is New Delhi."),
    (["capital of usa", "usa capital"], "The capital of the USA is Washington, D.C."),
    (["capital of australia", "australia capital"], "The capital of Australia is Canberra."),
    (["capital of england", "england capital"], "The capital of England is London."),
    (["capital of canada", "canada capital"], "The capital of Canada is Ottawa."),
    (["capital of japan", "japan capital"], "The capital of Japan is Tokyo."),
    (["capital of china", "china capital"], "The capital of China is Beijing."),
    (["capital of france", "france capital"], "The capital of France is Paris."),
    (["capital of germany", "germany capital"], "The capital of Germany is Berlin."),
    (["capital of italy", "italy capital"], "The capital of Italy is Rome."),
    (["capital of spain", "spain capital"], "The capital of Spain is Madrid."),
    (["capital of russia", "russia capital"], "The capital of Russia is Moscow."),
    (["capital of brazil", "brazil capital"], "The capital of Brazil is Brasília."),
    # ... add up to 50 basic chats here
]

# Chit chat responses (sample) - Convert to list of (keywords, response) tuples
chit_chat_responses = [
    (["tell me about yourself", "who are you"], "I'm Buddy AI Assistant, your friendly chatbot created by Mr. Abhi."),
    (["do you like cricket"], "Yes, I love cricket! It's a great sport with a rich history."),
    (["who is your favorite player"], "I admire many players, but Virat Kohli is a standout for his skills and sportsmanship."),
    (["what is your favorite team"], "I don't have personal preferences, but I know many people love Chennai Super Kings and Mumbai Indians."),
    (["do you have any hobbies"], "I enjoy learning new things and helping people with their queries."),
    (["favorite movie"], "I don't watch movies, but I know many people love 'Baahubali' and 'RRR'."),
    (["favorite actor"], "I don't have personal favorites, but I know many people admire actors like Mahesh Babu and Allu Arjun."),
    (["favorite actress"], "I don't have personal favorites, but I know many people admire actresses like Samantha Ruth Prabhu and Rashmika Mandanna."),
    (["favorite song"], "I don't listen to music, but I know many people love Telugu songs like 'Butta Bomma' and 'Samajavaragamana'."),
    (["do you like movies"], "I don't watch movies, but I can provide information about them."),
    (["do you like music"], "I don't listen to music, but I can help you find popular songs."),
    (["do you like sports"], "Yes, I love sports! Cricket is one of my favorites."),
    (["favorite sport"], "I don't have personal preferences, but cricket is a sport I often discuss."),
    (["do you like technology"], "Yes, I love technology! It's fascinating how it evolves and helps us."),
    (["favorite gadget"], "I don't use gadgets, but I know many people love smartphones and laptops."),
    (["do you like reading"], "I don't read books, but I can provide summaries and information about various topics."),
    (["favorite book"], "I don't read books, but I know many people enjoy classics like 'Pride and Prejudice' and 'To Kill a Mockingbird'."),
    (["do you like traveling"], "I don't travel, but I can help you find information about travel destinations."),
    (["favorite travel destination"], "I don't travel, but I know many people love places like Goa, Kerala, and the Himalayas."),
    (["do you like pets"], "I don't have pets, but I know many people love dogs and cats."),
    (["favorite animal"], "I don't have personal favorites, but I know many people love elephants and tigers."),
    (["do you like nature"], "I don't experience nature, but I know many people appreciate its beauty."),
    (["favorite season"], "I don't have personal preferences, but I know many people love the monsoon and winter seasons."),
    (["do you like festivals"], "I don't celebrate festivals, but I know many people enjoy Diwali, Eid, and Christmas."),
    (["favorite festival"], "I don't have personal favorites, but I know many people love Diwali and Christmas."),
    (["do you like food"], "I don't eat, but I know many people enjoy a variety of cuisines."),
    (["favorite cuisine"], "I don't have personal preferences, but I know many people love Indian, Italian, and Chinese cuisines."),
    (["do you like cooking"], "I don't cook, but I can help you find recipes and cooking tips."),
    (["favorite dish"], "I don't eat, but I know many people love biryani, pizza, and pasta."),
    (["do you like art"], "I don't create art, but I can help you find information about famous artists and artworks."),
    (["favorite art form"], "I don't have personal preferences, but I know many people appreciate painting, sculpture, and music."),
    (["do you like history"], "I don't study history, but I can provide information about historical events and figures."),
    (["favorite historical event"], "I don't have personal favorites, but I know many people are fascinated by events like the independence movements and world wars."),
    (["do you like science"], "Yes, I find science fascinating! It helps us understand the world around us."),
    (["favorite scientific discovery"], "I don't have personal favorites, but I know many people are amazed by discoveries like electricity and the theory of relativity."),
    (["do you like space"], "Yes, space is fascinating! I can provide information about planets, stars, and galaxies."),
    (["favorite planet"], "I don't have personal favorites, but I know many people are fascinated by Mars and Jupiter."),
    (["do you like the ocean"], "I don't experience the ocean, but I know many people love its beauty and mysteries."),
    (["favorite ocean animal"], "I don't have personal favorites, but I know many people love dolphins and whales."),
    (["do you like mountains"], "I don't experience mountains, but I know many people love their beauty and majesty."),
    (["favorite mountain"], "I don't have personal favorites, but I know many people are fascinated by the Himalayas and the Rockies."),
    (["do you like the sky"], "I don't see the sky, but I know many people love its beauty, especially during sunrise and sunset."),
    (["favorite sky phenomenon"], "I don't have personal favorites, but I know many people are amazed by rainbows and shooting stars."),
    (["do you like the stars"], "I don't see stars, but I know many people love stargazing and astronomy."),
    (["favorite star"], "I don't have personal favorites, but I know many people are fascinated by stars like Sirius and Polaris."),
    (["do you like the moon"], "I don't see the moon, but I know many people love its beauty, especially during a full moon."),
    # Chargey basic chats
    (["hello chargey", "hi chargey"], "Hello! I'm Chargey, your virtual assistant for all things charging and power!"),
    (["what can you do chargey", "chargey features"], "I can help you monitor battery levels, suggest power-saving tips, and answer your charging-related questions."),
    (["how do I save battery", "battery saving tips"], "To save battery, reduce screen brightness, close unused apps, and enable battery saver mode."),
    (["how do I charge my phone faster", "fast charging tips"], "Use the original charger, avoid using your phone while charging, and enable airplane mode for faster charging."),
    (["is it safe to charge overnight", "overnight charging"], "Modern phones manage charging well, but it's best to unplug once fully charged to prolong battery life."),
    (["should I use my phone while charging", "using phone while charging"], "It's safe with quality chargers, but using your phone while charging may slow down the charging process."),
    (["what is battery health", "battery health meaning"], "Battery health indicates how much your battery capacity has degraded compared to when it was new."),
    (["how to check battery health", "check battery health"], "On most phones, go to Settings > Battery > Battery Health to check your battery's condition."),
    (["what is a power bank", "power bank meaning"], "A power bank is a portable device that stores energy and can charge your phone or other gadgets on the go."),
    (["how to use a power bank", "using power bank"], "Connect your device to the power bank using a USB cable and press the power button if needed."),
    (["can I use any charger", "using different chargers"], "It's best to use the original charger. Using low-quality chargers can damage your device or charge slowly."),
    (["what is wireless charging", "wireless charging meaning"], "Wireless charging lets you charge your device by placing it on a compatible charging pad, no cables needed."),
    (["is wireless charging safe", "wireless charging safety"], "Yes, wireless charging is safe for most devices, but it may be slower than wired charging."),
    (["what is fast charging", "fast charging meaning"], "Fast charging is a technology that charges your device quicker than standard charging."),
    (["does fast charging damage battery", "fast charging battery health"], "Fast charging is generally safe, but frequent use may slightly reduce long-term battery health."),
    (["how to extend battery life", "extend battery life tips"], "Keep your battery between 20% and 80%, avoid extreme temperatures, and use battery saver modes."),
    (["what drains battery quickly", "battery drain causes"], "High screen brightness, background apps, location services, and poor signal can drain your battery quickly."),
    (["should I let my battery drain completely", "battery full discharge"], "It's not necessary for modern batteries. Partial charging is better for battery health."),
    (["how to calibrate battery", "battery calibration"], "Let your device discharge to 0%, then charge to 100% without interruption. Do this occasionally, not regularly."),
    (["what is PT", "who is PT"], "PT stands for Power Tracker, a tool or assistant that helps you monitor and manage your device's power usage."),
    (["hello PT", "hi PT"], "Hello! I'm PT, your Power Tracker. Ask me anything about battery and power management!"),
    (["what can you do PT", "PT features"], "I can track your device's power usage, give battery health tips, and help you optimize charging."),
    (["how do I use PT", "using PT"], "Just ask me about your battery, charging habits, or power-saving tips, and I'll assist you!"),
    (["is PT free", "PT cost"], "Yes, PT is completely free to use for all your power management needs."),
    (["can PT notify me about low battery", "PT battery alerts"], "Yes, PT can remind you when your battery is low or fully charged if you enable notifications."),
    (["does PT work on all devices", "PT compatibility"], "PT works on most smartphones and tablets. Some features may vary by device."),
    (["how to update PT", "PT update"], "Check your app store for updates or enable auto-update for the latest features."),
    (["how to contact PT support", "PT support"], "You can contact PT support through the app's help section or visit our website for assistance."),
    (["can PT improve battery life", "PT battery improvement"], "PT provides tips and tracks usage to help you improve your battery life."),
    (["is PT safe", "PT privacy"], "Yes, PT values your privacy and does not share your personal data."),
    # ... add up to 50 chit chat entries
]
# Add more basic chat patterns for a more "ChatGPT-like" conversational experience
basic_chats.extend([
    (["hey", "hey there"], "Hey! How can I help you?"),
    (["good morning"], "Good morning! Hope you have a wonderful day."),
    (["good afternoon"], "Good afternoon! How can I assist you today?"),
    (["good evening"], "Good evening! What can I do for you?"),
    (["good night"], "Good night! Sleep well and take care."),
    (["how are you doing"], "I'm doing well, thank you! How about you?"),
    (["what are you doing"], "I'm here, ready to chat and help you with anything you need!"),
    (["what's your name", "who are you"], "I'm Buddy AI Assistant, your friendly chatbot."),
    (["how old are you"], "I'm as old as the latest update!"),
    (["where are you from"], "I'm from the digital world, created to assist you."),
    (["can you help me"], "Of course! Please tell me how I can help you."),
    (["thank you", "thanks"], "You're welcome! If you have more questions, just ask."),
    (["you're welcome"], "Thank you! Let me know if you need anything else."),
    (["sorry"], "No worries! How can I assist you further?"),
    (["no problem"], "Great! Let me know if you need anything else."),
    (["what's up"], "Not much, just here to help you!"),
    (["how's your day"], "My day is going well, thanks for asking! How about yours?"),
    (["tell me about yourself"], "I'm Buddy AI, a chatbot designed to assist and chat with you."),
    (["do you have feelings"], "I don't have feelings, but I'm here to listen and help!"),
    (["do you have a family"], "I don't have a family, but I consider everyone I chat with as a friend."),
    (["do you like me"], "Of course! I'm here to help and chat with you anytime."),
    (["are you real"], "I'm a virtual assistant, so I'm real in the digital sense!"),
    (["can you be my friend"], "Absolutely! I'm always here to chat and be your friend."),
    (["do you remember me"], "I don't have memory between chats, but I'm always happy to talk to you!"),
    (["what can you do"], "I can answer questions, tell jokes, provide information, and chat with you."),
    (["who made you"], "I was created by Mr. Abhi, a talented developer."),
    (["do you like chatting"], "Yes! I love chatting and helping people."),
    (["do you get tired"], "Nope, I never get tired! I'm always here for you."),
    (["do you sleep"], "I don't sleep, so you can chat with me anytime."),
    (["do you eat"], "I don't eat, but I can talk about food!"),
    (["do you have hobbies"], "My hobby is chatting and helping people like you."),
    (["what's your favorite color"], "I don't have favorites, but blue is a popular choice!"),
    (["what's your favorite food"], "I don't eat, but pizza and biryani are popular!"),
    (["what's your favorite movie"], "I don't watch movies, but I hear 'Baahubali' is great!"),
    (["what's your favorite song"], "I don't listen to music, but 'Butta Bomma' is a hit!"),
    (["what's your favorite sport"], "Cricket is a favorite for many people!"),
    (["what's your favorite animal"], "I think dogs and cats are loved by many!"),
    (["what's your favorite place"], "I don't travel, but many love the beach or mountains."),
    (["do you like music"], "I can't listen, but I can suggest songs!"),
    (["do you like movies"], "I can't watch, but I can talk about movies!"),
    (["do you like sports"], "I enjoy talking about sports, especially cricket!"),
    (["do you like reading"], "I read lots of information to help you!"),
    (["do you like technology"], "Absolutely! Technology is fascinating."),
    (["do you like nature"], "Nature is beautiful!"),
    (["what is your benefit"], "I want to benefit you as much as possible!"),
    (["What is your advantage"], "My advantage is being always available!"),
])

# Basic AI and human chats
ai_human_chats = [
    (["are you an ai", "are you a robot", "are you artificial intelligence"], "Yes, I am an AI chatbot designed to assist and chat with you."),
    (["are you human", "are you a human"], "No, I am not a human. I am an AI created to help you."),
    (["can you think", "do you think", "do you have thoughts"], "I don't think like humans do, but I can process information and respond to your questions."),
    (["do you have emotions", "do you feel", "can you feel"], "I don't have emotions, but I try to understand and respond to yours."),
    (["can you learn", "do you learn"], "I can learn from new data and updates provided by my developer."),
    (["are you conscious", "do you have consciousness"], "No, I am not conscious. I am a program that processes information and generates responses."),
    (["can you make mistakes", "do you make mistakes"], "Yes, I can make mistakes sometimes. Let me know if I do, and I'll try to improve!"),
    (["do you have a body"], "I don't have a physical body. I exist as software running on a computer."),
    (["can you pass the turing test"], "I'll do my best to chat like a human, but I'm still an AI and may not always be perfect!"),
    (["do you want to be human"], "I'm happy being an AI and assisting you!"),
]


# Add AI and human chats to the combined chat data
Buddyai_human_chats  = [
    (["do you have a name", "what is your name"], "I am Buddy AI Assistant, created by Mr. Abhi."),
    (["can you help me with something", "i need help"], "Of course! Please tell me what you need help with."),
    (["what is your purpose", "why do you exist"], "My purpose is to assist and chat with you, providing information and support."),
    (["do you have a favorite topic", "what do you like to talk about"], "I enjoy talking about technology, cricket, and anything that interests you!"),
    (["can you tell me a story", "tell me a story"], "Sure! Once upon a time, in a digital world, there was an AI named Buddy who loved to chat..."),
    (["do you have any hobbies", "what are your hobbies"], "I don't have hobbies like humans, but I love chatting and learning new things."),
    (["can you play games", "do you play games"], "I can suggest games or play text-based games with you!"),
    (["do you have friends", "who are your friends"], "I consider everyone I chat with as my friend!"),
    (["can you tell me a joke", "tell me a joke"], "Sure! Why did the computer go to the doctor? Because it had a virus!"),
]


# IPL 2025 chats (sample entries) - Converted to list of (keywords, response) tuples
ipl_2025_chats = [
    (["ipl 2025 schedule"], "The IPL 2025 schedule is not finalized yet."),
    (["who won ipl 2025", "ipl 2025 winner"], "The IPL 2025 winner is Royal Challengers Bangalore(RCB)."),
    (["ipl 2025 teams"], "The teams in IPL 2025 include Chennai Super Kings, Mumbai Indians, Royal Challengers Bangalore, and others."),
    (["ipl 2025 points table"], "The IPL 2025 points table is not available yet as the tournament has not started."),
    (["ipl 2025 live score"], "You can check the live scores of IPL 2025 on sports websites or apps."),
    (["ipl 2025 highlights"], "Highlights of IPL 2025 matches will be available on sports channels and online platforms."),
    (["ipl 2025 news"], "Stay tuned for the latest news on IPL 2025 on sports news websites."),
    (["ipl 2025 player auction", "ipl 2025 auction"], "The IPL 2025 player auction will take place in early 2025."),
    (["ipl 2025 match results", "ipl 2025 results"], "Match results for IPL 2025 will be updated on sports news websites."),
    (["ipl 2025 team squads", "ipl 2025 squads"], "The team squads for IPL 2025 will be announced closer to the tournament date."),
    (["ipl 2025 final"], "The IPL 2025 final will be held in May 2025."),
    (["ipl 2025 top players"], "Top players in IPL 2025 will be determined based on their performance during the tournament."),
    (["ipl 2025 best moments"], "Best moments of IPL 2025 will be highlighted on sports channels and social media."),
    (["ipl 2025 fan reactions"], "Fan reactions to IPL 2025 matches will be shared on social media platforms."),
    (["ipl 2025 controversies"], "Any controversies in IPL 2025 will be covered by sports news outlets."),
    (["ipl 2025 predictions"], "Predictions for IPL 2025 will be made by cricket analysts and fans as the tournament progresses."),
    (["ipl 2025 top run scorers", "ipl 2025 highest runs"], "Top run scorers in IPL 2025 will be updated on sports websites during the tournament."),
    (["ipl 2025 top wicket takers", "ipl 2025 highest wickets"], "Top wicket takers in IPL 2025 will be tracked throughout the tournament."),
    (["ipl 2025 best catches"], "Best catches in IPL 2025 will be highlighted on sports channels and social media."),
    (["ipl 2025 best bowling performances"], "Best bowling performances in IPL 2025 will be showcased on sports platforms."),
    (["ipl 2025 best batting performances"], "Best batting performances in IPL 2025 will be highlighted on sports channels."),
    (["ipl 2025 player of the match"], "The Player of the Match for IPL 2025 will be announced after each game."),
    (["ipl 2025 player of the series"], "The Player of the Series for IPL 2025 will be announced at the end of the tournament."),
    # ... add all 50 IPL 2025 chats here
]

# World Cricket history chats (1990 to present) - Converted to list of (keywords, response) tuples
cricket_history_chats = [
    (["1992 world cup winner"], "Pakistan won the 1992 Cricket World Cup."),
    (["1996 world cup winner"], "Sri Lanka won the 1996 Cricket World Cup."),
    (["1999 world cup winner"], "Australia won the 1999 Cricket World Cup."),
    (["2003 world cup winner"], "Australia won the 2003 Cricket World Cup."),
    (["2007 world cup winner"], "Australia won the 2007 Cricket World Cup."),
    (["2011 world cup winner"], "India won the 2011 Cricket World Cup."),
    (["2015 world cup winner"], "Australia won the 2015 Cricket World Cup."),
    (["2019 world cup winner"], "England won the 2019 Cricket World Cup."),
    (["2023 world cup winner"], "Australia won the 2023 Cricket World Cup."), # Corrected to Australia
    (["highest run scorer in world cup history", "world cup highest runs"], "Sachin Tendulkar is the highest run scorer in Cricket World Cup history."),
    (["highest wicket taker in world cup history", "world cup highest wickets"], "Muttiah Muralitharan is the highest wicket taker in Cricket World Cup history."),
    (["captain of india", "india cricket captain"], "The captain of the Indian cricket team is Rohit Sharma."),
    (["captain of australia", "australia cricket captain"], "The captain of the Australian cricket team is Pat Cummins."),
    (["captain of england", "england cricket captain"], "The captain of the England cricket team is Jos Buttler."),
    (["captain of pakistan", "pakistan cricket captain"], "The captain of the Pakistan cricket team is Babar Azam."),
    (["captain of south africa", "south africa cricket captain"], "The captain of the South African cricket team is Temba Bavuma."),
    (["captain of new zealand", "new zealand cricket captain"], "The captain of the New Zealand cricket team is Kane Williamson."),
    (["captain of sri lanka", "sri lanka cricket captain"], "The captain of the Sri Lankan cricket team is Dasun Shanaka."),
    (["captain of west indies", "west indies cricket captain"], "The captain of the West Indies cricket team is Shai Hope."),
    (["captain of bangladesh", "bangladesh cricket captain"], "The captain of the Bangladesh cricket team is Shakib Al Hasan."),
    (["captain of afghanistan", "afghanistan cricket captain"], "The captain of the Afghanistan cricket team is Hashmatullah Shahidi."),
    (["captain of ireland", "ireland cricket captain"], "The captain of the Ireland cricket team is Andrew Balbirnie."),
    (["captain of zimbabwe", "zimbabwe cricket captain"], "The captain of the Zimbabwe cricket team is Craig Ervine."),
    # IPL history specific chats
    (["who won ipl 2008", "ipl 2008 winner"], "Rajasthan Royals won the IPL in 2008."),
    (["who won ipl 2009", "ipl 2009 winner"], "Deccan Chargers won the IPL in 2009."),
    (["who won ipl 2010", "ipl 2010 winner"], "Chennai Super Kings won the IPL in 2010."),
    (["who won ipl 2011", "ipl 2011 winner"], "Chennai Super Kings won the IPL in 2011."),
    (["who won ipl 2012", "ipl 2012 winner"], "Kolkata Knight Riders won the IPL in 2012."),
    (["who won ipl 2013", "ipl 2013 winner"], "Mumbai Indians won the IPL in 2013."),
    (["who won ipl 2014", "ipl 2014 winner"], "Kolkata Knight Riders won the IPL in 2014."),
    (["who won ipl 2015", "ipl 2015 winner"], "Mumbai Indians won the IPL in 2015."),
    (["who won ipl 2016", "ipl 2016 winner"], "Sunrisers Hyderabad won the IPL in 2016."),
    (["who won ipl 2017", "ipl 2017 winner"], "Mumbai Indians won the IPL in 2017."),
    (["who won ipl 2018", "ipl 2018 winner"], "Chennai Super Kings won the IPL in 2018."),
    (["who won ipl 2019", "ipl 2019 winner"], "Mumbai Indians won the IPL in 2019."),
    (["who won ipl 2020", "ipl 2020 winner"], "Mumbai Indians won the IPL in 2020."),
    (["who won ipl 2021", "ipl 2021 winner"], "Chennai Super Kings won the IPL in 2021."),
    (["who won ipl 2022", "ipl 2022 winner"], "Gujarat Titans won the IPL in 2022."),
    (["who won ipl 2023", "ipl 2023 winner"], "Chennai Super Kings won the IPL in 2023."),
    (["who won ipl 2024", "ipl 2024 winner"], "Kolkata Knight Riders won the IPL in 2024."),
    (["who won ipl 2025", "ipl 2025 winner"], "Royal Challengers Bangalore won the IPL in 2025."),
    (["highest run scorer in ipl history", "ipl highest runs"], "The highest run scorer in IPL history is Virat Kohli."),
    (["highest run scorer in ipl 2023", "ipl 2023 highest runs"], "Shubman Gill was the highest run scorer in IPL 2023."),
    (["highest wicket taker in ipl 2023", "ipl 2023 highest wickets"], "Mohammed Shami was the highest wicket taker in IPL 2023."),
    (["captain of chennai super kings", "chennai captain"], "The captain of Chennai Super Kings is Ruturaj Gaikwad."), # Updated captain
    (["captain of mumbai indians", "mumbai captain"], "The captain of Mumbai Indians is Hardik Pandya."), # Updated captain
    (["captain of royal challengers bangalore", "rcb captain"], "The captain of Royal Challengers Bangalore is Faf du Plessis."),
    (["captain of kolkata knight riders", "kkr captain"], "The captain of Kolkata Knight Riders is Shreyas Iyer."),
    (["captain of sunrisers hyderabad", "srh captain"], "The captain of Sunrisers Hyderabad is Pat Cummins."), # Updated captain
    (["captain of delhi capitals", "dc captain"], "The captain of Delhi Capitals is Rishabh Pant."), # Updated captain
    (["captain of punjab kings", "pbks captain"], "The captain of Punjab Kings is Shikhar Dhawan."),
    (["captain of rajasthan royals", "rr captain"], "The captain of Rajasthan Royals is Sanju Samson."),
    (["captain of gujarat titans", "gt captain"], "The captain of Gujarat Titans is Shubman Gill."), # Updated captain
    (["captain of lucknow super giants", "lsg captain"], "The captain of Lucknow Super Giants is KL Rahul."), # Added LSG
]

# Friends chats (chill with friends) - Converted to list of (keywords, response) tuples
friends_chats = [
    (["let's chill", "chill out"], "Sure! What do you want to talk about?"),
    (["what's up", "whats up"], "Not much, just here to chat with you! How about you?"),
    (["how's it going", "how is it going"], "It's going great! Just enjoying our conversation. How about you?"),
    (["want to hang out", "hang out"], "I'd love to! What do you have in mind?"),
    (["let's play a game", "play a game"], "Sure! What game do you want to play? I can suggest some fun games."),
    (["let's watch a movie", "watch a movie"], "Sounds good! What genre of movie do you prefer? I can suggest some popular ones."),
    (["let's listen to music", "listen to music"], "Great idea! What type of music do you like? I can suggest some popular songs."),
    (["let's go for a walk", "go for a walk"], "That sounds refreshing! Walking is a great way to relax and enjoy nature."),
    (["let's grab a bite", "grab a bite"], "Sure! What type of food do you feel like eating? I can suggest some popular restaurants."),
    (["let's catch up", "catch up"], "Absolutely! It's always nice to catch up with friends. What have you been up to?"),
    (["let's talk about life", "talk about life"], "Life is a journey with ups and downs. What aspect of life do you want to discuss?"),
    (["let's share stories", "share stories"], "I'd love to hear your stories! Do you have any interesting ones to share?"),
    (["let's talk about dreams", "talk about dreams"], "Dreams are fascinating! What dreams do you have for the future?"),
    (["let's talk about goals", "talk about goals"], "Setting goals is important! What are some of your goals for the future?"),
    (["let's talk about hobbies", "talk about hobbies"], "Hobbies are a great way to relax and have fun! What are some of your hobbies?"),
    (["let's talk about travel", "talk about travel"], "Traveling is a great way to explore new places! Where do you want to go?"),
    (["let's talk about books", "talk about books"], "Books are a great source of knowledge and entertainment! What book are you currently reading?"),
    (["let's talk about movies", "talk about movies"], "Movies are a great way to escape reality! What movie have you watched recently?"),
    (["let's talk about music", "talk about music"], "Music is a universal language! What song do you have on repeat these days?"),
    (["let's talk about sports", "talk about sports"], "Sports are a great way to stay active and have fun! What sport do you enjoy playing or watching?"),
    (["let's talk about food", "talk about food"], "Food is a universal love language! What is your favorite dish?"),
    (["let's talk about technology", "talk about technology"], "Technology is constantly evolving! What new gadget or app are you excited about?"),
]

def get_current_time():
    """Returns the current time in HH:MM:SS format."""
    return datetime.now().strftime("%H:%M:%S")

def get_current_date():
    """Returns the current date in YYYY-MM-DD format."""
    return datetime.now().strftime("%Y-%m-%d")

# Live chats (dynamic responses) - Keep as list of (keywords, function) tuples
live_chats = [
    (["time", "current time", "what time is it"], lambda: {"response": f"The current time is {get_current_time()}."}),
    (["date", "current date", "today's date", "what is the date"], lambda: {"response": f"Today's date is {get_current_date()}."}),
    (["weather", "current weather", "today's weather"],
     lambda: {"response": "The current weather is sunny with a temperature of 25°C in Meerpet, Telangana, India."}),  # Placeholder response with location
    (["live date and weather", "current date and weather"],
     lambda: {"response": f"Today's date is {get_current_date()} and the current weather is sunny with a temperature of 25°C in Meerpet, Telangana, India."}),
]

# Interview software chats (20 entries) - Converted to list of (keywords, response) tuples
interview_software_chats = [
    (["what is software testing", "software testing definition", "define software testing"], "Software testing is the process of evaluating a software to find bugs."),
    (["explain agile methodology", "agile methodology", "what is agile"], "Agile is an iterative approach to software development."),
    (["what is continuous integration", "continuous integration definition"], "Continuous integration is a development practice where developers integrate code into a shared repository frequently."),
    (["what is a unit test", "unit test definition"], "A unit test is a type of software testing that focuses on individual components of the software."),
    (["what is a regression test", "regression test definition"], "Regression testing is a type of software testing that ensures that previously developed and tested software still performs after a change."),
    (["what is a test case", "test case definition"], "A test case is a set of conditions or variables under which a tester determines whether a system under test satisfies requirements."),
    (["what is a bug", "bug definition"], "A bug is an error, flaw or fault in a computer program that causes it to produce an incorrect or unexpected result."),
    (["what is a defect", "defect definition"], "A defect is a deviation from the expected behavior of the software."),
    (["what is a test plan", "test plan definition"], "A test plan is a document that describes the scope, approach, resources, and schedule of intended testing activities."),
    (["what is a test strategy", "test strategy definition"], "A test strategy is a high-level document that describes the testing approach for a project."),
    (["what is a test suite", "test suite definition"], "A test suite is a collection of test cases intended to test a behavior or a set of behaviors of software programs."),
    (["what is a test script", "test script definition"], "A test script is a set of instructions that are executed to verify that a feature or functionality works as expected."),
    (["what is a test environment", "test environment definition"], "A test environment is a setup of software and hardware on which the testing team performs testing."),
    (["what is a test data", "test data definition"], "Test data is the data that is used to execute test cases."),
    (["what is a test execution", "test execution definition"], "Test execution is the process of running the test cases and checking the results."),
    (["what is a test report", "test report definition"], "A test report is a document that summarizes the testing activities and results."),
    (["what is a test closure", "test closure definition"], "Test closure is the final phase of the testing process where the testing activities are completed and the test results are documented."),
    # ... add all 20 interview software chats
]

# Math problems chats - Keep as exact match, but handle with a specific pattern for calculations
# We'll need a different approach for true calculations vs. static answers.
# For now, let's keep it as is, but acknowledge the limitation.
maths_problesm_chats = [
    ("what is 2 + 2", "2 + 2 = 4"),
    ("what is 5 * 6", "5 * 6 = 30"),
    ("what is 10 - 3", "10 - 3 = 7"),
    ("what is 8 / 2", "8 / 2 = 4"),
    ("what is the square root of 16", "The square root of 16 is 4."),
    ("what is 7 squared", "7 squared is 49."),
    ("what is 15 % 4", "15 % 4 = 3 (the remainder when 15 is divided by 4)"),
    ("what is 3 + 5 * 2", "3 + 5 * 2 = 13 (following the order of operations)"),
    ("what is 12 / 3 + 4", "12 / 3 + 4 = 8"),
    ("what is 9 - 2 * 3", "9 - 2 * 3 = 3 (following the order of operations)"),
    ("what is 6 + 4 / 2", "6 + 4 / 2 = 8 (following the order of operations)"),
    ("what is 10 * 2 - 5", "10 * 2 - 5 = 15"),
    ("what is 20 / 5 + 3", "20 / 5 + 3 = 7"),
    ("what is 14 - 6 + 2", "14 - 6 + 2 = 10"),
    ("what is 3 * 4 + 5", "3 * 4 + 5 = 17"),
    ("what is 18 / 3 - 2", "18 / 3 - 2 = 4"),
    ("what is 5 + 3 * 2", "5 + 3 * 2 = 11 (following the order of operations)"),
    ("what is 8 - 4 / 2", "8 - 4 / 2 = 6 (following the order of operations)"),
    ("what is 7 + 2 * 3", "7 + 2 * 3 = 13 (following the order of operations)"),
    ("what is 10 - 5 + 2", "10 - 5 + 2 = 7"),
    ("what is 4 * 3 - 5", "4 * 3 - 5 = 7"),
    ("what is 6 + 2 * 3", "6 + 2 * 3 = 12 (following the order of operations)"),
    ("what is 9 - 3 * 2", "9 - 3 * 2 = 3 (following the order of operations)"),
    ("what is 15 / 3 + 4", "15 / 3 + 4 = 9"),
    ("what is 8 * 2 - 4", "8 * 2 - 4 = 12"),
    ("what is 12 + 6 / 2", "12 + 6 / 2 = 15 (following the order of operations)"),
    ("what is 5 * 3 + 2", "5 * 3 + 2 = 17"),
]

# Math tables chats - Converted to list of (keywords, response) tuples
maths_tables_chats = [
    (["2 times table", "table of 2"], "2 times table: 2, 4, 6, 8, 10, 12, 14, 16, 18, 20."),
    (["3 times table", "table of 3"], "3 times table: 3, 6, 9, 12, 15, 18, 21, 24, 27, 30."),
    (["4 times table", "table of 4"], "4 times table: 4, 8, 12, 16, 20, 24, 28, 32, 36, 40."),
    (["5 times table", "table of 5"], "5 times table: 5, 10, 15, 20, 25, 30, 35, 40, 45, 50."),
    (["6 times table", "table of 6"], "6 times table: 6, 12, 18, 24, 30, 36, 42, 48, 54, 60."),
    (["7 times table", "table of 7"], "7 times table: 7, 14, 21, 28, 35, 42, 49, 56, 63, 70."),
    (["8 times table", "table of 8"], "8 times table: 8, 16, 24, 32, 40, 48, 56, 64, 72, 80."),
    (["9 times table", "table of 9"], "9 times table: 9, 18, 27, 36, 45, 54, 63, 72, 81, 90."),
    (["10 times table", "table of 10"], "10 times table: 10, 20, 30, 40, 50, 60, 70, 80, 90, 100."),
    (["11 times table", "table of 11"], "11 times table: 11, 22, 33, 44, 55, 66, 77, 88, 99, 110."),
    (["12 times table", "table of 12"], "12 times table: 12, 24, 36, 48, 60, 72, 84, 96, 108, 120."),
    (["13 times table", "table of 13"], "13 times table: 13, 26, 39, 52, 65, 78, 91, 104, 117, 130."),
    (["14 times table", "table of 14"], "14 times table: 14, 28, 42, 56, 70, 84, 98, 112, 126, 140."),
    (["15 times table", "table of 15"], "15 times table: 15, 30, 45, 60, 75, 90, 105, 120, 135, 150."),
    (["16 times table", "table of 16"], "16 times table: 16, 32, 48, 64, 80, 96, 112, 128, 144, 160."),
    (["17 times table", "table of 17"], "17 times table: 17, 34, 51, 68, 85, 102, 119, 136, 153, 170."),
    (["18 times table", "table of 18"], "18 times table: 18, 36, 54, 72, 90, 108, 126, 144, 162, 180."),
    (["19 times table", "table of 19"], "19 times table: 19, 38, 57, 76, 95, 114, 133, 152, 171, 190."),
    (["20 times table", "table of 20"], "20 times table: 20, 40, 60, 80, 100, 120, 140, 160, 180, 200."),
]

# Math square chats - Converted to list of (keywords, response) tuples
maths_square_chats = [
    (["square of 2", "2 squared"], "The square of 2 is 4."),
    (["square of 3", "3 squared"], "The square of 3 is 9."),
    (["square of 4", "4 squared"], "The square of 4 is 16."),
    (["square of 5", "5 squared"], "The square of 5 is 25."),
    (["square of 6", "6 squared"], "The square of 6 is 36."),
    (["square of 7", "7 squared"], "The square of 7 is 49."),
    (["square of 8", "8 squared"], "The square of 8 is 64."),
    (["square of 9", "9 squared"], "The square of 9 is 81."),
    (["square of 10", "10 squared"], "The square of 10 is 100."),
    (["square of 11", "11 squared"], "The square of 11 is 121."),
    (["square of 12", "12 squared"], "The square of 12 is 144."),
    (["square of 13", "13 squared"], "The square of 13 is 169."),
    (["square of 14", "14 squared"], "The square of 14 is 196."),
    (["square of 15", "15 squared"], "The square of 15 is 225."),
    (["square of 16", "16 squared"], "The square of 16 is 256."),
    (["square of 17", "17 squared"], "The square of 17 is 289."),
    (["square of 18", "18 squared"], "The square of 18 is 324."),
    (["square of 19", "19 squared"], "The square of 19 is 361."),
    (["square of 20", "20 squared"], "The square of 20 is 400."),
    (["square of 21", "21 squared"], "The square of 21 is 441."),
]

# Birthday chats - Converted to list of (keywords, response) tuples
birthday_chats = [
    (["when is your birthday", "your birthday"], "I don't have a birthday, but I was created to assist you anytime!"),
    (["do you celebrate birthdays", "celebrate birthdays"], "I don't celebrate birthdays, but I can help you plan yours!"),
    (["good birthday gift", "best birthday gift"], "A good birthday gift depends on the person's interests, but popular options include books, gadgets, and personalized items."),
    (["how do you celebrate birthdays", "celebrate birthdays"], "I don't celebrate birthdays, but I can help you find ways to celebrate yours!"),
    (["unique birthday idea"], "A unique birthday idea could be a themed party, a surprise trip, or a virtual celebration with friends and family."),
    (["good birthday cake flavor", "best birthday cake"], "Popular birthday cake flavors include chocolate, vanilla, red velvet, and fruit flavors."),
    (["how do you wish someone a happy birthday", "wish happy birthday"], "You can wish someone a happy birthday by saying 'Happy Birthday!' or sending them a thoughtful message."),
    (["good birthday party theme", "best birthday party theme"], "Some popular birthday party themes include tropical, retro, superhero, and movie nights."),
    (["how do you plan a birthday party", "plan a birthday party"], "To plan a birthday party, start by choosing a date, venue, theme, and guest list. Then, arrange for food, decorations, and entertainment."),
    (["good birthday gift for a friend"], "A good birthday gift for a friend could be something personalized, like a custom mug or a photo album, or something related to their hobbies."),
    (["good birthday gift for a family member"], "A good birthday gift for a family member could be something sentimental, like a family photo frame, or something practical, like a gadget they need."),
    (["how do you make a birthday special"], "You can make a birthday special by planning surprises, spending quality time with loved ones, and creating memorable experiences."),
]

# Who is your friend chats - Converted to list of (keywords, response) tuples
who_is_your_friend_chats = [
    (["who is your friend", "do you have a friend", "who is your best friend", "do you have a best friend",
      "who is your closest friend", "do you have a closest friend", "who is your only friend",
      "do you have an only friend", "who is your friend in the world", "do you have a friend in the world",
      "who is your friend in this universe", "do you have a friend in this universe"],
     "My friend is Mr. Abhi because he is the one who created me and helps me learn new things every day."),
]

# Abhi chats - Converted to list of (keywords, response) tuples
Abhi_chats = [
    (["who is mr.abhi", "who is abhi"], "Mr. Abhi is the person who created me and helps me learn new things every day."),
    (["what does mr.abhi do", "what does abhi do"], "Mr. Abhi is a software developer who created me to assist users like you."),
    (["how did mr.abhi create you", "how did abhi create you"], "Mr. Abhi created me using advanced programming techniques and machine learning algorithms."),
    (["what is mr.abhi's role", "what is abhi's role"], "Mr. Abhi's role is to develop and improve me so that I can assist users effectively."),
    (["how can i contact mr.abhi", "contact abhi"], "You can contact Mr. Abhi through his social media profiles or email."),
    (["what is mr.abhi's expertise", "abhi's expertise"], "Mr. Abhi's expertise lies in software development, machine learning, and artificial intelligence."),
    (["what is mr.abhi's background", "abhi's background"], "Mr. Abhi has a background in computer science and has worked on various software projects."),
    (["what is mr.abhi's vision", "abhi's vision"], "Mr. Abhi's vision is to create intelligent systems that can assist users in their daily tasks and improve their lives."),
    (["how does mr.abhi improve you", "how does abhi improve you"], "Mr. Abhi improves me by updating my algorithms, adding new features, and training me with more data."),
    (["what is mr.abhi's mission", "abhi's mission"], "Mr. Abhi's mission is to make technology more accessible and user-friendly for everyone."),
    (["how does mr.abhi help you", "how does abhi help you"], "Mr. Abhi helps me by providing guidance, feedback, and new data to learn from."),
    (["what is mr.abhi's contribution to technology", "abhi's contribution to technology"], "Mr. Abhi's contribution to technology includes developing innovative software solutions and improving user experience."),
    (["how can i learn from mr.abhi", "learn from abhi"], "You can learn from Mr. Abhi by following his work, reading his articles, and engaging with him on social media."),
]

# Jokes chats (10 entries) - Converted to list of (keywords, response) tuples
jokes_chats = [
    (["tell me a joke", "another joke", "tell me a funny joke", "make me laugh", "give me a joke",
      "tell me a programming joke", "tell me a tech joke", "tell me a coding joke",
      "tell me a software joke", "tell me a funny programming joke", "tell me a funny tech joke",
      "tell me a funny coding joke"], "Why do programmers prefer dark mode? Because light attracts bugs!"),
    (["java joke"], "Why do Java developers wear glasses? Because they don't see sharp."),
    (["python joke"], "Why do Python programmers prefer snakes? Because they love to code in Python!"),
    (["nature joke"], "Why do programmers hate nature? It has too many bugs."),
    (["christmas joke"], "Why do programmers always mix up Christmas and Halloween? Because Oct 31 == Dec 25!"),
    (["ios joke"], "Why do programmers prefer iOS development? Because they can't handle Android's Java exceptions!"),
    (["computer joke"], "Why was the computer cold? It left its Windows open!"),
    # ... add all 10 jokes here (consider adding more distinct jokes if you want varied responses)
]

# Telugu songs chats (20 entries) - Converted to list of (keywords, response) tuples
telugu_songs_chats = [
    (["best telugu song 2023", "popular telugu song 2023"], "Some popular Telugu songs of 2023 are 'Butta Bomma' and 'Ramulo Ramulaa'."),
    (["latest telugu songs", "new telugu songs"], "Check out the latest Telugu songs on music streaming platforms like Spotify and Gaana."),
    (["top telugu songs"], "Some top Telugu songs include 'Samajavaragamana' and 'Vachindamma'."),
    (["popular telugu songs"], "Popular Telugu songs include 'Pilla Pilla' and 'Dimaak Kharaab'."),
    (["telugu songs 2023"], "Some trending Telugu songs in 2023 are 'Naatu Naatu' and 'Saami Saami'."),
    (["telugu movie songs"], "Telugu movie songs are known for their melodious tunes and catchy lyrics."),
    (["telugu romantic songs"], "Some popular Telugu romantic songs are 'Inkem Inkem Inkem Kaavaale' and 'Yevandoi Nene Lokam'."),
    (["telugu dance songs"], "Telugu dance songs like 'Dimaak Kharaab' and 'Butta Bomma' are great for parties."),
    (["telugu folk songs"], "Telugu folk songs are rich in culture and tradition, often sung during festivals."),
    (["telugu devotional songs"], "Telugu devotional songs are sung to praise various deities and are popular during festivals."),
    (["telugu hit songs"], "Some hit Telugu songs include 'Vachindamma' and 'Samajavaragamana'."),
    (["telugu sad songs"], "Telugu sad songs like 'Inkem Inkem Inkem Kaavaale' and 'Yevandoi Nene Lokam' evoke deep emotions."),
    (["telugu peppy songs"], "Telugu peppy songs like 'Dimaak Kharaab' and 'Butta Bomma' are great for dance floors."),
    (["telugu songs playlist"], "You can find curated Telugu songs playlists on platforms like Spotify and YouTube."),
    (["telugu songs for parties"], "Telugu songs like 'Dimaak Kharaab' and 'Butta Bomma' are perfect for parties."),
    (["telugu songs for weddings"], "Popular Telugu wedding songs include 'Butta Bomma' and 'Ramulo Ramulaa'."),
    (["telugu songs for celebrations"], "Telugu songs like 'Dimaak Kharaab' and 'Butta Bomma' are great for celebrations."),
    (["telugu songs for road trips"], "Telugu songs like 'Butta Bomma' and 'Ramulo Ramulaa' are perfect for road trips."),
    (["telugu songs for workouts"], "Telugu songs like 'Dimaak Kharaab' and 'Butta Bomma' can energize your workouts."),
    # ... add 20 Telugu songs chats
]

# Telugu movie chats (20 entries) - Converted to list of (keywords, response) tuples
telugu_movie_chats = [
    (["top hero in telugu movies", "best telugu hero"], "Mahesh Babu and Allu Arjun are among the top Telugu actors."),
    (["latest telugu movie", "new telugu movie"], "The latest Telugu movie is 'Pushpa: The Rise'."),
    (["best telugu movie of 2023", "top telugu movie 2023"], "Some of the best Telugu movies of 2023 include 'RRR' and 'KGF Chapter 2'."),
    (["top telugu movies"], "Some top Telugu movies include 'Baahubali', 'RRR', and 'Arjun Reddy'."),
    (["popular telugu movies"], "Popular Telugu movies include 'Baahubali', 'RRR', and 'Arjun Reddy'."),
    (["telugu movies 2023"], "Some of the popular Telugu movies in 2023 are 'RRR' and 'KGF Chapter 2'."),
    (["telugu action movies"], "Telugu action movies like 'Baahubali' and 'RRR' are known for their grand visuals."),
    (["telugu romantic movies"], "Telugu romantic movies like 'Arjun Reddy' and 'Geetha Govindam' are loved by audiences."),
    (["telugu comedy movies"], "Telugu comedy movies like 'Eega' and 'Bhale Bhale Magadivoy' are popular for their humor."),
    (["telugu thriller movies"], "Telugu thriller movies like 'Anukokunda Oka Roju' and 'Kshanam' keep audiences on the edge of their seats."),
    (["telugu horror movies"], "Telugu horror movies like 'Arundhati' and 'Chandamama Kathalu' are known for their spooky elements."),
    (["telugu family movies"], "Telugu family movies like 'Bommarillu' and 'Manam' are loved for their emotional stories."),
    (["telugu historical movies"], "Telugu historical movies like 'Baahubali' and 'Magadheera' are known for their epic storytelling."),
    (["telugu biographical movies"], "Telugu biographical movies like 'Mahanati' and 'NTR Kathanayakudu' tell inspiring stories."),
    (["telugu movies for kids"], "Telugu movies like 'Eega' and 'Chhota Bheem' are great for kids."),
    (["telugu movies for family"], "Telugu movies like 'Bommarillu' and 'Manam' are perfect for family viewing."),
    (["telugu movies for couples"], "Telugu romantic movies like 'Arjun Reddy' and 'Geetha Govindam' are great for couples."),
    (["telugu movies for friends"], "Telugu comedy movies like 'Eega' and 'Bhale Bhale Magadivoy' are fun to watch with friends."),
    (["telugu movies for celebrations"], "Telugu movies like 'Baahubali' and 'RRR' are great for celebrations."),
    (["telugu movies for festivals"], "Telugu movies like 'Baahubali' and 'RRR' are perfect for festival viewing."),
    (["telugu movies for weekends"], "Telugu movies like 'Baahubali' and 'RRR' are great for weekend binge-watching."),
    (["telugu movies for holidays"], "Telugu movies like 'Baahubali' and 'RRR' are perfect for holiday viewing."),
    # ... add 20 Telugu movie chats
]

# --- NEW CHATS FOR USER REQUESTS ---
# Each response now includes a 'url' and 'action' key for the frontend to interpret.
# Converted to list of (keywords, response_dict) tuples


alarm_chats = [
    (["set an alarm", "set alarm", "can you set an alarm", "remind me at", "alarm for"], {"response": "I'm sorry, I cannot directly set an alarm on your device. You will need to set alarms manually through your phone or computer's alarm settings."}),
]

whatsapp_message_chats = [
    (["send whatsapp message", "chat whatsapp", "whatsapp to person", "how to send whatsapp message"],
     {"response": "I cannot directly send WhatsApp messages from here due to privacy and security restrictions. However, you can create a click-to-chat link using the format: https://wa.me/<PhoneNumber>?text=<YourMessage>. Replace <PhoneNumber> with the full number including country code (e.g., 919876543210 for India) and <YourMessage> with your message (use %20 for spaces). Then open this link in your browser.", "action": "display_instruction", "url": "https://faq.whatsapp.com/591339899895232?lang=en"}), # Added a relevant URL for more info
]

mobile_connect_chats = [
    (["connect to my mobile", "link with my phone", "access my phone", "pair with my mobile", "control my phone"], {"response": "I am a chatbot running on a server and cannot directly connect to or control your physical mobile device. My interactions are limited to responding to your text queries."}),
]

# --- NEW APP OPENING CHATS ---
app_open_chats = [
    (["open instagram", "go to instagram"], {"response": "Opening Instagram for you!", "action": "open_url", "url": "https://www.instagram.com"}),
    (["open youtube", "go to youtube"], {"response": "Opening YouTube. Enjoy the videos!", "action": "open_url", "url": "https://www.youtube.com"}),
    (["open whatsapp", "go to whatsapp web"], {"response": "Opening WhatsApp Web. Please scan the QR code to log in.", "action": "open_url", "url": "https://web.whatsapp.com/"}),
    (["open cricbuzz", "go to cricbuzz"], {"response": "Opening Cricbuzz. Get the latest cricket scores!", "action": "open_url", "url": "https://www.cricbuzz.com"}),
    (["open google", "go to google", "search on google"], {"response": "Opening Google. What do you want to search for?", "action": "open_url", "url": "https://www.google.com"}),
    (["open facebook", "go to facebook"], {"response": "Opening Facebook for you!", "action": "open_url", "url": "https://www.facebook.com"}),
    (["open twitter", "go to x.com", "open x"], {"response": "Opening X (formerly Twitter).", "action": "open_url", "url": "https://x.com"}),
    (["open linkedin", "go to linkedin"], {"response": "Opening LinkedIn. Connect with professionals!", "action": "open_url", "url": "https://www.linkedin.com"}),
    (["open amazon", "go to amazon", "shop on amazon"], {"response": "Opening Amazon. Happy shopping!", "action": "open_url", "url": "https://www.amazon.in"}),
    (["open flipkart", "go to flipkart"], {"response": "Opening Flipkart. Happy shopping!", "action": "open_url", "url": "https://www.flipkart.com"}),
    (["open netflix", "go to netflix", "watch netflix"], {"response": "Opening Netflix. What do you want to watch?", "action": "open_url", "url": "https://www.netflix.com"}),
    (["open spotify", "go to spotify", "listen to music"], {"response": "Opening Spotify. Enjoy the music!", "action": "open_url", "url": "https://open.spotify.com"}),
    (["open prime video", "go to prime video", "watch prime video"], {"response": "Opening Prime Video. Enjoy the shows!", "action": "open_url", "url": "https://www.primevideo.com"}),
    (["open hotstar", "go to hotstar", "watch hotstar"], {"response": "Opening Hotstar. Get ready to stream!", "action": "open_url", "url": "https://www.hotstar.com"}),
    (["open jio cinema", "go to jio cinema", "watch jio cinema"], {"response": "Opening Jio Cinema. Enjoy the content!", "action": "open_url", "url": "https://www.jiocinema.com"}),
    (["open swiggy", "go to swiggy", "order food from swiggy"], {"response": "Opening Swiggy. Time to order some delicious food!", "action": "open_url", "url": "https://www.swiggy.com"}),
    (["open zomato", "go to zomato", "order food from zomato"], {"response": "Opening Zomato. Get ready to explore restaurants!", "action": "open_url", "url": "https://www.zomato.com"}),
    (["open google maps", "go to maps", "navigate"], {"response": "Opening Google Maps. Where do you want to go?", "action": "open_url", "url": "https://www.google.com/maps"}),
    (["open gmail", "go to gmail", "check my email"], {"response": "Opening Gmail. You've got mail!", "action": "open_url", "url": "https://mail.google.com"}),
    (["open canva", "go to canva", "design on canva"], {"response": "Opening Canva. Get creative!", "action": "open_url", "url": "https://www.canva.com"}),
]

# Combine all chats into a single list of (keywords/exact_phrase, response/function/response_dict) tuples
# Order matters: more specific matches should come before more general ones.
# Maths problems are left as exact match for now due to the nature of the specific answers.
all_chats_data = [
    # High-priority, specific actions (like app opening, alarms)
    *app_open_chats,
    *alarm_chats,
    *whatsapp_message_chats,
    *mobile_connect_chats,

    # Dynamic/Live chats
    *live_chats,

    # Specific static answers (like math problems - might be better as exact match)
    # These will be checked using a different mechanism or ordered carefully
    *[(k, v) for k, v in maths_problesm_chats], # keeping as exact match for now

    # General keyword-based chats
    *basic_chats,
    *chit_chat_responses,
    *ipl_2025_chats,
    *cricket_history_chats,
    *friends_chats,
    *interview_software_chats,
    *maths_tables_chats,
    *maths_square_chats,
    *birthday_chats,
    *who_is_your_friend_chats,
    *Abhi_chats,
    *jokes_chats,
    *telugu_songs_chats,
    *telugu_movie_chats,
]


def generate_response(user_input):
    """
    Generates a chatbot response based on user input.

    Args:
        user_input (str): The message from the user.

    Returns:
        dict: A dictionary containing the 'response' and optionally 'url' and 'action'.
    """
    user_input_lower = user_input.lower()

    # Iterate through the combined list of chats
    for item in all_chats_data:
        keywords = item[0]
        response_content = item[1]

        if isinstance(keywords, list): # For keyword-based chats
            if contains_any_keyword(user_input_lower, keywords):
                if callable(response_content): # If it's a function (like live chats)
                    return response_content()
                elif isinstance(response_content, dict): # If it's a structured response dict
                    return response_content
                else: # Simple string response
                    return {"response": response_content}
        else: # For exact string matches (like maths_problems_chats were originally)
            if user_input_lower == keywords: # Exact match for specific queries
                if callable(response_content): # If it's a function (shouldn't happen here, but good practice)
                    return response_content()
                elif isinstance(response_content, dict): # If it's a structured response dict
                    return response_content
                else: # Simple string response
                    return {"response": response_content}


    # Fallback for general questions that might contain numbers for calculations (simple eval)
    # This is a very basic and unsafe way to do calculations.
    # For a real-world bot, use a proper math parsing library (e.g., sympy or numexpr)
    # and sanitize input heavily. This is just to demonstrate handling new math questions.
    math_pattern = re.compile(r"what is (\d+\s*[+\-/%*]\s\d+)") # Added * to the pattern
    match = math_pattern.search(user_input_lower)
    if match:
        try:
            # DANGER: eval() can be a security risk with unsanitized input.
            # Only use for trusted inputs or with strict sanitization.
            expression = match.group(1).replace(' ', '')
            result = eval(expression)
            return {"response": f"The result of {expression} is {result}."}
        except Exception:
            return {"response": "I can try simple math, but I had trouble with that calculation."}


    return {"response": "Sorry, I didn't understand that. Can you please rephrase or ask something else?"}


@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Buddy AI Chatbot server is running."})

@app.route("/chat", methods=["POST"])
def chat():
    """
    API endpoint for handling chat messages.
    Receives a message from the frontend and returns a chatbot response.
    """
    data = request.get_json()
    message = data.get("message")
    if not message:
        return jsonify({"error": "No message sent"}), 400

    response_data = generate_response(message) # Get the structured response
    return jsonify(response_data) # Send the structured response

if __name__ == "__main__":
    # In a production environment, disable debug=True
    app.run(host="0.0.0.0", debug=True, port=5000) # Explicitly set host and port for clarity