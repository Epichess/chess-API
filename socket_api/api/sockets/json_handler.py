import collections
from api.sockets.src.ia.chessBitBoard import Bitboard as Board
from api.sockets.src.ia.chessBitBoard import BitBoardMoveGenerator as BitBoardMoveGenerator
from api.sockets.src.ia.move import Move
import api.sockets.src.ia.boardInfo as boardInfo
from boardInfo import BoardInfo
from collections import deque
import json


class BoardEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Move):
            return {'debug': {}}
        if isinstance(obj, collections.deque):
            arr = []
            for elem in obj:
                arr.append(json.dumps(elem.__dict__))
            return json.dumps(arr)
        if isinstance(obj, BoardInfo):
            return json.dumps(obj.__dict__)
        if isinstance(obj, BitBoardMoveGenerator):
            return None
        return json.JSONEncoder.default(self, obj)


def BoardDecoder(dct):
    board = Board()

    board.pieces = dct['pieces']
    board.side_pieces = dct['side_pieces']
    board.occupancy = dct['occupancy']

    bmoves = json.loads(dct['moves'])
    ndeque = deque()
    for e in bmoves:
        elem = json.loads(e)
        ndeque.append(Move(
            int(elem['start']),
            int(elem['end']),
            int(elem['moveType']),
            int(elem['pieceType']),
            int(elem['capturedPieceType']),
            int(elem['specialMoveFlag']),
            int(elem['promotionPieceType']),
            bool(elem['castleSide'])
        ))
    board.moves = ndeque

    binfos = json.loads(dct['prev_board_infos'])
    ndeque = deque()
    for e in binfos:
        elem = json.loads(e)
        ndeque.append(BoardInfo(
            **elem
        ))
    board.prev_board_infos = ndeque

    binfo = json.loads(dct['board_info'])
    board.board_info = BoardInfo(**binfo)

    return board
