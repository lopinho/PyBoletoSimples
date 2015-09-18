# coding: utf-8
import sys

from unittest import TestCase
from mock import patch
import os

sys.path.append('../')

from boletosimples.base import BoletoSimplesBase


class BoletoSimplesBaseTestCase(TestCase):
    def setUp(self):
        self.token = 'xpto'
        self.password = '123'
        self.user_agent = 'MyApp (myapp@example.com)'
        self.atributos_inicializacao = {
            'token' : self.token,
            'password': self.password,
            'user_agent' : self.user_agent
        }
        self.object = BoletoSimplesBase(**self.atributos_inicializacao)

    def test_token_iniciado(self):
        self.assertEqual(self.object.token, self.token)

    def test_password_iniciado(self):
        self.assertEqual(self.object.password, self.password)

    def test_user_agent_iniciado(self):
        self.assertEqual(self.object.user_agent, self.user_agent)

    def test_valida_inicializacao_token(self):
        """
            Deve levantar erro se não passar o atributo token na inicialização
        """
        atributos = self.atributos_inicializacao
        del atributos['token']
        with patch.dict('os.environ'):
            del os.environ['BOLETOSIMPLES_TOKEN']
            self.assertRaisesRegexp(Exception, 'Atributo token faltando para iniciar o servico', BoletoSimplesBase, **atributos)

    def test_valida_inicializacao_user_agent(self):
        """
            Deve levantar erro se não passar o atributo user_agent na inicialização
        """
        atributos = self.atributos_inicializacao
        del atributos['user_agent']
        with patch.dict('os.environ'):
            del os.environ['BOLETOSIMPLES_APP_ID']
            self.assertRaisesRegexp(Exception, 'Atributo user_agent faltando para iniciar o servico', BoletoSimplesBase, **atributos)

    def test_headers_do_kwargs_vasio_deve_retornar_header_correto(self):
        resposta = self.object._headers_do_kwargs({})
        esperado = {'Content-Type': 'application/json','User-Agent': 'MyApp (myapp@example.com)'}
        self.assertEqual(resposta, esperado)

    def test_headers_do_kwargs_deve_manter_user_agent(self):
        resposta= self.object._headers_do_kwargs({'headers' :{'User-Agent' : 'valor'}})
        esperado = {'Content-Type': 'application/json','User-Agent': 'MyApp (myapp@example.com)'}
        self.assertEqual(resposta, esperado)

    def test_headers_do_kwargs_deve_manter_outros_valores(self):
        resposta= self.object._headers_do_kwargs({'headers' :{'Outro-Header' : 'valor'}})
        esperado = {
            'Outro-Header' : 'valor',
            'User-Agent': 'MyApp (myapp@example.com)',
            'Content-Type': 'application/json'
        }
        self.assertEqual(resposta, esperado)

    @patch('boletosimples.base.requests')
    def test_get_deve_ter_comportamento_correto(self, requests):
        self.object._get('url')
        requests.get.assert_called_once_with('url', auth=('xpto', '123'), headers={'Content-Type': 'application/json','User-Agent': 'MyApp (myapp@example.com)'})

    @patch('boletosimples.base.requests')
    def test_delete_deve_ter_comportamento_correto(self, requests):
        self.object._delete('url')
        requests.delete.assert_called_once_with('url', auth=('xpto', '123'), headers={'Content-Type': 'application/json','User-Agent': 'MyApp (myapp@example.com)'})

    @patch('boletosimples.base.requests')
    def test_post_deve_ter_comportamento_correto(self, requests):
        self.object._post('url', {'atributo' : 'valor'})
        requests.post.assert_called_once_with('url', auth=('xpto', '123'), headers={'Content-Type': 'application/json','User-Agent': 'MyApp (myapp@example.com)'}, data={'atributo': 'valor'})

    @patch('boletosimples.base.requests')
    def test_put_deve_ter_comportamento_correto(self, requests):
        self.object._put('url', {'atributo' : 'valor'})
        requests.put.assert_called_once_with('url', auth=('xpto', '123'), headers={'Content-Type': 'application/json','User-Agent': 'MyApp (myapp@example.com)'}, data={'atributo': 'valor'})

    @patch('boletosimples.base.requests')
    def test_patch_deve_ter_comportamento_correto(self, requests):
        self.object._patch('url', {'atributo' : 'valor'})
        requests.patch.assert_called_once_with('url', auth=('xpto', '123'), headers={'Content-Type': 'application/json','User-Agent': 'MyApp (myapp@example.com)'}, data={'atributo': 'valor'})

    def test_list_deve_levantar_erro_se_nao_estiver_nos_metodos_validos(self):
        self.object.metodos_validos.remove('list')
        self.assertRaisesRegexp(Exception,'Nao e permitido listar objetos nessa classe', self.object.list)

    def test_delete_deve_levantar_erro_se_nao_estiver_nos_metodos_validos(self):
        self.object.metodos_validos.remove('delete')
        self.assertRaisesRegexp(Exception,'Nao e permitido deletar objetos nessa classe', self.object.delete, 1)

    def test_create_deve_levantar_erro_se_nao_estiver_nos_metodos_validos(self):
        self.object.metodos_validos.remove('create')
        self.assertRaisesRegexp(Exception,'Nao e permitido criar objetos nessa classe', self.object.create, {})

    def test_change_deve_levantar_erro_se_nao_estiver_nos_metodos_validos(self):
        self.object.metodos_validos.remove('change')
        self.assertRaisesRegexp(Exception,'Nao e permitido alterar objetos nessa classe', self.object.change,1, {})

    def test_url_deve_levantar_erro_se_nao_estiver_implementado(self):
        self.assertRaisesRegexp(NotImplementedError, 'Necessario implementar a funcao url retornando a url base com app na classe BoletoSimplesBase', self.object.url)

    @patch('boletosimples.base.requests')
    @patch('boletosimples.base.BoletoSimplesBase.url')
    def test_url_deve_ter_comportamento_correto(self, url, requests):
        self.object.list()
        requests.get.assert_called_once_with(url.return_value, auth=('xpto', '123'), headers={'Content-Type': 'application/json','User-Agent': 'MyApp (myapp@example.com)'})

    @patch('boletosimples.base.requests')
    @patch('boletosimples.base.BoletoSimplesBase.url')
    def test_delete_deve_ter_comportamento_correto(self, url, requests):
        self.object.delete(1)
        requests.delete.assert_called_once_with(url.return_value + str(1), auth=('xpto', '123'), headers={'Content-Type': 'application/json','User-Agent': 'MyApp (myapp@example.com)'})

    @patch('boletosimples.base.requests')
    @patch('boletosimples.base.BoletoSimplesBase.url')
    def test_change_deve_ter_comportamento_correto(self, url, requests):
        self.object.change(1, {})
        requests.patch.assert_called_once_with(url.return_value + str(1), auth=('xpto', '123'), data={}, headers={'Content-Type': 'application/json','User-Agent': 'MyApp (myapp@example.com)'})

    @patch('boletosimples.base.requests')
    @patch('boletosimples.base.BoletoSimplesBase.url')
    def test_create_deve_ter_comportamento_correto(self, url, requests):
        self.object.create({})
        requests.post.assert_called_once_with(url.return_value, auth=('xpto', '123'), data={}, headers={'Content-Type': 'application/json','User-Agent': 'MyApp (myapp@example.com)'})

