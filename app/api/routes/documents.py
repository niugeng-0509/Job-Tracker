"""文件上传与元数据的 HTTP 适配层。"""

from uuid import UUID

from fastapi import APIRouter, File, Form, Response, UploadFile, status

from app.api.dependencies.auth import CurrentUser
from app.api.dependencies.database import SettingsDependency
from app.api.dependencies.services import DocumentServiceDependency
from app.db.models import DocumentRecord
from app.schemas import DocumentResponse

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("", response_model=list[DocumentResponse])
def list_documents(
    user: CurrentUser,
    service: DocumentServiceDependency,
) -> list[DocumentRecord]:
    return service.list(user.id)


@router.post(
    "", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED
)
def upload_document(
    user: CurrentUser,
    service: DocumentServiceDependency,
    settings: SettingsDependency,
    document_type: str = Form(...),
    job_id: UUID | None = Form(None),  # noqa: B008
    file: UploadFile = File(...),  # noqa: B008
) -> DocumentRecord:
    content = file.file.read(settings.max_upload_bytes + 1)
    return service.upload(
        user.id,
        document_type,
        job_id,
        file.filename or "upload",
        file.content_type or "application/octet-stream",
        content,
    )


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    document_id: UUID,
    user: CurrentUser,
    service: DocumentServiceDependency,
) -> Response:
    service.delete(user.id, document_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
