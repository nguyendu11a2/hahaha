grammar D95;
//1711026
@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    result = super().emit()
    if tk == self.UNCLOSE_STRING:       
        raise UncloseString(result.text)
    elif tk == self.ILLEGAL_ESCAPE:
        raise IllegalEscape(result.text)
    elif tk == self.ERROR_CHAR:
        raise ErrorToken(result.text)
    elif tk == self.UNTERMINATED_COMMENT:
        raise UnterminatedComment()
    else:
        return result;
}

options{
	language=Python3;
}
fragment IllegalEscape: '\\' ~[bfrnt"\\] ;
BREAK:'break'; 
CONTINUE:'continue'; 
IF:'if'; 
ELSEIF:'elseif'; 
ELSE:'else';
WHILE:'while' ;

AS:'as' ;
FUNCTION:'function';


ARRAY:'array' ;
DEFINE:'define';
ECHO:'echo';
READ:'read';
RETURN: 'return';

//Operators

//Arithmetic operators
INTADD          : '+';
INTSUB          : '-';
INTMUL          : '*';
INTDIV          : '/';
MOD             : '%';

//Boolean operators
NOT             : '!';
AND             : '&&';
OR              : '||';

//Relational operators
EQUAL           : '==';
ASSIGN          : '=';
NOTEQUAL        : '!=';
LT              : '<';
GT              : '>';
LE              : '<=';
GE              : '>=';
CCC             : '=>';

STRASSIGN       :'==.';
STRCON          : '+.';

//Separators

LB: '(' ;
RB: ')' ;
LP: '{' ;
RP: '}';
LSB: '[';
RSB: ']';
SEMI: ';';
COMMA: ',';
COLON: ':';



program: constants body EOF ;



body:  assignstmt | func_decl | assignstmt body | func_decl body;
constants   : constant | constant constants |;


literal     :  INLIT | STRINGLIT | FLOATLIT |BOOLEANLIT ; 

// --------------- Function --------------------

func_decl : FUNCTION IDFUNC LB  para RB LP stmts RP| FUNCTION IDFUNC LB RB LP stmts RP;
para:  IDVAR | IDVAR COMMA para  ;

//3.3.5 1.integer    NOTDONE

INLIT: UNDERINT | DECIMAL_INTEGER | OCT_INTEGER |HEX_INTEGER | BIN_INTEGER;

UNDERINT
  : [1-9] [0-9]*  UNDERDIGIT+ 
  {
    y = ""
    self.text = self.text[:]
    temp = str(self.text)
    for x in temp:   
        if x != '_':
            { 
                y := y + x
             }
    self.text = y
    }
      
  ;
UNDERDIGIT
  : '_' DIGIT+
  ;
DECIMAL_INTEGER
    :   NON_ZERO_DIGIT DIGIT*
    |   '0'
    ;
OCT_INTEGER
    :   '0' NON_ZERO_OCT_DIGIT OCT_DIGIT* 
    ;
HEX_INTEGER
    :   '0' [xX] NON_ZERO_HEX_DIGIT HEX_DIGIT* 
    ;
BIN_INTEGER
    :   '0' [bB] BIN_DIGIT*
    ;

fragment NON_ZERO_OCT_DIGIT
    : [1-7];

fragment OCT_DIGIT
    : [0-7];

fragment BIN_DIGIT:[0-1];

fragment NON_ZERO_HEX_DIGIT
    : [1-9a-fA-F];

fragment HEX_DIGIT
    : [0-9a-fA-F];




//3.3.5 2.Float NOTDONE
FLOATLIT:POINT_FLOAT | EXPONENT_FLOAT| INT_PART | INTPARTUNDER ;



INTPARTUNDER 
    : DIGIT+ ('_' DIGIT+)+ FRACTION  {
        y = ""
        self.text = self.text[:]
        temp = str(self.text)
        for x in temp:   
            if x != '_':
                { 
                    y := y + x
                }
        self.text = y
    }
    |  DIGIT+ ('_' DIGIT+)+ '.' {
        y = ""
        self.text = self.text[:]
        temp = str(self.text)
        for x in temp:   
            if x != '_':
                { 
                    y := y + x
                }
        self.text = y
    };

fragment POINT_FLOAT
    : INT_PART FRACTION
    | INT_PART '.' 
    ;
fragment EXPONENT_FLOAT
    : (INT_PART | POINT_FLOAT) EXPONENT
    ;
fragment INT_PART
    : [1-9] DIGIT+
    | [1-9] | '0'
    ;
fragment FRACTION
    : '.' DIGIT+
    ;
fragment EXPONENT
    : [eE] [+-]? DIGIT+
    ;
fragment NON_ZERO_DIGIT
    : [1-9];

fragment DIGIT
    : [0-9];

BOOLEANLIT: TRUE | FALSE;


DOLLARSIGN:'$';

parameterid: IDVAR ;

IDVAR: DOLLARSIGN [a-zA-Z0-9_]+ ;

IDCONSTANT: [A-Z] [a-zA-Z0-9_]* ;

IDFUNC: [_] [a-zA-Z0-9_]*;
TRUE:'true' ;
FALSE:'false' ;
//------------------------------- ARRAY 
array : ARRAY LB arrays RB;
arrays: index_array |  asocia_array | multi_array|; 

index_array: exp
            | exp COMMA index_array;

asocia_array: ele_asocia_array CCC value_associa | ele_asocia_array CCC value_associa COMMA asocia_array;
ele_asocia_array:INLIT | STRINGLIT;
value_associa: exp | array;

multi_array: array | array COMMA multi_array;



// constant

constant: DEFINE LB IDCONSTANT COMMA literal RB SEMI ; //NOT





// Type coercions
convert: STR2INT | INT2STR | STR2FLOAT | FLOAT2STR | STR2BOOL | BOOL2STR;
STR2INT: 'str2int';
INT2STR:'int2str';
STR2FLOAT: 'str2float';
FLOAT2STR: 'float2str';
STR2BOOL: 'str2bool';
BOOL2STR: 'bool2str';
// Expressions

exp:	exp1 CCC exp1 | exp1;
exp1:	exp2 op_string exp2 | exp2;
exp2:   exp3 op_relat exp3 | exp3;
exp3:   exp3 op_log exp4 | exp4;
exp4:   exp4 op_add_minus exp4 | exp5;
exp5:   exp5 op_mul_div_mod exp6 | exp6;
exp6:   op_not_minus exp6 | exp7;
exp7:   IDVAR op_index 
        | IDCONSTANT op_index 
        | exp8;
exp8:   LB exp RB
            | literal
            | funccall  //NOT
            | IDVAR 
            | IDCONSTANT
            | convert LB exp RB 
            | array;

op_string: STRASSIGN | STRCON; //
op_relat : EQUAL | NOTEQUAL | LT | GT | LE | GE  ;//
op_log: AND | OR ;//
op_add_minus: INTADD | INTSUB ;//
op_mul_div_mod: INTMUL | INTDIV | MOD;//
op_not_minus: NOT | INTSUB ;
op_index:LSB exp RSB | LSB exp RSB op_index;

expstmt: exp SEMI ; 
//    Statements
stmts:stmt | stmt stmts |;
stmt: assignstmt | ifstmt | foreachstmt | whilestmt | breakstmt |continuestmt | callstmt | expstmt |returnstmt;

assignstmt: IDVAR ASSIGN exp SEMI | exp7 ASSIGN exp SEMI ; //NOT


//    Statements if
ifstmt: IF LB exp RB LP stmts RP  elseifstmt  elsestmt  ;
elseifstmt: ELSEIF LB exp RB LP stmts RP 
            | ELSEIF LB exp RB LP stmts RP elseifstmt 
            | ;
elsestmt: ELSE LP stmts RP | ;
// Foreach 
FOREACH:'foreach' ;
foreachstmt: FOREACH LB exp AS IDVAR CCC IDVAR RB LP stmts RP ;
// while
whilestmt: WHILE LB exp RB LP stmts RP  ;
// Break
breakstmt: BREAK SEMI;
//  Continue statement
continuestmt: CONTINUE SEMI;
// Call statement
callstmt    : funccall SEMI ;
funccall    : IDFUNC LB callpara  RB ;
callpara    : exp | exp COMMA callpara ;
// Return
returnstmt: RETURN exp SEMI | RETURN SEMI;
//WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs, newlines
fragment Character: ~[\b\f\r\n\t"\\] | Escape | '\'"';
fragment Escape: '\\' [bfrnt'\\];
STRINGLIT: '"' Character* '"'{
    temp = str(self.text)
    self.text = temp[1:-1]
};


//------------------------------ Comment ------------------------------//
CMTBLOCK: '/''*' .*? '*''/' -> skip;
WS: [ \f\t\r\n]+ -> skip; // skip spaces, tabs, newlines





UNCLOSE_STRING: '"' Character* ([\b\f\r\n\t\\] | EOF) {
    esc = ['\b', '\t', '\n', '\f', '\r', '\\']
    temp = str(self.text)
    if temp[-1] in esc:
        raise UncloseString(temp[1:-1])
    else :
        raise UncloseString(temp[1:])
};
ILLEGAL_ESCAPE:'"' Character* IllegalEscape {
    temp = str(self.text)
    raise IllegalEscape(temp[1:])
};
ERROR_CHAR:.
{
    raise ErrorToken(self.text)
};

UNTERMINATED_COMMENT: '/''*' .*? {
    raise UnterminatedComment()
} ;