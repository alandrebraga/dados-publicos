# Dados Publicos da educação

Esse projeto tem o intuito de coletar os dados do censo da educação superior e indicadores de qualidade (IGC, CPC, IDD) e analisar se a demanda crescente de cursos EAD pode ter afetado os indicadores de qualidade dos cursos

## Como rodar?

Para rodar o projeto você precisa ter uma service account no gcp com acesso para criar, ler e destruir buckets e também acesso ao bigquery para criar tabelas. Após criar a service account salve o secret json na raiz desse projeto com o nome de 'secrets.json'

## Como subir a infraestrutura?

Deve-se ter o terraform instalado na maquina ou caso queira pode usar o docker compose para rodar

da raiz do projeto

```docker
docker compose -f infrastructure/docker-compose.yaml run terraform plan
docker compose -f infrastructure/docker-compose.yaml run terraform apply
```

e para destruir a infraestrutura basta rodar.

```docker
docker compose -f infrastructure/docker-compose.yaml run terraform destroy
```

Ao destruir caso você tenha dados em uso no bigquery o terraform vai reclamar, basta deletar as tabelas do big query para destruir o resto.

## TODO

[] Ajustar CLI para aceitar não fazer upload dos arquivos para o gcp e manter localmente
[] Criar um dockerfile com duckdb para rodar consulta direto nos csv salvos locamente
[] Coletar dados do IGC, CPC, IDD e Enade
