#!/usr/bin/env python3
"""批量更新导入路径的脚本"""

import os
import re
from pathlib import Path

# 导入路径映射表
IMPORT_MAPPINGS = {
    # DTOs
    'application.dtos.novel_dto': 'application.core.dtos.novel_dto',
    'application.dtos.chapter_dto': 'application.core.dtos.chapter_dto',
    'application.dtos.chapter_structure_dto': 'application.core.dtos.chapter_structure_dto',
    'application.dtos.bible_dto': 'application.world.dtos.bible_dto',
    'application.dtos.cast_dto': 'application.world.dtos.cast_dto',
    'application.dtos.knowledge_dto': 'application.world.dtos.knowledge_dto',
    'application.dtos.generation_result': 'application.engine.dtos.generation_result',
    'application.dtos.scene_director_dto': 'application.engine.dtos.scene_director_dto',
    'application.dtos.chapter_review_dto': 'application.audit.dtos.chapter_review_dto',
    'application.dtos.ghost_annotation': 'application.audit.dtos.ghost_annotation',
    'application.dtos.macro_refactor_dto': 'application.audit.dtos.macro_refactor_dto',
    'application.dtos.sandbox_dto': 'application.workbench.dtos.sandbox_dto',
    'application.dtos.writer_block_dto': 'application.workbench.dtos.writer_block_dto',

    # Services - Core
    'application.services.novel_service': 'application.core.services.novel_service',
    'application.services.chapter_service': 'application.core.services.chapter_service',
    'application.services.scene_generation_service': 'application.core.services.scene_generation_service',

    # Services - World
    'application.services.bible_service': 'application.world.services.bible_service',
    'application.services.auto_bible_generator': 'application.world.services.auto_bible_generator',
    'application.services.cast_service': 'application.world.services.cast_service',
    'application.services.knowledge_service': 'application.world.services.knowledge_service',
    'application.services.knowledge_graph_service': 'application.world.services.knowledge_graph_service',
    'application.services.auto_knowledge_generator': 'application.world.services.auto_knowledge_generator',
    'application.services.bible_location_triple_sync': 'application.world.services.bible_location_triple_sync',
    'application.services.worldbuilding_service': 'application.world.services.worldbuilding_service',

    # Services - Blueprint
    'application.services.continuous_planning_service': 'application.blueprint.services.continuous_planning_service',
    'application.services.beat_sheet_service': 'application.blueprint.services.beat_sheet_service',
    'application.services.story_structure_service': 'application.blueprint.services.story_structure_service',
    'application.services.setup_main_plot_suggestion_service': 'application.blueprint.services.setup_main_plot_suggestion_service',

    # Services - Engine
    'application.services.ai_generation_service': 'application.engine.services.ai_generation_service',
    'application.services.scene_director_service': 'application.engine.services.scene_director_service',
    'application.services.context_builder': 'application.engine.services.context_builder',
    'application.services.hosted_write_service': 'application.engine.services.hosted_write_service',
    'application.services.style_constraint_builder': 'application.engine.services.style_constraint_builder',
    'application.services.trigger_keyword_catalog': 'application.engine.services.trigger_keyword_catalog',

    # Services - Audit
    'application.services.chapter_review_service': 'application.audit.services.chapter_review_service',
    'application.services.conflict_detection_service': 'application.audit.services.conflict_detection_service',
    'application.services.cliche_scanner': 'application.audit.services.cliche_scanner',
    'application.services.macro_refactor_proposal_service': 'application.audit.services.macro_refactor_proposal_service',
    'application.services.macro_refactor_scanner': 'application.audit.services.macro_refactor_scanner',
    'application.services.macro_merge_engine': 'application.audit.services.macro_merge_engine',
    'application.services.mutation_applier': 'application.audit.services.mutation_applier',

    # Services - Analyst
    'application.services.voice_sample_service': 'application.analyst.services.voice_sample_service',
    'application.services.voice_fingerprint_service': 'application.analyst.services.voice_fingerprint_service',
    'application.services.voice_drift_service': 'application.analyst.services.voice_drift_service',
    'application.services.narrative_entity_state_service': 'application.analyst.services.narrative_entity_state_service',
    'application.services.state_extractor': 'application.analyst.services.state_extractor',
    'application.services.state_updater': 'application.analyst.services.state_updater',
    'application.services.indexing_service': 'application.analyst.services.indexing_service',
    'application.services.chapter_indexing_service': 'application.analyst.services.chapter_indexing_service',
    'application.services.character_indexer': 'application.analyst.services.character_indexer',
    'application.services.tension_analyzer': 'application.analyst.services.tension_analyzer',
    'application.services.subtext_matching_service': 'application.analyst.services.subtext_matching_service',

    # Services - Workbench
    'application.services.sandbox_dialogue_service': 'application.workbench.services.sandbox_dialogue_service',

    # Routes
    'interfaces.api.v1.novels': 'interfaces.api.v1.core.novels',
    'interfaces.api.v1.chapters': 'interfaces.api.v1.core.chapters',
    'interfaces.api.v1.scene_generation_routes': 'interfaces.api.v1.core.scene_generation_routes',
    'interfaces.api.v1.stats': 'interfaces.api.v1.core.stats',
    'interfaces.api.v1.bible': 'interfaces.api.v1.world.bible',
    'interfaces.api.v1.cast': 'interfaces.api.v1.world.cast',
    'interfaces.api.v1.knowledge': 'interfaces.api.v1.world.knowledge',
    'interfaces.api.v1.knowledge_graph_routes': 'interfaces.api.v1.world.knowledge_graph_routes',
    'interfaces.api.v1.worldbuilding_routes': 'interfaces.api.v1.world.worldbuilding_routes',
    'interfaces.api.v1.continuous_planning_routes': 'interfaces.api.v1.blueprint.continuous_planning_routes',
    'interfaces.api.v1.beat_sheet_routes': 'interfaces.api.v1.blueprint.beat_sheet_routes',
    'interfaces.api.v1.story_structure': 'interfaces.api.v1.blueprint.story_structure',
    'interfaces.api.v1.generation': 'interfaces.api.v1.engine.generation',
    'interfaces.api.v1.context_intelligence': 'interfaces.api.v1.engine.context_intelligence',
    'interfaces.api.v1.chapter_review_routes': 'interfaces.api.v1.audit.chapter_review_routes',
    'interfaces.api.v1.macro_refactor': 'interfaces.api.v1.audit.macro_refactor',
    'interfaces.api.v1.chapter_element_routes': 'interfaces.api.v1.audit.chapter_element_routes',
    'interfaces.api.v1.voice': 'interfaces.api.v1.analyst.voice',
    'interfaces.api.v1.narrative_state': 'interfaces.api.v1.analyst.narrative_state',
    'interfaces.api.v1.foreshadow_ledger': 'interfaces.api.v1.analyst.foreshadow_ledger',
    'interfaces.api.v1.sandbox': 'interfaces.api.v1.workbench.sandbox',
    'interfaces.api.v1.writer_block': 'interfaces.api.v1.workbench.writer_block',
}


