from argon2.low_level import Type, hash_secret_raw

# KFD constant function values
DEFAULT_MEMORY_COST = 65536
DEFAULT_TIME_COST = 2
DEFAULT_PARALLELISM = 1
ARGON2_TYPE = Type.ID
KEY_LENGTH = 32
SALT_LENGTH = 16

def derive_key(master_password,
               salt,
               memory_cost=DEFAULT_MEMORY_COST,
               time_cost=DEFAULT_TIME_COST,
               parallelism=DEFAULT_PARALLELISM,):
    """
    :param master_password: pandora's user master password secret input.
    :param salt: Random value used alongside the master password.
    :param memory_cost: Amount of memory, in KiB, used by kfd.
    :param time_cost: Number of times the memory processing is repeated.
    :param parallelism: Number of parallel lanes used by kfd.
    :return: The derived key from master_password and salt.
    """

    master_password = master_password.encode('utf-8')

    derived_key = hash_secret_raw(master_password,salt,
                                     time_cost, memory_cost,
                                     parallelism, KEY_LENGTH,
                                     type=ARGON2_TYPE)
    return derived_key