### The problem

Modern TVs generally integrate CEC capabilities. But a majority of constructors
implement their own version. And, on some brands, you can't have a full control
of the remote.

For example, LG has its own CEC system called "Simplink". When using Kodi on
a Raspberry Pi, it automatically detects the CEC capabilities of the TV.
But, some buttons aren't recognized by the CEC client. And it's a real pain to 
not be able to configure them, like the *Power* one. Especially when using kodi 
as a PVR client.

In a perfect world, and when using Kodi to watch TV, we should only have to 
press the Power button to turn the TV off **and** automatically stop the 
player, or in some cases, shutdown the Pi.
But sadly, it doesn't work that way, and for what i know, there is sometimes 
no possibility to manually configure the Power button or other ones as they 
are not detected by the CEC client when pressing them. So, let's use python to 
emulate a standard TV behavior.

### The solution

We gonna use ```tvservice``` which will return a different status 
code if the TV is On or Off.

```$ tvservice -s```  
```$ state 0x12000a [HDMI CEA (16) RGB lim 16:9], 1920x1080 @ 60.00Hz, progressive```

Then, i use Kodi web API to control it over HTTP. If the script detects that TV
is turned Off, it will check if there is any active player. If so, it will
automatically stop it.

### How to use

Setup a new crontab to launch the script at startup.

```# crontab -e```  
```@reboot python /path/to/python/script```

That way, it will regularly check the TV state and will stop any active player 
if TV is Off. Be sure to edit the script according to your own setup.  
Please note that at the moment, this script doesn't handle authentification if
you have configured credentials to connect to kodi web api. This feature will
be added later.

And taadaa! Problem solved. I hope it could be useful and save some time to 
people who have the same problem.
