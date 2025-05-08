from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import database, models, schemas

app = FastAPI()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup():
    database.Base.metadata.create_all(bind=database.engine)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/notes")
def get_all_notes(db: Session = Depends(get_db)):
    return db.query(models.Note).all()

@app.post("/notes")
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    db_note = models.Note(title=note.title, content=note.content)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note