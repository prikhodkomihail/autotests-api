from pydantic import BaseModel, ConfigDict, Field


class ExerciseSchema(BaseModel):
    """
    Описание структуры упражнения.
    """
    model_config = ConfigDict(populate_by_name=True)

    id: str
    title: str
    course_id: str = Field(alias='courseId')
    max_score: int = Field(alias='maxScore')
    min_score: int = Field(alias='minScore')
    order_index: int = Field(alias='orderIndex')
    description: str
    estimated_time: str = Field(alias='estimatedTime')


class GetExercisesQuerySchema(BaseModel):
    """
    Описание структуры запроса на получение списка упражнений.
    """
    model_config = ConfigDict(populate_by_name=True)

    course_id: str = Field(alias='courseId')


class GetExercisesResponseSchema(BaseModel):
    """
    Описание структуры ответа на получение списка упражнений.
    """
    exercises: list[ExerciseSchema]


class CreateExerciseRequestSchema(BaseModel):
    """
    Описание структуры запроса на создание упражнения.
    """
    model_config = ConfigDict(populate_by_name=True)

    title: str
    course_id: str = Field(alias='courseId')
    max_score: int = Field(alias='maxScore')
    min_score: int = Field(alias='minScore')
    order_index: int | None = Field(alias='orderIndex')
    description: str
    estimated_time: str = Field(alias='estimatedTime')


class CreateExerciseResponseSchema(BaseModel):
    """
    Описание структуры ответа на создание упражнения.
    """
    exercise: ExerciseSchema


class GetExerciseResponseSchema(BaseModel):
    """
    Описание структуры ответа на получение упражнения.
    """
    exercise: ExerciseSchema


class UpdateExerciseRequestSchema(BaseModel):
    """
    Описание структуры запроса на обновление упражнения.
    """
    model_config = ConfigDict(populate_by_name=True)

    title: str | None
    max_score: int | None = Field(alias='maxScore')
    min_score: int | None = Field(alias='minScore')
    order_index: int | None = Field(alias='orderIndex')
    description: str | None
    estimated_time: str | None = Field(alias='estimatedTime')


class UpdateExerciseResponseSchema(BaseModel):
    """
    Описание структуры ответа на обновление упражнения.
    """
    exercise: ExerciseSchema
