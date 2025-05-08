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
    """
    Retrieve all notes.
    """
    return db.query(models.Note).all()


@app.get("/notes/{note_id}")
def get_single_note(note_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single note by its ID.

    Returns:
        models.Note: The note with the specified ID.

    Raises:
        HTTPException (404): If the note with the given ID is not found.
    """
    found_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not found_note:
        raise HTTPException(status_code=404, detail="Note not found")
    else:
        return found_note


@app.post("/notes")
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    """
    Create a new note.

    Returns:
        models.Note: The newly created note.
    """
    db_note = models.Note(title=note.title, content=note.content)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    """
    Deletes a single note by its ID.

    Returns:
        models.Note: The note with the specified ID.

    Raises:
        HTTPException (404): If the note with the given ID is not found.
        HTTPException (500): If the note failed to be deleted.
    """
    deleted_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not deleted_note:
        raise HTTPException(status_code=404, detail="Note not found")
    else:
        try:
            db.delete(deleted_note)
            db.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")
        return