# ECOIA Classifier - Histórico de Mudanças


## Índice

- [Visão Geral](#visão-geral)
- [Resumo das Principais Evoluções](#resumo-das-principais-evoluções)
- [Detalhamento por Versão](#detalhamento-por-versão)
  - [Versão 1.10.1 → 1.10.3](#versão-1101--1103)
  - [Versão 1.10.3 → 1.10.4](#versão-1103--1104)
  - [Versão 1.10.4 → 1.10.5](#versão-1104--1105)
  - [Versão 1.10.5 → 1.10.6](#versão-1105--1106)
  - [Versão 1.10.6 → 1.10.7](#versão-1106--1107)
  - [Versão 1.10.7 → 1.10.8](#versão-1107--1108)
  - [Versão 1.10.8 → 1.12.0](#versão-1108--1120)
  - [Versão 1.12.0 → 1.12.1](#versão-1120--1121)
  - [Versão 1.12.1 → 1.13.0](#versão-1121--1130)
  - [Versão 1.13.0 → 1.13.1](#versão-1130--1131)
  - [Versão 1.13.1 → 1.14.0](#versão-1131--1140)

## Visão Geral

Este documento apresenta o histórico detalhado de mudanças do sistema ECOIA Classifier, destacando as principais alterações técnicas e seus respectivos impactos no ambiente de produção. O objetivo é fornecer uma visão clara da evolução do sistema, facilitando o planejamento de atualizações e a compreensão das melhorias implementadas ao longo do tempo.

## Resumo das Principais Evoluções

| Área | Evolução |
|------|----------|
| **Infraestrutura** | Migração para contêineres Docker, suporte a Python 3.11, integração com PM2 |
| **Arquitetura** | Normalização de código, sistema de atualização automática de modelos |
| **Classificação** | Novos modelos especializados (Picanha, Carcaça, Modelo 306), sistema de pré-filtro |
| **API** | Endpoint para inferência direta via upload de imagens, tratamento específico de erros |
| **Análise** | Pontuação de interseção entre hematomas e cortes, análise quantitativa de lesões |

## Detalhamento por Versão

### Versão 1.10.1 → 1.10.3

#### 🔄 Mudanças
- Implementação de mecanismo para atualização automática dos modelos de classificação

#### 💼 Impacto em Produção
- **Manutenção Simplificada**: Redução do tempo de inatividade durante atualizações de modelos
- **Maior Flexibilidade**: Capacidade de implantar novos modelos sem interromper o serviço

#### ⚙️ Considerações Técnicas
- Necessário verificar configurações de diretórios para garantir permissões adequadas ao mecanismo de atualização

---

### Versão 1.10.3 → 1.10.4

#### 🔄 Mudanças
- Adição completa de suporte a contêinerização com Docker
- Implementação de configurações Docker Compose para orquestração de serviços
- Ajustes nas dependências do projeto para garantir compatibilidade

#### 💼 Impacto em Produção
- **Implantação Padronizada**: Ambiente de execução consistente entre desenvolvimento e produção
- **Escalabilidade Melhorada**: Facilidade para escalar horizontalmente a aplicação
- **Isolamento de Ambiente**: Redução de conflitos de dependências

#### ⚙️ Considerações Técnicas
- Requer Docker e Docker Compose instalados no ambiente de produção
- Volumes persistentes devem ser configurados para armazenamento de modelos e dados

---

### Versão 1.10.4 → 1.10.5

#### 🔄 Mudanças
- Extensa refatoração e padronização do código-fonte
- Nova funcionalidade para detecção e análise de extensão de lesões
- Resolução de problemas críticos relacionados ao dimensionamento de imagens

#### 💼 Impacto em Produção
- **Maior Estabilidade**: Redução de erros relacionados ao dimensionamento de imagens
- **Melhor Manutenibilidade**: Código mais limpo e padronizado facilita manutenções futuras
- **Detecção Aprimorada**: Capacidade de identificar e analisar a extensão das lesões

#### ⚙️ Considerações Técnicas
- Possível necessidade de ajustes em sistemas que dependem do formato anterior das imagens processadas

---

### Versão 1.10.5 → 1.10.6

#### 🔄 Mudanças
- Implementação e integração do novo modelo de classificação (Modelo 306)
- Adição de modelo específico para classificação de cortes de picanha
- Atualização do sistema de gerenciamento de modelos
- Resolução de bug que afetava o funcionamento do sistema

#### 💼 Impacto em Produção
- **Precisão Aprimorada**: Novo modelo oferece melhor desempenho na classificação
- **Expansão de Funcionalidade**: Suporte específico para classificação de picanha
- **Gerenciamento Otimizado**: Melhor controle sobre os modelos utilizados

#### ⚙️ Considerações Técnicas
- Necessário verificar espaço em disco para acomodar os novos modelos
- Possível aumento no consumo de recursos computacionais

---

### Versão 1.10.6 → 1.10.7

#### 🔄 Mudanças
- Implementação de validação para pré-filtro e detecção de carcaça
- Múltiplas correções de bugs no sistema de atualização de modelos
- Ajustes específicos na funcionalidade de conformação
- Adição de funcionalidade para plotar retângulos em imagens com máscara

#### 💼 Impacto em Produção
- **Validação Aprimorada**: Melhor detecção de carcaças em ambiente de produção
- **Estabilidade do Atualizador**: Maior confiabilidade no processo de atualização de modelos
- **Visualização Melhorada**: Capacidade de visualizar áreas de interesse em imagens processadas

#### ⚙️ Considerações Técnicas
- Recomendado testar extensivamente o sistema de pré-filtro antes da implantação em produção

---

### Versão 1.10.7 → 1.10.8

#### 🔄 Mudanças
- Continuação das melhorias no sistema de pré-filtro e detecção de carcaça

#### 💼 Impacto em Produção
- **Maior Precisão**: Refinamento do sistema de pré-filtragem, reduzindo falsos positivos e negativos

#### ⚙️ Considerações Técnicas
- Mudanças incrementais que complementam as alterações da versão anterior

---

### Versão 1.10.8 → 1.12.0

#### 🔄 Mudanças
- Adição de novo modelo específico para classificação de carcaças
- Inclusão de tratamento específico para o erro 93 no sistema de integração
- Implementação da função `read_model_info` para obter informações do modelo via JSON
- Alteração na construção do caminho para o arquivo `model_info.json`

#### 💼 Impacto em Produção
- **Classificação Especializada**: Capacidade específica para classificação de carcaças
- **Tratamento de Erros**: Melhor gestão de erros específicos durante a integração
- **Configuração Flexível**: Capacidade de modificar parâmetros do modelo sem alteração de código

#### ⚙️ Considerações Técnicas
- Verificar a existência e formato correto dos arquivos JSON de configuração dos modelos
- Atualizar documentação de integração para incluir tratamento do erro 93

---

### Versão 1.12.0 → 1.12.1

#### 🔄 Mudanças
- Alteração significativa no sistema de detecção de lesões em cortes de picanha
- Nova feature que calcula a porcentagem do corte afetado por lesões/falhas
- Implementação de exclusão de background na checagem de lesões

#### 💼 Impacto em Produção
- **Análise Quantitativa**: Capacidade de quantificar o impacto das lesões nos cortes
- **Detecção Abrangente**: Verificação de todos os cortes afetados por lesões
- **Precisão Aumentada**: Exclusão de áreas de background na análise, reduzindo falsos positivos

#### ⚙️ Considerações Técnicas
- Sistemas que consomem dados de lesões precisarão ser adaptados para utilizar as novas métricas percentuais
- Possível necessidade de ajustes nos limiares de decisão baseados nas novas métricas

---

### Versão 1.12.1 → 1.13.0

#### 🔄 Mudanças
- Implementação de nova feature para mapeamento detalhado de lesões
- Adição de migrações para suportar as novas funcionalidades

#### 💼 Impacto em Produção
- **Análise Detalhada**: Capacidade de mapear lesões com maior precisão
- **Estrutura de Dados Aprimorada**: Suporte a novos campos e relações no banco de dados

#### ⚙️ Considerações Técnicas
- **Atenção**: Necessário executar migrações de banco de dados antes da atualização
- Verificar compatibilidade com sistemas que consomem dados de mapeamento de lesões

---

### Versão 1.13.0 → 1.13.1

#### 🔄 Mudanças
- Implementação do campo `cut_intersection_score` na tabela de hematomas
- Renomeação de método `get_id_cuts_affeted_by_bruises` para `get_id_intersection_scores_and_cuts_affected_by_bruises`
- Atualização do controlador de hematomas
- Reorganização de requisitos para melhor compatibilidade com Python 3.11
- Remoção de arquivos desnecessários
- Movimentação de dependências como pypylon e boto3 do script de instalação para os arquivos de requisitos

#### 💼 Impacto em Produção
- **⚠️ BREAKING CHANGE**: API de detecção de hematomas modificada, afetando integrações existentes
- **Análise Quantitativa de Hematomas**: Capacidade de avaliar numericamente a relação entre hematomas e cortes
- **Compatibilidade com Python 3.11**: Preparação para atualização da versão do Python
- **Gerenciamento de Dependências Melhorado**: Instalação mais confiável e reproduzível

#### ⚙️ Considerações Técnicas
- Necessário atualizar sistemas integrados que utilizam a API de detecção de hematomas
- Executar migrações de banco de dados para adicionar o novo campo `cut_intersection_score`
- Revisar scripts de implantação para utilizar os novos arquivos de requisitos

---

### Versão 1.13.1 → 1.14.0

#### 🔄 Mudanças
- Adição de novo endpoint na API para uploads diretos de imagens para inferência do modelo
- Adição de script de implantação para PM2 com Python 3.11
- Melhoria na documentação do README com instruções de instalação e scripts de implantação

#### 💼 Impacto em Produção
- **Flexibilidade de Integração**: Nova rota de API permite uploads diretos de imagens
- **Implantação Simplificada**: Script de implantação para PM2 facilita o gerenciamento do serviço
- **Onboarding Melhorado**: Documentação atualizada facilita configuração e manutenção

#### ⚙️ Considerações Técnicas
- Verificar configurações de segurança para o novo endpoint de upload de imagens
- Considerar limites de tamanho de arquivo e rate limiting para prevenir abusos
- Avaliar migração para Python 3.11 em produção utilizando os novos scripts de implantação

---
