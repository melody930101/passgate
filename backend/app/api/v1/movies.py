from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.staff import Staff
from app.models.movie import Movie
from app.schemas.movie import MovieCreate, MovieResponse
from app.services.movie_service import MovieService

router = APIRouter()


@router.get('/active', response_model=list[MovieResponse])
def get_active_movies(db: Session = Depends(get_db)):
    return MovieService.get_active(db)


@router.get('', response_model=list[MovieResponse])
def get_all_movies(
    current: Staff = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return MovieService.get_all(db)


@router.post('', response_model=MovieResponse)
def create_movie(
    data: MovieCreate,
    current: Staff = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        return MovieService.create(db, data, current.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put('/{id}', response_model=MovieResponse)
def update_movie(
    id: int,
    data: MovieCreate,
    current: Staff = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        return MovieService.update(db, id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/{id}/deactivate')
def deactivate_movie(
    id: int,
    current: Staff = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        MovieService.deactivate(db, id)
        return {'message': 'ok'}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
