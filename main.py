from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List

app = FastAPI(title="Api Para primer Examen",
              description="Api para registro de Estudiante Profesores y Materias",
              version="1.0.0")

class Person(BaseModel):
    id: int = Field(..., examples=[1])
    name: str = Field(..., examples=["Santiago Roldan"])
    email: str = Field(..., examples=["Santiago.Roldan@gmail.com"])

class Subject(BaseModel):
    id: int = Field(..., examples=[1])
    name: str = Field(..., examples=["Matematicas"])

class Note(BaseModel):
    estudiante: int = Field(..., examples=[1])
    profesor: int = Field(..., examples=[1])
    materia: int = Field(..., examples=[1])
    nota: float = Field(..., examples=[1.1])



student_db: List[Person] = []
teacher_db: List[Person] = []
subject_db: List[Subject] = []
notes_db: List[Note] = []

#Endpoints Notas

@app.get(
    "/notes/{id_student}",
    response_model=List[Note],
    summary="Obtener todos las notas de un estudiante segun id del estudiante y la materia buscada",
    description="Esto nos devuelve una lista con todas las notas registrads segun id del estudiante y la materia buscada",
    tags=["Nota"],
    responses={
        200: {
            "descripcion": "Lista de notas recuperada exitosamente."
        }
    }
)
def get_notes(id_student: int) -> List[Note]:
    notes: list[Note] = []
    for note in notes_db:
        if note.estudiante == id_student:  
            notes.append(note)  
    
    return notes

@app.get(
    "/notes",
    response_model=float,
    summary="Obtener promedio de las notas de un estudiante segun id del estudiante y la materia buscada",
    description="Esto nos devuelve una lista con el promedio de todas las notas registradas segun id del estudiante y la materia buscada",
    tags=["Nota"],
    responses={
        200: {
            "descripcion": "Promedio de notas recuperado exitosamente."
        }
    }
)
def get_average(id_student: int, id_subj: int) -> float:
    student_exists = any(student.id == id_student for student in student_db)
    if not student_exists:
        raise HTTPException(
            status_code=404,
            detail=f"El estudiante con ID {id_student} no esta registrado"
        )
    
    subject_exists = any(subject.id == id_subj for subject in subject_db)
    if not subject_exists:
        raise HTTPException(
            status_code=404,
            detail=f"La materia con ID {id_subj} no esta registrada"
        )
    
    notes: list[float] = []
    for note in notes_db:
        if note.estudiante == id_student and note.materia == id_subj:  
            notes.append(note.nota)  
    avg = sum(notes) / len(notes)
    return avg


@app.post(
    "/notes",
    status_code=201,
    summary="Crear una nota",
    description="Agregar una nueva nota a la base de datos simulada",
    tags=["nota"],
    responses={
        201: {
            "descripcion":"nota creada exitosamente"
        }
    }
)
def create_notes(note: Note) -> Note:
    student_exists = any(student.id == note.estudiante for student in student_db)
    if not student_exists:
        raise HTTPException(
            status_code=404,
            detail=f"El estudiante con ID {note.estudiante} no existe"
        )
    
    teacher_exists = any(teacher.id == note.profesor for teacher in teacher_db)
    if not teacher_exists:
        raise HTTPException(
            status_code=404,
            detail=f"El Profesor con ID {note.profesor} no existe"
        )
    
    subject_exists = any(subject.id == note.materia for subject in subject_db)
    if not subject_exists:
        raise HTTPException(
            status_code=404,
            detail=f"La materia con ID {note.materia} no existe"
        )

    notes_db.append(note)
    return note
            


# #Endpoints Materias

@app.get(
    "/subjects",
    response_model=List[Subject],
    summary="Obtener todos las materias",
    description="Esto nos devuelve una lista con todos las materias registrados",
    tags=["Materia"],
    responses={
        200: {
            "descripcion": "Lista de materias recuperada exitosamente."
        }
    }
)
def get_subjects() -> List[Subject]:
    return subject_db

@app.post(
    "/subjects",
    status_code=201,
    summary="Crear una materia",
    description="Agregar una nueva materia a la base de datos simulada",
    tags=["materia"],
    responses={
        201: {
            "descripcion":"materia creada exitosamente"
        },
        400: {
            "descripcion": "Id duplicado"
        }
    }
)
def create_subject(subject: Subject) -> Subject:
 
    for each_subject in subject_db:
        if each_subject.id == subject.id:
            raise HTTPException(status_code=400,detail="El ID ya existe")
    subject_db.append(subject)
    return subject

@app.put(
    "/subjects/{subject_id}",
    response_model= Subject,
    summary="Actualizar una Materia",
    description="Se actualiza la materia mediante su ID",
    tags=["Materia"],
    responses={
        200: {"descripcion": "Materia actualizada correctamente"},
        404:{"descripcion": "ID de la Materia no se encontro"}
    }
)
def update_subject(subject_id: int, updated_subject: Subject):
    for index, subject in enumerate(subject_db):
        if subject.id == subject_id:
            subject_db[index] = updated_subject
            return updated_subject
    raise HTTPException(status_code=404,detail="Materia no encontrada")

