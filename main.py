from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from fastapi.responses import HTMLResponse

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select

from models import AutoModels

engine = create_async_engine(
    "postgresql+asyncpg://postgres:postgres@db:5432/dvdrental", echo=True
)


auto_models = None


async def lifespan(app):
    print("startup")
    global auto_models
    auto_models = await AutoModels.create(engine)
    yield
    print("shutdown")


app = FastAPI(lifespan=lifespan)

# Route that returns hello world
@app.get("/api/v1/hello")
async def root():
    return {"message": "Hello World"}

# Route that returns a files components given an id
@app.get("/film/{id}", response_class=HTMLResponse)
async def film(id: int):
    async with AsyncSession(engine) as session:
        Film = await auto_models.get("film")
        film = await session.execute(select(Film).filter_by(film_id=id))
        film = film.scalars().first()

    if not film:
        raise HTTPException(status_code=404, detail="Film not found")

    with open(f"ui/dist/film.html") as file:
        return file.read()


@app.get("/api/v1/films/{id}", response_class=HTMLResponse)
async def get_film(id: int):
    async with AsyncSession(engine) as session:
        Film = await auto_models.get("film")
        film = await session.execute(select(Film).filter_by(film_id=id))
        film = film.scalars().first()

    if not film:
        raise HTTPException(status_code=404, detail="Film not found")

    return film


# Route that returns all films with corresponding descrips + ids
@app.get("/api/v1/films")
async def films():
    Film = await auto_models.get("film")

    results = []

    async with AsyncSession(engine) as session:
        films = await session.execute(select(Film))
        for film in films.scalars().all():
            results.append(
                {
                    "title": film.title,
                    "description": film.description,
                    "id": film.film_id,
                }
	    )
    return results


app.mount("/", StaticFiles(directory="ui/dist", html=True), name="ui")
