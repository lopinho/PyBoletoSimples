#BoletoSimples Python

Biblioteca Python para acessar informações do [Boleto Simples](http://boletosimples.com.br) através da [API](http://api.boletosimples.com.br).

## Instalação
pip install boletosimples

## Configuração
Pode se configurar por variáveis de ambiente ou na inicialização da classe que representa a APP

### Inicialização
Toda classe deve ser inicializada com os atributos token, user_agent:

import boletosimples
manager = boletosimples.BankBillet(token='....', user_agent='Pedro (pedro@example.com)')

### Variáveis de ambiente
É possivel configurar por variáveis de ambiente

BOLETOSIMPLES_APP_ID='Pedro (pedro@example.com)'

BOLETOSIMPLES_TOKEN='....'

Caso queira usar o ambiente de teste:
BOLETOSIMPLES_API_URL=https://sandbox.boletosimples.com.br/api/v1/

## Alias
Boleto = BankBillet

ContaBancaria = BankBilletAccount

Usuario = UserInfo

Cliente = Customer

Retorno = Discharge

Remessa = Remittance

## Exemplos
### Boletos Bancários
```python
import datetime
import boletosimples

# Instanciando o manager
manager = boletosimples.BankBillet(token='....', user_agent='Pedro (pedro@example.com)')

# Atributos para gerar um boleto
atributos = {
    "amount": 9.01,
    "description": 'Despesas do contrato 0012',
    "expire_at": datetime.date.today(),
    "customer_address": 'Rua quinhentos',
    "customer_address_complement": 'Sala 4',
    "customer_address_number": '111',
    "customer_city_name": 'Rio de Janeiro',
    "customer_cnpj_cpf": '012.345.678-90',
    "customer_email": 'cliente@example.com',
    "customer_neighborhood": 'Sao Francisco',
    "customer_person_name": 'Joao da Silva',
    "customer_person_type": 'individual',
    "customer_phone_number": '2112123434',
    "customer_state": 'RJ',
    "customer_zipcode": '12312-123'
}

# Criando um boleto
manager.create(atributos)

# Cancelando um boleto
manager.cancel(id_no_boletosimples)

# Consultando um boleto
manager.show(id_no_boletosimples)

# Listando boletos
manager.list()

# Criando boletos em massa
manager.bulk([atributos, atributos])


```
