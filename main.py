import os
import requests
import xmltodict
from common.models import DomainInfo
from common.error_codes import check_error_code

__author__ = 'goran.vrbaski'


class ContactModel:
    def __init__(self, first_name: str, last_name: str, address: str, city: str, state: str, country: str, email: str, phone: str, zip: str):
        """
        Model for manipulating NameSilo contacts
        :param first_name: First Name
        :param last_name: Last Name
        :param address: Address
        :param city: City
        :param state: State
        :param country: Country
        :param email: Email address
        :param phone: Telephone number
        :param zip: ZIP Code
        """
        self.first_name = self.__correct_formating(first_name)
        self.last_name = self.__correct_formating(last_name)
        self.address = self.__correct_formating(address)
        self.city = self.__correct_formating(city)
        self.state = self.__correct_formating(state)
        self.country = self.__correct_formating(country)
        self.email = self.__correct_formating(email)
        self.phone = self.__correct_formating(phone)
        self.zip = self.__correct_formating(zip)

    def __correct_formating(self, data: str):
        """
        Replacing all whitespaces with %20 (NameSilo requirement)
        :param data:
        :return:
        """
        return data.replace(" ", "%20")


class NameSilo:
    def __init__(self, token: str, sandbox: bool=True):
        """

        :param token: access token from namesilo.com
        :param sandbox: true or false
        """
        self.__token = token
        if sandbox:
            self.__base_url = "http://sandbox.namesilo.com/api/"
        else:
            self.__base_url = "https://www.namesilo.com/api/"

    def __process_data(self, url_extend):
        parsed_context = self.__get_content_xml(url_extend)
        check_error_code(self.__get_error_code(parsed_context))
        return parsed_context

    def __get_error_code(self, data):
        return int(data['namesilo']['reply']['code']), data['namesilo']['reply']['detail']

    def __get_content_xml(self, url):
        api_request = requests.get(os.path.join(self.__base_url, url))
        if api_request.status_code != 200:
            raise Exception("API responded with status code: %s" % api_request.status_code)

        content = xmltodict.parse(api_request.content.decode())
        return content

    def renew_domain(self, domain_name: str, years: int=1):
        """
        Renew domain name
        :param domain_name:
        :param years:
        :return:
        """
        url_extend = "renewDomain?version=1&type=xml&key=%s&domain=%s&years=%s" % (self.__token, domain_name, years)
        parsed_content = self.__get_content_xml(url_extend)
        check_error_code(self.__get_error_code(parsed_content))
        return True

    def get_prices(self):
        """
        Returns all supported tld prices
        :return:
        """
        url_extend = "getPrices?version=1&type=xml&key=%s" % self.__token
        parsed_content = self.__get_content_xml(url_extend)
        check_error_code(self.__get_error_code(parsed_content))
        return parsed_content['namesilo']['reply']

    def list_contacts(self):
        """
        Returns list of all contacts for current account
        :return:
        """
        contacts = []
        url_extend = "contactList?version=1&type=xml&key=%s" % self.__token
        parsed_context = self.__get_content_xml(url_extend)
        check_error_code(self.__get_error_code(parsed_context))
        for contact in parsed_context['namesilo']['reply']['contact']:
            contacts.append(contact)
        return contacts

    def add_contact(self, contact: ContactModel):
        """
        Adding new contact for current account
        :param contact:
        :return:
        """
        url_extend = "contactAdd?version=1&type=xml&key={0}&fn={1}&ln={2}&ad={3}&cy={4}&st={5}&zp={6}&ct={7}&em={8}" \
                     "&ph={9}".format(self.__token, contact.first_name, contact.last_name, contact.address,
                                      contact.city, contact.state, contact.zip, contact.country, contact.email,
                                      contact.phone)
        parsed_context = self.__get_content_xml(url_extend)
        check_error_code(self.__get_error_code(parsed_context))
        return True

    # TODO: need to finish update contact
    def update_contact(self, contact: ContactModel):
        url_extend = "contactUpdate?version=1&type=xml&key={0}&contact_id=1440&fn=Goran&ln=Vrbaski&ad=123%20N.%201st%20Street&cy=Anywhere&st=AZ&zp=55555&ct=US&em=test@test.com&ph=4805555555".format(self.__token)
        parsed_contect = self.__process_data(url_extend)
        return True

    def add_account_funds(self, amount: float, payment_id: int):
        url_extend = "addAccountFunds?version=1&type=xml&key=%s&amount=%s&payment_id=%s" % (self.__token, amount,
                                                                                            payment_id)
        parsed_context = self.__get_content_xml(url_extend)
        check_error_code(self.__get_error_code(parsed_context))
        amount = parsed_context['namesilo']['reply']['new_balance'].replace(",", "")
        return True, float(amount)

    def get_account_balance(self):
        url_extend = "getAccountBalance?version=1&type=xml&key=%s" % self.__token
        parsed_context = self.__get_content_xml(url_extend)
        check_error_code(self.__get_error_code(parsed_context))
        amount = parsed_context['namesilo']['reply']['balance'].replace(",", "")
        return float(amount)
