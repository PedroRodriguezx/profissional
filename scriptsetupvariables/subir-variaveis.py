import boto3

# Nome do arquivo contendo as variáveis de ambiente
arquivo_variaveis = "variaveis.txt"

ssm = boto3.client('ssm', region_name="us-east-1")

def carregar_variaveis_ambiente(arquivo):
    variaveis = {}

    with open(arquivo, 'r') as arquivo_variaveis:
        for linha in arquivo_variaveis:
            nome_variavel, valor_variavel = linha.strip().split('=')
            nome_variavel = nome_variavel.strip()  
            valor_variavel = valor_variavel.strip()  
            variaveis[nome_variavel] = valor_variavel

    return variaveis

def carregar_parametros_ssm(variaveis):
    for nome_variavel, valor_variavel in variaveis.items():
        if any(keyword in nome_variavel.upper() for keyword in ["KEY", "PASSWORD", "USERNAME", "USER", "TOKEN", "SECRET"]):
            # Se a variável contém palavras-chave, armazene como SecureString
            ssm.put_parameter(
                Name=nome_variavel,
                Value=valor_variavel,
                Type="SecureString",
                Overwrite=True
            )
            print(f"{nome_variavel} registrado com sucesso como SecureString")
        else:
            # Caso contrário, armazene como String padrão
            ssm.put_parameter(
                Name=nome_variavel,
                Value=valor_variavel,
                Type="String",
                Overwrite=True
            )
            print(f"{nome_variavel} registrado com sucesso como String")

if __name__ == "__main__":
    variaveis = carregar_variaveis_ambiente(arquivo_variaveis)
    carregar_parametros_ssm(variaveis)
    
    num_variaveis = len(variaveis)
    print(f"{num_variaveis} variáveis de ambiente carregadas no Parameter Store.")
