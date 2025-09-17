import time
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.schemas.user import Users
from app.use_cases.user import UserUseCases
from app.use_cases.evaluation import Evaluation
from app.db.connection import get_db_session



router = APIRouter()

def get_ms(func, *args, **kwargs):
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()
    execution_ms = (end - start) * 1000
    result['body']['execution_time_ms'] = round(execution_ms, 2)
    return result


@router.post('/users')
def post_users(user_data: list[Users], db_session: Session = Depends(get_db_session)):
    uc = UserUseCases(db_session=db_session)
    response = get_ms(uc.add_users, user_data)
    return JSONResponse(status_code=response['status'], content=response)


@router.get('/superusers')
def get_superusers(db_session: Session = Depends(get_db_session)):
    uc = UserUseCases(db_session=db_session)
    response = get_ms(uc.get_superusers)
    return JSONResponse(status_code=response['status'], content=response)


@router.get("/top-countries")
def get_top_countries(db_session: Session = Depends(get_db_session)):
    uc = UserUseCases(db_session=db_session)
    response = get_ms(uc.get_top_countries)
    return JSONResponse(status_code=response['status'], content=response)


@router.get('/team-insights')
def get_team_insights(db_session: Session = Depends(get_db_session)):
    uc = UserUseCases(db_session=db_session)
    response = get_ms(uc.get_team_insights)
    return JSONResponse(status_code=response['status'], content=response)


@router.get('/active-users-per-day')
def get_active_users_per_day(db_session: Session = Depends(get_db_session)):
    uc = UserUseCases(db_session=db_session)
    response = get_ms(uc.get_active_users_per_date)
    return JSONResponse(status_code=response['status'], content=response)


@router.get('/evaluation')
def evaluate_api():
    evaluation = Evaluation().evaluate_api()
    return evaluation
