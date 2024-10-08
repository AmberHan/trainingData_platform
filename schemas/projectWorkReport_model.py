from typing import Optional

from pydantic import BaseModel


class GetProjectWorkReportReply(BaseModel):
    accuracyTop_1: Optional[float] = None
    accuracyTop_5: Optional[float] = None
    precision: Optional[float] = None
    recall: Optional[float] = None
    f1Score: Optional[float] = None
