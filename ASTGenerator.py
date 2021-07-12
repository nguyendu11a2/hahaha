from AST import *
from D95Visitor import D95Visitor
from D95Parser import D95Parser


class ASTGenerator(D95Visitor):

    # Visit a parse tree produced by D95Parser#program.
    # def visitProgram(self, ctx: D95Parser.ProgramContext):
    #     return Program([ConstDecl(Id("ABC"), IntLit(10))], [Assign(Id("$x"), IntLit(5))])
    def visitProgram(self, ctx: D95Parser.ProgramContext):
        return Program(self.visit(ctx.constants()), self.visit(ctx.body()))
    
    def visitConstants(self, ctx:D95Parser.ConstantsContext):
        if ctx.getChildCount() == 2:
            return [self.visit(ctx.constant())] + self.visit(ctx.constants())
        elif ctx.getChildCount() == 1:
            return [self.visit(ctx.constant())]
        else:
            return []
    def visitConstant(self, ctx:D95Parser.ConstantContext):
        return ConstDecl(Id(ctx.IDCONSTANT().getText()), self.visit(ctx.literal()))


    def visitBody(self, ctx:D95Parser.BodyContext):
        if ctx.getChildCount() == 2:
            if ctx.func_decl():
                return [self.visit(ctx.func_decl())] + self.visit(ctx.body())
            else:
                return [self.visit(ctx.assignstmt())] + self.visit(ctx.body())
        elif ctx.getChildCount() == 1:
            if ctx.func_decl():
                return [self.visit(ctx.func_decl)]
            else:
                return [self.visit(ctx.assignstmt())]
        return []

    def visitFunc_decl(self, ctx: D95Parser.Func_declContext):
        if ctx.parameter():
            return FuncDecl(Id(ctx.IDFUNC().getText()), self.visit(ctx.para()), self.visit(ctx.stmts()))
        return FuncDecl(Id(ctx.IDFUNC().getText()), [], self.visit(ctx.stmts()))

    def visitPara(self, ctx: D95Parser.ParaContext):
        if ctx.getChildCount() == 1:
            return [ParamDecl(Id(ctx.IDVAR().getText()))]
        return [ParamDecl(Id(ctx.IDVAR().getText()))] + self.visit(ctx.para())



    ################################
    def visitStmts(self, ctx: D95Parser.StmtsContext):
        if ctx.getChildCount() == 1:
            return [self.visit(ctx.stmt())]
        if ctx.getChildCount() == 2:
            return [self.visit(ctx.stmt())] + self.visit(ctx.stmts())
        return []
    def visitStmt(self, ctx: D95Parser.StmtContext):  #NOT thiếu expsmtm?
        if ctx.assignstmt():
            return self.visit(ctx.assignstmt())

        elif ctx.ifstmt():
            return self.visit(ctx.ifstmt())

        elif ctx.foreachstmt():
            return self.visit(ctx.foreachstmt())

        elif ctx.whilestmt():
            return self.visit(ctx.whilestmt())
            
        elif ctx.breakstmt():
            return self.visit(ctx.breakstmt())

        elif ctx.continuestmt():
            return self.visit(ctx.continuestmt())
            
        elif ctx.callstmt():
            return self.visit(ctx.callstmt())

        elif ctx.returnstmt():
            return self.visit(ctx.returnstmt())

       
        ##########
    def visitAssignstmt(self, ctx: D95Parser.AssignstmtContext): #NOT ở exp7
        if ctx.exp7():
            return Assign(self.visit(ctx.exp7()), self.visit(ctx.exp()))
        return Assign(Id(ctx.IDVAR().getText()), self.visit(ctx.exp()))
    
    #NOT
    def visitIfstmt(self, ctx: D95Parser.IfstmtContext):
        return If([(self.visit(ctx.exp()), self.visit(ctx.stmts()))] + self.visit(ctx.elseifstmt()), self.visit(ctx.elsestmt()))

    def visitElseifstmt(self, ctx: D95Parser.ElseifstmtContext):
        if ctx.getChildCount == 7:
            return [(self.visit(ctx.expression()), self.visit(ctx.statements()))]
        elif ctx.getChildCount() == 8:
            return [(self.visit(ctx.exp()), self.visit(ctx.stmts()))] + self.visit(ctx.elseifstmt())
        return []
    def visitElsestmt(self, ctx: D95Parser.ElsestmtContext):
        if ctx.ELSE():
            return self.visit(ctx.stmts())
        return []



    def visitForeachstmt(self, ctx: D95Parser.ForeachstmtContext):
        return ForEach(self.visit(ctx.exp()), ID(ctx.IDVAR(0).getText()), ID(ctx.IDVAR(1).getText()), self.visit(ctx.stmts()))

    def visitWhilestmt(self, ctx: D95Parser.WhilestmtContext):
        return While(self.visit(ctx.exp()), self.visit(ctx.stmts()))

    def visitCallstmt(self, ctx: D95Parser.CallstmtContext):
        return self.visit(ctx.func_call())
    def visitFunccall(self, ctx: D95Parser.FunccallContext):
        if ctx.callpara():
            return Call(Id(ctx.IDFUNC().getText()), self.visit(ctx.callpara()))
        return Call(Id(ctx.IDFUNC().getText()), [])
    def visitCallpara(self, ctx: D95Parser.CallparaContext):
        if ctx.getChildCount() == 1:
            return [self.visit(ctx.exp())]
        return [self.visit(ctx.exp())] + self.visit(ctx.callpara())


    def visitBreakstmt(self, ctx: D95Parser.BreakstmtContext):
        return Break()

    def visitContinuestmt(self, ctx: D95Parser.ContinuestmtContext):
        return Continue()

    def visitReturnstmt(self, ctx: D95Parser.ReturnstmtContext):
        if ctx.exp():
            return Return(self.visit(ctx.exp()))
        return Return()
    

    ###################################################################    


    def visitExp(self, ctx: D95Parser.ExpContext):
        if ctx.getChildCount() == 1:  # exp
            return self.visit(ctx.exp1(0))
        left = self.visit(ctx.exp1(0))
        right = self.visit(ctx.exp1(1))
        op = ctx.getChild(1).getText()
        return BinExp(op, left, right)
    
    def visitExp1(self, ctx: D95Parser.Exp1Context):
        if ctx.getChildCount() == 1:  # exp1
            return self.visit(ctx.exp2(0))
        left = self.visit(ctx.exp2(0))
        right = self.visit(ctx.exp2(1))
        op = ctx.getChild(1).getText()
        return BinExp(op, left, right)
    def visitExp2(self, ctx: D95Parser.Exp2Context):
        if ctx.getChildCount() == 1:  # exp2
            return self.visit(ctx.exp3(0))
        left = self.visit(ctx.exp3(0))
        right = self.visit(ctx.exp3(1))
        op = ctx.getChild(1).getText()
        return BinExp(op, left, right)

    def visitExp3(self, ctx: D95Parser.Exp3Context):
        if ctx.getChildCount() == 1:  # exp3
            return self.visit(ctx.exp4())
        left = self.visit(ctx.exp3())
        right = self.visit(ctx.exp4())
        op = ctx.getChild(1).getText()
        return BinExp(op, left, right)
    def visitExp4(self, ctx: D95Parser.Exp4Context):
        if ctx.getChildCount() == 1:  # exp4
            return self.visit(ctx.exp5())
        left = self.visit(ctx.exp4(0))
        right = self.visit(ctx.exp4(1))
        op = ctx.getChild(1).getText()
        return BinExp(op, left, right)

    def visitExp5(self, ctx: D95Parser.Exp5Context):
        if ctx.getChildCount() == 1:  # ex5
            return self.visit(ctx.exp6())
        left = self.visit(ctx.exp5())
        right = self.visit(ctx.exp6())
        op = ctx.getChild(1).getText()
        return BinExp(op, left, right)

    def visitExp6(self, ctx: D95Parser.Exp6Context):
        if ctx.getChildCount() == 1:  # ex6
            return self.visit(ctx.exp7())
        exp = self.visit(ctx.exp6())
        op = ctx.getChild(0).getText()
        return UnExp(op, exp)

    def visitExp7(self, ctx: D95Parser.Exp7Context):
        if ctx.getChildCount() == 1:  # ex6
            return self.visit(ctx.exp8())
        elif ctx.IDVAR():
            return ArrayAccess(Id(ctx.IDVAR().getText()), self.visit(ctx.op_index()))
        else:
            return ArrayAccess(Id(ctx.IDCONSTANT().getText()), self.visit(ctx.op_index()))
    def visitExp8(self, ctx: D95Parser.Exp8Context):
        if ctx.getChildCount() == 3:
            return self.visit(ctx.exp())
        elif ctx.convert():
            return self.visit(ctx.convert())
        elif ctx.IDVAR():
            return Id(ctx.IDVAR().getText())
        elif ctx.IDCONSTANT():
            return Id(ctx.IDCONSTANT().getText()) 
        elif ctx.literal():
            return self.visit(ctx.literal())
        elif ctx.funccall():
            return self.visit(ctx.funccall())
        elif ctx.array():
            return self.visit(ctx.array())
        


    ##########################################

    def visitConvert(self, ctx:D95Parser.ConvertContext):
        if ctx.STR2INT():
            return Id(ctx.STR2INT().getText())

        elif ctx.INT2STR():
            return Id(ctx.INT2STR().getText())

        elif ctx.STR2FLOAT():
            return Id(ctx.STR2FLOAT().getText())

        elif ctx.FLOAT2STR():
            return Id(ctx.FLOAT2STR().getText())

        elif ctx.STR2BOOL():
            return Id(ctx.STR2BOOL().getText())

        elif ctx.BOOL2STR():
            return Id(ctx.BOOL2STR().getText())

    def visitLiteral(self, ctx:D95Parser.LiteralContext):
        if ctx.INLIT():
            return IntLit(int(ctx.INLIT().getText()))

        elif ctx.FLOATLIT():
            return FloatLit(float(ctx.FLOATLIT().getText()))

        elif ctx.STRINGLIT():
            return StringLit(ctx.STRINGLIT().getText())

        return BoolLit(True if ctx.BOOLEANLIT().getText() == "true" else False)




