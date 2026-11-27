"""Memory allocation simulation. All sizes are positive integer KB."""

METHODS = ('First Fit', 'Best Fit', 'Worst Fit')


def validate_sizes(values, name):
    if not isinstance(values, list) or not 1 <= len(values) <= 30:
        raise ValueError(f'{name}: enter between 1 and 30 sizes.')
    if any(type(v) is not int or not 1 <= v <= 1_000_000 for v in values):
        raise ValueError(f'{name}: sizes must be integers from 1 to 1,000,000 KB.')


def simulate(blocks, processes, method, mode='dynamic'):
    validate_sizes(blocks, 'Memory blocks')
    validate_sizes(processes, 'Processes')
    if method not in METHODS:
        raise ValueError('Unknown algorithm.')
    if mode not in ('dynamic', 'fixed'):
        raise ValueError('Unknown allocation mode.')
    remaining = blocks.copy()
    allocations = [[] for _ in blocks]
    wasted = [0] * len(blocks)
    trace = []
    checks = 0
    for pid, size in enumerate(processes, 1):
        before = remaining.copy()
        inspected = []
        candidates = []
        for j, free in enumerate(remaining):
            checks += 1
            inspected.append(j + 1)
            if free >= size:
                candidates.append(j)
                if method == 'First Fit':
                    break
        selected = None
        if candidates:
            if method == 'First Fit':
                selected = candidates[0]
            elif method == 'Best Fit':
                selected = min(candidates, key=lambda j: remaining[j])
            else:
                selected = max(candidates, key=lambda j: remaining[j])
            allocations[selected].append({'process': pid, 'size': size})
            remaining[selected] -= size
            if mode == 'fixed':
                wasted[selected] = remaining[selected]
                remaining[selected] = 0
        if selected is not None:
            reason = 'Allocated'
        elif sum(before) < size:
            reason = 'Insufficient total free memory'
        elif mode == 'dynamic':
            reason = 'External fragmentation: no single hole fits'
        else:
            reason = 'No free partition large enough'
        trace.append({'process': pid, 'size': size, 'block': None if selected is None else selected + 1,
                      'before': before, 'after': remaining.copy(), 'inspected': inspected,
                      'candidates': [j+1 for j in candidates], 'reason': reason})
    total = sum(blocks)
    free = sum(remaining)
    internal = sum(wasted)
    used = total - free - internal
    largest = max(remaining)
    count = sum(t['block'] is not None for t in trace)
    # External index is a distribution measure, not a count of permanently wasted KB.
    external = round(100 * (1 - largest / free), 2) if free and mode == 'dynamic' else None
    if mode == 'dynamic' and not free:
        external = 0.0
    return {'method': method, 'mode': mode, 'total': total, 'used': used, 'free': free,
            'internal': internal, 'largest': largest, 'external_index': external,
            'allocated': count, 'failed': len(processes)-count, 'checks': checks,
            'success_rate': round(100*count/len(processes), 2),
            'utilization': round(100*used/total, 2), 'trace': trace,
            'blocks': [{'id': j+1, 'capacity': size, 'remaining': remaining[j],
                        'internal': wasted[j], 'allocations': allocations[j]}
                       for j, size in enumerate(blocks)]}


def compare(blocks, processes, mode='dynamic'):
    return [simulate(blocks, processes, method, mode) for method in METHODS]
