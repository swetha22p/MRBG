def get_ppost(datacase, cond=None, data_seman=None, root_main=None, concept_type=None):
    ppost = ''

    if datacase == 'k7t':
        ppost = 'at'

    elif datacase == 'k3':
        ppost = 'with'

    elif datacase in ('k5', 'k5prk'):
        ppost = 'from'

    elif datacase == 'k7':
        ppost = 'on'

    elif datacase == 'k7p':
        ppost = 'in'

    elif datacase == 'k7a':
        ppost = 'according to'

    elif datacase in ('k4', 'k2', 'k2p'):
        ppost = 'to'

    elif datacase == 'rblak':
        ppost = 'after'

    elif datacase == 'rt':
        ppost = 'for'

    elif datacase == 'rblpk':
        ppost = 'before'

    elif datacase == 'rn':
        ppost = 'among'

    elif datacase == 'rd':
        ppost = 'towards'

    elif datacase == 'rp':
        ppost = 'through'

    elif datacase in ('rask1', 'rask2', 'rask3', 'rask4', 'rask5', 'k1as', 'k2as', 'k3as', 'k4as', 'k5as', 'k7as'):
        ppost = 'along with'

    elif datacase == 'r6':
        ppost = 'of'

    elif datacase == 'quantless':
        ppost = 'less than'

    elif datacase == 'quantmore':
        ppost = 'more than'

    elif datacase == 'rkl':
        ppost = 'after'

    elif datacase == 'rh':
        ppost = 'because of'

    elif datacase == 'rasneg':
        ppost = 'without'

    elif datacase == 'rp':
        ppost = 'via'

    elif datacase == 'rv':
        ppost = 'than'

    return ppost