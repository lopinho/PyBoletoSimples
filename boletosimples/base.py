# coding: utf-8
import requests

class BoletoSimplesBase:
    def url(self):
        raise NotImplementedError('Necessario implementar a funcao url retornando a url base com app na classe %s' % self.__class__.__name__)

    def show(self, object_id, **kwargs):
        if 'show' not in self.metodos_validos:
            raise Exception('Nao e permitido mostrar atributos do objeto nessa classe')
        resposta = self._get(self.url() + str(object_id), **kwargs)
        if resposta.status_code == 200:
            return resposta

    def list(self, **kwargs):
        if 'list' not in self.metodos_validos:
            raise Exception('Nao e permitido listar objetos nessa classe')
        resposta = self._get(self.url(), **kwargs)
        if resposta.status_code == 200:
            return resposta

    def delete(self, object_id, **kwargs):
        if 'delete' not in self.metodos_validos:
            raise Exception('Nao e permitido deletar objetos nessa classe')
        resposta = self._delete(self.url() + str(object_id), **kwargs)
        if resposta.status_code == 200:
            return resposta

    def change(self, object_id, attrs, **kwargs):
        if 'change' not in self.metodos_validos:
            raise Exception('Nao e permitido alterar objetos nessa classe')
        resposta = self._patch(self.url() + object_id, attrs, **kwargs)
        if resposta.status_code == 200:
            return resposta

    def create(self, attrs, **kwargs):
        if 'create' not in self.metodos_validos:
            raise Exception('Nao e permitido criar objetos nessa classe')
        resposta = self._post(self.url(), attrs, **kwargs)
        if resposta.status_code == 200:
            return resposta

    def _get(self, url, **kwargs):
        return requests.get(
            url,
            auth=(self.token, self.password),
            headers = self._headers_do_kwargs(kwargs),
            **kwargs
        )

    def _delete(self, url, **kwargs):
        return requests.delete(
            url,
            auth=(self.token, self.password),
            headers = self._headers_do_kwargs(kwargs),
            **kwargs
        )

    def _post(self, url, data, **kwargs):
        return requests.post(
            url,
            auth=(self.token, self.password),
            headers = self._headers_do_kwargs(kwargs),
            data=data,
            **kwargs
        )

    def _put(self, url, data, **kwargs):
        return requests.put(
            url,
            auth=(self.token, self.password),
            headers = self._headers_do_kwargs(kwargs),
            data=data,
            **kwargs
        )

    def _patch(self, url, data, **kwargs):
        return requests.patch(
            url,
            auth=(self.token, self.password),
            headers = self._headers_do_kwargs(kwargs),
            data=data,
            **kwargs
        )

    def _headers_do_kwargs(self, kwargs):
        if 'headers' in kwargs:
            kwargs['headers']['User-Agent'] = self.user_agent
            return kwargs.pop('headers')
        return {'User-Agent' : self.user_agent}

    def _valida_inicializacao(self, kwargs):
        necessarios = ['token', 'user_agent']
        for atributo in necessarios:
            if atributo not in kwargs:
                raise Exception('Atributo %s faltando para iniciar o servico' % atributo)
    def __init__(self, **kwargs):
        self._valida_inicializacao(kwargs)
        self.token = kwargs['token']
        self.user_agent = kwargs['user_agent']
        self.password = kwargs.get('password', 'x')
        self.metodos_validos= kwargs.get('metodos_validos',['create', 'delete', 'change', 'list', 'show'])

