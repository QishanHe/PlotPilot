"""
Stats API endpoints
"""
from fastapi import APIRouter, Depends
from typing import Dict, Any
from application.core.services.novel_service import NovelService
from interfaces.api.dependencies import get_novel_service

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/global")
async def get_global_stats(
    novel_service: NovelService = Depends(get_novel_service)
) -> Dict[str, Any]:
    """
    Get global statistics across all novels
    """
    novels = await novel_service.list_novels()

    total_books = len(novels)
    total_chapters = sum(len(novel.chapters) for novel in novels)
    total_words = sum(novel.total_word_count for novel in novels)

    # Count books by stage
    books_by_stage: Dict[str, int] = {}
    for novel in novels:
        stage = novel.stage
        books_by_stage[stage] = books_by_stage.get(stage, 0) + 1

    return {
        "total_books": total_books,
        "total_chapters": total_chapters,
        "total_words": total_words,
        "books_by_stage": books_by_stage
    }
