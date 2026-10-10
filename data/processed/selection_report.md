# Eval set selection report (DRAFT, not frozen)

Seed 0. Tasks selected: 60. Derived: 12. Overrides applied: 20 (spot_decisions.json found). Natural tasks ineligible (null pick on a kept slot): 0.

## Per bucket (quota -> selected)
| bucket | quota | selected |
| --- | --- | --- |
| multi_capability | 12 | 15 |
| semantic_distance | 12 | 12 |
| near_duplicate | 12 | 9 |
| taxonomy_collision | 10 | 10 |
| ambiguity | 10 | 10 |
| none | 4 | 4 |

## Per family
| family | n |
| --- | --- |
| academic_search | 7 |
| developer_tools | 2 |
| document_authoring | 4 |
| file_conversion | 2 |
| finance_analysis | 6 |
| gaming | 3 |
| geo_location | 5 |
| lifestyle_utilities | 5 |
| local_files | 7 |
| media_visual_audio | 3 |
| news_and_trends | 8 |
| security_network | 1 |
| shopping_research | 2 |
| travel_planning | 3 |
| web_research_writing | 2 |

## Per split
| split | n |
| --- | --- |
| dev | 18 |
| test | 42 |

## Split by bucket
| bucket/split | n |
| --- | --- |
| ambiguity/dev | 3 |
| ambiguity/test | 7 |
| multi_capability/dev | 4 |
| multi_capability/test | 11 |
| near_duplicate/dev | 3 |
| near_duplicate/test | 6 |
| none/dev | 1 |
| none/test | 3 |
| semantic_distance/dev | 4 |
| semantic_distance/test | 8 |
| taxonomy_collision/dev | 3 |
| taxonomy_collision/test | 7 |

## Shortfalls
- near_duplicate: short by 3
- Filled 3 of 3 missing slots from multi_capability.

Skips while selecting: {'duplicate_gold_set': 2}

## Override notes
- override applied: 5a2720cd reverse_geocode
- override applied: afd60e13 reverse_geocode
- override applied: 88ccea26 get_news
- override applied: 88ccea26 get_recommendations
- override applied: 6b7fc66e trial_references
- override applied: 567c79c3 list-component-examples
- override applied: a984d31b ddg-search
- override applied: 2bf318d4 variant_searcher
- override applied: 10b5dbf7 reverse_geocode
- override applied: 37d72d03 get_current_time
- override applied: 3819a831 playwright_screenshot
- override applied: 4d7582c4 execute_command
- override applied: de75630e get_maven_latest_version
- override applied: 04282571 reverse_geocode
- override applied: ea6e95fa playwright_screenshot
- override applied: 71a7a42a open_document
- override applied: c4d6c051 None
- override applied: 1f6a6db5 reverse_geocode
- override applied: cf6ea2ca get-juejin-article-rank
- override applied: 2293b5eb reverse_geocode
