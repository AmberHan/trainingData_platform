from typing import Optional

from pydantic import BaseModel


class GetProjectWorkReportReply(BaseModel):
    precision: Optional[float] = None
    recall: Optional[float] = None
    mAp: Optional[float] = None
