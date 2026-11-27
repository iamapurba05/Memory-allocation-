import unittest
from algorithms import simulate, compare, METHODS


class AllocationTests(unittest.TestCase):
    def test_standard_workload(self):
        results = compare([100, 500, 200, 300, 600], [212, 417, 112, 426])
        self.assertEqual([r['allocated'] for r in results], [3, 4, 3])
        self.assertEqual([[t['block'] for t in r['trace']] for r in results],
                         [[2, 5, 2, None], [4, 2, 3, 5], [5, 2, 5, None]])
        self.assertEqual([r['free'] for r in results], [959, 533, 959])

    def test_exact_fit(self):
        for method in METHODS:
            r = simulate([100], [100], method)
            self.assertEqual((r['used'], r['free'], r['external_index']), (100, 0, 0))

    def test_reuse_remainder(self):
        r = simulate([100], [40, 60], 'First Fit')
        self.assertEqual(r['allocated'], 2)
        self.assertEqual(r['free'], 0)

    def test_external_fragmentation(self):
        r = simulate([100, 100, 100], [150], 'Best Fit')
        self.assertEqual(r['allocated'], 0)
        self.assertIn('External fragmentation', r['trace'][0]['reason'])
        self.assertAlmostEqual(r['external_index'], 66.67)

    def test_insufficient_memory(self):
        r = simulate([100, 200], [400], 'Worst Fit')
        self.assertEqual(r['trace'][0]['reason'], 'Insufficient total free memory')

    def test_fixed_partition_waste(self):
        r = simulate([100], [40, 60], 'First Fit', 'fixed')
        self.assertEqual((r['allocated'], r['used'], r['internal'], r['free']), (1, 40, 60, 0))
        self.assertIsNone(r['external_index'])

    def test_ties_choose_first(self):
        for method in METHODS:
            self.assertEqual(simulate([100, 100], [50], method)['trace'][0]['block'], 1)

    def test_independent_runs(self):
        blocks = [100, 500, 200]
        original = blocks.copy()
        compare(blocks, [50, 60])
        self.assertEqual(blocks, original)

    def test_conservation(self):
        for mode in ('fixed', 'dynamic'):
            for r in compare([10, 20, 30], [11, 8, 13, 7, 22], mode):
                self.assertEqual(r['total'], r['used'] + r['internal'] + r['free'])
                for b in r['blocks']:
                    self.assertEqual(b['capacity'], sum(a['size'] for a in b['allocations']) + b['internal'] + b['remaining'])

    def test_checks(self):
        self.assertEqual([r['checks'] for r in compare([100, 200], [10])], [1, 2, 2])

    def test_invalid_sizes(self):
        for bad in ([], [0], [-1], [1.5], ['1'], [True], [1000001], [1]*31, None):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    simulate(bad, [1], 'First Fit')
                with self.assertRaises(ValueError):
                    simulate([1], bad, 'First Fit')

    def test_invalid_method_and_mode(self):
        with self.assertRaises(ValueError):
            simulate([1], [1], 'Unknown')
        with self.assertRaises(ValueError):
            simulate([1], [1], 'First Fit', 'Unknown')

    def test_min_max_input(self):
        r = simulate([1, 1000000], [1, 1000000], 'Best Fit')
        self.assertEqual(r['allocated'], 2)
        self.assertEqual(r['free'], 0)


if __name__ == '__main__':
    unittest.main()
