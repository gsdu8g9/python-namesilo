from .apiwrapper import DomainAPIWrapper
from .exceptions import DomainServiceException


class DomainService:
    def __init__(self):
        self._api = DomainAPIWrapper()

    @staticmethod
    def _parse_availability_response(api_response_content: dict):

        available_domains = api_response_content.get("available", {}).get("domain", None)
        unavailable_domains = api_response_content.get("unavailable", {}).get("domain", None)
        invalid_domains = api_response_content.get("invalid", {}).get("domain", None)

        return available_domains, unavailable_domains, invalid_domains

    def check_availability(self, domain: str):
        domain_available = False

        api_response = self._api.check_availability(domain)

        if api_response.success:
            available, unavailable, invalid = self._parse_availability_response(api_response.content)

            if available == domain:
                domain_available = True

            return domain_available
        else:
            raise DomainServiceException(api_response.error)

    def bulk_check_availability(self, *args: list):
        domains = ",".join(args)
        response = {}
        api_response = self._api.check_availability(domains)

        if api_response.success:
            available, unavailable, invalid = self._parse_availability_response(api_response.content)

            for domain in args:
                if domain in available:
                    response[domain] = True
                else:
                    response[domain] = False

            return response
        else:
            raise DomainServiceException(api_response.error)

    def register_domain(self, domain_name: str, years: int=1, auto_renew: bool=False, private: bool=False):
        """
        Register domain name
        :param domain_name: name of domain
        :param years:
        :param auto_renew:
        :param private:
        :return:
        """
        min_years = 1
        max_years = 10

        response = {}

        if years not in range(min_years, max_years+1):
            raise DomainServiceException("Valid value for years is between %s and %s" % (min_years, max_years))
        if auto_renew:
            auto_renew = 1
        else:
            auto_renew = 0
        if private:
            private = 1
        else:
            private = 0

        api_response = self._api.register_domain(domain_name, years, private, auto_renew)

        response["registered"] = api_response.success
        response["message"] = api_response.content.get("message", "")

        if api_response.success:
            response["price"] = api_response.content.get("order_amount", 0)
        else:
            response["message"] = api_response.error

        return response
