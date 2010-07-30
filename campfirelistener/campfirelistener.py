import sys
import pinder
from trac.core import *
from trac.ticket.api import ITicketChangeListener
from trac.wiki.api import IWikiChangeListener
from trac.config import Option, IntOption, ListOption, BoolOption

class CampfireListener(Component):
    implements(ITicketChangeListener)
    
    prefix = Option('campfire', 'prefix', '')
    projectPath = Option('campfire', 'path', '')
    tracfqdn = Option('campfire', 'trachost', '')
    subdomain = Option('campfire', 'subdomain', '')
    apiToken = Option('campfire', 'apitoken', '')
    roomId = Option('campfire', 'roomid', '')    

    def _sendText(self, ticketid, text):
        try:
            c = pinder.Campfire(self.subdomain, self.apiToken)
            room = c.room(self.roomId)
            room.speak("%s: ticket #%i (http://%s%s/ticket/%i) %s" % (self.prefix, ticketid, self.tracfqdn, self.projectPath, ticketid, text))

        except:
            self.env.log.error("Unexpected error: %s" % (sys.exc_info()[1]))
            return

    def ticket_created(self, ticket):
        self._sendText(ticket.id, "\"%s\" created by %s." % (ticket.values['summary'][0:100], ticket.values['reporter']))

    def ticket_changed(self, ticket, comment, author, old_values):
        self._sendText(ticket.id, "changed by %s, Comment: %s." % (author, comment[0:100]))

    def ticket_deleted(self, ticket):
        self._sendText(ticket.id, "Ticket deleted")

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
