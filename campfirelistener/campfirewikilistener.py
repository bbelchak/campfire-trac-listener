import sys
import pinder
from trac.core import *
from trac.wiki.api import IWikiChangeListener
from trac.config import Option, IntOption, ListOption, BoolOption

class CampfireWikiListener(Component):
    implements(IWikiChangeListener)

    prefix = Option('campfire', 'prefix', '')
    projectPath = Option('campfire', 'path', '')
    tracfqdn = Option('campfire', 'trachost', '')
    subdomain = Option('campfire', 'subdomain', '')
    apiToken = Option('campfire', 'apitoken', '')
    roomId = Option('campfire', 'roomid', '')    

    def _sendText(self, page, text):
        try:
            c = pinder.Campfire(self.subdomain, self.apiToken)
            room = c.room(self.roomId)
            room.speak("%s: wiki page %s (http://%s%s/ticket/%i) %s" % (self.prefix, page.name, self.tracfqdn, self.projectPath, page.name, text))

        except:
            self.env.log.error("Unexpected error: %s" % (sys.exc_info()[1]))
            return

    def wiki_page_added(self, page):
        self._sendText(page, "added by %s." % (page.author))

    def wiki_page_changed(self, page, version, t, comment, author, ipnr):
        self._sendText(page, "added by %s (comment: %s)." % (author, comment))

    def wiki_page_deleted(self, page):
        self._sendText(page, "deleted by %s." % (page.author))

    def wiki_page_version_deleted(self, page):
        self._sendText(page, "version %s deleted by %s." % (page.version, page.author))

    def wiki_page_renamed(self, page, old_name): 
        self._sendText(page, "renamed from %s to %s." % (old_name, page.name))
