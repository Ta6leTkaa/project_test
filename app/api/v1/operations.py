from fastapi import APIRouter, HTTPException

from app.schemas import OperationRequest
from app.service import operations as operations_service

router = APIRouter()

@router.post("/opperations/income")
def add_income(operation: OperationRequest):
    return operations_service.add_income(operation)


@router.post("/opperations/expense")
def add_expense(operation: OperationRequest):
    return operations_service.add_expense(operation)
