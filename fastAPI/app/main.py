from fastapi import FastAPI, Depends, HTTPException
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

@app.get("/notes/{note_id}")
def get_single_note(note_id: int, db: Session = Depends(get_db)):
    found_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not found_note:
        raise HTTPException(status_code=404, detail="Note not found")
    else:
        return found_note

@app.post("/notes")
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    db_note = models.Note(title=note.title, content=note.content)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note