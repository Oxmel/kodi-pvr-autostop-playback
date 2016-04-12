
Automatically stop Kodi's active player if TV is switched Off.

### The problem

Modern TVs generally integrate CEC capabilities. But some of the constructors
implement their own version. And, on some brands, you can't have a full control
on the remote.

For example, LG has it's own CEC version called "Simplink". When using Kodi on
a Raspberry Pi, it automatically detects the CEC capabilities of the TV.
But, some of the remote buttons aren't recognized. And it's a real pain to not be able to configure some of them, like the Power one. Especially when using kodi as a PVR client.

In a perfect world, things should be like this : When i use Kodi as a PVR client to watch TV, i should
only have to press the Power button to turn the TV Off AND automatically stop
the player to emulate a classic TV behavior. But sadly, it doesn't work that way, and for what i know, there is sometimes no possibility to manually configure the Power button as it is not detected by the CEC client when pressing it. So, let's use python to find a workaround.

### The solution

The solution i found is to use 'tvservice' which will return a different status code
if the TV is On or Off.

```$ tvservice -s ```  
```$ state 0x12000a [HDMI CEA (16) RGB lim 16:9], 1920x1080 @ 60.00Hz, progressive ```

Then, i use Kodi web API to control it over HTTP. If the script detects that TV
is turned Off, it will check if there is any active player. If so, it will
automatically stop it, emulating a normal TV behavior.

### Why not using libcec and cec-client?

That's true. Cec-client also provides an option to check the TV status by using
'cec-client -s'. And it probably could be used to send cec commands like Play/Pause/Stop.

But it also has a really annoying downgrade. When using this command, it always
unregister all cec-devices, breaking the link between TV and Kodi. Whatever option i
tried, it always ends up with the same behavior. That's what makes cec-client
totally unusable in some cases. Maybe there is a way, but i still didn't find it.

### How to use

The easiest way to use it is by setting up a new crontab to launch the script at startup.

```# crontab -e```  
```@reboot python /path/to/python/script```

That way, it will regularly check the TV state and will stop any active player if
TV is Off. Be sure to edit the script according to your own setup.

And taadaa! Problem solved. I hope it could be useful and save some time to people who have the same problem.
