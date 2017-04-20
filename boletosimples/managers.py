# coding: utf-8
import json

from utils import JSONEncoder
from base import BoletoSimplesBase


class BankBilletAccount(BoletoSimplesBase):
    """
        Manager Para Carteiras de cobranca
    """

    def url(self):
        return self.base_site + 'bank_billet_accounts/'


class BankBillet(BoletoSimplesBase):
    """
        Manager para Boletos
    """
    def _trata_resposta_bulk(self, resposta):
        retorno = []
        for item in resposta.json():
            if 'bank_billet' in item:
                item = item['bank_billet']
            retorno.append(item)
        return retorno

    def bulk(self, attrs, **kwargs):
        attrs = json.dumps({'bank_billets': attrs}, cls=JSONEncoder)

        resposta = self._post(self.url() + 'bulk/', attrs, **kwargs)
        if resposta.status_code == 204:
            return None
        if resposta.status_code == 201:
            return self._trata_resposta_bulk(resposta)
        self._raise_error(resposta)

    def url(self):
        return self.base_site + 'bank_billets/'

    def cancel(self, boleto_id, **kwargs):
        resposta = self._put(
            self.url() + str(boleto_id) + '/cancel',
            {},
            **kwargs)
        if resposta.status_code == 204:
            return None
        if resposta.status_code == 200:
            return resposta.json()
        self._raise_error(resposta)

    def __init__(self, **kwargs):
        return super(BankBillet, self).__init__(
            metodos_validos=['create', 'list', 'show', 'bulk'],
            **kwargs)


class UserInfo(BoletoSimplesBase):
    """
        Manager para o usuário logado
    """

    def url(self):
        return self.base_site + 'userinfo/'

    def show(self):
        resposta = self._get(self.url())
        if resposta.status_code == 200:
            return resposta.json()


class Customer(BoletoSimplesBase):
    """
        Manager para os clientes
    """

    def url(self):
        return self.base_site + 'customers/'


class Discharge(BoletoSimplesBase):
    """
        Manager para o CNAB (Retorno)
    """
    def url(self):
        return self.base_site + 'discharges/'

    def pay_off(self, object_id):
        return self._put(self.url() + object_id + '/pay_off', None)


class Remittance(BoletoSimplesBase):
    """
        Manager para o CNAB (Remessa)
    """
    def url(self):
        return self.base_site + 'remittances/'
