from __future__ import annotations

import unittest

from montage_ext.discovery.comparators import build_comparisons
from montage_ext.discovery.decision_packet import render_gate0_packet
from montage_ext.discovery.models import Observation
from montage_ext.discovery.opportunity import build_opportunity_record
from montage_ext.discovery.outliers import (
    ClassificationPolicy,
    calculate_outlier_multiple,
    classify_observation,
    enrich_observation,
)


def obs(
    item_id: str,
    *,
    views: int | None,
    baseline: float | None,
    topic: str = "steelpan history",
    format_name: str = "explainer",
    channel: str = "channel-a",
    channel_id: str | None = None,
) -> Observation:
    return Observation(
        id=item_id,
        source_url=f"https://example.com/{item_id}",
        platform="youtube",
        title=f"Video {item_id}",
        views=views,
        channel_baseline_views=baseline,
        topic=topic,
        format=format_name,
        channel=channel,
        channel_id=channel_id,
    )


class OutlierTests(unittest.TestCase):
    def test_outlier_calculation(self) -> None:
        self.assertEqual(calculate_outlier_multiple(300_000, 10_000), 30.0)

    def test_missing_or_zero_baseline_is_unknown(self) -> None:
        self.assertIsNone(calculate_outlier_multiple(300_000, None))
        self.assertIsNone(calculate_outlier_multiple(300_000, 0))

    def test_negative_values_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            calculate_outlier_multiple(-1, 10)
        with self.assertRaises(ValueError):
            calculate_outlier_multiple(10, -1)

    def test_default_classification_policy(self) -> None:
        self.assertEqual(classify_observation(obs("w", views=1000, baseline=100)), "winner")
        self.assertEqual(classify_observation(obs("f", views=40, baseline=100)), "failure")
        self.assertEqual(classify_observation(obs("c", views=100, baseline=100)), "comparator")
        self.assertEqual(classify_observation(obs("x", views=100, baseline=None)), "context")

    def test_manual_classification_is_preserved(self) -> None:
        item = Observation(
            id="manual",
            source_url="https://example.com/manual",
            platform="youtube",
            title="Manual",
            views=100,
            channel_baseline_views=100,
            classification="winner",
        )
        self.assertEqual(enrich_observation(item).classification, "winner")

    def test_invalid_policy_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ClassificationPolicy(winner_outlier_min=1, failure_outlier_max=1)


class ComparisonTests(unittest.TestCase):
    def test_pairs_winners_with_same_topic_failures(self) -> None:
        observations = [
            obs("winner", views=1000, baseline=100, format_name="explainer"),
            obs("failure-a", views=20, baseline=100, format_name="explainer"),
            obs("failure-b", views=20, baseline=100, format_name="documentary"),
            obs("other-topic", views=20, baseline=100, topic="car repair"),
        ]
        records = build_comparisons(observations)
        self.assertEqual([r.failure_id for r in records], ["failure-a", "failure-b"])
        self.assertTrue(records[0].format_match)
        self.assertFalse(records[1].format_match)
        self.assertAlmostEqual(records[0].outlier_gap or 0, 9.8)


class OpportunityTests(unittest.TestCase):
    def test_builds_evidence_summary_and_default_gate(self) -> None:
        observations = [
            obs("winner", views=1000, baseline=100, channel="A", channel_id="a"),
            obs("failure", views=20, baseline=100, channel="B", channel_id="b"),
            obs("context", views=100, baseline=None, channel="C", channel_id="c"),
        ]
        record = build_opportunity_record(
            opportunity_id="opp-1",
            market="steelpan",
            topic="steelpan history",
            observations=observations,
            original_contribution="Explain the evolution through design changes rather than biography.",
            titles=["How Steelpan Changed Shape"],
            thumbnails=["1940s pan -> modern tenor"],
            core_promise="Show why the instrument changed.",
            source_dependency_pass=True,
        )

        summary = record["evidence_summary"]
        self.assertEqual(summary["winners"], 1)
        self.assertEqual(summary["failures"], 1)
        self.assertEqual(summary["context"], 1)
        self.assertEqual(summary["unique_winner_channels"], 1)
        self.assertEqual(summary["observations_missing_baseline"], 1)
        self.assertEqual(record["gate0"]["decision"], "RESEARCH_MORE")

        packet = render_gate0_packet(record)
        self.assertIn("Gate 0 Decision Packet", packet)
        self.assertIn("PASS", packet)
        self.assertIn("PRODUCE / RESEARCH_MORE / REFRAME / REJECT", packet)

    def test_requires_packaging_and_original_contribution(self) -> None:
        with self.assertRaises(ValueError):
            build_opportunity_record(
                opportunity_id="opp-1",
                market="steelpan",
                topic="history",
                observations=[],
                original_contribution="",
                titles=[],
                thumbnails=[],
                core_promise="",
            )


if __name__ == "__main__":
    unittest.main()
