# Escopo da metodologia de utilização de LLM no projeto

# Limitações

Esse escopo foi desenvolvido com base nos seguintes cenários:

* Não tivemos acesso direto a uma amostra substancial de dados para análise.  
* Não realizamos reuniões com os idealizadores do projeto, o que dificultou uma compreensão mais detalhada de suas necessidades específicas.

# Descrição

Em virtude do acesso limitado a informações, a proposta de desenvolvimento do modelo de linguagem a ser usado se baseia em Thinking Models (Modelos de Raciocínio) e será contextualizado por Retrieval-Augmented Generation (RAG)  e opcionalmente por Few-shot.

## Thinking Models

Thinking Models (Modelos de Raciocínio) é um termo geral usado para descrever LLMs que são especificamente treinados ou ajustados para realizar um **raciocínio interno** antes de responder. O objetivo é que o modelo seja, dada determinada entrada, capaz de oferecer explicabilidade (explicar suas decisões e seu funcionamento interno).

A ideia é que o modelo atuaria no papel de **auxiliar** na tomada de decisões do usuário. 

## RAG

As forma de recuperação de informação evoluíram muito com o passar dos anos, por exemplo, recuperações por match exato ou aproximado de palavras com ou sem o uso de lematização ou radicalização, ngrams (busca por ocorrência de grupos de caracteres/palavras), BM25 (busca, mas leva em consideração a frequência das palavras), dentre outros. A escolha do RAG baseia-se na sua capacidade de, diferente dos métodos anteriormente citados, fazer uma busca contextual e ser um método de recuperação de informação já usado para retornar contextos a diversos modelos de linguagem.

Entendemos que os casos de auditoria dificilmente poderiam ser identificados apenas por meio de uma busca lexical. Isso porque as tentativas de burlar ou contornar as normas costumam se esconder nos detalhes, e não nas palavras explícitas. Além disso, não temos informações suficientes sobre a natureza dos dados, o que nos impede de estruturar ou organizar essas informações de forma hierárquica e compreensível.  
Diante disso, optamos por adotar a recuperação baseada em contexto — o que justifica o uso do RAG.

## Estruturação

O primeiro passo é fazer o modelo entrar em contato com os dados, seja por treinamento como finetuning, ou por inferência como prompt engineering, zero-shot e few-shot; o modelo precisa, de alguma forma, entrar em contato com os dados.

Nessa subseção, será descrito apenas o método de inferência pois compreendemos o expressivo custo de treinamento em grandes modelos e desconhecemos tanto a natureza geral dos dados quanto às limitações técnicas dos idealizadores do projeto. Portanto prompts específicos seriam desenvolvidos para que o modelo receba contextualização por meio de:

* RAG \- Que faria busca contextual na base de dados  
* Few-shot  (opcional) \- Oferecidos pelo próprio usuário


Por fim, o modelo apresentaria ao usuário uma decisão acompanhada das razões que a justificam. A partir disso, o usuário poderia analisar o raciocínio do modelo e utilizá-lo como apoio na tomada de decisão sobre o caso específico.
