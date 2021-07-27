# from api.sockets.chesssimul.board import Board
import collections
from api.sockets.src.ia.chessBitBoard import Bitboard as Board
from api.sockets.src.ia.chessBitBoard import BitBoardMoveGenerator as BitBoardMoveGenerator
from api.sockets.src.ia.move import Move
import api.sockets.src.ia.boardInfo as boardInfo
from boardInfo import BoardInfo
import json
# import api.sockets.chesssimul.square as square
# import api.sockets.chesssimul.piece as piece
# import api.sockets.chesssimul.move as coup
# from square import Square
# from piece import Color, PieceType
# from piece import *
# from square import Square


# class BoardEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, Square):
#             return {'kind': obj.piece.kind.value if obj.piece != None else None, 'color': obj.piece.color.value if obj.piece != None else None}
#         if isinstance(obj, Color):
#             return {'color': obj.value}
#         if isinstance(obj, coup.Move):
#             return {
#                 'start': obj.start,
#                 'end': obj.end,
#                 'promotion_kind': PieceType(obj.promotion_kind) if obj.promotion_kind != None else None}
#         return json.JSONEncoder.default(self, obj)

class MoveGeneratorEncoder(json.JSONEncoder):
    def default(self, obj):
        return json.JSONEncoder.default(self, obj)


class BoardEncoder(json.JSONEncoder):
    def default(self, obj):
        print("\n>>")
        print(type(obj))
        print(">>\n")
        if isinstance(obj, collections.deque):
            return {'moves': []}
        if isinstance(obj, BoardInfo):
            return {'board_info': []}
        if isinstance(obj, BitBoardMoveGenerator):
            return MoveGeneratorEncoder()
        return json.JSONEncoder.default(self, obj)


def get_board(dct):
    j_board = list()
    index = 0
    for line in dct:
        j_board.append(list())
        for square in line:
            if square['kind'] == None or square['color'] == None:
                j_board[index].append(Square(piece=None))
                continue
            j_board[index].append(
                Square(piece=Piece(kind=PieceType(square['kind']) if square['kind'] != None else None, color=Color(square['color']) if square['color'] != None else None)))
        index += 1
    return j_board


def BoardDecoder(dct):
    board = Board()

    board.move_list = dct['move_list']
    board.pos_piece_check = dct['pos_piece_check']
    board.list_piece_pin = dct['list_piece_pin']

    board.board = get_board(dct['board'])
    board.to_move = Color(dct['to_move']['color'])
    board.can_black_king_side_castle = dct['can_black_king_side_castle']
    board.can_black_queen_side_castle = dct['can_black_queen_side_castle']
    board.can_white_king_side_castle = dct['can_white_king_side_castle']
    board.can_white_queen_side_castle = dct['can_white_queen_side_castle']
    board.en_passant_target_square = dct['en_passant_target_square']
    board.white_check = dct['white_check']
    board.black_check = dct['black_check']
    board.halfmove_clock = dct['halfmove_clock']
    board.fullmove_number = dct['fullmove_number']
    return board
