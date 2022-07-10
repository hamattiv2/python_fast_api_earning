from lib2to3.pytree import convert
from fastapi import APIRouter, Depends, Request

router = APIRouter(
    prefix='/dependencies',
    tags=['dependencies']
)

def convert_headers(request: Request):
    out_headers = []
    for key, value in request.headers.items():
        out_headers.append(f'{key} -- {value}')
        
    return out_headers

@router.get('')
def get_items(headers = Depends(convert_headers)):
    return {
        'items': ['a', 'b'],
        'headers': headers
    }