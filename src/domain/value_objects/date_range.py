# src/domain/value_objects/date_range.py
from pydantic import BaseModel, field_validator
from datetime import date

class DateRange(BaseModel):
    start_date: date
    end_date: date

    @field_validator('end_date', mode='after')
    @classmethod
    def check_order(cls, v: date, values: dict) -> date:
        if 'start_date' in values and v < values['start_date']:
            raise ValueError("End date cannot be before the start date.")
        return v