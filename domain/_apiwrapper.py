from core.baseapiwrapper import BaseAPIWrapper


class DomainAPIWrapper(BaseAPIWrapper):
	def __init__(self):
		super().__init__()

	def check_availability(self, domains):
		url_suffix = "checkRegisterAvailability?version=1&type=xml&key=%s&domains=%s" % (self.token, domains)

		response = self.get(url_suffix)

		return response
