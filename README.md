## Explanation
This allows you to use a Python shell and Selenium to automate scrolling back through a teams chat and scrape the messages.
The key variable is the position; each message has an attribute data-scroll-pos; the last/most recent message is at data-scroll-pos = 0.
You can see this if you open the webtools and poke around, sometimes useful if the process gets borked and you're trying to restart it.
The page is most likely to get refreshed if you or someone else who has access to the chat does something in teams, obviously posting a message in the chat will do it, but I suspect someone changing their status also might cause it. When this happens, the page will scroll back to the bottom again, and you have to use the scrollback_loop method to recover. To avoid this, best to run the process during off-peak hours.

## Requirements
  Python\
  Selenium for Python

## To use:
  launch a Python interactive shell\
  paste the contents of the chat_scrape file into the console (this might be fiddly? sorry)\
  bring up teams in a browser and copy the url\
  in the console:\
  ss = SeleniumScrape()\
  ss.session_setup(url)\
  in the NEW browser that Selenium opened, log into teams and do the duo auth, also bring up the chat you want to scrape\
  in the console:\
  ss.capture_setup(filename) #where filename is the path/filename.txt that you want to write to\
  ss.capture_loop()
  
  Note that the capture loop will bork every so often. most of the time you can simply start it again\
  ss.capture_loop()\
  if the browser shows that teams has helpfully refreshed the page and you are now at the end of your chat history\
  you must run the scrollback. First take note of the last reported position, then\
  in the console:\
  ss.scrollback_setup(position)\
  ss.scrollback_loop()\
  Note that the scrollback loop may also bork, and hopefully will allow you to just restart it as well\
  Once the chat has scrolled back to where you left off, reset the position and restart the capture\
  ss.position = ss.target\
  ss.capture_loop
  
  

