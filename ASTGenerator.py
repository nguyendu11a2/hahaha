from initial.src.main.d95.utils.AST import IntLit
from AST import *
from D95Visitor import D95Visitor
from D95Parser import D95Parser


class ASTGenerator(D95Visitor):

    # Visit a parse tree produced by D95Parser#program.
    # def visitProgram(self, ctx: D95Parser.ProgramContext):
    #     return Program([ConstDecl(Id("ABC"), IntLit(10))], [Assign(Id("$x"), IntLit(5))])
    def visitProgram(self, ctx: D95Parser.ProgramContext):
        return self.visit(ctx.intLit())
    def visitDecl(self, ctx: D95Parser.ProgramContext):
        pass
    ################################
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

    def visitConstDecl(self, ctx: D95Parser.ProgramContext):
        pass

    def visitNonConstDecl(self, ctx: D95Parser.ProgramContext):
        pass
       
        ##########
    def visitAssignstmt(self, ctx: D95Parser.AssignstmtContext): #NOT ở exp7
        if ctx.exp7():
            return Assign(self.visit(ctx.exp7()), self.visit(ctx.exp()))
        return Assign(Id(ctx.IDVAR().getText()), self.visit(ctx.exp()))
    
    def visitIfstmt(self, ctx: D95Parser.IfstmtContext):
        return If([(self.visit(ctx.exp()), self.visit(ctx.stmts()))] + self.visit(ctx.elseifstmt()), self.visit(ctx.elsestmt()))

    def visitElseifstmt(self, ctx: D95Parser.ElseifstmtContext):
        pass
    def visitElsestmt(self, ctx: D95Parser.ElsestmtContext):
        pass


    def visitForeachstmt(self, ctx: D95Parser.ForeachstmtContext):
        return ForEach(self.visit(ctx.exp()), ID(ctx.IDVAR(0).getText()), ID(ctx.IDVAR(1).getText()), self.visit(ctx.stmts()))

    def visitWhilestmt(self, ctx: D95Parser.WhilestmtContext):
        return While(self.visit(ctx.exp()), self.visit(ctx.stmts()))

    
    def visitBreakstmt(self, ctx: D95Parser.BreakstmtContext):
        return Break()

    def visitContinuestmt(self, ctx: D95Parser.ContinuestmtContext):
        return Continue()

    def visitReturnstmt(self, ctx: D95Parser.ReturnstmtContext):
        if ctx.exp():
            return Return(self.visit(ctx.exp()))
        return Return()
    

    ###################################################################    


    def visitExp(self, ctx: D95Parser.ProgramContext):
        pass
    
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
        if ctx.INTEGER():
            return IntLit(int(ctx.INLIT().getText()))

        elif ctx.FLOAT():
            return FloatLit(float(ctx.FLOATLIT().getText()))

        elif ctx.STRING():
            return StringLit(ctx.STRINGLIT().getText())

        return BoolLit(True if ctx.BOOLEANLIT().getText() == "true" else False)

    #Array
    def visitArray(self, ctx: D95Parser.ProgramContext):
        return ArrayLit(self.visit(ctx.arrays()))

    def visitArrays(self, ctx:D95Parser.Array_bodyContext):
        if ctx.index_array():
            return self.visit(ctx.index_array())
        if ctx.asocia_array():
            return self.visit(ctx.asocia_array())
        if ctx.multi_array():
            return self.visit(ctx.multi_array())
        return []

    def visitIndex_array(self, ctx:D95Parser.Array_indexContext):
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

    def visitMulti_array(self, ctx:D95Parser.Array_multidimensionalContext):
        if ctx.getChildCount() == 1:
            return [self.visit(ctx.array())]
        return [self.visit(ctx.array())] + self.visit(ctx.array_multidimensional())
    