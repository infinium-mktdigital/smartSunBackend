import math

def calcular_energia_mensal_por_placa(irradiacao_solar):
    return irradiacao_solar * 0.55 * 30 * 0.75

def calcular_numero_placas_necessarias(consumo_mensal, energia_mensal_por_placa):
    return math.ceil(consumo_mensal / energia_mensal_por_placa)

def calcular_geracao_mensal(energia_mensal_por_placa, numero_placas):
    return energia_mensal_por_placa * numero_placas

def calcular_estimativa_investimento(numero_placas):
    return numero_placas * 1000 + 4500

def calcular_economia_mensal(consumo_mensal, custo_por_kwh):
    return consumo_mensal * custo_por_kwh

def calcular_economia_anual(economia_mensal):
    return economia_mensal * 12

def calcular_payback(investimento_total, economia_anual):
    return investimento_total / economia_anual if economia_anual > 0 else 0

def calcular_reducao_co2(numero_placas, energia_mensal_por_placa):
    return numero_placas * energia_mensal_por_placa * 0.071 * 12

def calcular_arvores_plantadas(reducao_co2_kg):
    return reducao_co2_kg / 21

def calcular_reducao_combustivel_fossil(numero_placas, energia_mensal_por_placa):
    return (numero_placas * energia_mensal_por_placa) / 10

def calcular_sistema_solar(consumo_mensal, irradiacao_solar, custo_por_kwh):    
    # Cálculos base
    energia_mensal_por_placa = calcular_energia_mensal_por_placa(irradiacao_solar)
    numero_placas = calcular_numero_placas_necessarias(consumo_mensal, energia_mensal_por_placa)
    geracao_mensal = calcular_geracao_mensal(energia_mensal_por_placa, numero_placas)
    
    # Cálculos de investimento
    estimativa_investimento = calcular_estimativa_investimento(numero_placas)
    economia_mensal = calcular_economia_mensal(consumo_mensal, custo_por_kwh)
    economia_anual = calcular_economia_anual(economia_mensal)
    payback = calcular_payback(estimativa_investimento, economia_anual)
    
    # Cálculos ambientais
    reducao_co2 = calcular_reducao_co2(numero_placas, energia_mensal_por_placa)
    arvores_plantadas = calcular_arvores_plantadas(reducao_co2)
    reducao_combustivel = calcular_reducao_combustivel_fossil(numero_placas, energia_mensal_por_placa)
    
    # Montagem do dicionário de retorno
    data = {
        "suggestion": {
            "monthly": round(geracao_mensal, 2),
            "potency": 550,  # Potência fixa de placa conforme especificado
            "quantity": numero_placas
        },
        "estimated": {
            "co2Reduced": round(reducao_co2, 2),
            "treePlanted": round(arvores_plantadas, 2),
            "reduction": round(reducao_combustivel, 2)
        },
        "invest": {
            "estimated": round(estimativa_investimento, 2),
            "payback": round(payback, 2),
            "annualEconomy": round(economia_anual, 2)
        }
    }
    
    return data