"""应用层 DTOs"""
from application.core.dtos.novel_dto import NovelDTO
from application.core.dtos.chapter_dto import ChapterDTO
from application.world.dtos.bible_dto import BibleDTO, CharacterDTO, WorldSettingDTO
from application.audit.dtos.macro_refactor_dto import LogicBreakpoint, BreakpointScanRequest
from application.workbench.dtos.writer_block_dto import TensionSlingshotRequest, TensionDiagnosis

__all__ = ["NovelDTO", "ChapterDTO", "BibleDTO", "CharacterDTO", "WorldSettingDTO", "LogicBreakpoint", "BreakpointScanRequest", "TensionSlingshotRequest", "TensionDiagnosis"]
