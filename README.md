# Projeto de Engenharia de Dados: Pipeline Bancário com Airflow, Kafka, Apache Pinot e Superset

Este projeto simula um pipeline de dados bancários, totalmente containerizado com Docker Compose, integrando Airflow, Kafka (Redpanda), Apache Pinot e Superset para geração, ingestão, processamento e visualização de dados.

## Visão Geral

- **Geração de Dados**: Utiliza DAGS do Airflow para gerar dados sintéticos de transações bancárias e dimensões (branch, account, customer) com auxílio da biblioteca Faker.
- **Ingestão Batch**: As dimensões são geradas em arquivos CSV e carregadas em tabelas OFFLINE do Apache Pinot.
- **Ingestão Streaming**: Fatos de transações são enviados para um tópico Kafka (Redpanda) e consumidos em tempo real por uma tabela REALTIME do Apache Pinot.
- **Visualização**: O Apache Superset conecta-se ao Pinot para criação de dashboards e análises dos dados.
- **Orquestração**: Todo o ecossistema é orquestrado via Docker Compose, incluindo Airflow (Celery + PostgreSQL), Redpanda, Pinot e Superset.

## Arquitetura

```
[Airflow DAGs] --> [CSV/Batch] --> [Pinot OFFLINE Tables]
         |
         +--> [Kafka (Redpanda)] --> [Pinot REALTIME Table]
                                         |
                                   [Superset Dashboards]
```

## Componentes

- **Airflow**: Orquestra a geração e ingestão dos dados.
- **Kafka (Redpanda)**: Gerencia o streaming de dados de transações.
- **Apache Pinot**: Armazena dados em tabelas OFFLINE (dimensões) e REALTIME (fatos).
- **Superset**: Visualização dos dados.
- **PostgreSQL & Redis**: Backend do Airflow.
- **Docker Compose**: Orquestra todos os serviços.

## Como Executar

1. **Clone o repositório**
    ```sh
    git clone <url-do-repo>
    cd airflow-streaming-project
    ```

2. **Suba os containers**
    ```sh
    docker-compose up --build
    ```

3. **Acesse os serviços**
    - Airflow: [http://localhost:8081](http://localhost:8081)
    - Superset: [http://localhost:8088](http://localhost:8088)
    - Redpanda Console: [http://localhost:8080](http://localhost:8080)
    - Pinot Controller: [http://localhost:9000](http://localhost:9000)

4. **Execute as DAGs no Airflow**
    - `account_dim_generator`, `branch_dim_generator`, `customer_dim_generator`: Geram dados das dimensões em CSV.
    - `loader_dag`: Realiza ingestão batch dos CSVs para o Pinot.
    - `schema_dag` e `table_dag`: Criam schemas e tabelas no Pinot.
    - `transaction_facts_generator`: Gera fatos de transações e envia para o Kafka.

5. **Visualize os dados no Superset**
    - Configure o datasource apontando para o Apache Pinot.
    - Crie dashboards e análises a partir das tabelas.

## Estrutura das Tabelas

- **Dimensões**: `branch_dim`, `account_dim`, `customer_dim` (OFFLINE)
- **Fato**: `transaction_facts` (REALTIME)

## Principais Pastas

- `dags/`: DAGs do Airflow e scripts de geração de dados.
- `plugins/`: Operadores customizados para integração com Kafka e Pinot.
- `superset/`: Configuração e Dockerfile do Superset.
- `logs/`: Logs do Airflow.
- `config/`: Configurações adicionais.

## Observações

- O projeto é totalmente modular e pode ser expandido para outros cenários de dados.
- As credenciais e variáveis de ambiente podem ser ajustadas nos arquivos `.env` e `docker-compose.yml`.

---

Sinta-se à vontade para adaptar este README conforme a evolução do seu projeto!