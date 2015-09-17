# coding: utf-8
from base import BoletoSimplesBase

class BankBillet(BoletoSimplesBase):
    """
        Manager para Boletos
    """
    def url(self):
        return self.base_site + 'bank_billets/'

    def cancel(self, boleto_id, **kwargs):
        return self._put(self.url() + boleto_id + '/cancel', **kwargs)

    def __init__(self, **kwargs):
        return super(BankBillet, self).__init__(
            metodos_validos=['create', 'list', 'show'],
            **kwargs)


class BankBilletAccount(BoletoSimplesBase):
    """
        Manager Para Carteiras de cobranca
    """

    def url(self):
        return self.base_site + 'bank_billet_accounts/'


class UserInfo(BoletoSimplesBase):
    """
        Manager para o usuário logado
    """

    def url(self):
        return self.base_site + 'userinfo/'

    def show(self):
        return self._get(self._userinfo_url())

class Customers(BoletoSimplesBase):
    """
        Manager para os clientes
    """

    def url(self):
        return self.base_site + 'customers/'

class Discharges(BoletoSimplesBase):
    """
        Manager para o CNAB (Retorno)
    """
    def url(self):
        return self.base_site + 'discharges/'

    def pay_off(self, object_id):
        return self._put(self.url() + object_id + '/pay_off', None)

class Remittances(BoletoSimplesBase):
    """
        Manager para o CNAB (Remessa)
    """
    def url(self):
        return self.base_site + 'remittances/'


