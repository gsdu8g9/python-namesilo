from core.baseapiwrapper import BaseAPIWrapper


class DomainAPIWrapper(BaseAPIWrapper):
    def __init__(self):
        super().__init__()

    def check_availability(self, domains):
        url_suffix = "checkRegisterAvailability?version=1&type=xml&key=%s&domains=%s" % (self.token, domains)

        return self.get(url_suffix)

    def register_domain(self, domain, years, private, auto_renew):
        url_suffix = "registerDomain?version=1&type=xml&key=%s&domain=%s&years=%s&private=%s&auto_renew=%s" % \
                     (self.token, domain, years, private, auto_renew)

        return self.get(url_suffix)
