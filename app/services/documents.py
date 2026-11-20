"""文件与元数据业务服务。"""

from pathlib import Path
from uuid import UUID, uuid4

from app.core.config import Settings
from app.db.models import DocumentRecord
from app.domain.exceptions import (
    NotFoundError,
    PayloadTooLargeError,
    PersistenceError,
    UnsupportedMediaError,
)
from app.repositories import UnitOfWork


class DocumentService:
    def __init__(self, uow: UnitOfWork, settings: Settings) -> None:
        self._uow, self._settings = uow, settings

    def list(self, user_id: UUID) -> list[DocumentRecord]:
        return self._uow.documents.list_owned(user_id)

    def upload(
        self,
        user_id: UUID,
        document_type: str,
        job_id: UUID | None,
        filename: str,
        content_type: str,
        content: bytes,
    ) -> DocumentRecord:
        if (
            job_id is not None
            and self._uow.jobs.get_owned(user_id, job_id) is None
        ):
            raise NotFoundError("岗位不存在")
        if content_type not in {"application/pdf", "text/plain"}:
            raise UnsupportedMediaError("仅支持 PDF 和纯文本文件")
        if len(content) > self._settings.max_upload_bytes:
            raise PayloadTooLargeError("文件超过大小限制")
        if content_type == "application/pdf" and not content.startswith(
            b"%PDF-"
        ):
            raise UnsupportedMediaError("文件内容不是有效 PDF")
        if content_type == "text/plain":
            try:
                content.decode("utf-8")
            except UnicodeDecodeError as error:
                raise UnsupportedMediaError(
                    "文本文件必须使用 UTF-8"
                ) from error
        suffix = Path(filename or "upload").suffix.lower()
        user_dir = self._settings.upload_dir / str(user_id)
        user_dir.mkdir(parents=True, exist_ok=True)
        stored_path = user_dir / f"{uuid4()}{suffix}"
        try:
            stored_path.write_bytes(content)
        except OSError as error:
            raise PersistenceError("文件保存失败") from error
        document = DocumentRecord(
            user_id=user_id,
            job_id=job_id,
            document_type=document_type,
            filename=Path(filename or "upload").name,
            stored_path=str(stored_path),
            content_type=content_type,
            size_bytes=len(content),
        )
        self._uow.documents.add(document)
        try:
            self._uow.commit()
        except PersistenceError:
            stored_path.unlink(missing_ok=True)
            raise
        self._uow.documents.refresh(document)
        return document

    def delete(self, user_id: UUID, document_id: UUID) -> None:
        document = self._uow.documents.get_owned(user_id, document_id)
        if document is None:
            raise NotFoundError("文件不存在")
        try:
            Path(document.stored_path).unlink(missing_ok=True)
        except OSError as error:
            raise PersistenceError("文件删除失败") from error
        self._uow.documents.delete(document)
        self._uow.commit()
