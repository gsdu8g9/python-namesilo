from ._apiwrapper import DomainAPIWrapper


class DomainService:
	def __init__(self):
		self.__base_url = "http://sandbox.namesilo.com/api/"

		self.api = DomainAPIWrapper()

	@staticmethod
	def _parse_response(api_response_content):
		payload = api_response_content["namesilo"]["reply"]

		available_domains = payload.get("available").get("domain", [])
		unavailable_domains = payload.get("unavailable").get("domain", [])
		invalid_domains = payload.get("invalid").get("domain", [])

		return available_domains, unavailable_domains, invalid_domains

	def check_availability(self, *args):
		domains = ",".join(args)

		api_response = self.api.check_availability(domains)

		if api_response.success:
			available, unavailable, invalid = self._parse_response(api_response.content)

			return available, unavailable, invalid
		else:
			raise Exception(api_response.error)
