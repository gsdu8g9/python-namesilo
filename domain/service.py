from .apiwrapper import DomainAPIWrapper
from .exceptions import DomainServiceException
from common.models import ServiceResponse


class DomainService:
    def __init__(self):
        self._api = DomainAPIWrapper()

    @staticmethod
    def _validate_years(years: int):
        """
        Validates if years parameter falls within an accepted range
        :param years:
        :return:
        """
        min_years = 1
        max_years = 10

        if years not in range(min_years, max_years + 1):
            raise DomainServiceException("Value for years must be between %s and %s" % (min_years, max_years))

        return True

    def check_availability(self, domain: str):
        """
        Check availability of a single domain
        :param domain: domain name
        :return: bool
        """
        domain_available = False

        api_response = self._api.check_availability(domain)

        if api_response.success:
            available = api_response.content.get("available", {}).get("domain", None)

            if available == domain:
                domain_available = True

            return domain_available
        else:
            raise DomainServiceException(api_response.error)

    def bulk_check_availability(self, *args: list):
        """
        Checks availability for multiple domains
        :param args: domain names
        :return: ServiceResponse
        """
        domains = ",".join(args)
        service_response = ServiceResponse()
        api_response = self._api.check_availability(domains)

        if api_response.success:
            service_response.success = True
            available_domains = api_response.content.get("available", {}).get("domain", None)

            for domain in args:
                if domain in available_domains:
                    service_response.return_value[domain] = True
                else:
                    service_response.return_value[domain] = False

            return service_response
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
        service_response = ServiceResponse()

        DomainService._validate_years(years)

        if auto_renew:
            auto_renew = 1
        else:
            auto_renew = 0
        if private:
            private = 1
        else:
            private = 0

        api_response = self._api.register_domain(domain_name, years, private, auto_renew)

        service_response.success = api_response.success
        service_response.message = api_response.content.get("message", "")

        if api_response.success:
            service_response.price = api_response.content.get("order_amount", 0)
        else:
            service_response.message = api_response.error

        return service_response

    def list_domains(self):
        """
        List all domains registered with current account
        :return: list of registered domains
        """
        service_response = ServiceResponse()
        api_response = self._api.list_domains()

        if api_response.success:
            service_response.success = True
            service_response.return_value = api_response.content.get("domains", {}).get("domain", [])

        return service_response

    def renew_domain(self, domain_name: str, years: int=1):
        """
        Renew domain name
        :param domain_name:
        :param years:
        :return:
        """
        service_response = ServiceResponse()
        DomainService._validate_years(years)

        api_response = self._api.renew_domain(domain_name, years)

        service_response.success = api_response.success
        service_response.message = api_response.content.get("message", "")

        if api_response.success:
            service_response.price = api_response.content.get("order_amount", 0)
        else:
            service_response.message = api_response.error

        return service_response
