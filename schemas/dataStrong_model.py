from typing import Optional

from pydantic import BaseModel

from sqlmodels.dataStrong import DataStrong as DataStrongSql


class DataStrong(BaseModel):
    id: Optional[str] = None
    dataId: Optional[str] = None
    strongParam: Optional[str] = None

    @classmethod
    def from_orm(cls, data: DataStrongSql) -> 'DataStrong':
        return DataStrong(
            id=data.Id,
            dataId=data.DataId,
            strongParam=data.StrongParam,
        )


class DataStrongParam(DataStrong):
    open_cross_validation: bool = False
    is_test: bool = False
    training_data_num: Optional[str] = None
    validation_num: Optional[str] = None
    test_data_num: Optional[str] = None
    open_center_cut: bool = False
    center_cut_width: Optional[str] = None
    center_cut_height: Optional[str] = None
    open_regular: bool = False
    regular_mean: Optional[str] = None
    regular_std: Optional[str] = None
    open_fill: bool = False
    fill_width: Optional[str] = None
    fill_height: Optional[str] = None
    open_random_cut: bool = False
    random_cut_width: Optional[str] = None
    random_cut_height: Optional[str] = None
    open_change_size: bool = False
    change_size_width: Optional[str] = None
    change_size_height: Optional[str] = None
    open_random_delete: bool = False
    random_delete_erase_prob: Optional[str] = None
    random_delete_min_area_ratio: Optional[str] = None
    random_delete_max_area_ratio: Optional[str] = None
    open_random_flip: bool = False
    random_flip_prob: Optional[str] = None
    random_flip_direction: Optional[str] = None
    open_random_grey: bool = False
    random_grey_prob: Optional[str] = None