############################################################
    #Array
    def visitArray(self, ctx: D95Parser.ProgramContext):
        return ArrayLit(self.visit(ctx.arrays()))

    def visitArrays(self, ctx:D95Parser.ArraysContext):
        if ctx.index_array():
            return self.visit(ctx.index_array())
        if ctx.asocia_array():
            return self.visit(ctx.asocia_array())
        if ctx.multi_array():
            return self.visit(ctx.multi_array())
        return []

    def visitIndex_array(self, ctx:D95Parser.Index_arrayContext):
        if ctx.getChildCount() == 1:
            return [self.visit(ctx.exp())]
        return [self.visit(ctx.exp())] + self.visit(ctx.index_array())

    def visitAsocia_array(self, ctx:D95Parser.Asocia_arrayContext):
        if ctx.getChildCount() == 3:
            return [AssocExp(self.visit(ctx.ele_asocia_array()), self.visit(ctx.value_associa()))]
        return [AssocExp(self.visit(ctx.ele_asocia_array()), self.visit(ctx.value_associa()))] + self.visit(ctx.array_associative())
    def visitEle_asocia_array(self, ctx:D95Parser.Ele_asocia_arrayContext):
        if ctx.INLIT():
            return IntLit(int(ctx.INLIT().getText()))
        return StringLit(ctx.STRINGLIT().getText())
    def visitValue_associa(self, ctx:D95Parser.Value_associaContext):
        if ctx.exp():
            return self.visit(ctx.exp())
        return self.visit(ctx.array())

    def visitMulti_array(self, ctx:D95Parser.Multi_arrayContext):
        if ctx.getChildCount() == 1:
            return [self.visit(ctx.array())]
        return [self.visit(ctx.array())] + self.visit(ctx.array_multidimensional())
    
