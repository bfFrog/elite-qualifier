
#Hi, i'm Jose Monroy, and this is my webscraping project. It scrapes information from steam, and allows the user to monitor the prices of a game on it. When that game falls to or under the requested price, you will receive an email informing you.

#It is meant to run 24/7, so I plan on being able to refine this further and be able to put it on my website, where it can hopefully run forever.

from bs4 import BeautifulSoup
import requests
import smtplib
import time

#error occurs if wrong link is input
#maybe in future use flask to let user select list of games, so they can't copy and paste random non working links
URL = input("What steam game do you want? (copy and paste the link): ")
# response = requests.get(URL)
# if response.status_code == 200:
#     print('exists')
# else:
#     print('does not exist') 



while True:
  requestedPrice = input("What price do you want it? $")
  if requestedPrice.replace(".","",1).isdigit():
    requestedPrice = float(requestedPrice)
    break
  else: 
    print ("please input an actual number")


email = input("What is your email? ")


def checkPrice():
  page = requests.get(URL)

  soup = BeautifulSoup(page.content, 'html.parser')

  global gameName
  global discountedPrice
  global discountPercent
  global gameDescription
  global truePrice

  gameName = soup.find('div', class_='apphub_AppName').get_text(strip=True)

  currentPrice = soup.find('div', class_='game_area_purchase_game').find('div', class_='game_purchase_price price')

  discountedPrice = soup.find('div', class_='game_area_purchase_game').find('div', class_='discount_final_price')

  originalPrice = soup.find('div', class_='game_area_purchase_game').find('div', class_='discount_original_price')

  discountPercent = soup.find('div', class_='game_area_purchase_game').find('div', class_='discount_pct')

  gameDescription = soup.find('div', class_='game_description_snippet')


  if currentPrice != None:
    currentPrice = float(currentPrice.get_text(strip=True)[1:])
    
  if discountedPrice != None:
    discountedPrice = float(discountedPrice.get_text(strip=True)[1:])

  if originalPrice != None:
    originalPrice = float(originalPrice.get_text(strip=True)[1:])

  if discountPercent != None:
    discountPercent = discountPercent.get_text(strip=True)[1:]

  if gameDescription != None:
    gameDescription = gameDescription.get_text(strip=True)

  #this makes the on sale original price and the regular price the same

  if currentPrice != None:
    truePrice = currentPrice
  if originalPrice != None:
    truePrice = originalPrice

  # print (gameName)
  # print (gameDescription)
  # print (currentPrice)
  # print (discountedPrice)
  # print (originalPrice)
  # print (discountPercent)
 

  if (truePrice <= requestedPrice):
    sendEmail()

  else:
    print ("it is still not at your price")

def sendEmail():
  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.ehlo()
  server.starttls()
  server.ehlo()

  server.login('steampricemonitor@gmail.com', 'kmzgdvsbensxtwrw')


  subject = f'{gameName}\'s price is reduced'

  if discountPercent != None:
    subject += f" by {discountPercent}!"
  else:
    subject += "!"


  requestedPriceMessage = f'The requested price was ${requestedPrice}'



  if discountPercent != None:
    currentPriceMessage =  f'The price went from ${truePrice} to ${discountedPrice}'
  else:
    currentPriceMessage = f'The price is ${truePrice}'
 
  link = f'Check the link {URL}'
  

  msg = f"Subject: {subject}\n\n{requestedPriceMessage}\n{currentPriceMessage}\n{link}"

  server.sendmail('steampricemonitor@gmail.com', 'toxicvenom224@gmail.com', msg)

  print("mail has been sent!")
  server.quit()



while(True):
  checkPrice()
  time.sleep(60*5)

