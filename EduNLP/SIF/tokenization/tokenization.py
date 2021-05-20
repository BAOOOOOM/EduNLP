# coding: utf-8
# 2021/5/18 @ tongshiwei

import itertools as it
from EduNLP.Formula.Formula import link_variable, Formula
from ..constants import Symbol, TEXT_SYMBOL, FIGURE_SYMBOL, FORMULA_SYMBOL, QUES_MARK_SYMBOL
from ..segment import (SegmentList, TextSegment, FigureSegment, LatexFormulaSegment, FigureFormulaSegment,
                       QuesMarkSegment, Figure)
from . import text, formula


class TokenList(object):
    def __init__(self, segment_list: SegmentList, text_params=None, formula_params=None, figure_params=None):
        self._tokens = []
        self._text_tokens = []
        self._formula_tokens = []
        self._figure_tokens = []
        self._ques_mark_tokens = []
        self.text_params = text_params if text_params is not None else {}
        self.formula_params = formula_params if formula_params is not None else {"method": "linear"}
        self.formula_tokenize_method = self.formula_params.get("method")
        self.figure_params = figure_params if figure_params is not None else {}
        self.extend(segment_list.segments)

    def _variable_standardization(self):
        if self.formula_tokenize_method == "ast":
            link_variable(list(it.chain(*[self._tokens[i].element for i in self._formula_tokens])))
            for i in self._formula_tokens:
                self._tokens[i].variable_standardization(inplace=True)

    @property
    def tokens(self):
        tokens = []
        for token in self._tokens:
            self.__add_token(token, tokens)
        return tokens

    def add(self, *segment):
        for seg in segment:
            self.append(seg, False)
        self._variable_standardization()

    def append_text(self, segment, symbol=False):
        if symbol is False:
            tokens = text.tokenize(segment, **self.text_params)
            for token in tokens:
                self._text_tokens.append(len(self._tokens))
                self._tokens.append(token)
        else:
            self._text_tokens.append(len(self._tokens))
            self._tokens.append(segment)

    def append_formula(self, segment, symbol=False):
        if symbol is True:
            self._formula_tokens.append(len(self._tokens))
            self._tokens.append(segment)
        elif isinstance(segment, FigureFormulaSegment):
            self._formula_tokens.append(len(self._tokens))
            self._tokens.append(segment)
        elif self.formula_params.get("method") == "ast":
            self._formula_tokens.append(len(self._tokens))
            self._tokens.append(Formula(segment))
        else:
            tokens = formula.tokenize(segment, **self.formula_params)
            for token in tokens:
                self._formula_tokens.append(len(self._tokens))
                self._tokens.append(token)

    def append_figure(self, segment, **kwargs):
        self._figure_tokens.append(len(self._tokens))
        self._tokens.append(segment)

    def append_ques_mark(self, segment, **kwargs):
        self._ques_mark_tokens.append(len(self._tokens))
        self._tokens.append(segment)

    def append(self, segment, lazy=False):
        if isinstance(segment, TextSegment):
            self.append_text(segment)
        elif isinstance(segment, (LatexFormulaSegment, FigureFormulaSegment)):
            self.append_formula(segment)
            if lazy is False:
                self._variable_standardization()
        elif isinstance(segment, FigureSegment):
            self.append_figure(segment)
        elif isinstance(segment, QuesMarkSegment):
            self.append_ques_mark(segment)
        elif isinstance(segment, Symbol):
            if segment == TEXT_SYMBOL:
                self.append_text(segment, symbol=True)
            elif segment == FORMULA_SYMBOL:
                self.append_formula(segment, symbol=True)
            elif segment == FIGURE_SYMBOL:
                self.append_figure(segment, symbol=True)
            elif segment == QUES_MARK_SYMBOL:
                self.append_ques_mark(segment, symbol=True)
            else:
                raise TypeError()
        else:
            raise TypeError()

    def extend(self, segments):
        for segment in segments:
            self.append(segment, False)
        self._variable_standardization()

    @property
    def text_tokens(self):
        return [self.tokens[i] for i in self._text_tokens]

    def __add_token(self, token, tokens):
        if isinstance(token, Formula):
            if self.formula_params.get("return_type") == "list":
                tokens.extend(formula.traversal_formula(token.ast, **self.formula_params))
            elif self.formula_params.get("return_type") == "ast":
                tokens.append(token.ast)
            else:
                tokens.append(token)
        elif isinstance(token, Figure):
            if self.figure_params.get("figure_instance") is True:
                if token.base64 is True:
                    tokens.append(token.base64_to_numpy(token.figure))
                else:
                    tokens.append(token)
            else:
                tokens.append(token)
        else:
            tokens.append(token)

    @property
    def formula_tokens(self):
        tokens = []
        for i in self._formula_tokens:
            self.__add_token(self.tokens[i], tokens)
        return tokens

    @property
    def figure_tokens(self):
        tokens = []
        for i in self._figure_tokens:
            self.__add_token(self.tokens[i], tokens)
        return tokens

    @property
    def ques_mark_tokens(self):
        return [self.tokens[i] for i in self._ques_mark_tokens]


def tokenize(segment_list: SegmentList, text_params=None, formula_params=None):
    return TokenList(segment_list, text_params, formula_params).tokens