import xbmcaddon, xbmcgui, xbmc, xbmcvfs
import os, shutil, urllib
from shutil import copyfile
from shutil import make_archive


"""
If you want to create your own addon using Audrey you just need to require it in the addon.xml and then pass your feed and feed type to the feedme() function

feedme(string feed, string type)

feed (string) Path or URL to json file
type (string) Either "file" or "url" depending on where the file is located

"""

addon=xbmcaddon.Addon()


def fail(message):
    xbmcgui.Dialog().ok("Audrey Addon Creation Failed", message)
    exit()

if xbmcaddon.Addon().getSetting('create_addon')=="true":
    if xbmcaddon.Addon().getSetting('addon_name'):
        # addon.xml file
        xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<addon id="{{addon_id}}" name="{{addon_name}}" version="{{addon_version}}" provider-name="{{author}}">\n\t<requires>\n\t\t<import addon="script.module.audrey" />\n\t</requires>\n\t<extension point="xbmc.python.pluginsource" library="default.py">\n\t\t<provides>video</provides>\n\t</extension>\n\t<extension point="xbmc.addon.metadata">\n\t\t<summary lang="en">{{summary}}</summary>\n\t\t<description>{{description}}</description>\n\t\t<platform>all</platform>\n\t\t<language>en</language>\n\t\t<email>{{email}}</email>\n\t</extension>\n</addon>'

        # default.py file for local files
        local_file = 'import xbmc, xbmcaddon, os, audrey\naddon=xbmcaddon.Addon()\nhome=xbmc.translatePath(addon.getAddonInfo("path"))\naudrey.feedme(os.path.join(home, "sites.json"), "file")'

        # default.py file for online files
        url_file = 'import audrey, xbmcaddon\naudrey.feedme({{url}}, "url")'
        
        try:
            save_location = xbmc.translatePath(xbmcaddon.Addon().getSetting('folder'))
        except:
            fail("Error: No save folder has been specified")
        try:
            save_folder = 'plugin.video.'+xbmcaddon.Addon().getSetting('addon_name').lower().replace(" ", "")
        except:
            fail("Error: Addon name is required")
        try:
            version = xbmcaddon.Addon().getSetting('addon_version')
        except:
            fail("Error: Verson number is required")
        try:
            author = xbmcaddon.Addon().getSetting('addon_author')
        except:
            fail("Error: Addon author is required")
        try:
            email = xbmcaddon.Addon().getSetting('addon_email')
        except:
            fail("Error: Addon author is required")
        try:
            description = xbmcaddon.Addon().getSetting('addon_description')
        except:
            fail("Error: Addon description is required")
        try:
            summary = xbmcaddon.Addon().getSetting('addon_summary')
        except:
            fail("Error: Addon description is required")
        try:
            icon = xbmc.translatePath(xbmcaddon.Addon().getSetting('addon_icon'))
        except:
            fail("Error: Addon icon is required")
        try:
            fanart = xbmc.translatePath(xbmcaddon.Addon().getSetting('addon_fanart'))
        except:
            fail("Error: Addon fanart is required")
        
        # start creating addon
        try:
            os.makedirs(os.path.join(save_location, save_folder, save_folder))
        except:
            fail("Error: Unable to create folder/folder already exists")
            
        # create addon.xml file
        f = open(os.path.join(save_location, save_folder, save_folder, "addon.xml"), "w+")
        f.write(xml.replace("{{addon_id}}", save_folder).replace("{{addon_name}}", xbmcaddon.Addon().getSetting('addon_name')).replace("{{addon_version}}", version).replace("{{author}}", author).replace("{{description}}", description).replace("{{summary}}", summary).replace("{{email}}", email))
        f.close()
        
        # create default.py file
        if xbmcaddon.Addon().getSetting('type')=="0":
            f = open(os.path.join(save_location, save_folder, save_folder, "default.py"), "w+")
            f.write(local_file)
            f.close()
            copyfile(xbmc.translatePath(xbmcaddon.Addon().getSetting('file')), os.path.join(save_location, save_folder, save_folder, "sites.json"))
        else:
            f = open(os.path.join(save_location, save_folder, save_folder, "default.py"), "w+")
            f.write(url_file.replace("{{url}}", '"'+xbmcaddon.Addon().getSetting('url')+'"'))
            f.close()
        
        
        # copy images
        parts = icon.split(".")
        copyfile(icon, os.path.join(save_location, save_folder, save_folder, "icon."+parts[-1]))
        parts = fanart.split(".")
        copyfile(fanart, os.path.join(save_location, save_folder, save_folder, "fanart."+parts[-1]))
        
        # zip it all up
        make_archive(os.path.join(save_location, save_folder), "zip", os.path.join(save_location, save_folder))
        
        #delete folder
        shutil.rmtree(os.path.join(save_location, save_folder))
        
        xbmcaddon.Addon().setSetting('create_addon', "false")
        xbmcgui.Dialog().ok("Audrey Addon Creation Complete", "Your addon has been created in the save location specified")
        exit()
else:
    import audrey
    if xbmcaddon.Addon().getSetting('type')=="0":
        # load audrey using a local file
        file=xbmc.translatePath(xbmcaddon.Addon().getSetting('file'))
        audrey.feedme(file, "file")
    elif xbmcaddon.Addon().getSetting('type')=="1":
        # load audrey using a file stored online
        audrey.feedme(xbmcaddon.Addon().getSetting('url'), "url")