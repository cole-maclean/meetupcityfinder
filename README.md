
<h1>Introduction</h1>

Back in February of this year, I packed up my comfortable Canadian life in Calgary, Alberta and moved to Barcelona, Spain to obtain an education in the Mediterranean lifestyle, European cultures, un poco español and some Artificial Intelligence. Having never moved to a new country on my own before, I was overwhelmed by the diverse languages and cultures of Barcelona, and for the first time, I felt truely lonely. With so many cool things to explore and experience in my new city, it took longer than I anticipated to find a group of people to share those experiences with. I realized that making new friends in your mid-twenties isn't quite the same as it was back on the playground, so I began to break out of my comfort zone by using [meetup.com](https://www.meetup.com/) to attend events I found interesting. It's been a fantastic application for finding new friends and helping me settle into my new life in Barcelona.

Meetup.com provides a platform for anybody to build a community around a topic of interest, scheduling events from casual drinks in a bar, hikes in the mountains or performing in a singing group. With meetup.com, you can "Find your people" by sharing your interests with others in your local community. This platform provides an interesting opportunity to explore which world cities have the most active users for any given topic, allowing us to find our ideal cities and perhaps learn a little about different cultures around the world. Fortunately, meetup.com provides a robust [API](http://www.meetup.com/meetup_api/) to allow us to explore this dataset for ourselves.

<h1>The Final Visualization</h1>

The aim of this project is to build an interface to allow the user to explore various topics of interest and visualize the best cities for that unique grouping of topics. I've used my hometown of Calgary in the below example image with data science and spanish language as topics. The final visualization can be viewed [here.](https://cole-maclean.github.io/meetupcityfinder/) Feel free to go play with it, the rest of this post outlines how to retrieve the data from meetup.com using it's API.

<img src="calgary_example.png">

<h1>The Build</h1>

<h2>Meetup.com API</h2>

Meetup.com has a very well documented API, and memebers of the community have built API wrappers for many popular programming languages. Python being my language of choice, I've utilized the Python [meetup-api](https://pypi.python.org/pypi/meetup-api/) library for this project. To use the package, we first need to obtain an [API key](https://secure.meetup.com/meetup_api/key/) to be used as authentication for our client object. 


```python
import meetup.api
import configparser
import time

config = configparser.ConfigParser()
config.read('secrets.ini')

meetup_api_key = config.get('meetup', 'api_key')
client = meetup.api.Client(meetup_api_key)
```

What we need from the API is to iterate over all groups that exist on the platform, collect the topic tags that group organizers assign their group, and collect the member count for each group. The meetup.api python package provides a GET function to obtain a list of groups having certain input filter parameters. The request returns a results object with a list of groups and their respecitive data including topic keywords.


```python
groups = client.GetGroups(lat=51.0486, lon=-114.0708,radius=50,fields=['topics']) #example meetup API call with Calgary as center
                                                                                  #GPS coords and 50 mile radius. Optional data
                                                                                  #request to return each groups list of topics
groups.results[1]
```

    29/30 (10 seconds remaining)
    




    {'category': {'id': 2,
      'name': 'career/business',
      'shortname': 'career-business'},
     'city': 'Calgary',
     'country': 'CA',
     'created': 1038423812000,
     'description': '<p><img src="http://photos1.meetupstatic.com/photos/event/b/0/5/c/600_435105148.jpeg"></p>\n<p><span><i><b>PLEASE READ BEFORE JOINING OUR GROUP</b> <br></i></span></p>\n<p><span>The Calgary Business Professionals Group ("CBP") is the premier business-related Meetup in the Calgary area. &nbsp;We cater to Calgary entrepreneurs.</span></p>\n<p><span>The CBP is all about forging strong relationships with no strings attached.&nbsp;</span></p>\n<p><span>We are not trying to sell you anything!&nbsp;</span></p>\n<p><span>Our strength is our membership (over 2000 members) and our events (we have hosted over 300).</span></p>\n<p><span>The CBP Meetup Group is one of the largest and longest running Meetup groups in Calgary (in existence since 2002).&nbsp;</span>&nbsp;</p>\n<p><b>Our events are invitation-only, private functions and are open to CBP Meetup Group members and their guests only.</b> <br></p>\n<p>Our events are free to attend (our breakfast event does require you to spend $10 minimum to support our venue).</p>\n<p>There are great food and drink specials at our "Beer and Wings" event, but you are on the hook for what you consume (our host venue runs individual tabs for all attendees). Please tip your server!</p>\n<p><span><b>In the interests of "good networking", we require ALL new members to include:</b></span></p>\n<p><span><b>&nbsp;(1) A recognizable photo (headshot or similar), NO ADVERTISING OR LOGOS!</b></span></p>\n<p><span><b>(2) BOTH your first AND last name on both your Meetup AND Group profiles</b></span></p>\n<p><span><b><i>Your application for membership will be rejected without this information</i></b></span></p>\n<p><span><b>In addition:</b></span></p>\n<p><strong>(3) We do not permit members of Multi-Level Marketing ("MLM") or other "Network Marketing" organizations to join this group.&nbsp;</strong></p>\n<p><strong>(4) We allow members of other networking groups to join, but PLEASE, do not recruit our members or promote your events at our functions. Doing so will result in removal from CBP.</strong> <br></p>\n<p><strong>(5) Please use Meetup\'s messaging function to communicate to follow members but selling or promoting your product or service in an unsolicited fashion is not permitted. Any violations of this policy will result in removal from the group.&nbsp; <br></strong></p>\n<p><span>We look forward to meeting you at one of our events.</span></p>\n<p><span>Yours in business and entrepreneurship;</span> <br></p>\n<p><b>Lisa Marie Genovese</b>, Organizer</p>\n<p><b>Sean Phillips</b>, Co-Organizer and Host of the monthly breakfast event</p>\n<p><b>Brad Celmainis</b>, Co-Organizer and Host of the monthly Beer and Wings event</p>\n<p><img src="http://photos4.meetupstatic.com/photos/event/b/0/6/4/600_435105156.jpeg"></p>\n<p> <br></p>',
     'group_photo': {'highres_link': 'http://photos3.meetupstatic.com/photos/event/a/4/7/6/highres_228822102.jpeg',
      'photo_id': 228822102,
      'photo_link': 'http://photos3.meetupstatic.com/photos/event/a/4/7/6/600_228822102.jpeg',
      'thumb_link': 'http://photos3.meetupstatic.com/photos/event/a/4/7/6/thumb_228822102.jpeg'},
     'id': 54766,
     'join_mode': 'approval',
     'lat': 51.04999923706055,
     'link': 'http://www.meetup.com/businessincalgary/',
     'lon': -114.08000183105469,
     'members': 2071,
     'name': 'Calgary Business Professionals Group',
     'organizer': {'member_id': 13068793,
      'name': 'Lisa Marie Genovese',
      'photo': {'highres_link': 'http://photos3.meetupstatic.com/photos/member/a/3/7/highres_246782615.jpeg',
       'photo_id': 246782615,
       'photo_link': 'http://photos3.meetupstatic.com/photos/member/a/3/7/member_246782615.jpeg',
       'thumb_link': 'http://photos3.meetupstatic.com/photos/member/a/3/7/thumb_246782615.jpeg'}},
     'rating': 4.47,
     'state': 'AB',
     'timezone': 'Canada/Mountain',
     'topics': [{'id': 389, 'name': 'Small Business', 'urlkey': 'smallbiz'},
      {'id': 1238, 'name': 'Marketing', 'urlkey': 'marketing'},
      {'id': 3880, 'name': 'Professional Development', 'urlkey': 'prodev'},
      {'id': 4422, 'name': 'Social Networking', 'urlkey': 'socialnetwork'},
      {'id': 15405,
       'name': 'Business Referral Networking',
       'urlkey': 'business-referral-networking'},
      {'id': 15720,
       'name': 'Professional Networking',
       'urlkey': 'professional-networking'},
      {'id': 17325,
       'name': 'Small Business Marketing Strategy',
       'urlkey': 'small-business-marketing-strategy'},
      {'id': 17635, 'name': 'Business Strategy', 'urlkey': 'business-strategy'},
      {'id': 19882, 'name': 'Entrepreneurship', 'urlkey': 'entrepreneurship'},
      {'id': 20060,
       'name': 'Entrepreneur Networking',
       'urlkey': 'business-entrepreneur-networking'},
      {'id': 20743,
       'name': 'Small Business Owners',
       'urlkey': 'small-business-owners'},
      {'id': 45636, 'name': 'Calgary Business', 'urlkey': 'calgary-business'},
      {'id': 65792, 'name': 'B2B Networking', 'urlkey': 'b2b-networking'},
      {'id': 72702,
       'name': 'Calgary Entrepreneurs',
       'urlkey': 'calgary-entrepreneurs'}],
     'urlname': 'businessincalgary',
     'utc_offset': -21600000,
     'visibility': 'public_limited',
     'who': 'Business Professionals'}



The meetup.com API does not provide a clear way to access every group on the platform, as the design of the system is such that a user selects a center location to search from in a geographic radius to ensure users are recommended groups close to their desired location. One option to obtain all availible groups is to input an impossibly high radius to encompass the entire globe.


```python
groups = client.GetGroups(lat=51.0486, lon=-114.0708,radius=10000000000,fields=['topics'])
groups.meta['total_count']
```

    28/30 (7 seconds remaining)
    




    257973



Although this option is technically feasible, and as of today returns a total of 257,973 unique groups, the total time to make that single request is over a minute. The meetup.com API is limited to only return 200 results at a time, which  would require over 1290 of these requests. To overcome the limit of 200 results, the API provides a page offset parameter to programmatically scroll through each page containing the next 200 groups.


```python
groups_per_page = 200

groups = client.GetGroups(lat=51.0486, lon=-114.0708,radius=5)#initial request to obtain total request pages
time.sleep(1)
pages = int(groups.meta['total_count']/groups_per_page)
print("total request groups = " + str(groups.meta['total_count']))
for i in range(0,pages + 1): #iterate over each request page
    print("page " + str(i) + "/" + str(pages))
    #get offseted request by current request page
    groups = client.GetGroups(lat=51.0486, lon=-114.0708,radius=5,fields=['topics'],pages=groups_per_page,offset=i)
```

    29/30 (10 seconds remaining)
    total request groups = 903
    page 0/4
    28/30 (8 seconds remaining)
    page 1/4
    27/30 (6 seconds remaining)
    page 2/4
    26/30 (5 seconds remaining)
    page 3/4
    25/30 (3 seconds remaining)
    page 4/4
    24/30 (2 seconds remaining)
    

Initally I attempted to use the above method to iterate over the entire 1290 pages of groups on meetup.com, but each request required me to pass the impossibly high radius parameter with each respective offset page, which I worried was hammering meetup.com's servers and would have taken a few days of straight API requests. The alternate solution I ended up using was to obtain a list of the top 250 global cities by population and use each as the centroid GPS location with a 300 mile radius to obtain the nearby groups. The complete API requests and data structure handling done for collecting the meetup.com data can be viewed in main.py in the projects [repo.](https://github.com/cole-maclean/meetupcityfinder/tree/gh-pages) To keep the data within githubs maximum 100mb file limit and ensure a performant d3.js visualization, city-topics with less then 100 members are filtered out of the dataset.

<h1>The Viz</h1>

The visualization is made up of 3 main components:  
1. Globe with city markings indicating cities containing the user selected topics and color coded by that cities sum total ranking in each topic - the lowest total score is the highest ranking city for that unique list of topics. The base for the d3.js globe was modified from [here](https://gist.github.com/serdaradali/11346541)
2. Top 10 ranking cities for user selected list of topics  
3. Detailed data for user selected city indicating that cities top 5 ranked topics, plus the rank for each of the user inputted topics

<h2>My Example</h2>

To test out the final viz, I added a few of the topic that interest me to find my ideal city. The following image depicts the results for my list of topics.

<img src="my_example.png">

The best city for all 8 topics appears to be New York, which is usually the number one city for any list of topics. Meetup.com was started in New York, and I believe New York is a large percentage of the total meetup.com user base, so most queries will show it as being the top city for most given list of topics. The results past New York become more interesting for my example, especially Sydney. It does well in all of the topics that interest me, plus it ranks first in the category "fun fun fun". Maybe I'll have to check out Sydney once I'm done my studies here in Barcelona.

<h1>Conclusions</h1>

The meetup.com API is a really cool dataset that can be used to explore the world and how people are interacting in it. There's probably alot more that can be done with this dataset, and I'm looking forward to playing with it some more to find further insights and interesting anomolies. Hopefully others have fun finding their ideal city and exploring the world through this lens. 
