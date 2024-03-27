<!-- The body of a program in HULK always ends with a single global expression -->
Program -> Body Exp
<!-- (and, if necessary, a final semicolon) -->
Body -> FunctionList Body | ClassList Body | Epsilon

Exp -> Expression ; | BlockExpression
PExp -> Expression  | BlockExpression
<!-- As the documentation is not clear, we will asume a BlockExpression cannot have a BlockExpresion inside -->
BlockExpression -> { ExpressionList } Pc

Pc  -> ; | Epsilon

Expression -> PrintExpression | ArithmeticExpression | LetExpression | DestructiveExpression | IfExpression | WhileExpression

Value -> String | ArithmeticExpression | LetExpression | DestructiveExpression | IfExpression | new Identifier ( Arguments ) | Identifier as Identifier | Vector

Vector -> [ Explicit ] | [ Expression "||" Iterable ]

Explicit -> Value | Value , Explicit

ExpressionList -> Expression  | Expression ; ExpressionList

# ArithmeticExpression
    ArithmeticExpression -> Term | ArithmeticExpression + Term | ArithmeticExpression - Term

    Term -> USub | Term * USub | Term / USub | Term % USub

    USub -> Factor | - Factor

    Factor -> Base | Base ^ Factor

    Base -> Number | ( ArithmeticExpression ) | Identifier PosibleArguments

    PosibleArguments -> ( ArgumentList ) | . Identifier PosibleArguments | [ ArithmeticExpression ] PossibleArguments | Epsilon

    ArgumentList -> ArithmeticExpression | ArithmeticExpression , ArgumentList | Epsilon

# PrintExpression
    PrintExpression -> print ( CanPrint )

    CanPrint -> Value

# StringExpression
StringExpresion -> String ConcatString

ConcatString -> @ Value ConcatString | Epsilon



# Functions
Function -> FunctionHeader => Exp | FunctionHeader BlockExpression

FunctionHeader ->  function Identifier ( Params ) TypeCheck

Params -> Identifier TypeCheck | Identifier TypeCheck , Params | Epsilon

FuctionList -> Function | Fuction FunctionList | Epsilon

# Variables
LetExpression -> let AssignList in AfterIn

AfterIn -> Exp | LetExpression | ( Expression ) Pc

AssignList -> Identifier TypeCheck = Value | Identifier TypeCheck = Value , AssignList

DestructiveExpression -> Identifier := Value

# Conditionals

IfExpression -> if ( ConditionalExpression ) PExp ElseExpression

ElseExpression -> elif ( ConditionalExpression ) PExp ElseExpression | else Expression

ConditionalExpression -> Not | Nor & ConditionalExpresion | Nor "|" ConditionalExpresion

Nor -> Comparable | ! Comparable

Comparable -> true | false | Value < Value | Value <= Value | Value > Value | Value >= Value | Value == Value | Value != Value | Identifier is Identifier | Expression is Identifier

# Loops

WhileExpression -> while ( ConditionalExpression ) Exp

ForExpression -> for ( Iterable ) Exp

Iterable -> Identifier in Identifier PosibleArguments 


# Types

TypeDeclaration -> type Identifier TypeParams Inherit { TypeBody }

Inherit -> inherit Identifier TypeParams | Epsilon

TypeParams -> ( Params ) | Epsilon

TypeBody -> AttributeDef TypeBody | MethodDef TypeBody | Epsilon

AttributeDef -> Identifier TypeCheck = Expression ;

MethodDef -> Identifier ( Params ) => Exp | Identifier ( Params ) BlockExpression

# TypesChecking

TypeCheck -> : Identifier | Epsilon

# Protocols

ProtocolDefinition -> protocol Identifier { MethodDefList }

ProtocolsMethods -> Identifier ( Params ) : Identifier => Exp | Identifier ( Params ) : Identifier BlockExpression

MethodDefList -> ProtocolsMethods MethodDefList | ProtocolsMethods


literals -> Numbers | String | boolean

Numbers -> [1-9] NextNumbers Decimal
Decimal -> . [0-9] NextNumbers | Epsilon
NextNumbers ->  [0-9] NextNumbers | Epsilon

String -> " Char "
Char -> \" Char | [ASCII] Char | Epsilon

Identifier -> [_,a-z,A-Z] NextIdentifier
NextIdentifier -> [_,0-9,a-z,A-Z] NextIdentifier | Epsilon
