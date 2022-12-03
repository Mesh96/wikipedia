#!/usr/bin/env python

# Import the necessary libraries 
import requests 
import re 
import csv 
import json

# Ask the user to input a valid Wikipedia link 
wiki_link = input("Please enter a valid Wikipedia link: ")

# Check if the link is a valid Wikipedia link 
if not re.match(r'^https://en\.wikipedia\.org/wiki/', wiki_link): 
   print("This is not a valid Wikipedia link.")

# Ask the user to input a valid integer between 1 to 20
n = int(input("Please enter a valid integer between 1 and 20: ")) 
if n not in range(1,21):
   print("Not a valid integer.")

# Scrape the link for all wiki links embedded in the page and store them in a list
def scrape_wiki_links(url, n):
    # Initialize a list to store the wiki links
    wiki_links = []
    # Get the HTML content of the page
    html_content = requests.get(url).text
    # Find all the wiki links in the content
    links = re.findall('href="(/wiki/.*?)"', html_content)
    # Append the wiki links to the list
    for link in links:
       wiki_links.append('https://en.wikipedia.org' + link)
    # Set the base condition
    if n == 0:
       return wiki_links
    else:
       # Recursively call the function to get all the wiki links at the given level
       for link in links:
          wiki_links += scrape_wiki_links('https://en.wikipedia.org' + link, n-1)
       # Return the final list of wiki links
       return wiki_links

# Call the function to get the list of wiki links
wiki_links = scrape_wiki_links(wiki_link, n)

# Get the total count and unique count of the links
total_count = len(wiki_links)
unique_count = len(set(wiki_links))

# Write the results to a CSV file
with open('wiki_links.csv', 'w') as csv_file:
   writer = csv.writer(csv_file)
   writer.writerow(["Wiki Links"])
   for link in wiki_links:
      writer.writerow([link])
   writer.writerow(["Total Count:", total_count])
   writer.writerow(["Unique Count:", unique_count])

# Write the results to a JSON file
with open('wiki_links.json', 'w') as json_file:
   json_data = {"wiki_links": wiki_links, "total_count": total_count, "unique_count": unique_count}
   json.dump(json_data, json_file)

print("The results are successfully written to the CSV and JSON files.")