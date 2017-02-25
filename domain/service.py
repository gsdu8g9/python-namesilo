from .apiwrapper import DomainAPIWrapper


class DomainService:
    def __init__(self):
        self._api = DomainAPIWrapper()

    @staticmethod
    def _parse_response(api_response_content):
        payload = api_response_content["namesilo"]["reply"]

        available_domains = payload.get("available", {}).get("domain", None)
        unavailable_domains = payload.get("unavailable", {}).get("domain", None)
        invalid_domains = payload.get("invalid", {}).get("domain", None)

        return available_domains, unavailable_domains, invalid_domains


    def check_availability(self, domain):
        domain_available = False

        api_response = self._api.check_availability(domain)

        if api_response.success:
            available, unavailable, invalid = self._parse_response(api_response.content)

            if available == domain:
                domain_available = True

            return domain_available
        else:
            raise Exception(api_response.error)

    def bulk_check_availability(self, *args):
        domains = ",".join(args)
        response = {}
        api_response = self._api.check_availability(domains)

        if api_response.success:
            available, unavailable, invalid = self._parse_response(api_response.content)

            for domain in args:
                if domain in available:
                    response[domain] = True
                else:
                    response[domain] = False

            return response
        else:
            raise Exception(api_response.error)
