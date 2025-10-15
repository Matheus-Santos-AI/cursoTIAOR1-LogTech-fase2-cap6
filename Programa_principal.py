# Grupo:
# Matheus de Souza Santos
# Ricardo José Amorim Campos
# Victor Oliveira Fedeli Tate
# Paulo Roberto Silva Amaral Ribeiro Junior

# Importação dos módulos
import os
import oracledb
import pandas as pd

# Try para tentativa de Conexão com o Banco de Dados
try:
    # Efetua a conexão com o Usuário no servidor
    conn = oracledb.connect(user='rm566901', password="160393", dsn='oracle.fiap.com.br:1521/ORCL')
    # Cria as instruções para cada módulo
    inst_cadastro = conn.cursor()
    inst_consulta = conn.cursor()
    inst_alteracao = conn.cursor()
    inst_exclusao = conn.cursor()
except Exception as e:
    # Informa o erro
    print("Erro: ", e)
    # Flag para não executar a Aplicação
    conexao = False
else:
    # Flag para executar a Aplicação
    conexao = True
margem = ' ' * 4 # Define uma margem para a exibição da aplicação

# Enquanto o flag conexao estiver apontado com True
while conexao:
    # Limpa a tela via SO
    os.system('cls')

    # Apresenta o menu
    print("------- Logistica Facil -------")
    print("""
    1 - Cadastrar Empresas de Logistica
    2 - Listar Empresas de Logistica
    3 - Editar Empresa
    4 - Excluir Empresa
    5 - EXCLUIR TODAS AS EMPRESAS
    6 - Calcular o melhor FRETE
    7 - SAIR
    """)

    # Captura a escolha do usuário
    escolha = input(margem + "Escolha -> ")

    # Verifica se o número digitado é um valor numérico
    if escolha.isdigit():
        escolha = int(escolha)
    else:
        escolha = 8
        print("Digite um número.\nReinicie a Aplicação!")

    os.system('cls')  # Limpa a tela via SO

    # VERIFICA QUAL A ESCOLHA DO USUÁRIO
    match escolha:

        # CADASTRAR UMA EMPRESA
        case 1:
            try:
                print("----- CADASTRAR EMPRESA -----\n")
                # Recebe os valores para cadastro
                nome = input(margem + "Digite o nome da empresa....: ")
                print("DIGITE 'OK' PARA AS QUANTIDADES QUE A EMPRESA TRANSPORTA\n----12ton /14ton /22ton /30ton /42ton----")
                dose = input(margem + "Digite 'OK' para confirmar ou '0' para continuar\n 12 Toneladas:")
                if dose not in ["OK","ok","Ok" "0"]:
                    print("Entrada inválida. Digite 'OK' ou '0'.")
                else:
                    print("--------------------------------------")
                quatorze = input(margem + "Digite 'OK' para confirmar ou '0' para continuar\n 14 Toneladas:")
                if quatorze not in ["OK","ok","Ok" "0"]:
                    print("Entrada inválida. Digite 'OK' ou '0'.")
                else:
                    print("--------------------------------------")
                vinte_e_dois = input(margem + "Digite 'OK' para confirmar ou '0' para continuar\n 22 Toneladas:")
                if vinte_e_dois not in ["OK","ok","Ok" "0"]:
                    print("Entrada inválida. Digite 'OK' ou '0'.")
                else:
                    print("--------------------------------------")
                trinta = input(margem + "Digite 'OK' para confirmar ou '0' para continuar\n 30 Toneladas:")
                if trinta not in ["OK","ok","Ok" "0"]:
                    print("Entrada inválida. Digite 'OK' ou '0'.")
                else:
                    print("--------------------------------------")
                quarenta_e_dois = input(margem + "Digite 'OK' para confirmar ou '0' para continuar\n 42 Toneladas:")
                if quarenta_e_dois not in ["OK","ok","Ok" "0"]:
                    print("Entrada inválida. Digite 'OK' ou '0'.")
                else:
                    print("--------------------------------------")

                custo_curto = float(input(margem + "Digite o custo do frete até 700km...\n R$: "))
                custo_longo = float(input(margem + "Digite o custo do frete acima de 700km...\n R$: "))

                # Monta a instrução SQL de cadastro em uma string
                cadastro = f""" INSERT INTO empresas_log (nome, dose, quatorze, vinte_e_dois,trinta,quarenta_e_dois, custo_curto,custo_longo)VALUES ('{nome}', '{dose}', '{quatorze}', '{vinte_e_dois}', '{trinta}','{quarenta_e_dois}', {custo_curto},{custo_longo}) """

                # Executa e grava o Registro na Tabela nome, dose, quatorze, vinte_e_dois,trinta,quarenta_e_dois, custo_curto,custo_longo
                inst_cadastro.execute(cadastro)
                conn.commit()


            except ValueError:
                # Erro de número não digitar um número na idade
                print("Digite um número valido!")
            except:
                # Caso ocorra algum erro de conexão ou no BD
                print("Erro na transação do BD")
            else:
                # Caso haja sucesso na gravação
                print("\n##### Dados GRAVADOS #####")

        # LISTAR TODAS EMPRESAS
        case 2:
            print("----- LISTAR EMPRESAS -----\n")
            lista_dados = []  # Lista para captura de dados do Banco



            pd.set_option('display.max_columns', None)
            # Monta a instrução SQL de seleção de todos os registros da tabela
            inst_consulta.execute('SELECT * FROM empresas_log')
            # Captura todos os registros da tabela e armazena no objeto data
            data = inst_consulta.fetchall()

            # Insere os valores da tabela na Lista
            for dt in data:
                lista_dados.append(dt)

            # ordena a lista
            lista_dados = sorted(lista_dados)

            # Gera um DataFrame com os dados da lista utilizando o Pandas
            dados_df = pd.DataFrame.from_records(lista_dados, columns=['Id','nome', 'dose', 'quatorze', 'vinte_e_dois','trinta','quarenta_e_dois', 'custo_curto','custo_longo'], index='Id')

            # Verifica se não há registro através do dataframe
            if dados_df.empty:
                print(f"Não há empresas cadastradas!")
            else:
                print(dados_df) # Exibe os dados selecionados da tabela

            print("\n##### LISTADOS! #####")



        # ALTERAR OS DADOS DE UM REGISTRO
        case 3:
            try:
                # ALTERANDO UM REGISTRO
                print("----- ALTERAR DADOS DA EMPRESA -----\n")

                lista_dados = []  # Lista para captura de dados da tabela

                empresa_id = int(input(margem + "Escolha um Id: "))  # Permite o usuário escolher um Pet pelo id

                # Constrói a instrução de consulta para verificar a existência ou não do id
                consulta = f""" SELECT * FROM empresas_log WHERE id = {empresa_id}"""
                inst_consulta.execute(consulta)
                data = inst_consulta.fetchall()

                # Preenche a lista com o registro encontrado (ou não)
                for dt in data:
                    lista_dados.append(dt)

                # analisa se foi encontrado algo
                if len(lista_dados) == 0: # se não há o id
                    print(f"Não há uma empresa cadastrada com o ID = {empresa_id}")
                    input("\nPressione ENTER")
                else:
                    # Captura os novos dados nome, dose, quatorze, vinte_e_dois,trinta,quarenta_e_dois, custo_curto,custo_longo
                    novo_nome = input(margem + "Digite o nome da empresa....: ")
                    print("DIGITE 'OK' PARA AS QUANTIDADES QUE A EMPRESA TRANSPORTA\n12ton,14ton,22ton,30ton, 42ton")
                    novo_dose = input(margem + "Digite 'OK' ou '0' para continuar\n 12 Toneladas:")
                    if novo_dose not in ["OK", "0"]:
                        print("Entrada inválida. Digite 'OK' ou '0'.")
                    else:
                        print("Entrada aceita:", novo_dose)
                    novo_quatorze = input(margem + "Digite 'OK' ou '0' para continuar\n 14 Toneladas:")
                    if novo_quatorze not in ["OK", "0"]:
                        print("Entrada inválida. Digite 'OK' ou '0'.")
                    else:
                        print("Entrada aceita:", novo_quatorze)
                    novo_vinte_e_dois = input(margem + "Digite 'OK' ou '0' para continuar\n 22 Toneladas:")
                    if novo_vinte_e_dois not in ["OK", "0"]:
                        print("Entrada inválida. Digite 'OK' ou '0'.")
                    else:
                        print("Entrada aceita:", novo_vinte_e_dois)
                    novo_trinta = input(margem + "Digite 'OK' ou '0' para continuar\n 30 Toneladas:")
                    if novo_trinta not in ["OK", "0"]:
                        print("Entrada inválida. Digite 'OK' ou '0'.")
                    else:
                        print("Entrada aceita:", novo_trinta)
                    novo_quarenta_e_dois = input(margem + "Digite 'OK' ou '0' para continuar\n 42 Toneladas:")
                    if novo_quarenta_e_dois not in ["OK", "0"]:
                        print("Entrada inválida. Digite 'OK' ou '0'.")
                    else:
                        print("Entrada aceita:", novo_quarenta_e_dois)

                    novo_custo_curto = float(input(margem + "Digite o custo do frete até 700km...: "))
                    novo_custo_longo = float(input(margem + "Digite o custo do frete acima de 700km...: "))

                    # Constrói a instrução de edição do registro com os novos dados
                    alteracao = f"""
                    UPDATE empresas_log SET nome='{novo_nome}', dose='{novo_dose}', quatorze='{novo_quatorze}', vinte_e_dois ='{novo_vinte_e_dois}', trinta = '{novo_trinta}', quarenta_e_dois = '{novo_quarenta_e_dois}', custo_curto ='{novo_custo_curto}', custo_longo = '{custo_longo}' WHERE id={empresa_id}
                    """
                    inst_alteracao.execute(alteracao)
                    conn.commit()
            except ValueError:
                    print("Digite um número valido!")
            except:
                print(margem + "Erro na transação do BD")
            else:
                print("\n##### Dados ATUALIZADOS! #####")

        # EXCLUIR UM REGISTRO
        case 4:
            print("----- EXCLUIR EMPRESA -----\n")
            lista_dados = []  # Lista para captura de dados da tabela
            empresa_id = input(margem + "Escolha um Id: ")  # Permite o usuário escolher um Pet pelo ID
            if empresa_id.isdigit():
                empresa_id = int(empresa_id)
                consulta = f""" SELECT * FROM empresas_log WHERE id = {empresa_id} """
                inst_consulta.execute(consulta)
                data = inst_consulta.fetchall()

                # Insere os valores da tabela na lista
                for dt in data:
                    lista_dados.append(dt)

                # Verifica se o registro está cadastrado
                if len(lista_dados) == 0:
                    print(f"Não há uma empresa cadastrada com o ID = {empresa_id}")
                else:
                    # Cria a instrução SQL de exclusão pelo ID
                    exclusao = f"DELETE FROM empresas_log WHERE id={empresa_id}"
                    # Executa a instrução e atualiza a tabela
                    inst_exclusao.execute(exclusao)
                    conn.commit()
                    print("\n##### Empresa APAGADA! #####")  # Exibe mensagem caso haja sucesso
            else:
                print("O Id não é numérico!")

        # EXCLUIR TODOS OS REGISTROS
        case 5:
            print("\n!!!!! EXCLUI TODOS OS DADOS TABELA !!!!!\n")
            confirma = input(margem + "CONFIRMA A EXCLUSÃO DE TODAS AS EMPRESAS? [S]im ou [N]ÃO?")
            if confirma.upper() == "S":
                # Apaga todos os registros
                exclusao = "DELETE FROM empresas_log"
                inst_exclusao.execute(exclusao)
                conn.commit()

                # Depois de excluir todos os registros ele zera o ID
                data_reset_ids = """ ALTER TABLE empresas_log MODIFY(ID GENERATED AS IDENTITY (START WITH 1)) """
                inst_exclusao.execute(data_reset_ids)
                conn.commit()

                print("##### Todos os registros foram excluídos! #####")
            else:
                print(margem + "Operação cancelada pelo usuário!")

        case 6:

            distancia_cliente = float
            distancia = str
            nome_cliente = input(margem + "Digite o nome do cliente: ")
            distancia_cliente = float(input(margem + "Digite a distancia até o cliente em Km: "))
            data_orcamento = str(input(margem + "Digite a data da compra: "))
            try:
                quantidade = int(
                input("Digite a quantidade de toneladas do pedido (cargas padrões: 12, 14, 22, 30, 42 ton): "))
            except ValueError:
                print("Entrada invalida")
            # Mapeamento da quantidade para nome da coluna
            quantidade_colunas = {
                12: "dose",
                14: "quatorze",
                22: "vinte_e_dois",
                30: "trinta",
                42: "quarenta_e_dois"
            }

            quantidade_texto = quantidade_colunas.get(quantidade)



            if quantidade_texto is None:
                print("Quantidade inválida.")
            else:
                lista_dados = []  # Lista para captura de dados da tabela
                consulta = f"SELECT * FROM empresas_log WHERE {quantidade_texto} = 'ok'"
                inst_consulta.execute(consulta)
                data = inst_consulta.fetchall()
                lista_dados.extend(data)

                lista_dados = sorted(lista_dados)



                import pandas as pd

                colunas = [desc[0] for desc in inst_consulta.description]
                df = pd.DataFrame(lista_dados, columns=colunas)
                if distancia_cliente > 700:
                    df = df.sort_values(by='CUSTO_LONGO')
                    valor_frete = df.iloc[0, 8]
                elif distancia_cliente <= 700:
                    df = df.sort_values(by='CUSTO_CURTO')
                    valor_frete = df.iloc[0, 7]

                print("-----------------------------------------------------------------------")
                print("\n")
                print("RELAÇÃO DE EMPRESAS QUE ATENDEM ESSA QUANTIDADE DE CARGA")
                print(df)



                valor_frete_final = valor_frete * quantidade

                nome_melhor_frete = df.iloc[0,1]

                print(f"Melhor empresa para realizar a entrega : {nome_melhor_frete}")
                print(f"Pelo custo de R${valor_frete}/Ton , Totalizando R${valor_frete_final}")
                entrega_estimada = print(f"Tempo de transporte :{int(distancia_cliente / 40)} - {int(distancia_cliente / 55)} horas")

                #dicionario dados do orçamento
                clientes_orcados = {
                    '{nome_cliente}':{
                    "nome do cliente": nome_cliente,
                    "Data da compra": data_orcamento,
                    "distancia até o cliente": distancia_cliente,
                    "quantidade da carga": quantidade,
                    "Melhor empresa de entrega": nome_melhor_frete,
                    "Custo do Frete": valor_frete,
                    }
                }
                import json

                clientes_orcados_json = json.dumps(clientes_orcados)  # dump permite codificar um objeto python jogando em uma string

                clientes_orcados_json = json.dumps(clientes_orcados,
                                          indent=4)  # faz com que o conteudo do objeto seja formatado com 4 espaços de identação



                with open(f"{nome_cliente}.txt", "w+") as file:
                    file.write(clientes_orcados_json)

#--------------------------------------------------------------------------------------------------------------------------------------
                with open(f"{nome_cliente}.json", "w+") as arq:
                    conteudo = (
                        f"Proposta de FRETE para {nome_cliente}\n"
                        f"Melhor empresa para realizar a entrega: {nome_melhor_frete}\n"
                        f"Custo de R${valor_frete}/Ton, totalizando R${valor_frete_final}\n"
                    )
                    arq.write(conteudo)
                    arq.seek(0)










        # SAI DA APLICAÇÃO
        case 7:
            # Modificando o flag da conexão
            conexao = False


        case _:
            input(margem + "Digite um número entre 1 e 7.")

    # Pausa o fluxo da aplicação para a leitura das informações
    input(margem + "Pressione ENTER")
else:

    print("Obrigado por utilizar a nossa aplicação! :)")
