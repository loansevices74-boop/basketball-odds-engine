import math
from typing import Dict, Any

class BasketballPredictor:
    """Calculates safe total point boundaries (>70% probability)."""

    @staticmethod
    def calculate_bounds(avg_home_score: float, avg_away_score: float, league_avg: float = 158.0) -> Dict[str, Any]:
        expected_total = (avg_home_score + avg_away_score)

        # Standard deviation for European/Professional basketball total points ~ 12.5 points
        std_dev = 12.5

        # 70% Confidence interval bounds (z ~ 1.28 for conservative 90% one-tailed)
        ft_under_70 = expected_total + (1.28 * std_dev)
        ft_over_70 = max(135.0, expected_total - (1.28 * std_dev))

        ht_expected = expected_total * 0.49
        ht_under_70 = ht_expected + (1.28 * (std_dev * 0.55))
        ht_over_70 = max(65.0, ht_expected - (1.28 * (std_dev * 0.55)))

        return {
            "expected_fulltime": round(expected_total, 1),
            "ft_over_70": round(ft_over_70 - 0.5, 0) + 0.5,
            "ft_under_70": round(ft_under_70 + 0.5, 0) - 0.5,
            "ht_over_70": round(ht_over_70 - 0.5, 0) + 0.5,
            "ht_under_70": round(ht_under_70 + 0.5, 0) - 0.5,
        }