@app.delete(
    "/subjects/{subject_id}",
    summary="Eliminar una Materia",
    description="Se elimina una Materia de la base de datos por Id",
    tags=["Materia"],
    responses={
        200: {"descripcion": "Materia eliminada correctamente"},
        404:{"descripcion": "ID de la Materia no se encontro"}
    }
)

def delete_subject(subject_id: int):
    for index, subject in enumerate(subject_db):
        if subject.id == subject_id:
            deleted_subject = subject_db.pop(index)
            return {
                "mensaje": "Materia eliminada correctamente",
                "materia": deleted_subject
            }
    raise HTTPException(status_code=404, detail="Materia no encontrada")


# # Endpoints Profesores

@app.get(
    "/teachers",
    response_model=List[Person],
    summary="Obtener todos los profesores",
    description="Esto nos devuelve una lista con todos los profesores registrados",
    tags=["Estudiante"],
    responses={
        200: {
            "descripcion": "Lista de profesores recuperada exitosamente."
        }
    }
)
def get_teachers() -> List[Person]:
    return teacher_db

@app.post(
    "/teachers",
    status_code=201,
    summary="Crear un profesor",
    description="Agregar un nuevo profesor a la base de datos simulada",
    tags=["profesor"],
    responses={
        201: {
            "descripcion":"profesor creado exitosamente"
        },
        400: {
            "descripcion": "Id duplicado"
        }
    }
)
def create_teacher(teacher: Person) -> Person:
 
    for each_teacher in teacher_db:
        if each_teacher.id == teacher.id:
            raise HTTPException(status_code=400,detail="El ID ya existe")
    teacher_db.append(teacher)
    return teacher

@app.put(
    "/teachers/{teacher_id}",
    response_model= Person,
    summary="Actualizar un Profesor",
    description="Se actualiza el Profesor mediante su ID",
    tags=["Profesor"],
    responses={
        200: {"descripcion": "Profesor actualizado correctamente"},
        404:{"descripcion": "ID del Profesor no se encontro"}
    }
)
def update_teacher(teacher_id: int, updated_teacher: Person):
    for index, teacher in enumerate(teacher_db):
        if teacher.id == teacher_id:
            teacher_db[index] = updated_teacher
            return updated_teacher
    raise HTTPException(status_code=404,detail="Profesor no encontrado")

@app.delete(
    "/teachers/{teacher_id}",
    summary="Eliminar un Profesor",
    description="Se elimina un Profesor de la base de datos por Id",
    tags=["Profesor"],
    responses={
        200: {"descripcion": "Profesor eliminado correctamente"},
        404:{"descripcion": "ID del Profesor no se encontro"}
    }
)

def delete_teacher(teacher_id: int):
    for index, teacher in enumerate(teacher_db):
        if teacher.id == teacher_id:
            deleted_teacher = teacher_db.pop(index)
            return {
                "mensaje": "Profesor eliminado correctamente",
                "profesor": deleted_teacher
            }
    raise HTTPException(status_code=404, detail="Profesor no encontrado")




# # #Endpoints Estudiantes

@app.get(
    "/students",
    response_model=List[Person],
    summary="Obtener todos los estudiantes",
    description="Esto nos devuelve una lista con todos los estudiantes registrados",
    tags=["Estudiante"],
    responses={
        200: {
            "descripcion": "Lista de Estudiantes recuperada exitosamente."
        }
    }
)
def get_users() -> List[Person]:
    return student_db

@app.post(
    "/students",
    status_code=201,
    summary="Crear un estudiante",
    description="Agregar un nuevo estudiante a la base de datos simulada",
    tags=["Estudiante"],
    responses={
        201: {
            "descripcion":"Estudiante creado exitosamente"
        },
        400: {
            "descripcion": "Id duplicado"
        }
    }
)
def create_student(student: Person) -> Person:
    """
    
    
    """
    for each_student in student_db:
        if each_student.id == student.id:
            raise HTTPException(status_code=400,detail="El ID ya existe")
    student_db.append(student)
    return student

@app.put(
    "/students/{student_id}",
    response_model= Person,
    summary="Actualizar un Estudiante",
    description="Se actualiza el Estudiante mediante su ID",
    tags=["Estudiante"],
    responses={
        200: {"descripcion": "Estudiante actualizado correctamente"},
        404:{"descripcion": "ID del Estudiante no se encontro"}
    }
)
def update_student(student_id: int, updated_student: Person):
    for index, student in enumerate(student_db):
        if student.id == student_id:
            student_db[index] = updated_student
            return updated_student
    raise HTTPException(status_code=404,detail="Estudiante no encontrado")

@app.delete(
    "/students/{student_id}",
    summary="Eliminar un Estudiante",
    description="Se elimina un Estudiante de la base de datos por Id",
    tags=["Estudiante"],
    responses={
        200: {"descripcion": "Estudiante eliminado correctamente"},
        404:{"descripcion": "ID del Estudiante no se encontro"}
    }
)

def delete_student(student_id: int):
    for index, student in enumerate(student_db):
        if student.id == student_id:
            deleted_student = student_db.pop(index)
            return {
                "mensaje": "Estudiante eliminado correctamente",
                "estudiante": deleted_student
            }
    raise HTTPException(status_code=404, detail="Estudiante no encontrado")

