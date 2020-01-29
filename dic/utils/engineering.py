from world.content.gases import specific_entropy_gas, MINIMUM_TRANSFER_MOLES, R_IDEAL_GAS_EQUATION


def moles_to_pressure(moles, temperature, volume_litres):
    return round((moles * R_IDEAL_GAS_EQUATION * temperature) / volume_litres, 2)
