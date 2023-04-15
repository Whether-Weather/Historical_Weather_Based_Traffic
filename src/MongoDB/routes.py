from typing import List

from fastapi import APIRouter, Body, HTTPException, Request, Response, status
from fastapi.encoders import jsonable_encoder
from models import SegmentData, SegmentDataUpdate

router = APIRouter()
@router.post("/", response_description="Create a Segment Data", status_code=status.HTTP_201_CREATED, response_model=SegmentData)
def create_Segment(request: Request, seg: SegmentData = Body(...)):
    seg = jsonable_encoder(seg)
    print(request.app.database["segs"])
    new_seg = request.app.database["segs"].insert_one(seg)
    print("NEW SEG DONE")
    created_seg = request.app.database["segs"].find_one(
        {"_id": new_seg.inserted_id}
    )

    return created_seg

# @router.post("/", response_description="Create Segment Data From Iterable", status_code=status.HTTP_201_CREATED, response_model=SegmentData)
# def create_Segment(request: Request, seg_dict: dict(SegmentData)):
#     seg_dict = jsonable_encoder(seg_dict)
#     print(request.app.database["segs"])
#     new_seg = request.app.database["segs"].insert_many(seg_dict)
#     print("NEW SEG DONE")
#     created_seg = request.app.database["segs"].find_one(
#         {"_id": new_seg.inserted_id}
#     )

#     return created_seg


@router.get("/", response_description="List all Segments", response_model=List[SegmentData])
def list_Segments(request: Request):
    Segments = list(request.app.database["segs"].find(limit=100))
    return Segments

@router.get("/{id}", response_description="Get a single Segment by id", response_model=SegmentData)
def find_segment(id: str, request: Request):
    print("GETTING")
    if (book := request.app.database["segs"].find_one({"_id": id})) is not None:
        return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Segment with ID {id} not found")

@router.put("/{id}", response_description="Update a Segment", response_model=SegmentData)
def update_segment(id: str, request: Request, seg: SegmentDataUpdate = Body(...)):
    seg = {k: v for k, v in seg.dict().items() if v is not None}
    if len(seg) >= 1:
        update_result = request.app.database["segs"].update_one(
            {"_id": id}, {"$set": seg}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Segment with ID {id} not found")

    if (
        existing_segment := request.app.database["segs"].find_one({"_id": id})
    ) is not None:
        return existing_segment

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Segment Data with ID {id} not found")

@router.delete("/{id}", response_description="Delete a Segment")
def delete_segment(id: str, request: Request, response: Response):
    delete_result = request.app.database["segs"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Segment Data with ID {id} not found")