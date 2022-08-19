# Discord Vcc Generator 
### create unlimited vcc with this discord bot
![gif](https://user-images.githubusercontent.com/74266531/185586725-9c66e1ca-aee8-40b2-9dd8-6b9a941d36db.gif)

# Requirements 
* create an account on [Moon](https://paywithmoon.com/)
* deposit at least 5$ 
* create a new discord bot and get bot access token
* get your moon account access token (detailed more in bottom of readme)

# Installation and running
* you must have python installed 
* run ```pip install -r requirements.txt```
* opens ``config.json`` edit ``bot_access_token``  with your discord bot token
* run ``app.py`` !
* run ``/setup``

# Commands
| command | usage
| ---- | :----:
|/setup <token> | save your moon account access token to bot
|/generate | generate a new vcc and delete old one
|/transcations | get your lastest 10 transactions


### how to get moon access token ? 
1. Go to the [Moon](https://paywithmoon.com/) website on your desktop browser and log into your account.

2. Next, press Ctrl+Shift+I (or Cmd+Option+I on Mac) or(right click + inspect) on your keyboard to enter Developer Tools. Click Network from the toolbar at the top.
![alt](https://user-images.githubusercontent.com/74266531/185573582-5f81e268-7888-4260-87ca-a07b39739482.png)
![alt](https://user-images.githubusercontent.com/74266531/185575409-06ed3c91-260d-4f01-acef-9866d8f7e8fe.png)
3. Reload the tab by pressing F5.
4. ![alt](https://user-images.githubusercontent.com/74266531/185575793-b5996518-3299-489b-9125-f7888bb16988.png)
5. There will be many more values within Network. Type onchain/ into the field marked Filter. From the results below, click latest one.
![alt](https://user-images.githubusercontent.com/74266531/185576434-bea0d977-49f0-445e-ae27-a41934f134ac.png)
6. Within invoice, click the Headers tab. Scroll down until you see authorization.after ``Bearer`` This is your moon access token.
![alt](https://user-images.githubusercontent.com/74266531/185578177-61c41dda-d754-4529-b272-6578796e0718.jpg)