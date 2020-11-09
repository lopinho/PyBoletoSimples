# coding: utf-8
import os
import time
import requests
import json

from utils import JSONEncoder, cc_to_

CONNECT_TIMEOUT, READ_TIMEOUT = 5.0, 30.0


class BoletoSimplesBase(object):
    def url(self):
        raise NotImplementedError(
            'Implementar funcao url retornando a url para o servico %s' %
            self.__class__.__name__)

    def show(self, object_id, **kwargs):
        if 'show' not in self.metodos_validos:
            raise Exception(
                'Nao e permitido mostrar atributos do objeto nessa classe')
        resposta = self._get(self.url() + str(object_id), **kwargs)
        if resposta.status_code == 200:
            return resposta.json()
        if resposta.status_code == 429:
            if 'Retry-After' in resposta.headers:
                time.sleep(long(resposta.headers['Retry-After']))
                return self.show(object_id, **kwargs)
        self._raise_error(resposta)

    def get(self, object_id, **kwargs):
        return self.show(object_id, **kwargs)

    def list(self, **kwargs):
        if 'list' not in self.metodos_validos:
            raise Exception('Nao e permitido listar objetos nessa classe')
        resposta = self._get(self.url(), **kwargs)

        if resposta.status_code == 204:
            return None
        if resposta.status_code == 200:
            return resposta.json()
        self._raise_error(resposta)

    def find(self, **kwargs):
        return self.list(**kwargs)

    def delete(self, object_id, **kwargs):
        if 'delete' not in self.metodos_validos:
            raise Exception('Nao e permitido deletar objetos nessa classe')
        resposta = self._delete(self.url() + str(object_id), **kwargs)
        if resposta.status_code == 204:
            return None
        if resposta.status_code == 200:
            return resposta.json()
        self._raise_error(resposta)

    def update(self, object_id, attrs, **kwargs):
        return self.change(object_id, attrs, **kwargs)

    def change(self, object_id, attrs, **kwargs):
        attrs = self._safe_dict(attrs)
        if 'change' not in self.metodos_validos:
            raise Exception('Nao e permitido alterar objetos nessa classe')

        attrs = json.dumps(attrs, cls=JSONEncoder)
        resposta = self._patch(self.url() + str(object_id), attrs, **kwargs)
        if resposta.status_code == 204:
            return None
        if resposta.status_code == 200:
            return resposta.json()
        self._raise_error(resposta)

    def create(self, attrs, **kwargs):
        attrs = self._safe_dict(attrs)
        if 'create' not in self.metodos_validos:
            raise Exception('Nao e permitido criar objetos nessa classe')

        attrs = json.dumps(attrs, cls=JSONEncoder)
        resposta = self._post(self.url(), attrs, **kwargs)
        if resposta.status_code == 204:
            return None
        if resposta.status_code == 201:
            return resposta.json()
        self._raise_error(resposta)

    def _safe_dict(self, dicionario):
        key = cc_to_(self.__class__.__name__)
        if key not in dicionario:
            return {key: dicionario}

    def _get(self, url, **kwargs):
        timeout = kwargs.get('timeout', (CONNECT_TIMEOUT, READ_TIMEOUT))
        return requests.get(
            url,
            headers=self._headers_do_kwargs(kwargs),
            timeout=timeout,
            **kwargs
        )

    def _delete(self, url, **kwargs):
        timeout = kwargs.get('timeout', (CONNECT_TIMEOUT, READ_TIMEOUT))
        return requests.delete(
            url,
            headers = self._headers_do_kwargs(kwargs),
            timeout=timeout,
            **kwargs
        )

    def _post(self, url, data, **kwargs):
        timeout = kwargs.get('timeout', (CONNECT_TIMEOUT, READ_TIMEOUT))
        return requests.post(
            url,
            headers = self._headers_do_kwargs(kwargs),
            timeout=timeout,
            data=data,
            **kwargs
        )

    def _put(self, url, data, **kwargs):
        timeout = kwargs.get('timeout', (CONNECT_TIMEOUT, READ_TIMEOUT))
        return requests.put(
            url,
            headers = self._headers_do_kwargs(kwargs),
            timeout=timeout,
            data=data,
            **kwargs
        )

    def _patch(self, url, data, **kwargs):
        timeout = kwargs.get('timeout', (CONNECT_TIMEOUT, READ_TIMEOUT))
        return requests.patch(
            url,
            headers = self._headers_do_kwargs(kwargs),
            timeout=timeout,
            data=data,
            **kwargs)

    def _raise_error(self, resposta):
        content_type = resposta.headers.get('content-type') or\
            resposta.headers.get('Content-Type')
        if 'JSON' not in content_type.upper():
            if 'status' in resposta.header:
                raise Exception(resposta.header['status'])
            else:
                raise Exception(resposta.status_code)
        if resposta.text:
            try:
                objeto = resposta.json()
                if 'error' in objeto:
                    mensagem = objeto['error']
                else:
                    if 'errors' in objeto:
                        items = objeto['errors'].items()
                    else:
                        items = objeto.items()
                    lista = list()
                    for campo, erros in items:
                        erro = u'%s: %s' % (campo, u", ".join(erros))
                        lista.append(erro)
                        mensagem = u", ".join(lista)
            except:
                mensagem = resposta.text
            raise Exception(mensagem.encode('utf-8'))
        raise Exception(resposta.headers.get('status', resposta.status_code))

    def _headers_do_kwargs(self, kwargs):
        headers = kwargs.get('headers', {})
        headers['User-Agent'] = self.user_agent
        headers['Content-Type'] = 'application/json'
        headers['Authorization'] = 'Bearer {}'.format(self.token)
        return headers

    def _valida_inicializacao(self, kwargs):
        necessarios = ['token', 'user_agent']
        for atributo in necessarios:
            if atributo not in kwargs:
                erro = 'Atributo %s faltando para iniciar o servico' %\
                    atributo
                raise Exception(erro)

    def _atualiza_kwargs_com_variaveis_ambiente(self, kwargs):
        user_agent = os.environ.get('BOLETOSIMPLES_APP_ID')
        token = os.environ.get('BOLETOSIMPLES_TOKEN')

        if user_agent and 'user_agent' not in kwargs:
            kwargs['user_agent'] = user_agent

        if token and 'token' not in kwargs:
            kwargs['token'] = token

    def __init__(self, is_production=True, **kwargs):
        self._atualiza_kwargs_com_variaveis_ambiente(kwargs)
        self._valida_inicializacao(kwargs)

        if is_production:
            self.base_site = 'https://boletosimples.com.br/api/v1/'
        else:
            self.base_site = 'https://sandbox.boletosimples.com.br/api/v1/'

        self.token = kwargs['token']
        self.user_agent = kwargs['user_agent']
        self.metodos_validos = kwargs.get(
            'metodos_validos',
            ['create', 'delete', 'change', 'list', 'show']
        )
