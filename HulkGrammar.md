<!-- The body of a program in HULK always ends with a single global expression -->
Program -> Body Exp 
<!-- (and, if necessary, a final semicolon) -->
Body -> FunctionList Body | ClassList Body | Epsilon

Exp -> Expression ; | BlockExpression
PExp -> Expression  | BlockExpression
<!-- As the documentation is not clear, we will asume a BlockExpression cannot have a BlockExpresion inside -->
BlockExpression -> { ExpressionList } Pc

Pc  -> ; | Epsilon

Expression -> PrintExpression | ArithmeticExpression | LetExpression | DestructiveExpression | IfExpression

ExpressionList -> Expression  | Expression ; ExpressionList
# ArithmeticExpression
    ArithmeticExpression -> Term | Term + ArithmeticExpression | Term - ArithmeticExpression 

    Term -> Factor | Factor * Term | Factor / Term | Factor % Term

    Factor -> Potency | Potency ^ Factor 
    
    Potency -> - Primary | Primary

    Primary -> Numbers | ( ArithmeticExpression ) | Identifier PosibleArguments 

    PosibleArguments -> ( Arguments ) | Epsilon

    Arguments -> ArithmeticExpression | ArithmeticExpression , Arguments | Epsilon


# PrintExpression
    PrintExpression -> print ( CanPrint )

    CanPrint -> Value

# StringExpression
StringExpresion -> String ConcatString

ConcatString -> @ Value ConcatString | Epsilon

Value -> String | ArithmeticExpression | LetExpression | DestructiveExpression | IfExpression

# Functions
Function -> FunctionHeader => Exp | FunctionHeader BlockExpression

FunctionHeader ->  function Identifier ( Params )

Params -> Identifier | Identifier , Params | Epsilon

FuctionList -> Function | Fuction FunctionList | Epsilon

# Variables
LetExpression -> let AssignList in AfterIn

AfterIn -> Exp | LetExpression | ( Expression ) Pc

AssignList -> Identifier = Value | Identifier = Value , AssignList

DestructiveExpression -> Identifier := Value

# Conditionals

IfExpression -> if ( ConditionalExpression ) PExp ElseExpression

ElseExpression -> elif ( ConditionalExpression ) PExp ElseExpression | else Expression

ConditionalExpression -> Not | Nor & ConditionalExpresion | Nor "|" ConditionalExpresion 

Nor -> Comparable | ! Comparable

Comparable -> true | false | Value < Value | Value <= Value | Value > Value | Value >= Value | Value == Value | Value != Value

# Loops




literals -> Numbers | String | boolean

Numbers -> [1-9] NextNumbers Decimal
Decimal -> . [0-9] NextNumbers | Epsilon
NextNumbers ->  [0-9] NextNumbers | Epsilon

String -> " Char " 
Char -> \" Char | [ASCII] Char | Epsilon

Identifier -> [_,a-z,A-Z] NextIdentifier
NextIdentifier -> [_,0-9,a-z,A-Z] NextIdentifier | Epsilon