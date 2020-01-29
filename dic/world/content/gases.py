import math


SPECIFIC_ENTROPY_VACUUM = 0
R_IDEAL_GAS_EQUATION = 8.31  # kPa*L/(K*mol).
TCMB = 2.7  # -270.3 degrees celsius
IDEAL_GAS_ENTROPY_CONSTANT = 0
MINIMUM_TRANSFER_MOLES = 0.04

OXYGEN = {
    "key": "oxygen",
    "molar_mass": 15.999,
    "specific_heat": 0.92
}

NITROGEN = {
    "key": "nitrogen",
    "molar_mass": 14.0067,
    "specific_heat": 1.04
}

CO2 = {
    "key": "co2",
    "molar_mass": 44.01,
    "specific_heat": 0.871
}

FLUORINE = {
    "key": "fluorine",
    "molar_mass": 18.998403,
    "specific_heat": 0.82
}

ARGON = {
    "key": "argon",
    "molar_mass": 39.948,
    "specific_heat": 0.52
}

HELIUM = {
    "key": "helium",
    "molar_mass": 4.002602,
    "specific_heat": 5.193
}

GASES = [
    OXYGEN, NITROGEN, CO2, FLUORINE, ARGON, HELIUM
]


def get_gas(key):
    return next((g for g in GASES if g["key"] == key), None)


def specific_entropy_gas(key, temperature, moles, volume):
    gas = get_gas(key)
    if not gas:
        return SPECIFIC_ENTROPY_VACUUM

    # group_multiplier gets divided out in volume/gas[key] - also, V/(m*T) = R/(partial pressure)
    molar_mass = gas["molar_mass"]
    specific_heat = gas["specific_heat"]
    safe_temp = max(temperature, TCMB)

    return R_IDEAL_GAS_EQUATION * (math.log((IDEAL_GAS_ENTROPY_CONSTANT * volume/(moles * safe_temp))
                                   * (molar_mass*specific_heat*safe_temp)**(2/3) + 1) + 15)
