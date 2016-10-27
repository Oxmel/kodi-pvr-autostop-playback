### The problem

A lot of TVs natively support CEC nowadays. But, on some brands, only a few 
number of buttons are recognized by the client. Mainly because a majority of 
constructors implement their own CEC version. And it's a real pain to not be 
able to configure some of them, like the *Power* one. Especially when using kodi 
as a PVR client.

So, let's use python to emulate a standard TV behavior. Aka automatically stop 
playback if the TV is turner Off.

### The solution

Let's use ```tvservice``` which will return a different status 
code if the TV is On or Off.

```$ tvservice -s```  
```$ state 0x12000a [HDMI CEA (16) RGB lim 16:9], 1920x1080 @ 60.00Hz, progressive```

Then, we use Kodi web API to control it over HTTP. If the script detects that TV
is turned Off, it will check if there is any active player. If so, it will
automatically stop it.

### How to use

Setup a new crontab to exec the script every 2 minutes for example.

```# crontab -e```  
```*/2 * * * * python /path/to/python/script```

And Tadaa! Problem solved :)
