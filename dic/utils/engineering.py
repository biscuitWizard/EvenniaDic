from world.content.gases import specific_entropy_gas, MINIMUM_TRANSFER_MOLES, R_IDEAL_GAS_EQUATION, GASES


def moles_to_pressure(moles, temperature, volume_litres):
    return round((moles * R_IDEAL_GAS_EQUATION * temperature) / volume_litres, 2)


def heat_capacity(gas_mixture):
    result = 0
    for gas in gas_mixture:
        gas_data = next((g for g in GASES if g["key"] == gas["key"]), None)
        if not gas_data:
            result += gas["moles"]
            continue
        result += gas["moles"] * gas_data["specific_heat"]
    return result