def update_imports_in_file(file_path: Path):
    """更新单个文件中的导入路径"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        modified = False

        # 更新每个导入路径
        for old_path, new_path in IMPORT_MAPPINGS.items():
            # 匹配 from xxx import yyy
            pattern1 = rf'\bfrom\s+{re.escape(old_path)}\s+import\b'
            if re.search(pattern1, content):
                content = re.sub(pattern1, f'from {new_path} import', content)
                modified = True

            # 匹配 import xxx
            pattern2 = rf'\bimport\s+{re.escape(old_path)}\b'
            if re.search(pattern2, content):
                content = re.sub(pattern2, f'import {new_path}', content)
                modified = True

        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Updated: {file_path}")
            return True
        return False

    except Exception as e:
        print(f"✗ Error processing {file_path}: {e}")
        return False


def main():
    """主函数"""
    root = Path(__file__).parent

    # 需要扫描的目录
    directories = [
        root / 'application',
        root / 'interfaces',
        root / 'domain',
        root / 'infrastructure',
        root / 'web',
    ]

    total_files = 0
    updated_files = 0

    print("🔄 开始更新导入路径...\n")

    for directory in directories:
        if not directory.exists():
            continue

        for py_file in directory.rglob('*.py'):
            # 跳过 __pycache__ 和测试文件
            if '__pycache__' in str(py_file):
                continue

            total_files += 1
            if update_imports_in_file(py_file):
                updated_files += 1

    print(f"\n✅ 完成！")
    print(f"   扫描文件: {total_files}")
    print(f"   更新文件: {updated_files}")


if __name__ == '__main__':
    main()
