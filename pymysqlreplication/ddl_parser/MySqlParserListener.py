# Generated from MySqlParser.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .MySqlParser import MySqlParser
else:
    from MySqlParser import MySqlParser

# This class defines a complete listener for a parse tree produced by MySqlParser.
class MySqlParserListener(ParseTreeListener):

    # Enter a parse tree produced by MySqlParser#root.
    def enterRoot(self, ctx:MySqlParser.RootContext):
        pass

    # Exit a parse tree produced by MySqlParser#root.
    def exitRoot(self, ctx:MySqlParser.RootContext):
        pass


    # Enter a parse tree produced by MySqlParser#sqlStatements.
    def enterSqlStatements(self, ctx:MySqlParser.SqlStatementsContext):
        pass

    # Exit a parse tree produced by MySqlParser#sqlStatements.
    def exitSqlStatements(self, ctx:MySqlParser.SqlStatementsContext):
        pass


    # Enter a parse tree produced by MySqlParser#sqlStatement.
    def enterSqlStatement(self, ctx:MySqlParser.SqlStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#sqlStatement.
    def exitSqlStatement(self, ctx:MySqlParser.SqlStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#emptyStatement_.
    def enterEmptyStatement_(self, ctx:MySqlParser.EmptyStatement_Context):
        pass

    # Exit a parse tree produced by MySqlParser#emptyStatement_.
    def exitEmptyStatement_(self, ctx:MySqlParser.EmptyStatement_Context):
        pass


    # Enter a parse tree produced by MySqlParser#ddlStatement.
    def enterDdlStatement(self, ctx:MySqlParser.DdlStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#ddlStatement.
    def exitDdlStatement(self, ctx:MySqlParser.DdlStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#dmlStatement.
    def enterDmlStatement(self, ctx:MySqlParser.DmlStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#dmlStatement.
    def exitDmlStatement(self, ctx:MySqlParser.DmlStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#transactionStatement.
    def enterTransactionStatement(self, ctx:MySqlParser.TransactionStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#transactionStatement.
    def exitTransactionStatement(self, ctx:MySqlParser.TransactionStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#replicationStatement.
    def enterReplicationStatement(self, ctx:MySqlParser.ReplicationStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#replicationStatement.
    def exitReplicationStatement(self, ctx:MySqlParser.ReplicationStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#preparedStatement.
    def enterPreparedStatement(self, ctx:MySqlParser.PreparedStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#preparedStatement.
    def exitPreparedStatement(self, ctx:MySqlParser.PreparedStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#compoundStatement.
    def enterCompoundStatement(self, ctx:MySqlParser.CompoundStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#compoundStatement.
    def exitCompoundStatement(self, ctx:MySqlParser.CompoundStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#administrationStatement.
    def enterAdministrationStatement(self, ctx:MySqlParser.AdministrationStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#administrationStatement.
    def exitAdministrationStatement(self, ctx:MySqlParser.AdministrationStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#utilityStatement.
    def enterUtilityStatement(self, ctx:MySqlParser.UtilityStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#utilityStatement.
    def exitUtilityStatement(self, ctx:MySqlParser.UtilityStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#createDatabase.
    def enterCreateDatabase(self, ctx:MySqlParser.CreateDatabaseContext):
        pass

    # Exit a parse tree produced by MySqlParser#createDatabase.
    def exitCreateDatabase(self, ctx:MySqlParser.CreateDatabaseContext):
        pass


    # Enter a parse tree produced by MySqlParser#createEvent.
    def enterCreateEvent(self, ctx:MySqlParser.CreateEventContext):
        pass

    # Exit a parse tree produced by MySqlParser#createEvent.
    def exitCreateEvent(self, ctx:MySqlParser.CreateEventContext):
        pass


    # Enter a parse tree produced by MySqlParser#createIndex.
    def enterCreateIndex(self, ctx:MySqlParser.CreateIndexContext):
        pass

    # Exit a parse tree produced by MySqlParser#createIndex.
    def exitCreateIndex(self, ctx:MySqlParser.CreateIndexContext):
        pass


    # Enter a parse tree produced by MySqlParser#createLogfileGroup.
    def enterCreateLogfileGroup(self, ctx:MySqlParser.CreateLogfileGroupContext):
        pass

    # Exit a parse tree produced by MySqlParser#createLogfileGroup.
    def exitCreateLogfileGroup(self, ctx:MySqlParser.CreateLogfileGroupContext):
        pass


    # Enter a parse tree produced by MySqlParser#createProcedure.
    def enterCreateProcedure(self, ctx:MySqlParser.CreateProcedureContext):
        pass

    # Exit a parse tree produced by MySqlParser#createProcedure.
    def exitCreateProcedure(self, ctx:MySqlParser.CreateProcedureContext):
        pass


    # Enter a parse tree produced by MySqlParser#createFunction.
    def enterCreateFunction(self, ctx:MySqlParser.CreateFunctionContext):
        pass

    # Exit a parse tree produced by MySqlParser#createFunction.
    def exitCreateFunction(self, ctx:MySqlParser.CreateFunctionContext):
        pass


    # Enter a parse tree produced by MySqlParser#createRole.
    def enterCreateRole(self, ctx:MySqlParser.CreateRoleContext):
        pass

    # Exit a parse tree produced by MySqlParser#createRole.
    def exitCreateRole(self, ctx:MySqlParser.CreateRoleContext):
        pass


    # Enter a parse tree produced by MySqlParser#createServer.
    def enterCreateServer(self, ctx:MySqlParser.CreateServerContext):
        pass

    # Exit a parse tree produced by MySqlParser#createServer.
    def exitCreateServer(self, ctx:MySqlParser.CreateServerContext):
        pass


    # Enter a parse tree produced by MySqlParser#copyCreateTable.
    def enterCopyCreateTable(self, ctx:MySqlParser.CopyCreateTableContext):
        pass

    # Exit a parse tree produced by MySqlParser#copyCreateTable.
    def exitCopyCreateTable(self, ctx:MySqlParser.CopyCreateTableContext):
        pass


    # Enter a parse tree produced by MySqlParser#queryCreateTable.
    def enterQueryCreateTable(self, ctx:MySqlParser.QueryCreateTableContext):
        pass

    # Exit a parse tree produced by MySqlParser#queryCreateTable.
    def exitQueryCreateTable(self, ctx:MySqlParser.QueryCreateTableContext):
        pass


    # Enter a parse tree produced by MySqlParser#columnCreateTable.
    def enterColumnCreateTable(self, ctx:MySqlParser.ColumnCreateTableContext):
        pass

    # Exit a parse tree produced by MySqlParser#columnCreateTable.
    def exitColumnCreateTable(self, ctx:MySqlParser.ColumnCreateTableContext):
        pass


    # Enter a parse tree produced by MySqlParser#createTablespaceInnodb.
    def enterCreateTablespaceInnodb(self, ctx:MySqlParser.CreateTablespaceInnodbContext):
        pass

    # Exit a parse tree produced by MySqlParser#createTablespaceInnodb.
    def exitCreateTablespaceInnodb(self, ctx:MySqlParser.CreateTablespaceInnodbContext):
        pass


    # Enter a parse tree produced by MySqlParser#createTablespaceNdb.
    def enterCreateTablespaceNdb(self, ctx:MySqlParser.CreateTablespaceNdbContext):
        pass

    # Exit a parse tree produced by MySqlParser#createTablespaceNdb.
    def exitCreateTablespaceNdb(self, ctx:MySqlParser.CreateTablespaceNdbContext):
        pass


    # Enter a parse tree produced by MySqlParser#createTrigger.
    def enterCreateTrigger(self, ctx:MySqlParser.CreateTriggerContext):
        pass

    # Exit a parse tree produced by MySqlParser#createTrigger.
    def exitCreateTrigger(self, ctx:MySqlParser.CreateTriggerContext):
        pass


    # Enter a parse tree produced by MySqlParser#withClause.
    def enterWithClause(self, ctx:MySqlParser.WithClauseContext):
        pass

    # Exit a parse tree produced by MySqlParser#withClause.
    def exitWithClause(self, ctx:MySqlParser.WithClauseContext):
        pass


    # Enter a parse tree produced by MySqlParser#commonTableExpressions.
    def enterCommonTableExpressions(self, ctx:MySqlParser.CommonTableExpressionsContext):
        pass

    # Exit a parse tree produced by MySqlParser#commonTableExpressions.
    def exitCommonTableExpressions(self, ctx:MySqlParser.CommonTableExpressionsContext):
        pass


    # Enter a parse tree produced by MySqlParser#cteName.
    def enterCteName(self, ctx:MySqlParser.CteNameContext):
        pass

    # Exit a parse tree produced by MySqlParser#cteName.
    def exitCteName(self, ctx:MySqlParser.CteNameContext):
        pass


    # Enter a parse tree produced by MySqlParser#cteColumnName.
    def enterCteColumnName(self, ctx:MySqlParser.CteColumnNameContext):
        pass

    # Exit a parse tree produced by MySqlParser#cteColumnName.
    def exitCteColumnName(self, ctx:MySqlParser.CteColumnNameContext):
        pass


    # Enter a parse tree produced by MySqlParser#createView.
    def enterCreateView(self, ctx:MySqlParser.CreateViewContext):
        pass

    # Exit a parse tree produced by MySqlParser#createView.
    def exitCreateView(self, ctx:MySqlParser.CreateViewContext):
        pass


    # Enter a parse tree produced by MySqlParser#createDatabaseOption.
    def enterCreateDatabaseOption(self, ctx:MySqlParser.CreateDatabaseOptionContext):
        pass

    # Exit a parse tree produced by MySqlParser#createDatabaseOption.
    def exitCreateDatabaseOption(self, ctx:MySqlParser.CreateDatabaseOptionContext):
        pass


    # Enter a parse tree produced by MySqlParser#charSet.
    def enterCharSet(self, ctx:MySqlParser.CharSetContext):
        pass

    # Exit a parse tree produced by MySqlParser#charSet.
    def exitCharSet(self, ctx:MySqlParser.CharSetContext):
        pass


    # Enter a parse tree produced by MySqlParser#ownerStatement.
    def enterOwnerStatement(self, ctx:MySqlParser.OwnerStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#ownerStatement.
    def exitOwnerStatement(self, ctx:MySqlParser.OwnerStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#preciseSchedule.
    def enterPreciseSchedule(self, ctx:MySqlParser.PreciseScheduleContext):
        pass

    # Exit a parse tree produced by MySqlParser#preciseSchedule.
    def exitPreciseSchedule(self, ctx:MySqlParser.PreciseScheduleContext):
        pass


    # Enter a parse tree produced by MySqlParser#intervalSchedule.
    def enterIntervalSchedule(self, ctx:MySqlParser.IntervalScheduleContext):
        pass

    # Exit a parse tree produced by MySqlParser#intervalSchedule.
    def exitIntervalSchedule(self, ctx:MySqlParser.IntervalScheduleContext):
        pass


    # Enter a parse tree produced by MySqlParser#timestampValue.
    def enterTimestampValue(self, ctx:MySqlParser.TimestampValueContext):
        pass

    # Exit a parse tree produced by MySqlParser#timestampValue.
    def exitTimestampValue(self, ctx:MySqlParser.TimestampValueContext):
        pass


    # Enter a parse tree produced by MySqlParser#intervalExpr.
    def enterIntervalExpr(self, ctx:MySqlParser.IntervalExprContext):
        pass

    # Exit a parse tree produced by MySqlParser#intervalExpr.
    def exitIntervalExpr(self, ctx:MySqlParser.IntervalExprContext):
        pass


    # Enter a parse tree produced by MySqlParser#intervalType.
    def enterIntervalType(self, ctx:MySqlParser.IntervalTypeContext):
        pass

    # Exit a parse tree produced by MySqlParser#intervalType.
    def exitIntervalType(self, ctx:MySqlParser.IntervalTypeContext):
        pass


    # Enter a parse tree produced by MySqlParser#enableType.
    def enterEnableType(self, ctx:MySqlParser.EnableTypeContext):
        pass

    # Exit a parse tree produced by MySqlParser#enableType.
    def exitEnableType(self, ctx:MySqlParser.EnableTypeContext):
        pass


    # Enter a parse tree produced by MySqlParser#indexType.
    def enterIndexType(self, ctx:MySqlParser.IndexTypeContext):
        pass

    # Exit a parse tree produced by MySqlParser#indexType.
    def exitIndexType(self, ctx:MySqlParser.IndexTypeContext):
        pass


    # Enter a parse tree produced by MySqlParser#indexOption.
    def enterIndexOption(self, ctx:MySqlParser.IndexOptionContext):
        pass

    # Exit a parse tree produced by MySqlParser#indexOption.
    def exitIndexOption(self, ctx:MySqlParser.IndexOptionContext):
        pass


    # Enter a parse tree produced by MySqlParser#procedureParameter.
    def enterProcedureParameter(self, ctx:MySqlParser.ProcedureParameterContext):
        pass

    # Exit a parse tree produced by MySqlParser#procedureParameter.
    def exitProcedureParameter(self, ctx:MySqlParser.ProcedureParameterContext):
        pass


    # Enter a parse tree produced by MySqlParser#functionParameter.
    def enterFunctionParameter(self, ctx:MySqlParser.FunctionParameterContext):
        pass

    # Exit a parse tree produced by MySqlParser#functionParameter.
    def exitFunctionParameter(self, ctx:MySqlParser.FunctionParameterContext):
        pass


    # Enter a parse tree produced by MySqlParser#routineComment.
    def enterRoutineComment(self, ctx:MySqlParser.RoutineCommentContext):
        pass

    # Exit a parse tree produced by MySqlParser#routineComment.
    def exitRoutineComment(self, ctx:MySqlParser.RoutineCommentContext):
        pass


    # Enter a parse tree produced by MySqlParser#routineLanguage.
    def enterRoutineLanguage(self, ctx:MySqlParser.RoutineLanguageContext):
        pass

    # Exit a parse tree produced by MySqlParser#routineLanguage.
    def exitRoutineLanguage(self, ctx:MySqlParser.RoutineLanguageContext):
        pass


    # Enter a parse tree produced by MySqlParser#routineBehavior.
    def enterRoutineBehavior(self, ctx:MySqlParser.RoutineBehaviorContext):
        pass

    # Exit a parse tree produced by MySqlParser#routineBehavior.
    def exitRoutineBehavior(self, ctx:MySqlParser.RoutineBehaviorContext):
        pass


    # Enter a parse tree produced by MySqlParser#routineData.
    def enterRoutineData(self, ctx:MySqlParser.RoutineDataContext):
        pass

    # Exit a parse tree produced by MySqlParser#routineData.
    def exitRoutineData(self, ctx:MySqlParser.RoutineDataContext):
        pass


    # Enter a parse tree produced by MySqlParser#routineSecurity.
    def enterRoutineSecurity(self, ctx:MySqlParser.RoutineSecurityContext):
        pass

    # Exit a parse tree produced by MySqlParser#routineSecurity.
    def exitRoutineSecurity(self, ctx:MySqlParser.RoutineSecurityContext):
        pass


    # Enter a parse tree produced by MySqlParser#serverOption.
    def enterServerOption(self, ctx:MySqlParser.ServerOptionContext):
        pass

    # Exit a parse tree produced by MySqlParser#serverOption.
    def exitServerOption(self, ctx:MySqlParser.ServerOptionContext):
        pass


    # Enter a parse tree produced by MySqlParser#createDefinitions.
    def enterCreateDefinitions(self, ctx:MySqlParser.CreateDefinitionsContext):
        pass

    # Exit a parse tree produced by MySqlParser#createDefinitions.
    def exitCreateDefinitions(self, ctx:MySqlParser.CreateDefinitionsContext):
        pass


    # Enter a parse tree produced by MySqlParser#columnDeclaration.
    def enterColumnDeclaration(self, ctx:MySqlParser.ColumnDeclarationContext):
        pass

    # Exit a parse tree produced by MySqlParser#columnDeclaration.
    def exitColumnDeclaration(self, ctx:MySqlParser.ColumnDeclarationContext):
        pass


    # Enter a parse tree produced by MySqlParser#constraintDeclaration.
    def enterConstraintDeclaration(self, ctx:MySqlParser.ConstraintDeclarationContext):
        pass

    # Exit a parse tree produced by MySqlParser#constraintDeclaration.
    def exitConstraintDeclaration(self, ctx:MySqlParser.ConstraintDeclarationContext):
        pass


    # Enter a parse tree produced by MySqlParser#indexDeclaration.
    def enterIndexDeclaration(self, ctx:MySqlParser.IndexDeclarationContext):
        pass

    # Exit a parse tree produced by MySqlParser#indexDeclaration.
    def exitIndexDeclaration(self, ctx:MySqlParser.IndexDeclarationContext):
        pass


    # Enter a parse tree produced by MySqlParser#columnDefinition.
    def enterColumnDefinition(self, ctx:MySqlParser.ColumnDefinitionContext):
        pass

    # Exit a parse tree produced by MySqlParser#columnDefinition.
    def exitColumnDefinition(self, ctx:MySqlParser.ColumnDefinitionContext):
        pass


    # Enter a parse tree produced by MySqlParser#nullColumnConstraint.
    def enterNullColumnConstraint(self, ctx:MySqlParser.NullColumnConstraintContext):
        pass

    # Exit a parse tree produced by MySqlParser#nullColumnConstraint.
    def exitNullColumnConstraint(self, ctx:MySqlParser.NullColumnConstraintContext):
        pass


    # Enter a parse tree produced by MySqlParser#defaultColumnConstraint.
    def enterDefaultColumnConstraint(self, ctx:MySqlParser.DefaultColumnConstraintContext):
        pass

    # Exit a parse tree produced by MySqlParser#defaultColumnConstraint.
    def exitDefaultColumnConstraint(self, ctx:MySqlParser.DefaultColumnConstraintContext):
        pass


    # Enter a parse tree produced by MySqlParser#visibilityColumnConstraint.
    def enterVisibilityColumnConstraint(self, ctx:MySqlParser.VisibilityColumnConstraintContext):
        pass

    # Exit a parse tree produced by MySqlParser#visibilityColumnConstraint.
    def exitVisibilityColumnConstraint(self, ctx:MySqlParser.VisibilityColumnConstraintContext):
        pass


    # Enter a parse tree produced by MySqlParser#invisibilityColumnConstraint.
    def enterInvisibilityColumnConstraint(self, ctx:MySqlParser.InvisibilityColumnConstraintContext):
        pass

    # Exit a parse tree produced by MySqlParser#invisibilityColumnConstraint.
    def exitInvisibilityColumnConstraint(self, ctx:MySqlParser.InvisibilityColumnConstraintContext):
        pass


    # Enter a parse tree produced by MySqlParser#autoIncrementColumnConstraint.
    def enterAutoIncrementColumnConstraint(self, ctx:MySqlParser.AutoIncrementColumnConstraintContext):
        pass

    # Exit a parse tree produced by MySqlParser#autoIncrementColumnConstraint.
    def exitAutoIncrementColumnConstraint(self, ctx:MySqlParser.AutoIncrementColumnConstraintContext):
        pass


    # Enter a parse tree produced by MySqlParser#primaryKeyColumnConstraint.
    def enterPrimaryKeyColumnConstraint(self, ctx:MySqlParser.PrimaryKeyColumnConstraintContext):
        pass

    # Exit a parse tree produced by MySqlParser#primaryKeyColumnConstraint.
    def exitPrimaryKeyColumnConstraint(self, ctx:MySqlParser.PrimaryKeyColumnConstraintContext):
        pass


    # Enter a parse tree produced by MySqlParser#uniqueKeyColumnConstraint.
    def enterUniqueKeyColumnConstraint(self, ctx:MySqlParser.UniqueKeyColumnConstraintContext):
        pass

    # Exit a parse tree produced by MySqlParser#uniqueKeyColumnConstraint.
    def exitUniqueKeyColumnConstraint(self, ctx:MySqlParser.UniqueKeyColumnConstraintContext):
        pass


    # Enter a parse tree produced by MySqlParser#commentColumnConstraint.
    def enterCommentColumnConstraint(self, ctx:MySqlParser.CommentColumnConstraintContext):
        pass

    # Exit a parse tree produced by MySqlParser#commentColumnConstraint.
    def exitCommentColumnConstraint(self, ctx:MySqlParser.CommentColumnConstraintContext):
        pass


    # Enter a parse tree produced by MySqlParser#formatColumnConstraint.
    def enterFormatColumnConstraint(self, ctx:MySqlParser.FormatColumnConstraintContext):
        pass

    # Exit a parse tree produced by MySqlParser#formatColumnConstraint.
    def exitFormatColumnConstraint(self, ctx:MySqlParser.FormatColumnConstraintContext):
        pass


    # Enter a parse tree produced by MySqlParser#storageColumnConstraint.
    def enterStorageColumnConstraint(self, ctx:MySqlParser.StorageColumnConstraintContext):
        pass

    # Exit a parse tree produced by MySqlParser#storageColumnConstraint.
    def exitStorageColumnConstraint(self, ctx:MySqlParser.StorageColumnConstraintContext):
        pass


    # Enter a parse tree produced by MySqlParser#referenceColumnConstraint.
    def enterReferenceColumnConstraint(self, ctx:MySqlParser.ReferenceColumnConstraintContext):
        pass

    # Exit a parse tree produced by MySqlParser#referenceColumnConstraint.
    def exitReferenceColumnConstraint(self, ctx:MySqlParser.ReferenceColumnConstraintContext):
        pass


    # Enter a parse tree produced by MySqlParser#collateColumnConstraint.
    def enterCollateColumnConstraint(self, ctx:MySqlParser.CollateColumnConstraintContext):
        pass

    # Exit a parse tree produced by MySqlParser#collateColumnConstraint.
    def exitCollateColumnConstraint(self, ctx:MySqlParser.CollateColumnConstraintContext):
        pass


    # Enter a parse tree produced by MySqlParser#generatedColumnConstraint.
    def enterGeneratedColumnConstraint(self, ctx:MySqlParser.GeneratedColumnConstraintContext):
        pass

    # Exit a parse tree produced by MySqlParser#generatedColumnConstraint.
    def exitGeneratedColumnConstraint(self, ctx:MySqlParser.GeneratedColumnConstraintContext):
        pass


    # Enter a parse tree produced by MySqlParser#serialDefaultColumnConstraint.
    def enterSerialDefaultColumnConstraint(self, ctx:MySqlParser.SerialDefaultColumnConstraintContext):
        pass

    # Exit a parse tree produced by MySqlParser#serialDefaultColumnConstraint.
    def exitSerialDefaultColumnConstraint(self, ctx:MySqlParser.SerialDefaultColumnConstraintContext):
        pass


    # Enter a parse tree produced by MySqlParser#checkColumnConstraint.
    def enterCheckColumnConstraint(self, ctx:MySqlParser.CheckColumnConstraintContext):
        pass

    # Exit a parse tree produced by MySqlParser#checkColumnConstraint.
    def exitCheckColumnConstraint(self, ctx:MySqlParser.CheckColumnConstraintContext):
        pass


    # Enter a parse tree produced by MySqlParser#primaryKeyTableConstraint.
    def enterPrimaryKeyTableConstraint(self, ctx:MySqlParser.PrimaryKeyTableConstraintContext):
        pass

    # Exit a parse tree produced by MySqlParser#primaryKeyTableConstraint.
    def exitPrimaryKeyTableConstraint(self, ctx:MySqlParser.PrimaryKeyTableConstraintContext):
        pass


    # Enter a parse tree produced by MySqlParser#uniqueKeyTableConstraint.
    def enterUniqueKeyTableConstraint(self, ctx:MySqlParser.UniqueKeyTableConstraintContext):
        pass

    # Exit a parse tree produced by MySqlParser#uniqueKeyTableConstraint.
    def exitUniqueKeyTableConstraint(self, ctx:MySqlParser.UniqueKeyTableConstraintContext):
        pass


    # Enter a parse tree produced by MySqlParser#foreignKeyTableConstraint.
    def enterForeignKeyTableConstraint(self, ctx:MySqlParser.ForeignKeyTableConstraintContext):
        pass

    # Exit a parse tree produced by MySqlParser#foreignKeyTableConstraint.
    def exitForeignKeyTableConstraint(self, ctx:MySqlParser.ForeignKeyTableConstraintContext):
        pass


    # Enter a parse tree produced by MySqlParser#checkTableConstraint.
    def enterCheckTableConstraint(self, ctx:MySqlParser.CheckTableConstraintContext):
        pass

    # Exit a parse tree produced by MySqlParser#checkTableConstraint.
    def exitCheckTableConstraint(self, ctx:MySqlParser.CheckTableConstraintContext):
        pass


    # Enter a parse tree produced by MySqlParser#referenceDefinition.
    def enterReferenceDefinition(self, ctx:MySqlParser.ReferenceDefinitionContext):
        pass

    # Exit a parse tree produced by MySqlParser#referenceDefinition.
    def exitReferenceDefinition(self, ctx:MySqlParser.ReferenceDefinitionContext):
        pass


    # Enter a parse tree produced by MySqlParser#referenceAction.
    def enterReferenceAction(self, ctx:MySqlParser.ReferenceActionContext):
        pass

    # Exit a parse tree produced by MySqlParser#referenceAction.
    def exitReferenceAction(self, ctx:MySqlParser.ReferenceActionContext):
        pass


    # Enter a parse tree produced by MySqlParser#referenceControlType.
    def enterReferenceControlType(self, ctx:MySqlParser.ReferenceControlTypeContext):
        pass

    # Exit a parse tree produced by MySqlParser#referenceControlType.
    def exitReferenceControlType(self, ctx:MySqlParser.ReferenceControlTypeContext):
        pass


    # Enter a parse tree produced by MySqlParser#simpleIndexDeclaration.
    def enterSimpleIndexDeclaration(self, ctx:MySqlParser.SimpleIndexDeclarationContext):
        pass

    # Exit a parse tree produced by MySqlParser#simpleIndexDeclaration.
    def exitSimpleIndexDeclaration(self, ctx:MySqlParser.SimpleIndexDeclarationContext):
        pass


    # Enter a parse tree produced by MySqlParser#specialIndexDeclaration.
    def enterSpecialIndexDeclaration(self, ctx:MySqlParser.SpecialIndexDeclarationContext):
        pass

    # Exit a parse tree produced by MySqlParser#specialIndexDeclaration.
    def exitSpecialIndexDeclaration(self, ctx:MySqlParser.SpecialIndexDeclarationContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableOptionEngine.
    def enterTableOptionEngine(self, ctx:MySqlParser.TableOptionEngineContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableOptionEngine.
    def exitTableOptionEngine(self, ctx:MySqlParser.TableOptionEngineContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableOptionEngineAttribute.
    def enterTableOptionEngineAttribute(self, ctx:MySqlParser.TableOptionEngineAttributeContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableOptionEngineAttribute.
    def exitTableOptionEngineAttribute(self, ctx:MySqlParser.TableOptionEngineAttributeContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableOptionAutoextendSize.
    def enterTableOptionAutoextendSize(self, ctx:MySqlParser.TableOptionAutoextendSizeContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableOptionAutoextendSize.
    def exitTableOptionAutoextendSize(self, ctx:MySqlParser.TableOptionAutoextendSizeContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableOptionAutoIncrement.
    def enterTableOptionAutoIncrement(self, ctx:MySqlParser.TableOptionAutoIncrementContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableOptionAutoIncrement.
    def exitTableOptionAutoIncrement(self, ctx:MySqlParser.TableOptionAutoIncrementContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableOptionAverage.
    def enterTableOptionAverage(self, ctx:MySqlParser.TableOptionAverageContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableOptionAverage.
    def exitTableOptionAverage(self, ctx:MySqlParser.TableOptionAverageContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableOptionCharset.
    def enterTableOptionCharset(self, ctx:MySqlParser.TableOptionCharsetContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableOptionCharset.
    def exitTableOptionCharset(self, ctx:MySqlParser.TableOptionCharsetContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableOptionChecksum.
    def enterTableOptionChecksum(self, ctx:MySqlParser.TableOptionChecksumContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableOptionChecksum.
    def exitTableOptionChecksum(self, ctx:MySqlParser.TableOptionChecksumContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableOptionCollate.
    def enterTableOptionCollate(self, ctx:MySqlParser.TableOptionCollateContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableOptionCollate.
    def exitTableOptionCollate(self, ctx:MySqlParser.TableOptionCollateContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableOptionComment.
    def enterTableOptionComment(self, ctx:MySqlParser.TableOptionCommentContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableOptionComment.
    def exitTableOptionComment(self, ctx:MySqlParser.TableOptionCommentContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableOptionCompression.
    def enterTableOptionCompression(self, ctx:MySqlParser.TableOptionCompressionContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableOptionCompression.
    def exitTableOptionCompression(self, ctx:MySqlParser.TableOptionCompressionContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableOptionConnection.
    def enterTableOptionConnection(self, ctx:MySqlParser.TableOptionConnectionContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableOptionConnection.
    def exitTableOptionConnection(self, ctx:MySqlParser.TableOptionConnectionContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableOptionDataDirectory.
    def enterTableOptionDataDirectory(self, ctx:MySqlParser.TableOptionDataDirectoryContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableOptionDataDirectory.
    def exitTableOptionDataDirectory(self, ctx:MySqlParser.TableOptionDataDirectoryContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableOptionDelay.
    def enterTableOptionDelay(self, ctx:MySqlParser.TableOptionDelayContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableOptionDelay.
    def exitTableOptionDelay(self, ctx:MySqlParser.TableOptionDelayContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableOptionEncryption.
    def enterTableOptionEncryption(self, ctx:MySqlParser.TableOptionEncryptionContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableOptionEncryption.
    def exitTableOptionEncryption(self, ctx:MySqlParser.TableOptionEncryptionContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableOptionPageCompressed.
    def enterTableOptionPageCompressed(self, ctx:MySqlParser.TableOptionPageCompressedContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableOptionPageCompressed.
    def exitTableOptionPageCompressed(self, ctx:MySqlParser.TableOptionPageCompressedContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableOptionPageCompressionLevel.
    def enterTableOptionPageCompressionLevel(self, ctx:MySqlParser.TableOptionPageCompressionLevelContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableOptionPageCompressionLevel.
    def exitTableOptionPageCompressionLevel(self, ctx:MySqlParser.TableOptionPageCompressionLevelContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableOptionEncryptionKeyId.
    def enterTableOptionEncryptionKeyId(self, ctx:MySqlParser.TableOptionEncryptionKeyIdContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableOptionEncryptionKeyId.
    def exitTableOptionEncryptionKeyId(self, ctx:MySqlParser.TableOptionEncryptionKeyIdContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableOptionIndexDirectory.
    def enterTableOptionIndexDirectory(self, ctx:MySqlParser.TableOptionIndexDirectoryContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableOptionIndexDirectory.
    def exitTableOptionIndexDirectory(self, ctx:MySqlParser.TableOptionIndexDirectoryContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableOptionInsertMethod.
    def enterTableOptionInsertMethod(self, ctx:MySqlParser.TableOptionInsertMethodContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableOptionInsertMethod.
    def exitTableOptionInsertMethod(self, ctx:MySqlParser.TableOptionInsertMethodContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableOptionKeyBlockSize.
    def enterTableOptionKeyBlockSize(self, ctx:MySqlParser.TableOptionKeyBlockSizeContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableOptionKeyBlockSize.
    def exitTableOptionKeyBlockSize(self, ctx:MySqlParser.TableOptionKeyBlockSizeContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableOptionMaxRows.
    def enterTableOptionMaxRows(self, ctx:MySqlParser.TableOptionMaxRowsContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableOptionMaxRows.
    def exitTableOptionMaxRows(self, ctx:MySqlParser.TableOptionMaxRowsContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableOptionMinRows.
    def enterTableOptionMinRows(self, ctx:MySqlParser.TableOptionMinRowsContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableOptionMinRows.
    def exitTableOptionMinRows(self, ctx:MySqlParser.TableOptionMinRowsContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableOptionPackKeys.
    def enterTableOptionPackKeys(self, ctx:MySqlParser.TableOptionPackKeysContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableOptionPackKeys.
    def exitTableOptionPackKeys(self, ctx:MySqlParser.TableOptionPackKeysContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableOptionPassword.
    def enterTableOptionPassword(self, ctx:MySqlParser.TableOptionPasswordContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableOptionPassword.
    def exitTableOptionPassword(self, ctx:MySqlParser.TableOptionPasswordContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableOptionRowFormat.
    def enterTableOptionRowFormat(self, ctx:MySqlParser.TableOptionRowFormatContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableOptionRowFormat.
    def exitTableOptionRowFormat(self, ctx:MySqlParser.TableOptionRowFormatContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableOptionStartTransaction.
    def enterTableOptionStartTransaction(self, ctx:MySqlParser.TableOptionStartTransactionContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableOptionStartTransaction.
    def exitTableOptionStartTransaction(self, ctx:MySqlParser.TableOptionStartTransactionContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableOptionSecondaryEngineAttribute.
    def enterTableOptionSecondaryEngineAttribute(self, ctx:MySqlParser.TableOptionSecondaryEngineAttributeContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableOptionSecondaryEngineAttribute.
    def exitTableOptionSecondaryEngineAttribute(self, ctx:MySqlParser.TableOptionSecondaryEngineAttributeContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableOptionRecalculation.
    def enterTableOptionRecalculation(self, ctx:MySqlParser.TableOptionRecalculationContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableOptionRecalculation.
    def exitTableOptionRecalculation(self, ctx:MySqlParser.TableOptionRecalculationContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableOptionPersistent.
    def enterTableOptionPersistent(self, ctx:MySqlParser.TableOptionPersistentContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableOptionPersistent.
    def exitTableOptionPersistent(self, ctx:MySqlParser.TableOptionPersistentContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableOptionSamplePage.
    def enterTableOptionSamplePage(self, ctx:MySqlParser.TableOptionSamplePageContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableOptionSamplePage.
    def exitTableOptionSamplePage(self, ctx:MySqlParser.TableOptionSamplePageContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableOptionTablespace.
    def enterTableOptionTablespace(self, ctx:MySqlParser.TableOptionTablespaceContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableOptionTablespace.
    def exitTableOptionTablespace(self, ctx:MySqlParser.TableOptionTablespaceContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableOptionTableType.
    def enterTableOptionTableType(self, ctx:MySqlParser.TableOptionTableTypeContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableOptionTableType.
    def exitTableOptionTableType(self, ctx:MySqlParser.TableOptionTableTypeContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableOptionTransactional.
    def enterTableOptionTransactional(self, ctx:MySqlParser.TableOptionTransactionalContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableOptionTransactional.
    def exitTableOptionTransactional(self, ctx:MySqlParser.TableOptionTransactionalContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableOptionUnion.
    def enterTableOptionUnion(self, ctx:MySqlParser.TableOptionUnionContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableOptionUnion.
    def exitTableOptionUnion(self, ctx:MySqlParser.TableOptionUnionContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableType.
    def enterTableType(self, ctx:MySqlParser.TableTypeContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableType.
    def exitTableType(self, ctx:MySqlParser.TableTypeContext):
        pass


    # Enter a parse tree produced by MySqlParser#tablespaceStorage.
    def enterTablespaceStorage(self, ctx:MySqlParser.TablespaceStorageContext):
        pass

    # Exit a parse tree produced by MySqlParser#tablespaceStorage.
    def exitTablespaceStorage(self, ctx:MySqlParser.TablespaceStorageContext):
        pass


    # Enter a parse tree produced by MySqlParser#partitionDefinitions.
    def enterPartitionDefinitions(self, ctx:MySqlParser.PartitionDefinitionsContext):
        pass

    # Exit a parse tree produced by MySqlParser#partitionDefinitions.
    def exitPartitionDefinitions(self, ctx:MySqlParser.PartitionDefinitionsContext):
        pass


    # Enter a parse tree produced by MySqlParser#partitionFunctionHash.
    def enterPartitionFunctionHash(self, ctx:MySqlParser.PartitionFunctionHashContext):
        pass

    # Exit a parse tree produced by MySqlParser#partitionFunctionHash.
    def exitPartitionFunctionHash(self, ctx:MySqlParser.PartitionFunctionHashContext):
        pass


    # Enter a parse tree produced by MySqlParser#partitionFunctionKey.
    def enterPartitionFunctionKey(self, ctx:MySqlParser.PartitionFunctionKeyContext):
        pass

    # Exit a parse tree produced by MySqlParser#partitionFunctionKey.
    def exitPartitionFunctionKey(self, ctx:MySqlParser.PartitionFunctionKeyContext):
        pass


    # Enter a parse tree produced by MySqlParser#partitionFunctionRange.
    def enterPartitionFunctionRange(self, ctx:MySqlParser.PartitionFunctionRangeContext):
        pass

    # Exit a parse tree produced by MySqlParser#partitionFunctionRange.
    def exitPartitionFunctionRange(self, ctx:MySqlParser.PartitionFunctionRangeContext):
        pass


    # Enter a parse tree produced by MySqlParser#partitionFunctionList.
    def enterPartitionFunctionList(self, ctx:MySqlParser.PartitionFunctionListContext):
        pass

    # Exit a parse tree produced by MySqlParser#partitionFunctionList.
    def exitPartitionFunctionList(self, ctx:MySqlParser.PartitionFunctionListContext):
        pass


    # Enter a parse tree produced by MySqlParser#subPartitionFunctionHash.
    def enterSubPartitionFunctionHash(self, ctx:MySqlParser.SubPartitionFunctionHashContext):
        pass

    # Exit a parse tree produced by MySqlParser#subPartitionFunctionHash.
    def exitSubPartitionFunctionHash(self, ctx:MySqlParser.SubPartitionFunctionHashContext):
        pass


    # Enter a parse tree produced by MySqlParser#subPartitionFunctionKey.
    def enterSubPartitionFunctionKey(self, ctx:MySqlParser.SubPartitionFunctionKeyContext):
        pass

    # Exit a parse tree produced by MySqlParser#subPartitionFunctionKey.
    def exitSubPartitionFunctionKey(self, ctx:MySqlParser.SubPartitionFunctionKeyContext):
        pass


    # Enter a parse tree produced by MySqlParser#partitionComparison.
    def enterPartitionComparison(self, ctx:MySqlParser.PartitionComparisonContext):
        pass

    # Exit a parse tree produced by MySqlParser#partitionComparison.
    def exitPartitionComparison(self, ctx:MySqlParser.PartitionComparisonContext):
        pass


    # Enter a parse tree produced by MySqlParser#partitionListAtom.
    def enterPartitionListAtom(self, ctx:MySqlParser.PartitionListAtomContext):
        pass

    # Exit a parse tree produced by MySqlParser#partitionListAtom.
    def exitPartitionListAtom(self, ctx:MySqlParser.PartitionListAtomContext):
        pass


    # Enter a parse tree produced by MySqlParser#partitionListVector.
    def enterPartitionListVector(self, ctx:MySqlParser.PartitionListVectorContext):
        pass

    # Exit a parse tree produced by MySqlParser#partitionListVector.
    def exitPartitionListVector(self, ctx:MySqlParser.PartitionListVectorContext):
        pass


    # Enter a parse tree produced by MySqlParser#partitionSimple.
    def enterPartitionSimple(self, ctx:MySqlParser.PartitionSimpleContext):
        pass

    # Exit a parse tree produced by MySqlParser#partitionSimple.
    def exitPartitionSimple(self, ctx:MySqlParser.PartitionSimpleContext):
        pass


    # Enter a parse tree produced by MySqlParser#partitionDefinerAtom.
    def enterPartitionDefinerAtom(self, ctx:MySqlParser.PartitionDefinerAtomContext):
        pass

    # Exit a parse tree produced by MySqlParser#partitionDefinerAtom.
    def exitPartitionDefinerAtom(self, ctx:MySqlParser.PartitionDefinerAtomContext):
        pass


    # Enter a parse tree produced by MySqlParser#partitionDefinerVector.
    def enterPartitionDefinerVector(self, ctx:MySqlParser.PartitionDefinerVectorContext):
        pass

    # Exit a parse tree produced by MySqlParser#partitionDefinerVector.
    def exitPartitionDefinerVector(self, ctx:MySqlParser.PartitionDefinerVectorContext):
        pass


    # Enter a parse tree produced by MySqlParser#subpartitionDefinition.
    def enterSubpartitionDefinition(self, ctx:MySqlParser.SubpartitionDefinitionContext):
        pass

    # Exit a parse tree produced by MySqlParser#subpartitionDefinition.
    def exitSubpartitionDefinition(self, ctx:MySqlParser.SubpartitionDefinitionContext):
        pass


    # Enter a parse tree produced by MySqlParser#partitionOptionEngine.
    def enterPartitionOptionEngine(self, ctx:MySqlParser.PartitionOptionEngineContext):
        pass

    # Exit a parse tree produced by MySqlParser#partitionOptionEngine.
    def exitPartitionOptionEngine(self, ctx:MySqlParser.PartitionOptionEngineContext):
        pass


    # Enter a parse tree produced by MySqlParser#partitionOptionComment.
    def enterPartitionOptionComment(self, ctx:MySqlParser.PartitionOptionCommentContext):
        pass

    # Exit a parse tree produced by MySqlParser#partitionOptionComment.
    def exitPartitionOptionComment(self, ctx:MySqlParser.PartitionOptionCommentContext):
        pass


    # Enter a parse tree produced by MySqlParser#partitionOptionDataDirectory.
    def enterPartitionOptionDataDirectory(self, ctx:MySqlParser.PartitionOptionDataDirectoryContext):
        pass

    # Exit a parse tree produced by MySqlParser#partitionOptionDataDirectory.
    def exitPartitionOptionDataDirectory(self, ctx:MySqlParser.PartitionOptionDataDirectoryContext):
        pass


    # Enter a parse tree produced by MySqlParser#partitionOptionIndexDirectory.
    def enterPartitionOptionIndexDirectory(self, ctx:MySqlParser.PartitionOptionIndexDirectoryContext):
        pass

    # Exit a parse tree produced by MySqlParser#partitionOptionIndexDirectory.
    def exitPartitionOptionIndexDirectory(self, ctx:MySqlParser.PartitionOptionIndexDirectoryContext):
        pass


    # Enter a parse tree produced by MySqlParser#partitionOptionMaxRows.
    def enterPartitionOptionMaxRows(self, ctx:MySqlParser.PartitionOptionMaxRowsContext):
        pass

    # Exit a parse tree produced by MySqlParser#partitionOptionMaxRows.
    def exitPartitionOptionMaxRows(self, ctx:MySqlParser.PartitionOptionMaxRowsContext):
        pass


    # Enter a parse tree produced by MySqlParser#partitionOptionMinRows.
    def enterPartitionOptionMinRows(self, ctx:MySqlParser.PartitionOptionMinRowsContext):
        pass

    # Exit a parse tree produced by MySqlParser#partitionOptionMinRows.
    def exitPartitionOptionMinRows(self, ctx:MySqlParser.PartitionOptionMinRowsContext):
        pass


    # Enter a parse tree produced by MySqlParser#partitionOptionTablespace.
    def enterPartitionOptionTablespace(self, ctx:MySqlParser.PartitionOptionTablespaceContext):
        pass

    # Exit a parse tree produced by MySqlParser#partitionOptionTablespace.
    def exitPartitionOptionTablespace(self, ctx:MySqlParser.PartitionOptionTablespaceContext):
        pass


    # Enter a parse tree produced by MySqlParser#partitionOptionNodeGroup.
    def enterPartitionOptionNodeGroup(self, ctx:MySqlParser.PartitionOptionNodeGroupContext):
        pass

    # Exit a parse tree produced by MySqlParser#partitionOptionNodeGroup.
    def exitPartitionOptionNodeGroup(self, ctx:MySqlParser.PartitionOptionNodeGroupContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterSimpleDatabase.
    def enterAlterSimpleDatabase(self, ctx:MySqlParser.AlterSimpleDatabaseContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterSimpleDatabase.
    def exitAlterSimpleDatabase(self, ctx:MySqlParser.AlterSimpleDatabaseContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterUpgradeName.
    def enterAlterUpgradeName(self, ctx:MySqlParser.AlterUpgradeNameContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterUpgradeName.
    def exitAlterUpgradeName(self, ctx:MySqlParser.AlterUpgradeNameContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterEvent.
    def enterAlterEvent(self, ctx:MySqlParser.AlterEventContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterEvent.
    def exitAlterEvent(self, ctx:MySqlParser.AlterEventContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterFunction.
    def enterAlterFunction(self, ctx:MySqlParser.AlterFunctionContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterFunction.
    def exitAlterFunction(self, ctx:MySqlParser.AlterFunctionContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterInstance.
    def enterAlterInstance(self, ctx:MySqlParser.AlterInstanceContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterInstance.
    def exitAlterInstance(self, ctx:MySqlParser.AlterInstanceContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterLogfileGroup.
    def enterAlterLogfileGroup(self, ctx:MySqlParser.AlterLogfileGroupContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterLogfileGroup.
    def exitAlterLogfileGroup(self, ctx:MySqlParser.AlterLogfileGroupContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterProcedure.
    def enterAlterProcedure(self, ctx:MySqlParser.AlterProcedureContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterProcedure.
    def exitAlterProcedure(self, ctx:MySqlParser.AlterProcedureContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterServer.
    def enterAlterServer(self, ctx:MySqlParser.AlterServerContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterServer.
    def exitAlterServer(self, ctx:MySqlParser.AlterServerContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterTable.
    def enterAlterTable(self, ctx:MySqlParser.AlterTableContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterTable.
    def exitAlterTable(self, ctx:MySqlParser.AlterTableContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterTablespace.
    def enterAlterTablespace(self, ctx:MySqlParser.AlterTablespaceContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterTablespace.
    def exitAlterTablespace(self, ctx:MySqlParser.AlterTablespaceContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterView.
    def enterAlterView(self, ctx:MySqlParser.AlterViewContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterView.
    def exitAlterView(self, ctx:MySqlParser.AlterViewContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByTableOption.
    def enterAlterByTableOption(self, ctx:MySqlParser.AlterByTableOptionContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByTableOption.
    def exitAlterByTableOption(self, ctx:MySqlParser.AlterByTableOptionContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByAddColumn.
    def enterAlterByAddColumn(self, ctx:MySqlParser.AlterByAddColumnContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByAddColumn.
    def exitAlterByAddColumn(self, ctx:MySqlParser.AlterByAddColumnContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByAddColumns.
    def enterAlterByAddColumns(self, ctx:MySqlParser.AlterByAddColumnsContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByAddColumns.
    def exitAlterByAddColumns(self, ctx:MySqlParser.AlterByAddColumnsContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByAddIndex.
    def enterAlterByAddIndex(self, ctx:MySqlParser.AlterByAddIndexContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByAddIndex.
    def exitAlterByAddIndex(self, ctx:MySqlParser.AlterByAddIndexContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByAddPrimaryKey.
    def enterAlterByAddPrimaryKey(self, ctx:MySqlParser.AlterByAddPrimaryKeyContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByAddPrimaryKey.
    def exitAlterByAddPrimaryKey(self, ctx:MySqlParser.AlterByAddPrimaryKeyContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByAddUniqueKey.
    def enterAlterByAddUniqueKey(self, ctx:MySqlParser.AlterByAddUniqueKeyContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByAddUniqueKey.
    def exitAlterByAddUniqueKey(self, ctx:MySqlParser.AlterByAddUniqueKeyContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByAddSpecialIndex.
    def enterAlterByAddSpecialIndex(self, ctx:MySqlParser.AlterByAddSpecialIndexContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByAddSpecialIndex.
    def exitAlterByAddSpecialIndex(self, ctx:MySqlParser.AlterByAddSpecialIndexContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByAddForeignKey.
    def enterAlterByAddForeignKey(self, ctx:MySqlParser.AlterByAddForeignKeyContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByAddForeignKey.
    def exitAlterByAddForeignKey(self, ctx:MySqlParser.AlterByAddForeignKeyContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByAddCheckTableConstraint.
    def enterAlterByAddCheckTableConstraint(self, ctx:MySqlParser.AlterByAddCheckTableConstraintContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByAddCheckTableConstraint.
    def exitAlterByAddCheckTableConstraint(self, ctx:MySqlParser.AlterByAddCheckTableConstraintContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByAlterCheckTableConstraint.
    def enterAlterByAlterCheckTableConstraint(self, ctx:MySqlParser.AlterByAlterCheckTableConstraintContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByAlterCheckTableConstraint.
    def exitAlterByAlterCheckTableConstraint(self, ctx:MySqlParser.AlterByAlterCheckTableConstraintContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterBySetAlgorithm.
    def enterAlterBySetAlgorithm(self, ctx:MySqlParser.AlterBySetAlgorithmContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterBySetAlgorithm.
    def exitAlterBySetAlgorithm(self, ctx:MySqlParser.AlterBySetAlgorithmContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByChangeDefault.
    def enterAlterByChangeDefault(self, ctx:MySqlParser.AlterByChangeDefaultContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByChangeDefault.
    def exitAlterByChangeDefault(self, ctx:MySqlParser.AlterByChangeDefaultContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByChangeColumn.
    def enterAlterByChangeColumn(self, ctx:MySqlParser.AlterByChangeColumnContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByChangeColumn.
    def exitAlterByChangeColumn(self, ctx:MySqlParser.AlterByChangeColumnContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByRenameColumn.
    def enterAlterByRenameColumn(self, ctx:MySqlParser.AlterByRenameColumnContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByRenameColumn.
    def exitAlterByRenameColumn(self, ctx:MySqlParser.AlterByRenameColumnContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByLock.
    def enterAlterByLock(self, ctx:MySqlParser.AlterByLockContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByLock.
    def exitAlterByLock(self, ctx:MySqlParser.AlterByLockContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByModifyColumn.
    def enterAlterByModifyColumn(self, ctx:MySqlParser.AlterByModifyColumnContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByModifyColumn.
    def exitAlterByModifyColumn(self, ctx:MySqlParser.AlterByModifyColumnContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByDropColumn.
    def enterAlterByDropColumn(self, ctx:MySqlParser.AlterByDropColumnContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByDropColumn.
    def exitAlterByDropColumn(self, ctx:MySqlParser.AlterByDropColumnContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByDropConstraintCheck.
    def enterAlterByDropConstraintCheck(self, ctx:MySqlParser.AlterByDropConstraintCheckContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByDropConstraintCheck.
    def exitAlterByDropConstraintCheck(self, ctx:MySqlParser.AlterByDropConstraintCheckContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByDropPrimaryKey.
    def enterAlterByDropPrimaryKey(self, ctx:MySqlParser.AlterByDropPrimaryKeyContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByDropPrimaryKey.
    def exitAlterByDropPrimaryKey(self, ctx:MySqlParser.AlterByDropPrimaryKeyContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByDropIndex.
    def enterAlterByDropIndex(self, ctx:MySqlParser.AlterByDropIndexContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByDropIndex.
    def exitAlterByDropIndex(self, ctx:MySqlParser.AlterByDropIndexContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByRenameIndex.
    def enterAlterByRenameIndex(self, ctx:MySqlParser.AlterByRenameIndexContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByRenameIndex.
    def exitAlterByRenameIndex(self, ctx:MySqlParser.AlterByRenameIndexContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByAlterColumnDefault.
    def enterAlterByAlterColumnDefault(self, ctx:MySqlParser.AlterByAlterColumnDefaultContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByAlterColumnDefault.
    def exitAlterByAlterColumnDefault(self, ctx:MySqlParser.AlterByAlterColumnDefaultContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByAlterIndexVisibility.
    def enterAlterByAlterIndexVisibility(self, ctx:MySqlParser.AlterByAlterIndexVisibilityContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByAlterIndexVisibility.
    def exitAlterByAlterIndexVisibility(self, ctx:MySqlParser.AlterByAlterIndexVisibilityContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByDropForeignKey.
    def enterAlterByDropForeignKey(self, ctx:MySqlParser.AlterByDropForeignKeyContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByDropForeignKey.
    def exitAlterByDropForeignKey(self, ctx:MySqlParser.AlterByDropForeignKeyContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByDisableKeys.
    def enterAlterByDisableKeys(self, ctx:MySqlParser.AlterByDisableKeysContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByDisableKeys.
    def exitAlterByDisableKeys(self, ctx:MySqlParser.AlterByDisableKeysContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByEnableKeys.
    def enterAlterByEnableKeys(self, ctx:MySqlParser.AlterByEnableKeysContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByEnableKeys.
    def exitAlterByEnableKeys(self, ctx:MySqlParser.AlterByEnableKeysContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByRename.
    def enterAlterByRename(self, ctx:MySqlParser.AlterByRenameContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByRename.
    def exitAlterByRename(self, ctx:MySqlParser.AlterByRenameContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByOrder.
    def enterAlterByOrder(self, ctx:MySqlParser.AlterByOrderContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByOrder.
    def exitAlterByOrder(self, ctx:MySqlParser.AlterByOrderContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByConvertCharset.
    def enterAlterByConvertCharset(self, ctx:MySqlParser.AlterByConvertCharsetContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByConvertCharset.
    def exitAlterByConvertCharset(self, ctx:MySqlParser.AlterByConvertCharsetContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByDefaultCharset.
    def enterAlterByDefaultCharset(self, ctx:MySqlParser.AlterByDefaultCharsetContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByDefaultCharset.
    def exitAlterByDefaultCharset(self, ctx:MySqlParser.AlterByDefaultCharsetContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByDiscardTablespace.
    def enterAlterByDiscardTablespace(self, ctx:MySqlParser.AlterByDiscardTablespaceContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByDiscardTablespace.
    def exitAlterByDiscardTablespace(self, ctx:MySqlParser.AlterByDiscardTablespaceContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByImportTablespace.
    def enterAlterByImportTablespace(self, ctx:MySqlParser.AlterByImportTablespaceContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByImportTablespace.
    def exitAlterByImportTablespace(self, ctx:MySqlParser.AlterByImportTablespaceContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByForce.
    def enterAlterByForce(self, ctx:MySqlParser.AlterByForceContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByForce.
    def exitAlterByForce(self, ctx:MySqlParser.AlterByForceContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByValidate.
    def enterAlterByValidate(self, ctx:MySqlParser.AlterByValidateContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByValidate.
    def exitAlterByValidate(self, ctx:MySqlParser.AlterByValidateContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByAddDefinitions.
    def enterAlterByAddDefinitions(self, ctx:MySqlParser.AlterByAddDefinitionsContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByAddDefinitions.
    def exitAlterByAddDefinitions(self, ctx:MySqlParser.AlterByAddDefinitionsContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterPartition.
    def enterAlterPartition(self, ctx:MySqlParser.AlterPartitionContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterPartition.
    def exitAlterPartition(self, ctx:MySqlParser.AlterPartitionContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByAddPartition.
    def enterAlterByAddPartition(self, ctx:MySqlParser.AlterByAddPartitionContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByAddPartition.
    def exitAlterByAddPartition(self, ctx:MySqlParser.AlterByAddPartitionContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByDropPartition.
    def enterAlterByDropPartition(self, ctx:MySqlParser.AlterByDropPartitionContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByDropPartition.
    def exitAlterByDropPartition(self, ctx:MySqlParser.AlterByDropPartitionContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByDiscardPartition.
    def enterAlterByDiscardPartition(self, ctx:MySqlParser.AlterByDiscardPartitionContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByDiscardPartition.
    def exitAlterByDiscardPartition(self, ctx:MySqlParser.AlterByDiscardPartitionContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByImportPartition.
    def enterAlterByImportPartition(self, ctx:MySqlParser.AlterByImportPartitionContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByImportPartition.
    def exitAlterByImportPartition(self, ctx:MySqlParser.AlterByImportPartitionContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByTruncatePartition.
    def enterAlterByTruncatePartition(self, ctx:MySqlParser.AlterByTruncatePartitionContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByTruncatePartition.
    def exitAlterByTruncatePartition(self, ctx:MySqlParser.AlterByTruncatePartitionContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByCoalescePartition.
    def enterAlterByCoalescePartition(self, ctx:MySqlParser.AlterByCoalescePartitionContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByCoalescePartition.
    def exitAlterByCoalescePartition(self, ctx:MySqlParser.AlterByCoalescePartitionContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByReorganizePartition.
    def enterAlterByReorganizePartition(self, ctx:MySqlParser.AlterByReorganizePartitionContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByReorganizePartition.
    def exitAlterByReorganizePartition(self, ctx:MySqlParser.AlterByReorganizePartitionContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByExchangePartition.
    def enterAlterByExchangePartition(self, ctx:MySqlParser.AlterByExchangePartitionContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByExchangePartition.
    def exitAlterByExchangePartition(self, ctx:MySqlParser.AlterByExchangePartitionContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByAnalyzePartition.
    def enterAlterByAnalyzePartition(self, ctx:MySqlParser.AlterByAnalyzePartitionContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByAnalyzePartition.
    def exitAlterByAnalyzePartition(self, ctx:MySqlParser.AlterByAnalyzePartitionContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByCheckPartition.
    def enterAlterByCheckPartition(self, ctx:MySqlParser.AlterByCheckPartitionContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByCheckPartition.
    def exitAlterByCheckPartition(self, ctx:MySqlParser.AlterByCheckPartitionContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByOptimizePartition.
    def enterAlterByOptimizePartition(self, ctx:MySqlParser.AlterByOptimizePartitionContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByOptimizePartition.
    def exitAlterByOptimizePartition(self, ctx:MySqlParser.AlterByOptimizePartitionContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByRebuildPartition.
    def enterAlterByRebuildPartition(self, ctx:MySqlParser.AlterByRebuildPartitionContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByRebuildPartition.
    def exitAlterByRebuildPartition(self, ctx:MySqlParser.AlterByRebuildPartitionContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByRepairPartition.
    def enterAlterByRepairPartition(self, ctx:MySqlParser.AlterByRepairPartitionContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByRepairPartition.
    def exitAlterByRepairPartition(self, ctx:MySqlParser.AlterByRepairPartitionContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByRemovePartitioning.
    def enterAlterByRemovePartitioning(self, ctx:MySqlParser.AlterByRemovePartitioningContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByRemovePartitioning.
    def exitAlterByRemovePartitioning(self, ctx:MySqlParser.AlterByRemovePartitioningContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterByUpgradePartitioning.
    def enterAlterByUpgradePartitioning(self, ctx:MySqlParser.AlterByUpgradePartitioningContext):
        pass

    # Exit a parse tree produced by MySqlParser#alterByUpgradePartitioning.
    def exitAlterByUpgradePartitioning(self, ctx:MySqlParser.AlterByUpgradePartitioningContext):
        pass


    # Enter a parse tree produced by MySqlParser#dropDatabase.
    def enterDropDatabase(self, ctx:MySqlParser.DropDatabaseContext):
        pass

    # Exit a parse tree produced by MySqlParser#dropDatabase.
    def exitDropDatabase(self, ctx:MySqlParser.DropDatabaseContext):
        pass


    # Enter a parse tree produced by MySqlParser#dropEvent.
    def enterDropEvent(self, ctx:MySqlParser.DropEventContext):
        pass

    # Exit a parse tree produced by MySqlParser#dropEvent.
    def exitDropEvent(self, ctx:MySqlParser.DropEventContext):
        pass


    # Enter a parse tree produced by MySqlParser#dropIndex.
    def enterDropIndex(self, ctx:MySqlParser.DropIndexContext):
        pass

    # Exit a parse tree produced by MySqlParser#dropIndex.
    def exitDropIndex(self, ctx:MySqlParser.DropIndexContext):
        pass


    # Enter a parse tree produced by MySqlParser#dropLogfileGroup.
    def enterDropLogfileGroup(self, ctx:MySqlParser.DropLogfileGroupContext):
        pass

    # Exit a parse tree produced by MySqlParser#dropLogfileGroup.
    def exitDropLogfileGroup(self, ctx:MySqlParser.DropLogfileGroupContext):
        pass


    # Enter a parse tree produced by MySqlParser#dropProcedure.
    def enterDropProcedure(self, ctx:MySqlParser.DropProcedureContext):
        pass

    # Exit a parse tree produced by MySqlParser#dropProcedure.
    def exitDropProcedure(self, ctx:MySqlParser.DropProcedureContext):
        pass


    # Enter a parse tree produced by MySqlParser#dropFunction.
    def enterDropFunction(self, ctx:MySqlParser.DropFunctionContext):
        pass

    # Exit a parse tree produced by MySqlParser#dropFunction.
    def exitDropFunction(self, ctx:MySqlParser.DropFunctionContext):
        pass


    # Enter a parse tree produced by MySqlParser#dropServer.
    def enterDropServer(self, ctx:MySqlParser.DropServerContext):
        pass

    # Exit a parse tree produced by MySqlParser#dropServer.
    def exitDropServer(self, ctx:MySqlParser.DropServerContext):
        pass


    # Enter a parse tree produced by MySqlParser#dropTable.
    def enterDropTable(self, ctx:MySqlParser.DropTableContext):
        pass

    # Exit a parse tree produced by MySqlParser#dropTable.
    def exitDropTable(self, ctx:MySqlParser.DropTableContext):
        pass


    # Enter a parse tree produced by MySqlParser#dropTablespace.
    def enterDropTablespace(self, ctx:MySqlParser.DropTablespaceContext):
        pass

    # Exit a parse tree produced by MySqlParser#dropTablespace.
    def exitDropTablespace(self, ctx:MySqlParser.DropTablespaceContext):
        pass


    # Enter a parse tree produced by MySqlParser#dropTrigger.
    def enterDropTrigger(self, ctx:MySqlParser.DropTriggerContext):
        pass

    # Exit a parse tree produced by MySqlParser#dropTrigger.
    def exitDropTrigger(self, ctx:MySqlParser.DropTriggerContext):
        pass


    # Enter a parse tree produced by MySqlParser#dropView.
    def enterDropView(self, ctx:MySqlParser.DropViewContext):
        pass

    # Exit a parse tree produced by MySqlParser#dropView.
    def exitDropView(self, ctx:MySqlParser.DropViewContext):
        pass


    # Enter a parse tree produced by MySqlParser#dropRole.
    def enterDropRole(self, ctx:MySqlParser.DropRoleContext):
        pass

    # Exit a parse tree produced by MySqlParser#dropRole.
    def exitDropRole(self, ctx:MySqlParser.DropRoleContext):
        pass


    # Enter a parse tree produced by MySqlParser#setRole.
    def enterSetRole(self, ctx:MySqlParser.SetRoleContext):
        pass

    # Exit a parse tree produced by MySqlParser#setRole.
    def exitSetRole(self, ctx:MySqlParser.SetRoleContext):
        pass


    # Enter a parse tree produced by MySqlParser#renameTable.
    def enterRenameTable(self, ctx:MySqlParser.RenameTableContext):
        pass

    # Exit a parse tree produced by MySqlParser#renameTable.
    def exitRenameTable(self, ctx:MySqlParser.RenameTableContext):
        pass


    # Enter a parse tree produced by MySqlParser#renameTableClause.
    def enterRenameTableClause(self, ctx:MySqlParser.RenameTableClauseContext):
        pass

    # Exit a parse tree produced by MySqlParser#renameTableClause.
    def exitRenameTableClause(self, ctx:MySqlParser.RenameTableClauseContext):
        pass


    # Enter a parse tree produced by MySqlParser#truncateTable.
    def enterTruncateTable(self, ctx:MySqlParser.TruncateTableContext):
        pass

    # Exit a parse tree produced by MySqlParser#truncateTable.
    def exitTruncateTable(self, ctx:MySqlParser.TruncateTableContext):
        pass


    # Enter a parse tree produced by MySqlParser#callStatement.
    def enterCallStatement(self, ctx:MySqlParser.CallStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#callStatement.
    def exitCallStatement(self, ctx:MySqlParser.CallStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#deleteStatement.
    def enterDeleteStatement(self, ctx:MySqlParser.DeleteStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#deleteStatement.
    def exitDeleteStatement(self, ctx:MySqlParser.DeleteStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#doStatement.
    def enterDoStatement(self, ctx:MySqlParser.DoStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#doStatement.
    def exitDoStatement(self, ctx:MySqlParser.DoStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#handlerStatement.
    def enterHandlerStatement(self, ctx:MySqlParser.HandlerStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#handlerStatement.
    def exitHandlerStatement(self, ctx:MySqlParser.HandlerStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#insertStatement.
    def enterInsertStatement(self, ctx:MySqlParser.InsertStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#insertStatement.
    def exitInsertStatement(self, ctx:MySqlParser.InsertStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#loadDataStatement.
    def enterLoadDataStatement(self, ctx:MySqlParser.LoadDataStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#loadDataStatement.
    def exitLoadDataStatement(self, ctx:MySqlParser.LoadDataStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#loadXmlStatement.
    def enterLoadXmlStatement(self, ctx:MySqlParser.LoadXmlStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#loadXmlStatement.
    def exitLoadXmlStatement(self, ctx:MySqlParser.LoadXmlStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#replaceStatement.
    def enterReplaceStatement(self, ctx:MySqlParser.ReplaceStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#replaceStatement.
    def exitReplaceStatement(self, ctx:MySqlParser.ReplaceStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#simpleSelect.
    def enterSimpleSelect(self, ctx:MySqlParser.SimpleSelectContext):
        pass

    # Exit a parse tree produced by MySqlParser#simpleSelect.
    def exitSimpleSelect(self, ctx:MySqlParser.SimpleSelectContext):
        pass


    # Enter a parse tree produced by MySqlParser#parenthesisSelect.
    def enterParenthesisSelect(self, ctx:MySqlParser.ParenthesisSelectContext):
        pass

    # Exit a parse tree produced by MySqlParser#parenthesisSelect.
    def exitParenthesisSelect(self, ctx:MySqlParser.ParenthesisSelectContext):
        pass


    # Enter a parse tree produced by MySqlParser#unionSelect.
    def enterUnionSelect(self, ctx:MySqlParser.UnionSelectContext):
        pass

    # Exit a parse tree produced by MySqlParser#unionSelect.
    def exitUnionSelect(self, ctx:MySqlParser.UnionSelectContext):
        pass


    # Enter a parse tree produced by MySqlParser#unionParenthesisSelect.
    def enterUnionParenthesisSelect(self, ctx:MySqlParser.UnionParenthesisSelectContext):
        pass

    # Exit a parse tree produced by MySqlParser#unionParenthesisSelect.
    def exitUnionParenthesisSelect(self, ctx:MySqlParser.UnionParenthesisSelectContext):
        pass


    # Enter a parse tree produced by MySqlParser#withLateralStatement.
    def enterWithLateralStatement(self, ctx:MySqlParser.WithLateralStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#withLateralStatement.
    def exitWithLateralStatement(self, ctx:MySqlParser.WithLateralStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#updateStatement.
    def enterUpdateStatement(self, ctx:MySqlParser.UpdateStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#updateStatement.
    def exitUpdateStatement(self, ctx:MySqlParser.UpdateStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#valuesStatement.
    def enterValuesStatement(self, ctx:MySqlParser.ValuesStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#valuesStatement.
    def exitValuesStatement(self, ctx:MySqlParser.ValuesStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#insertStatementValue.
    def enterInsertStatementValue(self, ctx:MySqlParser.InsertStatementValueContext):
        pass

    # Exit a parse tree produced by MySqlParser#insertStatementValue.
    def exitInsertStatementValue(self, ctx:MySqlParser.InsertStatementValueContext):
        pass


    # Enter a parse tree produced by MySqlParser#updatedElement.
    def enterUpdatedElement(self, ctx:MySqlParser.UpdatedElementContext):
        pass

    # Exit a parse tree produced by MySqlParser#updatedElement.
    def exitUpdatedElement(self, ctx:MySqlParser.UpdatedElementContext):
        pass


    # Enter a parse tree produced by MySqlParser#assignmentField.
    def enterAssignmentField(self, ctx:MySqlParser.AssignmentFieldContext):
        pass

    # Exit a parse tree produced by MySqlParser#assignmentField.
    def exitAssignmentField(self, ctx:MySqlParser.AssignmentFieldContext):
        pass


    # Enter a parse tree produced by MySqlParser#lockClause.
    def enterLockClause(self, ctx:MySqlParser.LockClauseContext):
        pass

    # Exit a parse tree produced by MySqlParser#lockClause.
    def exitLockClause(self, ctx:MySqlParser.LockClauseContext):
        pass


    # Enter a parse tree produced by MySqlParser#singleDeleteStatement.
    def enterSingleDeleteStatement(self, ctx:MySqlParser.SingleDeleteStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#singleDeleteStatement.
    def exitSingleDeleteStatement(self, ctx:MySqlParser.SingleDeleteStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#multipleDeleteStatement.
    def enterMultipleDeleteStatement(self, ctx:MySqlParser.MultipleDeleteStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#multipleDeleteStatement.
    def exitMultipleDeleteStatement(self, ctx:MySqlParser.MultipleDeleteStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#handlerOpenStatement.
    def enterHandlerOpenStatement(self, ctx:MySqlParser.HandlerOpenStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#handlerOpenStatement.
    def exitHandlerOpenStatement(self, ctx:MySqlParser.HandlerOpenStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#handlerReadIndexStatement.
    def enterHandlerReadIndexStatement(self, ctx:MySqlParser.HandlerReadIndexStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#handlerReadIndexStatement.
    def exitHandlerReadIndexStatement(self, ctx:MySqlParser.HandlerReadIndexStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#handlerReadStatement.
    def enterHandlerReadStatement(self, ctx:MySqlParser.HandlerReadStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#handlerReadStatement.
    def exitHandlerReadStatement(self, ctx:MySqlParser.HandlerReadStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#handlerCloseStatement.
    def enterHandlerCloseStatement(self, ctx:MySqlParser.HandlerCloseStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#handlerCloseStatement.
    def exitHandlerCloseStatement(self, ctx:MySqlParser.HandlerCloseStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#singleUpdateStatement.
    def enterSingleUpdateStatement(self, ctx:MySqlParser.SingleUpdateStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#singleUpdateStatement.
    def exitSingleUpdateStatement(self, ctx:MySqlParser.SingleUpdateStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#multipleUpdateStatement.
    def enterMultipleUpdateStatement(self, ctx:MySqlParser.MultipleUpdateStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#multipleUpdateStatement.
    def exitMultipleUpdateStatement(self, ctx:MySqlParser.MultipleUpdateStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#orderByClause.
    def enterOrderByClause(self, ctx:MySqlParser.OrderByClauseContext):
        pass

    # Exit a parse tree produced by MySqlParser#orderByClause.
    def exitOrderByClause(self, ctx:MySqlParser.OrderByClauseContext):
        pass


    # Enter a parse tree produced by MySqlParser#orderByExpression.
    def enterOrderByExpression(self, ctx:MySqlParser.OrderByExpressionContext):
        pass

    # Exit a parse tree produced by MySqlParser#orderByExpression.
    def exitOrderByExpression(self, ctx:MySqlParser.OrderByExpressionContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableSources.
    def enterTableSources(self, ctx:MySqlParser.TableSourcesContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableSources.
    def exitTableSources(self, ctx:MySqlParser.TableSourcesContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableSourceBase.
    def enterTableSourceBase(self, ctx:MySqlParser.TableSourceBaseContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableSourceBase.
    def exitTableSourceBase(self, ctx:MySqlParser.TableSourceBaseContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableSourceNested.
    def enterTableSourceNested(self, ctx:MySqlParser.TableSourceNestedContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableSourceNested.
    def exitTableSourceNested(self, ctx:MySqlParser.TableSourceNestedContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableJson.
    def enterTableJson(self, ctx:MySqlParser.TableJsonContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableJson.
    def exitTableJson(self, ctx:MySqlParser.TableJsonContext):
        pass


    # Enter a parse tree produced by MySqlParser#atomTableItem.
    def enterAtomTableItem(self, ctx:MySqlParser.AtomTableItemContext):
        pass

    # Exit a parse tree produced by MySqlParser#atomTableItem.
    def exitAtomTableItem(self, ctx:MySqlParser.AtomTableItemContext):
        pass


    # Enter a parse tree produced by MySqlParser#subqueryTableItem.
    def enterSubqueryTableItem(self, ctx:MySqlParser.SubqueryTableItemContext):
        pass

    # Exit a parse tree produced by MySqlParser#subqueryTableItem.
    def exitSubqueryTableItem(self, ctx:MySqlParser.SubqueryTableItemContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableSourcesItem.
    def enterTableSourcesItem(self, ctx:MySqlParser.TableSourcesItemContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableSourcesItem.
    def exitTableSourcesItem(self, ctx:MySqlParser.TableSourcesItemContext):
        pass


    # Enter a parse tree produced by MySqlParser#indexHint.
    def enterIndexHint(self, ctx:MySqlParser.IndexHintContext):
        pass

    # Exit a parse tree produced by MySqlParser#indexHint.
    def exitIndexHint(self, ctx:MySqlParser.IndexHintContext):
        pass


    # Enter a parse tree produced by MySqlParser#indexHintType.
    def enterIndexHintType(self, ctx:MySqlParser.IndexHintTypeContext):
        pass

    # Exit a parse tree produced by MySqlParser#indexHintType.
    def exitIndexHintType(self, ctx:MySqlParser.IndexHintTypeContext):
        pass


    # Enter a parse tree produced by MySqlParser#innerJoin.
    def enterInnerJoin(self, ctx:MySqlParser.InnerJoinContext):
        pass

    # Exit a parse tree produced by MySqlParser#innerJoin.
    def exitInnerJoin(self, ctx:MySqlParser.InnerJoinContext):
        pass


    # Enter a parse tree produced by MySqlParser#straightJoin.
    def enterStraightJoin(self, ctx:MySqlParser.StraightJoinContext):
        pass

    # Exit a parse tree produced by MySqlParser#straightJoin.
    def exitStraightJoin(self, ctx:MySqlParser.StraightJoinContext):
        pass


    # Enter a parse tree produced by MySqlParser#outerJoin.
    def enterOuterJoin(self, ctx:MySqlParser.OuterJoinContext):
        pass

    # Exit a parse tree produced by MySqlParser#outerJoin.
    def exitOuterJoin(self, ctx:MySqlParser.OuterJoinContext):
        pass


    # Enter a parse tree produced by MySqlParser#naturalJoin.
    def enterNaturalJoin(self, ctx:MySqlParser.NaturalJoinContext):
        pass

    # Exit a parse tree produced by MySqlParser#naturalJoin.
    def exitNaturalJoin(self, ctx:MySqlParser.NaturalJoinContext):
        pass


    # Enter a parse tree produced by MySqlParser#joinSpec.
    def enterJoinSpec(self, ctx:MySqlParser.JoinSpecContext):
        pass

    # Exit a parse tree produced by MySqlParser#joinSpec.
    def exitJoinSpec(self, ctx:MySqlParser.JoinSpecContext):
        pass


    # Enter a parse tree produced by MySqlParser#queryExpression.
    def enterQueryExpression(self, ctx:MySqlParser.QueryExpressionContext):
        pass

    # Exit a parse tree produced by MySqlParser#queryExpression.
    def exitQueryExpression(self, ctx:MySqlParser.QueryExpressionContext):
        pass


    # Enter a parse tree produced by MySqlParser#queryExpressionNointo.
    def enterQueryExpressionNointo(self, ctx:MySqlParser.QueryExpressionNointoContext):
        pass

    # Exit a parse tree produced by MySqlParser#queryExpressionNointo.
    def exitQueryExpressionNointo(self, ctx:MySqlParser.QueryExpressionNointoContext):
        pass


    # Enter a parse tree produced by MySqlParser#querySpecification.
    def enterQuerySpecification(self, ctx:MySqlParser.QuerySpecificationContext):
        pass

    # Exit a parse tree produced by MySqlParser#querySpecification.
    def exitQuerySpecification(self, ctx:MySqlParser.QuerySpecificationContext):
        pass


    # Enter a parse tree produced by MySqlParser#querySpecificationNointo.
    def enterQuerySpecificationNointo(self, ctx:MySqlParser.QuerySpecificationNointoContext):
        pass

    # Exit a parse tree produced by MySqlParser#querySpecificationNointo.
    def exitQuerySpecificationNointo(self, ctx:MySqlParser.QuerySpecificationNointoContext):
        pass


    # Enter a parse tree produced by MySqlParser#unionParenthesis.
    def enterUnionParenthesis(self, ctx:MySqlParser.UnionParenthesisContext):
        pass

    # Exit a parse tree produced by MySqlParser#unionParenthesis.
    def exitUnionParenthesis(self, ctx:MySqlParser.UnionParenthesisContext):
        pass


    # Enter a parse tree produced by MySqlParser#unionStatement.
    def enterUnionStatement(self, ctx:MySqlParser.UnionStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#unionStatement.
    def exitUnionStatement(self, ctx:MySqlParser.UnionStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#lateralStatement.
    def enterLateralStatement(self, ctx:MySqlParser.LateralStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#lateralStatement.
    def exitLateralStatement(self, ctx:MySqlParser.LateralStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#jsonTable.
    def enterJsonTable(self, ctx:MySqlParser.JsonTableContext):
        pass

    # Exit a parse tree produced by MySqlParser#jsonTable.
    def exitJsonTable(self, ctx:MySqlParser.JsonTableContext):
        pass


    # Enter a parse tree produced by MySqlParser#jsonColumnList.
    def enterJsonColumnList(self, ctx:MySqlParser.JsonColumnListContext):
        pass

    # Exit a parse tree produced by MySqlParser#jsonColumnList.
    def exitJsonColumnList(self, ctx:MySqlParser.JsonColumnListContext):
        pass


    # Enter a parse tree produced by MySqlParser#jsonColumn.
    def enterJsonColumn(self, ctx:MySqlParser.JsonColumnContext):
        pass

    # Exit a parse tree produced by MySqlParser#jsonColumn.
    def exitJsonColumn(self, ctx:MySqlParser.JsonColumnContext):
        pass


    # Enter a parse tree produced by MySqlParser#jsonOnEmpty.
    def enterJsonOnEmpty(self, ctx:MySqlParser.JsonOnEmptyContext):
        pass

    # Exit a parse tree produced by MySqlParser#jsonOnEmpty.
    def exitJsonOnEmpty(self, ctx:MySqlParser.JsonOnEmptyContext):
        pass


    # Enter a parse tree produced by MySqlParser#jsonOnError.
    def enterJsonOnError(self, ctx:MySqlParser.JsonOnErrorContext):
        pass

    # Exit a parse tree produced by MySqlParser#jsonOnError.
    def exitJsonOnError(self, ctx:MySqlParser.JsonOnErrorContext):
        pass


    # Enter a parse tree produced by MySqlParser#selectSpec.
    def enterSelectSpec(self, ctx:MySqlParser.SelectSpecContext):
        pass

    # Exit a parse tree produced by MySqlParser#selectSpec.
    def exitSelectSpec(self, ctx:MySqlParser.SelectSpecContext):
        pass


    # Enter a parse tree produced by MySqlParser#selectElements.
    def enterSelectElements(self, ctx:MySqlParser.SelectElementsContext):
        pass

    # Exit a parse tree produced by MySqlParser#selectElements.
    def exitSelectElements(self, ctx:MySqlParser.SelectElementsContext):
        pass


    # Enter a parse tree produced by MySqlParser#selectStarElement.
    def enterSelectStarElement(self, ctx:MySqlParser.SelectStarElementContext):
        pass

    # Exit a parse tree produced by MySqlParser#selectStarElement.
    def exitSelectStarElement(self, ctx:MySqlParser.SelectStarElementContext):
        pass


    # Enter a parse tree produced by MySqlParser#selectColumnElement.
    def enterSelectColumnElement(self, ctx:MySqlParser.SelectColumnElementContext):
        pass

    # Exit a parse tree produced by MySqlParser#selectColumnElement.
    def exitSelectColumnElement(self, ctx:MySqlParser.SelectColumnElementContext):
        pass


    # Enter a parse tree produced by MySqlParser#selectFunctionElement.
    def enterSelectFunctionElement(self, ctx:MySqlParser.SelectFunctionElementContext):
        pass

    # Exit a parse tree produced by MySqlParser#selectFunctionElement.
    def exitSelectFunctionElement(self, ctx:MySqlParser.SelectFunctionElementContext):
        pass


    # Enter a parse tree produced by MySqlParser#selectExpressionElement.
    def enterSelectExpressionElement(self, ctx:MySqlParser.SelectExpressionElementContext):
        pass

    # Exit a parse tree produced by MySqlParser#selectExpressionElement.
    def exitSelectExpressionElement(self, ctx:MySqlParser.SelectExpressionElementContext):
        pass


    # Enter a parse tree produced by MySqlParser#selectIntoVariables.
    def enterSelectIntoVariables(self, ctx:MySqlParser.SelectIntoVariablesContext):
        pass

    # Exit a parse tree produced by MySqlParser#selectIntoVariables.
    def exitSelectIntoVariables(self, ctx:MySqlParser.SelectIntoVariablesContext):
        pass


    # Enter a parse tree produced by MySqlParser#selectIntoDumpFile.
    def enterSelectIntoDumpFile(self, ctx:MySqlParser.SelectIntoDumpFileContext):
        pass

    # Exit a parse tree produced by MySqlParser#selectIntoDumpFile.
    def exitSelectIntoDumpFile(self, ctx:MySqlParser.SelectIntoDumpFileContext):
        pass


    # Enter a parse tree produced by MySqlParser#selectIntoTextFile.
    def enterSelectIntoTextFile(self, ctx:MySqlParser.SelectIntoTextFileContext):
        pass

    # Exit a parse tree produced by MySqlParser#selectIntoTextFile.
    def exitSelectIntoTextFile(self, ctx:MySqlParser.SelectIntoTextFileContext):
        pass


    # Enter a parse tree produced by MySqlParser#selectFieldsInto.
    def enterSelectFieldsInto(self, ctx:MySqlParser.SelectFieldsIntoContext):
        pass

    # Exit a parse tree produced by MySqlParser#selectFieldsInto.
    def exitSelectFieldsInto(self, ctx:MySqlParser.SelectFieldsIntoContext):
        pass


    # Enter a parse tree produced by MySqlParser#selectLinesInto.
    def enterSelectLinesInto(self, ctx:MySqlParser.SelectLinesIntoContext):
        pass

    # Exit a parse tree produced by MySqlParser#selectLinesInto.
    def exitSelectLinesInto(self, ctx:MySqlParser.SelectLinesIntoContext):
        pass


    # Enter a parse tree produced by MySqlParser#fromClause.
    def enterFromClause(self, ctx:MySqlParser.FromClauseContext):
        pass

    # Exit a parse tree produced by MySqlParser#fromClause.
    def exitFromClause(self, ctx:MySqlParser.FromClauseContext):
        pass


    # Enter a parse tree produced by MySqlParser#groupByClause.
    def enterGroupByClause(self, ctx:MySqlParser.GroupByClauseContext):
        pass

    # Exit a parse tree produced by MySqlParser#groupByClause.
    def exitGroupByClause(self, ctx:MySqlParser.GroupByClauseContext):
        pass


    # Enter a parse tree produced by MySqlParser#havingClause.
    def enterHavingClause(self, ctx:MySqlParser.HavingClauseContext):
        pass

    # Exit a parse tree produced by MySqlParser#havingClause.
    def exitHavingClause(self, ctx:MySqlParser.HavingClauseContext):
        pass


    # Enter a parse tree produced by MySqlParser#windowClause.
    def enterWindowClause(self, ctx:MySqlParser.WindowClauseContext):
        pass

    # Exit a parse tree produced by MySqlParser#windowClause.
    def exitWindowClause(self, ctx:MySqlParser.WindowClauseContext):
        pass


    # Enter a parse tree produced by MySqlParser#groupByItem.
    def enterGroupByItem(self, ctx:MySqlParser.GroupByItemContext):
        pass

    # Exit a parse tree produced by MySqlParser#groupByItem.
    def exitGroupByItem(self, ctx:MySqlParser.GroupByItemContext):
        pass


    # Enter a parse tree produced by MySqlParser#limitClause.
    def enterLimitClause(self, ctx:MySqlParser.LimitClauseContext):
        pass

    # Exit a parse tree produced by MySqlParser#limitClause.
    def exitLimitClause(self, ctx:MySqlParser.LimitClauseContext):
        pass


    # Enter a parse tree produced by MySqlParser#limitClauseAtom.
    def enterLimitClauseAtom(self, ctx:MySqlParser.LimitClauseAtomContext):
        pass

    # Exit a parse tree produced by MySqlParser#limitClauseAtom.
    def exitLimitClauseAtom(self, ctx:MySqlParser.LimitClauseAtomContext):
        pass


    # Enter a parse tree produced by MySqlParser#startTransaction.
    def enterStartTransaction(self, ctx:MySqlParser.StartTransactionContext):
        pass

    # Exit a parse tree produced by MySqlParser#startTransaction.
    def exitStartTransaction(self, ctx:MySqlParser.StartTransactionContext):
        pass


    # Enter a parse tree produced by MySqlParser#beginWork.
    def enterBeginWork(self, ctx:MySqlParser.BeginWorkContext):
        pass

    # Exit a parse tree produced by MySqlParser#beginWork.
    def exitBeginWork(self, ctx:MySqlParser.BeginWorkContext):
        pass


    # Enter a parse tree produced by MySqlParser#commitWork.
    def enterCommitWork(self, ctx:MySqlParser.CommitWorkContext):
        pass

    # Exit a parse tree produced by MySqlParser#commitWork.
    def exitCommitWork(self, ctx:MySqlParser.CommitWorkContext):
        pass


    # Enter a parse tree produced by MySqlParser#rollbackWork.
    def enterRollbackWork(self, ctx:MySqlParser.RollbackWorkContext):
        pass

    # Exit a parse tree produced by MySqlParser#rollbackWork.
    def exitRollbackWork(self, ctx:MySqlParser.RollbackWorkContext):
        pass


    # Enter a parse tree produced by MySqlParser#savepointStatement.
    def enterSavepointStatement(self, ctx:MySqlParser.SavepointStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#savepointStatement.
    def exitSavepointStatement(self, ctx:MySqlParser.SavepointStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#rollbackStatement.
    def enterRollbackStatement(self, ctx:MySqlParser.RollbackStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#rollbackStatement.
    def exitRollbackStatement(self, ctx:MySqlParser.RollbackStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#releaseStatement.
    def enterReleaseStatement(self, ctx:MySqlParser.ReleaseStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#releaseStatement.
    def exitReleaseStatement(self, ctx:MySqlParser.ReleaseStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#lockTables.
    def enterLockTables(self, ctx:MySqlParser.LockTablesContext):
        pass

    # Exit a parse tree produced by MySqlParser#lockTables.
    def exitLockTables(self, ctx:MySqlParser.LockTablesContext):
        pass


    # Enter a parse tree produced by MySqlParser#unlockTables.
    def enterUnlockTables(self, ctx:MySqlParser.UnlockTablesContext):
        pass

    # Exit a parse tree produced by MySqlParser#unlockTables.
    def exitUnlockTables(self, ctx:MySqlParser.UnlockTablesContext):
        pass


    # Enter a parse tree produced by MySqlParser#setAutocommitStatement.
    def enterSetAutocommitStatement(self, ctx:MySqlParser.SetAutocommitStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#setAutocommitStatement.
    def exitSetAutocommitStatement(self, ctx:MySqlParser.SetAutocommitStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#setTransactionStatement.
    def enterSetTransactionStatement(self, ctx:MySqlParser.SetTransactionStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#setTransactionStatement.
    def exitSetTransactionStatement(self, ctx:MySqlParser.SetTransactionStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#transactionMode.
    def enterTransactionMode(self, ctx:MySqlParser.TransactionModeContext):
        pass

    # Exit a parse tree produced by MySqlParser#transactionMode.
    def exitTransactionMode(self, ctx:MySqlParser.TransactionModeContext):
        pass


    # Enter a parse tree produced by MySqlParser#lockTableElement.
    def enterLockTableElement(self, ctx:MySqlParser.LockTableElementContext):
        pass

    # Exit a parse tree produced by MySqlParser#lockTableElement.
    def exitLockTableElement(self, ctx:MySqlParser.LockTableElementContext):
        pass


    # Enter a parse tree produced by MySqlParser#lockAction.
    def enterLockAction(self, ctx:MySqlParser.LockActionContext):
        pass

    # Exit a parse tree produced by MySqlParser#lockAction.
    def exitLockAction(self, ctx:MySqlParser.LockActionContext):
        pass


    # Enter a parse tree produced by MySqlParser#transactionOption.
    def enterTransactionOption(self, ctx:MySqlParser.TransactionOptionContext):
        pass

    # Exit a parse tree produced by MySqlParser#transactionOption.
    def exitTransactionOption(self, ctx:MySqlParser.TransactionOptionContext):
        pass


    # Enter a parse tree produced by MySqlParser#transactionLevel.
    def enterTransactionLevel(self, ctx:MySqlParser.TransactionLevelContext):
        pass

    # Exit a parse tree produced by MySqlParser#transactionLevel.
    def exitTransactionLevel(self, ctx:MySqlParser.TransactionLevelContext):
        pass


    # Enter a parse tree produced by MySqlParser#changeMaster.
    def enterChangeMaster(self, ctx:MySqlParser.ChangeMasterContext):
        pass

    # Exit a parse tree produced by MySqlParser#changeMaster.
    def exitChangeMaster(self, ctx:MySqlParser.ChangeMasterContext):
        pass


    # Enter a parse tree produced by MySqlParser#changeReplicationFilter.
    def enterChangeReplicationFilter(self, ctx:MySqlParser.ChangeReplicationFilterContext):
        pass

    # Exit a parse tree produced by MySqlParser#changeReplicationFilter.
    def exitChangeReplicationFilter(self, ctx:MySqlParser.ChangeReplicationFilterContext):
        pass


    # Enter a parse tree produced by MySqlParser#purgeBinaryLogs.
    def enterPurgeBinaryLogs(self, ctx:MySqlParser.PurgeBinaryLogsContext):
        pass

    # Exit a parse tree produced by MySqlParser#purgeBinaryLogs.
    def exitPurgeBinaryLogs(self, ctx:MySqlParser.PurgeBinaryLogsContext):
        pass


    # Enter a parse tree produced by MySqlParser#resetMaster.
    def enterResetMaster(self, ctx:MySqlParser.ResetMasterContext):
        pass

    # Exit a parse tree produced by MySqlParser#resetMaster.
    def exitResetMaster(self, ctx:MySqlParser.ResetMasterContext):
        pass


    # Enter a parse tree produced by MySqlParser#resetSlave.
    def enterResetSlave(self, ctx:MySqlParser.ResetSlaveContext):
        pass

    # Exit a parse tree produced by MySqlParser#resetSlave.
    def exitResetSlave(self, ctx:MySqlParser.ResetSlaveContext):
        pass


    # Enter a parse tree produced by MySqlParser#startSlave.
    def enterStartSlave(self, ctx:MySqlParser.StartSlaveContext):
        pass

    # Exit a parse tree produced by MySqlParser#startSlave.
    def exitStartSlave(self, ctx:MySqlParser.StartSlaveContext):
        pass


    # Enter a parse tree produced by MySqlParser#stopSlave.
    def enterStopSlave(self, ctx:MySqlParser.StopSlaveContext):
        pass

    # Exit a parse tree produced by MySqlParser#stopSlave.
    def exitStopSlave(self, ctx:MySqlParser.StopSlaveContext):
        pass


    # Enter a parse tree produced by MySqlParser#startGroupReplication.
    def enterStartGroupReplication(self, ctx:MySqlParser.StartGroupReplicationContext):
        pass

    # Exit a parse tree produced by MySqlParser#startGroupReplication.
    def exitStartGroupReplication(self, ctx:MySqlParser.StartGroupReplicationContext):
        pass


    # Enter a parse tree produced by MySqlParser#stopGroupReplication.
    def enterStopGroupReplication(self, ctx:MySqlParser.StopGroupReplicationContext):
        pass

    # Exit a parse tree produced by MySqlParser#stopGroupReplication.
    def exitStopGroupReplication(self, ctx:MySqlParser.StopGroupReplicationContext):
        pass


    # Enter a parse tree produced by MySqlParser#masterStringOption.
    def enterMasterStringOption(self, ctx:MySqlParser.MasterStringOptionContext):
        pass

    # Exit a parse tree produced by MySqlParser#masterStringOption.
    def exitMasterStringOption(self, ctx:MySqlParser.MasterStringOptionContext):
        pass


    # Enter a parse tree produced by MySqlParser#masterDecimalOption.
    def enterMasterDecimalOption(self, ctx:MySqlParser.MasterDecimalOptionContext):
        pass

    # Exit a parse tree produced by MySqlParser#masterDecimalOption.
    def exitMasterDecimalOption(self, ctx:MySqlParser.MasterDecimalOptionContext):
        pass


    # Enter a parse tree produced by MySqlParser#masterBoolOption.
    def enterMasterBoolOption(self, ctx:MySqlParser.MasterBoolOptionContext):
        pass

    # Exit a parse tree produced by MySqlParser#masterBoolOption.
    def exitMasterBoolOption(self, ctx:MySqlParser.MasterBoolOptionContext):
        pass


    # Enter a parse tree produced by MySqlParser#masterRealOption.
    def enterMasterRealOption(self, ctx:MySqlParser.MasterRealOptionContext):
        pass

    # Exit a parse tree produced by MySqlParser#masterRealOption.
    def exitMasterRealOption(self, ctx:MySqlParser.MasterRealOptionContext):
        pass


    # Enter a parse tree produced by MySqlParser#masterUidListOption.
    def enterMasterUidListOption(self, ctx:MySqlParser.MasterUidListOptionContext):
        pass

    # Exit a parse tree produced by MySqlParser#masterUidListOption.
    def exitMasterUidListOption(self, ctx:MySqlParser.MasterUidListOptionContext):
        pass


    # Enter a parse tree produced by MySqlParser#stringMasterOption.
    def enterStringMasterOption(self, ctx:MySqlParser.StringMasterOptionContext):
        pass

    # Exit a parse tree produced by MySqlParser#stringMasterOption.
    def exitStringMasterOption(self, ctx:MySqlParser.StringMasterOptionContext):
        pass


    # Enter a parse tree produced by MySqlParser#decimalMasterOption.
    def enterDecimalMasterOption(self, ctx:MySqlParser.DecimalMasterOptionContext):
        pass

    # Exit a parse tree produced by MySqlParser#decimalMasterOption.
    def exitDecimalMasterOption(self, ctx:MySqlParser.DecimalMasterOptionContext):
        pass


    # Enter a parse tree produced by MySqlParser#boolMasterOption.
    def enterBoolMasterOption(self, ctx:MySqlParser.BoolMasterOptionContext):
        pass

    # Exit a parse tree produced by MySqlParser#boolMasterOption.
    def exitBoolMasterOption(self, ctx:MySqlParser.BoolMasterOptionContext):
        pass


    # Enter a parse tree produced by MySqlParser#channelOption.
    def enterChannelOption(self, ctx:MySqlParser.ChannelOptionContext):
        pass

    # Exit a parse tree produced by MySqlParser#channelOption.
    def exitChannelOption(self, ctx:MySqlParser.ChannelOptionContext):
        pass


    # Enter a parse tree produced by MySqlParser#doDbReplication.
    def enterDoDbReplication(self, ctx:MySqlParser.DoDbReplicationContext):
        pass

    # Exit a parse tree produced by MySqlParser#doDbReplication.
    def exitDoDbReplication(self, ctx:MySqlParser.DoDbReplicationContext):
        pass


    # Enter a parse tree produced by MySqlParser#ignoreDbReplication.
    def enterIgnoreDbReplication(self, ctx:MySqlParser.IgnoreDbReplicationContext):
        pass

    # Exit a parse tree produced by MySqlParser#ignoreDbReplication.
    def exitIgnoreDbReplication(self, ctx:MySqlParser.IgnoreDbReplicationContext):
        pass


    # Enter a parse tree produced by MySqlParser#doTableReplication.
    def enterDoTableReplication(self, ctx:MySqlParser.DoTableReplicationContext):
        pass

    # Exit a parse tree produced by MySqlParser#doTableReplication.
    def exitDoTableReplication(self, ctx:MySqlParser.DoTableReplicationContext):
        pass


    # Enter a parse tree produced by MySqlParser#ignoreTableReplication.
    def enterIgnoreTableReplication(self, ctx:MySqlParser.IgnoreTableReplicationContext):
        pass

    # Exit a parse tree produced by MySqlParser#ignoreTableReplication.
    def exitIgnoreTableReplication(self, ctx:MySqlParser.IgnoreTableReplicationContext):
        pass


    # Enter a parse tree produced by MySqlParser#wildDoTableReplication.
    def enterWildDoTableReplication(self, ctx:MySqlParser.WildDoTableReplicationContext):
        pass

    # Exit a parse tree produced by MySqlParser#wildDoTableReplication.
    def exitWildDoTableReplication(self, ctx:MySqlParser.WildDoTableReplicationContext):
        pass


    # Enter a parse tree produced by MySqlParser#wildIgnoreTableReplication.
    def enterWildIgnoreTableReplication(self, ctx:MySqlParser.WildIgnoreTableReplicationContext):
        pass

    # Exit a parse tree produced by MySqlParser#wildIgnoreTableReplication.
    def exitWildIgnoreTableReplication(self, ctx:MySqlParser.WildIgnoreTableReplicationContext):
        pass


    # Enter a parse tree produced by MySqlParser#rewriteDbReplication.
    def enterRewriteDbReplication(self, ctx:MySqlParser.RewriteDbReplicationContext):
        pass

    # Exit a parse tree produced by MySqlParser#rewriteDbReplication.
    def exitRewriteDbReplication(self, ctx:MySqlParser.RewriteDbReplicationContext):
        pass


    # Enter a parse tree produced by MySqlParser#tablePair.
    def enterTablePair(self, ctx:MySqlParser.TablePairContext):
        pass

    # Exit a parse tree produced by MySqlParser#tablePair.
    def exitTablePair(self, ctx:MySqlParser.TablePairContext):
        pass


    # Enter a parse tree produced by MySqlParser#threadType.
    def enterThreadType(self, ctx:MySqlParser.ThreadTypeContext):
        pass

    # Exit a parse tree produced by MySqlParser#threadType.
    def exitThreadType(self, ctx:MySqlParser.ThreadTypeContext):
        pass


    # Enter a parse tree produced by MySqlParser#gtidsUntilOption.
    def enterGtidsUntilOption(self, ctx:MySqlParser.GtidsUntilOptionContext):
        pass

    # Exit a parse tree produced by MySqlParser#gtidsUntilOption.
    def exitGtidsUntilOption(self, ctx:MySqlParser.GtidsUntilOptionContext):
        pass


    # Enter a parse tree produced by MySqlParser#masterLogUntilOption.
    def enterMasterLogUntilOption(self, ctx:MySqlParser.MasterLogUntilOptionContext):
        pass

    # Exit a parse tree produced by MySqlParser#masterLogUntilOption.
    def exitMasterLogUntilOption(self, ctx:MySqlParser.MasterLogUntilOptionContext):
        pass


    # Enter a parse tree produced by MySqlParser#relayLogUntilOption.
    def enterRelayLogUntilOption(self, ctx:MySqlParser.RelayLogUntilOptionContext):
        pass

    # Exit a parse tree produced by MySqlParser#relayLogUntilOption.
    def exitRelayLogUntilOption(self, ctx:MySqlParser.RelayLogUntilOptionContext):
        pass


    # Enter a parse tree produced by MySqlParser#sqlGapsUntilOption.
    def enterSqlGapsUntilOption(self, ctx:MySqlParser.SqlGapsUntilOptionContext):
        pass

    # Exit a parse tree produced by MySqlParser#sqlGapsUntilOption.
    def exitSqlGapsUntilOption(self, ctx:MySqlParser.SqlGapsUntilOptionContext):
        pass


    # Enter a parse tree produced by MySqlParser#userConnectionOption.
    def enterUserConnectionOption(self, ctx:MySqlParser.UserConnectionOptionContext):
        pass

    # Exit a parse tree produced by MySqlParser#userConnectionOption.
    def exitUserConnectionOption(self, ctx:MySqlParser.UserConnectionOptionContext):
        pass


    # Enter a parse tree produced by MySqlParser#passwordConnectionOption.
    def enterPasswordConnectionOption(self, ctx:MySqlParser.PasswordConnectionOptionContext):
        pass

    # Exit a parse tree produced by MySqlParser#passwordConnectionOption.
    def exitPasswordConnectionOption(self, ctx:MySqlParser.PasswordConnectionOptionContext):
        pass


    # Enter a parse tree produced by MySqlParser#defaultAuthConnectionOption.
    def enterDefaultAuthConnectionOption(self, ctx:MySqlParser.DefaultAuthConnectionOptionContext):
        pass

    # Exit a parse tree produced by MySqlParser#defaultAuthConnectionOption.
    def exitDefaultAuthConnectionOption(self, ctx:MySqlParser.DefaultAuthConnectionOptionContext):
        pass


    # Enter a parse tree produced by MySqlParser#pluginDirConnectionOption.
    def enterPluginDirConnectionOption(self, ctx:MySqlParser.PluginDirConnectionOptionContext):
        pass

    # Exit a parse tree produced by MySqlParser#pluginDirConnectionOption.
    def exitPluginDirConnectionOption(self, ctx:MySqlParser.PluginDirConnectionOptionContext):
        pass


    # Enter a parse tree produced by MySqlParser#gtuidSet.
    def enterGtuidSet(self, ctx:MySqlParser.GtuidSetContext):
        pass

    # Exit a parse tree produced by MySqlParser#gtuidSet.
    def exitGtuidSet(self, ctx:MySqlParser.GtuidSetContext):
        pass


    # Enter a parse tree produced by MySqlParser#xaStartTransaction.
    def enterXaStartTransaction(self, ctx:MySqlParser.XaStartTransactionContext):
        pass

    # Exit a parse tree produced by MySqlParser#xaStartTransaction.
    def exitXaStartTransaction(self, ctx:MySqlParser.XaStartTransactionContext):
        pass


    # Enter a parse tree produced by MySqlParser#xaEndTransaction.
    def enterXaEndTransaction(self, ctx:MySqlParser.XaEndTransactionContext):
        pass

    # Exit a parse tree produced by MySqlParser#xaEndTransaction.
    def exitXaEndTransaction(self, ctx:MySqlParser.XaEndTransactionContext):
        pass


    # Enter a parse tree produced by MySqlParser#xaPrepareStatement.
    def enterXaPrepareStatement(self, ctx:MySqlParser.XaPrepareStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#xaPrepareStatement.
    def exitXaPrepareStatement(self, ctx:MySqlParser.XaPrepareStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#xaCommitWork.
    def enterXaCommitWork(self, ctx:MySqlParser.XaCommitWorkContext):
        pass

    # Exit a parse tree produced by MySqlParser#xaCommitWork.
    def exitXaCommitWork(self, ctx:MySqlParser.XaCommitWorkContext):
        pass


    # Enter a parse tree produced by MySqlParser#xaRollbackWork.
    def enterXaRollbackWork(self, ctx:MySqlParser.XaRollbackWorkContext):
        pass

    # Exit a parse tree produced by MySqlParser#xaRollbackWork.
    def exitXaRollbackWork(self, ctx:MySqlParser.XaRollbackWorkContext):
        pass


    # Enter a parse tree produced by MySqlParser#xaRecoverWork.
    def enterXaRecoverWork(self, ctx:MySqlParser.XaRecoverWorkContext):
        pass

    # Exit a parse tree produced by MySqlParser#xaRecoverWork.
    def exitXaRecoverWork(self, ctx:MySqlParser.XaRecoverWorkContext):
        pass


    # Enter a parse tree produced by MySqlParser#prepareStatement.
    def enterPrepareStatement(self, ctx:MySqlParser.PrepareStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#prepareStatement.
    def exitPrepareStatement(self, ctx:MySqlParser.PrepareStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#executeStatement.
    def enterExecuteStatement(self, ctx:MySqlParser.ExecuteStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#executeStatement.
    def exitExecuteStatement(self, ctx:MySqlParser.ExecuteStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#deallocatePrepare.
    def enterDeallocatePrepare(self, ctx:MySqlParser.DeallocatePrepareContext):
        pass

    # Exit a parse tree produced by MySqlParser#deallocatePrepare.
    def exitDeallocatePrepare(self, ctx:MySqlParser.DeallocatePrepareContext):
        pass


    # Enter a parse tree produced by MySqlParser#routineBody.
    def enterRoutineBody(self, ctx:MySqlParser.RoutineBodyContext):
        pass

    # Exit a parse tree produced by MySqlParser#routineBody.
    def exitRoutineBody(self, ctx:MySqlParser.RoutineBodyContext):
        pass


    # Enter a parse tree produced by MySqlParser#blockStatement.
    def enterBlockStatement(self, ctx:MySqlParser.BlockStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#blockStatement.
    def exitBlockStatement(self, ctx:MySqlParser.BlockStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#caseStatement.
    def enterCaseStatement(self, ctx:MySqlParser.CaseStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#caseStatement.
    def exitCaseStatement(self, ctx:MySqlParser.CaseStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#ifStatement.
    def enterIfStatement(self, ctx:MySqlParser.IfStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#ifStatement.
    def exitIfStatement(self, ctx:MySqlParser.IfStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#iterateStatement.
    def enterIterateStatement(self, ctx:MySqlParser.IterateStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#iterateStatement.
    def exitIterateStatement(self, ctx:MySqlParser.IterateStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#leaveStatement.
    def enterLeaveStatement(self, ctx:MySqlParser.LeaveStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#leaveStatement.
    def exitLeaveStatement(self, ctx:MySqlParser.LeaveStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#loopStatement.
    def enterLoopStatement(self, ctx:MySqlParser.LoopStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#loopStatement.
    def exitLoopStatement(self, ctx:MySqlParser.LoopStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#repeatStatement.
    def enterRepeatStatement(self, ctx:MySqlParser.RepeatStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#repeatStatement.
    def exitRepeatStatement(self, ctx:MySqlParser.RepeatStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#returnStatement.
    def enterReturnStatement(self, ctx:MySqlParser.ReturnStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#returnStatement.
    def exitReturnStatement(self, ctx:MySqlParser.ReturnStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#whileStatement.
    def enterWhileStatement(self, ctx:MySqlParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#whileStatement.
    def exitWhileStatement(self, ctx:MySqlParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#CloseCursor.
    def enterCloseCursor(self, ctx:MySqlParser.CloseCursorContext):
        pass

    # Exit a parse tree produced by MySqlParser#CloseCursor.
    def exitCloseCursor(self, ctx:MySqlParser.CloseCursorContext):
        pass


    # Enter a parse tree produced by MySqlParser#FetchCursor.
    def enterFetchCursor(self, ctx:MySqlParser.FetchCursorContext):
        pass

    # Exit a parse tree produced by MySqlParser#FetchCursor.
    def exitFetchCursor(self, ctx:MySqlParser.FetchCursorContext):
        pass


    # Enter a parse tree produced by MySqlParser#OpenCursor.
    def enterOpenCursor(self, ctx:MySqlParser.OpenCursorContext):
        pass

    # Exit a parse tree produced by MySqlParser#OpenCursor.
    def exitOpenCursor(self, ctx:MySqlParser.OpenCursorContext):
        pass


    # Enter a parse tree produced by MySqlParser#declareVariable.
    def enterDeclareVariable(self, ctx:MySqlParser.DeclareVariableContext):
        pass

    # Exit a parse tree produced by MySqlParser#declareVariable.
    def exitDeclareVariable(self, ctx:MySqlParser.DeclareVariableContext):
        pass


    # Enter a parse tree produced by MySqlParser#declareCondition.
    def enterDeclareCondition(self, ctx:MySqlParser.DeclareConditionContext):
        pass

    # Exit a parse tree produced by MySqlParser#declareCondition.
    def exitDeclareCondition(self, ctx:MySqlParser.DeclareConditionContext):
        pass


    # Enter a parse tree produced by MySqlParser#declareCursor.
    def enterDeclareCursor(self, ctx:MySqlParser.DeclareCursorContext):
        pass

    # Exit a parse tree produced by MySqlParser#declareCursor.
    def exitDeclareCursor(self, ctx:MySqlParser.DeclareCursorContext):
        pass


    # Enter a parse tree produced by MySqlParser#declareHandler.
    def enterDeclareHandler(self, ctx:MySqlParser.DeclareHandlerContext):
        pass

    # Exit a parse tree produced by MySqlParser#declareHandler.
    def exitDeclareHandler(self, ctx:MySqlParser.DeclareHandlerContext):
        pass


    # Enter a parse tree produced by MySqlParser#handlerConditionCode.
    def enterHandlerConditionCode(self, ctx:MySqlParser.HandlerConditionCodeContext):
        pass

    # Exit a parse tree produced by MySqlParser#handlerConditionCode.
    def exitHandlerConditionCode(self, ctx:MySqlParser.HandlerConditionCodeContext):
        pass


    # Enter a parse tree produced by MySqlParser#handlerConditionState.
    def enterHandlerConditionState(self, ctx:MySqlParser.HandlerConditionStateContext):
        pass

    # Exit a parse tree produced by MySqlParser#handlerConditionState.
    def exitHandlerConditionState(self, ctx:MySqlParser.HandlerConditionStateContext):
        pass


    # Enter a parse tree produced by MySqlParser#handlerConditionName.
    def enterHandlerConditionName(self, ctx:MySqlParser.HandlerConditionNameContext):
        pass

    # Exit a parse tree produced by MySqlParser#handlerConditionName.
    def exitHandlerConditionName(self, ctx:MySqlParser.HandlerConditionNameContext):
        pass


    # Enter a parse tree produced by MySqlParser#handlerConditionWarning.
    def enterHandlerConditionWarning(self, ctx:MySqlParser.HandlerConditionWarningContext):
        pass

    # Exit a parse tree produced by MySqlParser#handlerConditionWarning.
    def exitHandlerConditionWarning(self, ctx:MySqlParser.HandlerConditionWarningContext):
        pass


    # Enter a parse tree produced by MySqlParser#handlerConditionNotfound.
    def enterHandlerConditionNotfound(self, ctx:MySqlParser.HandlerConditionNotfoundContext):
        pass

    # Exit a parse tree produced by MySqlParser#handlerConditionNotfound.
    def exitHandlerConditionNotfound(self, ctx:MySqlParser.HandlerConditionNotfoundContext):
        pass


    # Enter a parse tree produced by MySqlParser#handlerConditionException.
    def enterHandlerConditionException(self, ctx:MySqlParser.HandlerConditionExceptionContext):
        pass

    # Exit a parse tree produced by MySqlParser#handlerConditionException.
    def exitHandlerConditionException(self, ctx:MySqlParser.HandlerConditionExceptionContext):
        pass


    # Enter a parse tree produced by MySqlParser#procedureSqlStatement.
    def enterProcedureSqlStatement(self, ctx:MySqlParser.ProcedureSqlStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#procedureSqlStatement.
    def exitProcedureSqlStatement(self, ctx:MySqlParser.ProcedureSqlStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#caseAlternative.
    def enterCaseAlternative(self, ctx:MySqlParser.CaseAlternativeContext):
        pass

    # Exit a parse tree produced by MySqlParser#caseAlternative.
    def exitCaseAlternative(self, ctx:MySqlParser.CaseAlternativeContext):
        pass


    # Enter a parse tree produced by MySqlParser#elifAlternative.
    def enterElifAlternative(self, ctx:MySqlParser.ElifAlternativeContext):
        pass

    # Exit a parse tree produced by MySqlParser#elifAlternative.
    def exitElifAlternative(self, ctx:MySqlParser.ElifAlternativeContext):
        pass


    # Enter a parse tree produced by MySqlParser#alterUserMysqlV56.
    def enterAlterUserMysqlV56(self, ctx:MySqlParser.AlterUserMysqlV56Context):
        pass

    # Exit a parse tree produced by MySqlParser#alterUserMysqlV56.
    def exitAlterUserMysqlV56(self, ctx:MySqlParser.AlterUserMysqlV56Context):
        pass


    # Enter a parse tree produced by MySqlParser#alterUserMysqlV80.
    def enterAlterUserMysqlV80(self, ctx:MySqlParser.AlterUserMysqlV80Context):
        pass

    # Exit a parse tree produced by MySqlParser#alterUserMysqlV80.
    def exitAlterUserMysqlV80(self, ctx:MySqlParser.AlterUserMysqlV80Context):
        pass


    # Enter a parse tree produced by MySqlParser#createUserMysqlV56.
    def enterCreateUserMysqlV56(self, ctx:MySqlParser.CreateUserMysqlV56Context):
        pass

    # Exit a parse tree produced by MySqlParser#createUserMysqlV56.
    def exitCreateUserMysqlV56(self, ctx:MySqlParser.CreateUserMysqlV56Context):
        pass


    # Enter a parse tree produced by MySqlParser#createUserMysqlV80.
    def enterCreateUserMysqlV80(self, ctx:MySqlParser.CreateUserMysqlV80Context):
        pass

    # Exit a parse tree produced by MySqlParser#createUserMysqlV80.
    def exitCreateUserMysqlV80(self, ctx:MySqlParser.CreateUserMysqlV80Context):
        pass


    # Enter a parse tree produced by MySqlParser#dropUser.
    def enterDropUser(self, ctx:MySqlParser.DropUserContext):
        pass

    # Exit a parse tree produced by MySqlParser#dropUser.
    def exitDropUser(self, ctx:MySqlParser.DropUserContext):
        pass


    # Enter a parse tree produced by MySqlParser#grantStatement.
    def enterGrantStatement(self, ctx:MySqlParser.GrantStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#grantStatement.
    def exitGrantStatement(self, ctx:MySqlParser.GrantStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#roleOption.
    def enterRoleOption(self, ctx:MySqlParser.RoleOptionContext):
        pass

    # Exit a parse tree produced by MySqlParser#roleOption.
    def exitRoleOption(self, ctx:MySqlParser.RoleOptionContext):
        pass


    # Enter a parse tree produced by MySqlParser#grantProxy.
    def enterGrantProxy(self, ctx:MySqlParser.GrantProxyContext):
        pass

    # Exit a parse tree produced by MySqlParser#grantProxy.
    def exitGrantProxy(self, ctx:MySqlParser.GrantProxyContext):
        pass


    # Enter a parse tree produced by MySqlParser#renameUser.
    def enterRenameUser(self, ctx:MySqlParser.RenameUserContext):
        pass

    # Exit a parse tree produced by MySqlParser#renameUser.
    def exitRenameUser(self, ctx:MySqlParser.RenameUserContext):
        pass


    # Enter a parse tree produced by MySqlParser#detailRevoke.
    def enterDetailRevoke(self, ctx:MySqlParser.DetailRevokeContext):
        pass

    # Exit a parse tree produced by MySqlParser#detailRevoke.
    def exitDetailRevoke(self, ctx:MySqlParser.DetailRevokeContext):
        pass


    # Enter a parse tree produced by MySqlParser#shortRevoke.
    def enterShortRevoke(self, ctx:MySqlParser.ShortRevokeContext):
        pass

    # Exit a parse tree produced by MySqlParser#shortRevoke.
    def exitShortRevoke(self, ctx:MySqlParser.ShortRevokeContext):
        pass


    # Enter a parse tree produced by MySqlParser#roleRevoke.
    def enterRoleRevoke(self, ctx:MySqlParser.RoleRevokeContext):
        pass

    # Exit a parse tree produced by MySqlParser#roleRevoke.
    def exitRoleRevoke(self, ctx:MySqlParser.RoleRevokeContext):
        pass


    # Enter a parse tree produced by MySqlParser#revokeProxy.
    def enterRevokeProxy(self, ctx:MySqlParser.RevokeProxyContext):
        pass

    # Exit a parse tree produced by MySqlParser#revokeProxy.
    def exitRevokeProxy(self, ctx:MySqlParser.RevokeProxyContext):
        pass


    # Enter a parse tree produced by MySqlParser#setPasswordStatement.
    def enterSetPasswordStatement(self, ctx:MySqlParser.SetPasswordStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#setPasswordStatement.
    def exitSetPasswordStatement(self, ctx:MySqlParser.SetPasswordStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#userSpecification.
    def enterUserSpecification(self, ctx:MySqlParser.UserSpecificationContext):
        pass

    # Exit a parse tree produced by MySqlParser#userSpecification.
    def exitUserSpecification(self, ctx:MySqlParser.UserSpecificationContext):
        pass


    # Enter a parse tree produced by MySqlParser#hashAuthOption.
    def enterHashAuthOption(self, ctx:MySqlParser.HashAuthOptionContext):
        pass

    # Exit a parse tree produced by MySqlParser#hashAuthOption.
    def exitHashAuthOption(self, ctx:MySqlParser.HashAuthOptionContext):
        pass


    # Enter a parse tree produced by MySqlParser#randomAuthOption.
    def enterRandomAuthOption(self, ctx:MySqlParser.RandomAuthOptionContext):
        pass

    # Exit a parse tree produced by MySqlParser#randomAuthOption.
    def exitRandomAuthOption(self, ctx:MySqlParser.RandomAuthOptionContext):
        pass


    # Enter a parse tree produced by MySqlParser#stringAuthOption.
    def enterStringAuthOption(self, ctx:MySqlParser.StringAuthOptionContext):
        pass

    # Exit a parse tree produced by MySqlParser#stringAuthOption.
    def exitStringAuthOption(self, ctx:MySqlParser.StringAuthOptionContext):
        pass


    # Enter a parse tree produced by MySqlParser#moduleAuthOption.
    def enterModuleAuthOption(self, ctx:MySqlParser.ModuleAuthOptionContext):
        pass

    # Exit a parse tree produced by MySqlParser#moduleAuthOption.
    def exitModuleAuthOption(self, ctx:MySqlParser.ModuleAuthOptionContext):
        pass


    # Enter a parse tree produced by MySqlParser#simpleAuthOption.
    def enterSimpleAuthOption(self, ctx:MySqlParser.SimpleAuthOptionContext):
        pass

    # Exit a parse tree produced by MySqlParser#simpleAuthOption.
    def exitSimpleAuthOption(self, ctx:MySqlParser.SimpleAuthOptionContext):
        pass


    # Enter a parse tree produced by MySqlParser#authOptionClause.
    def enterAuthOptionClause(self, ctx:MySqlParser.AuthOptionClauseContext):
        pass

    # Exit a parse tree produced by MySqlParser#authOptionClause.
    def exitAuthOptionClause(self, ctx:MySqlParser.AuthOptionClauseContext):
        pass


    # Enter a parse tree produced by MySqlParser#module.
    def enterModule(self, ctx:MySqlParser.ModuleContext):
        pass

    # Exit a parse tree produced by MySqlParser#module.
    def exitModule(self, ctx:MySqlParser.ModuleContext):
        pass


    # Enter a parse tree produced by MySqlParser#passwordModuleOption.
    def enterPasswordModuleOption(self, ctx:MySqlParser.PasswordModuleOptionContext):
        pass

    # Exit a parse tree produced by MySqlParser#passwordModuleOption.
    def exitPasswordModuleOption(self, ctx:MySqlParser.PasswordModuleOptionContext):
        pass


    # Enter a parse tree produced by MySqlParser#tlsOption.
    def enterTlsOption(self, ctx:MySqlParser.TlsOptionContext):
        pass

    # Exit a parse tree produced by MySqlParser#tlsOption.
    def exitTlsOption(self, ctx:MySqlParser.TlsOptionContext):
        pass


    # Enter a parse tree produced by MySqlParser#userResourceOption.
    def enterUserResourceOption(self, ctx:MySqlParser.UserResourceOptionContext):
        pass

    # Exit a parse tree produced by MySqlParser#userResourceOption.
    def exitUserResourceOption(self, ctx:MySqlParser.UserResourceOptionContext):
        pass


    # Enter a parse tree produced by MySqlParser#userPasswordOption.
    def enterUserPasswordOption(self, ctx:MySqlParser.UserPasswordOptionContext):
        pass

    # Exit a parse tree produced by MySqlParser#userPasswordOption.
    def exitUserPasswordOption(self, ctx:MySqlParser.UserPasswordOptionContext):
        pass


    # Enter a parse tree produced by MySqlParser#userLockOption.
    def enterUserLockOption(self, ctx:MySqlParser.UserLockOptionContext):
        pass

    # Exit a parse tree produced by MySqlParser#userLockOption.
    def exitUserLockOption(self, ctx:MySqlParser.UserLockOptionContext):
        pass


    # Enter a parse tree produced by MySqlParser#privelegeClause.
    def enterPrivelegeClause(self, ctx:MySqlParser.PrivelegeClauseContext):
        pass

    # Exit a parse tree produced by MySqlParser#privelegeClause.
    def exitPrivelegeClause(self, ctx:MySqlParser.PrivelegeClauseContext):
        pass


    # Enter a parse tree produced by MySqlParser#privilege.
    def enterPrivilege(self, ctx:MySqlParser.PrivilegeContext):
        pass

    # Exit a parse tree produced by MySqlParser#privilege.
    def exitPrivilege(self, ctx:MySqlParser.PrivilegeContext):
        pass


    # Enter a parse tree produced by MySqlParser#currentSchemaPriviLevel.
    def enterCurrentSchemaPriviLevel(self, ctx:MySqlParser.CurrentSchemaPriviLevelContext):
        pass

    # Exit a parse tree produced by MySqlParser#currentSchemaPriviLevel.
    def exitCurrentSchemaPriviLevel(self, ctx:MySqlParser.CurrentSchemaPriviLevelContext):
        pass


    # Enter a parse tree produced by MySqlParser#globalPrivLevel.
    def enterGlobalPrivLevel(self, ctx:MySqlParser.GlobalPrivLevelContext):
        pass

    # Exit a parse tree produced by MySqlParser#globalPrivLevel.
    def exitGlobalPrivLevel(self, ctx:MySqlParser.GlobalPrivLevelContext):
        pass


    # Enter a parse tree produced by MySqlParser#definiteSchemaPrivLevel.
    def enterDefiniteSchemaPrivLevel(self, ctx:MySqlParser.DefiniteSchemaPrivLevelContext):
        pass

    # Exit a parse tree produced by MySqlParser#definiteSchemaPrivLevel.
    def exitDefiniteSchemaPrivLevel(self, ctx:MySqlParser.DefiniteSchemaPrivLevelContext):
        pass


    # Enter a parse tree produced by MySqlParser#definiteFullTablePrivLevel.
    def enterDefiniteFullTablePrivLevel(self, ctx:MySqlParser.DefiniteFullTablePrivLevelContext):
        pass

    # Exit a parse tree produced by MySqlParser#definiteFullTablePrivLevel.
    def exitDefiniteFullTablePrivLevel(self, ctx:MySqlParser.DefiniteFullTablePrivLevelContext):
        pass


    # Enter a parse tree produced by MySqlParser#definiteFullTablePrivLevel2.
    def enterDefiniteFullTablePrivLevel2(self, ctx:MySqlParser.DefiniteFullTablePrivLevel2Context):
        pass

    # Exit a parse tree produced by MySqlParser#definiteFullTablePrivLevel2.
    def exitDefiniteFullTablePrivLevel2(self, ctx:MySqlParser.DefiniteFullTablePrivLevel2Context):
        pass


    # Enter a parse tree produced by MySqlParser#definiteTablePrivLevel.
    def enterDefiniteTablePrivLevel(self, ctx:MySqlParser.DefiniteTablePrivLevelContext):
        pass

    # Exit a parse tree produced by MySqlParser#definiteTablePrivLevel.
    def exitDefiniteTablePrivLevel(self, ctx:MySqlParser.DefiniteTablePrivLevelContext):
        pass


    # Enter a parse tree produced by MySqlParser#renameUserClause.
    def enterRenameUserClause(self, ctx:MySqlParser.RenameUserClauseContext):
        pass

    # Exit a parse tree produced by MySqlParser#renameUserClause.
    def exitRenameUserClause(self, ctx:MySqlParser.RenameUserClauseContext):
        pass


    # Enter a parse tree produced by MySqlParser#analyzeTable.
    def enterAnalyzeTable(self, ctx:MySqlParser.AnalyzeTableContext):
        pass

    # Exit a parse tree produced by MySqlParser#analyzeTable.
    def exitAnalyzeTable(self, ctx:MySqlParser.AnalyzeTableContext):
        pass


    # Enter a parse tree produced by MySqlParser#checkTable.
    def enterCheckTable(self, ctx:MySqlParser.CheckTableContext):
        pass

    # Exit a parse tree produced by MySqlParser#checkTable.
    def exitCheckTable(self, ctx:MySqlParser.CheckTableContext):
        pass


    # Enter a parse tree produced by MySqlParser#checksumTable.
    def enterChecksumTable(self, ctx:MySqlParser.ChecksumTableContext):
        pass

    # Exit a parse tree produced by MySqlParser#checksumTable.
    def exitChecksumTable(self, ctx:MySqlParser.ChecksumTableContext):
        pass


    # Enter a parse tree produced by MySqlParser#optimizeTable.
    def enterOptimizeTable(self, ctx:MySqlParser.OptimizeTableContext):
        pass

    # Exit a parse tree produced by MySqlParser#optimizeTable.
    def exitOptimizeTable(self, ctx:MySqlParser.OptimizeTableContext):
        pass


    # Enter a parse tree produced by MySqlParser#repairTable.
    def enterRepairTable(self, ctx:MySqlParser.RepairTableContext):
        pass

    # Exit a parse tree produced by MySqlParser#repairTable.
    def exitRepairTable(self, ctx:MySqlParser.RepairTableContext):
        pass


    # Enter a parse tree produced by MySqlParser#checkTableOption.
    def enterCheckTableOption(self, ctx:MySqlParser.CheckTableOptionContext):
        pass

    # Exit a parse tree produced by MySqlParser#checkTableOption.
    def exitCheckTableOption(self, ctx:MySqlParser.CheckTableOptionContext):
        pass


    # Enter a parse tree produced by MySqlParser#createUdfunction.
    def enterCreateUdfunction(self, ctx:MySqlParser.CreateUdfunctionContext):
        pass

    # Exit a parse tree produced by MySqlParser#createUdfunction.
    def exitCreateUdfunction(self, ctx:MySqlParser.CreateUdfunctionContext):
        pass


    # Enter a parse tree produced by MySqlParser#installPlugin.
    def enterInstallPlugin(self, ctx:MySqlParser.InstallPluginContext):
        pass

    # Exit a parse tree produced by MySqlParser#installPlugin.
    def exitInstallPlugin(self, ctx:MySqlParser.InstallPluginContext):
        pass


    # Enter a parse tree produced by MySqlParser#uninstallPlugin.
    def enterUninstallPlugin(self, ctx:MySqlParser.UninstallPluginContext):
        pass

    # Exit a parse tree produced by MySqlParser#uninstallPlugin.
    def exitUninstallPlugin(self, ctx:MySqlParser.UninstallPluginContext):
        pass


    # Enter a parse tree produced by MySqlParser#setVariable.
    def enterSetVariable(self, ctx:MySqlParser.SetVariableContext):
        pass

    # Exit a parse tree produced by MySqlParser#setVariable.
    def exitSetVariable(self, ctx:MySqlParser.SetVariableContext):
        pass


    # Enter a parse tree produced by MySqlParser#setCharset.
    def enterSetCharset(self, ctx:MySqlParser.SetCharsetContext):
        pass

    # Exit a parse tree produced by MySqlParser#setCharset.
    def exitSetCharset(self, ctx:MySqlParser.SetCharsetContext):
        pass


    # Enter a parse tree produced by MySqlParser#setNames.
    def enterSetNames(self, ctx:MySqlParser.SetNamesContext):
        pass

    # Exit a parse tree produced by MySqlParser#setNames.
    def exitSetNames(self, ctx:MySqlParser.SetNamesContext):
        pass


    # Enter a parse tree produced by MySqlParser#setPassword.
    def enterSetPassword(self, ctx:MySqlParser.SetPasswordContext):
        pass

    # Exit a parse tree produced by MySqlParser#setPassword.
    def exitSetPassword(self, ctx:MySqlParser.SetPasswordContext):
        pass


    # Enter a parse tree produced by MySqlParser#setTransaction.
    def enterSetTransaction(self, ctx:MySqlParser.SetTransactionContext):
        pass

    # Exit a parse tree produced by MySqlParser#setTransaction.
    def exitSetTransaction(self, ctx:MySqlParser.SetTransactionContext):
        pass


    # Enter a parse tree produced by MySqlParser#setAutocommit.
    def enterSetAutocommit(self, ctx:MySqlParser.SetAutocommitContext):
        pass

    # Exit a parse tree produced by MySqlParser#setAutocommit.
    def exitSetAutocommit(self, ctx:MySqlParser.SetAutocommitContext):
        pass


    # Enter a parse tree produced by MySqlParser#setNewValueInsideTrigger.
    def enterSetNewValueInsideTrigger(self, ctx:MySqlParser.SetNewValueInsideTriggerContext):
        pass

    # Exit a parse tree produced by MySqlParser#setNewValueInsideTrigger.
    def exitSetNewValueInsideTrigger(self, ctx:MySqlParser.SetNewValueInsideTriggerContext):
        pass


    # Enter a parse tree produced by MySqlParser#showMasterLogs.
    def enterShowMasterLogs(self, ctx:MySqlParser.ShowMasterLogsContext):
        pass

    # Exit a parse tree produced by MySqlParser#showMasterLogs.
    def exitShowMasterLogs(self, ctx:MySqlParser.ShowMasterLogsContext):
        pass


    # Enter a parse tree produced by MySqlParser#showLogEvents.
    def enterShowLogEvents(self, ctx:MySqlParser.ShowLogEventsContext):
        pass

    # Exit a parse tree produced by MySqlParser#showLogEvents.
    def exitShowLogEvents(self, ctx:MySqlParser.ShowLogEventsContext):
        pass


    # Enter a parse tree produced by MySqlParser#showObjectFilter.
    def enterShowObjectFilter(self, ctx:MySqlParser.ShowObjectFilterContext):
        pass

    # Exit a parse tree produced by MySqlParser#showObjectFilter.
    def exitShowObjectFilter(self, ctx:MySqlParser.ShowObjectFilterContext):
        pass


    # Enter a parse tree produced by MySqlParser#showColumns.
    def enterShowColumns(self, ctx:MySqlParser.ShowColumnsContext):
        pass

    # Exit a parse tree produced by MySqlParser#showColumns.
    def exitShowColumns(self, ctx:MySqlParser.ShowColumnsContext):
        pass


    # Enter a parse tree produced by MySqlParser#showCreateDb.
    def enterShowCreateDb(self, ctx:MySqlParser.ShowCreateDbContext):
        pass

    # Exit a parse tree produced by MySqlParser#showCreateDb.
    def exitShowCreateDb(self, ctx:MySqlParser.ShowCreateDbContext):
        pass


    # Enter a parse tree produced by MySqlParser#showCreateFullIdObject.
    def enterShowCreateFullIdObject(self, ctx:MySqlParser.ShowCreateFullIdObjectContext):
        pass

    # Exit a parse tree produced by MySqlParser#showCreateFullIdObject.
    def exitShowCreateFullIdObject(self, ctx:MySqlParser.ShowCreateFullIdObjectContext):
        pass


    # Enter a parse tree produced by MySqlParser#showCreateUser.
    def enterShowCreateUser(self, ctx:MySqlParser.ShowCreateUserContext):
        pass

    # Exit a parse tree produced by MySqlParser#showCreateUser.
    def exitShowCreateUser(self, ctx:MySqlParser.ShowCreateUserContext):
        pass


    # Enter a parse tree produced by MySqlParser#showEngine.
    def enterShowEngine(self, ctx:MySqlParser.ShowEngineContext):
        pass

    # Exit a parse tree produced by MySqlParser#showEngine.
    def exitShowEngine(self, ctx:MySqlParser.ShowEngineContext):
        pass


    # Enter a parse tree produced by MySqlParser#showGlobalInfo.
    def enterShowGlobalInfo(self, ctx:MySqlParser.ShowGlobalInfoContext):
        pass

    # Exit a parse tree produced by MySqlParser#showGlobalInfo.
    def exitShowGlobalInfo(self, ctx:MySqlParser.ShowGlobalInfoContext):
        pass


    # Enter a parse tree produced by MySqlParser#showErrors.
    def enterShowErrors(self, ctx:MySqlParser.ShowErrorsContext):
        pass

    # Exit a parse tree produced by MySqlParser#showErrors.
    def exitShowErrors(self, ctx:MySqlParser.ShowErrorsContext):
        pass


    # Enter a parse tree produced by MySqlParser#showCountErrors.
    def enterShowCountErrors(self, ctx:MySqlParser.ShowCountErrorsContext):
        pass

    # Exit a parse tree produced by MySqlParser#showCountErrors.
    def exitShowCountErrors(self, ctx:MySqlParser.ShowCountErrorsContext):
        pass


    # Enter a parse tree produced by MySqlParser#showSchemaFilter.
    def enterShowSchemaFilter(self, ctx:MySqlParser.ShowSchemaFilterContext):
        pass

    # Exit a parse tree produced by MySqlParser#showSchemaFilter.
    def exitShowSchemaFilter(self, ctx:MySqlParser.ShowSchemaFilterContext):
        pass


    # Enter a parse tree produced by MySqlParser#showRoutine.
    def enterShowRoutine(self, ctx:MySqlParser.ShowRoutineContext):
        pass

    # Exit a parse tree produced by MySqlParser#showRoutine.
    def exitShowRoutine(self, ctx:MySqlParser.ShowRoutineContext):
        pass


    # Enter a parse tree produced by MySqlParser#showGrants.
    def enterShowGrants(self, ctx:MySqlParser.ShowGrantsContext):
        pass

    # Exit a parse tree produced by MySqlParser#showGrants.
    def exitShowGrants(self, ctx:MySqlParser.ShowGrantsContext):
        pass


    # Enter a parse tree produced by MySqlParser#showIndexes.
    def enterShowIndexes(self, ctx:MySqlParser.ShowIndexesContext):
        pass

    # Exit a parse tree produced by MySqlParser#showIndexes.
    def exitShowIndexes(self, ctx:MySqlParser.ShowIndexesContext):
        pass


    # Enter a parse tree produced by MySqlParser#showOpenTables.
    def enterShowOpenTables(self, ctx:MySqlParser.ShowOpenTablesContext):
        pass

    # Exit a parse tree produced by MySqlParser#showOpenTables.
    def exitShowOpenTables(self, ctx:MySqlParser.ShowOpenTablesContext):
        pass


    # Enter a parse tree produced by MySqlParser#showProfile.
    def enterShowProfile(self, ctx:MySqlParser.ShowProfileContext):
        pass

    # Exit a parse tree produced by MySqlParser#showProfile.
    def exitShowProfile(self, ctx:MySqlParser.ShowProfileContext):
        pass


    # Enter a parse tree produced by MySqlParser#showSlaveStatus.
    def enterShowSlaveStatus(self, ctx:MySqlParser.ShowSlaveStatusContext):
        pass

    # Exit a parse tree produced by MySqlParser#showSlaveStatus.
    def exitShowSlaveStatus(self, ctx:MySqlParser.ShowSlaveStatusContext):
        pass


    # Enter a parse tree produced by MySqlParser#variableClause.
    def enterVariableClause(self, ctx:MySqlParser.VariableClauseContext):
        pass

    # Exit a parse tree produced by MySqlParser#variableClause.
    def exitVariableClause(self, ctx:MySqlParser.VariableClauseContext):
        pass


    # Enter a parse tree produced by MySqlParser#showCommonEntity.
    def enterShowCommonEntity(self, ctx:MySqlParser.ShowCommonEntityContext):
        pass

    # Exit a parse tree produced by MySqlParser#showCommonEntity.
    def exitShowCommonEntity(self, ctx:MySqlParser.ShowCommonEntityContext):
        pass


    # Enter a parse tree produced by MySqlParser#showFilter.
    def enterShowFilter(self, ctx:MySqlParser.ShowFilterContext):
        pass

    # Exit a parse tree produced by MySqlParser#showFilter.
    def exitShowFilter(self, ctx:MySqlParser.ShowFilterContext):
        pass


    # Enter a parse tree produced by MySqlParser#showGlobalInfoClause.
    def enterShowGlobalInfoClause(self, ctx:MySqlParser.ShowGlobalInfoClauseContext):
        pass

    # Exit a parse tree produced by MySqlParser#showGlobalInfoClause.
    def exitShowGlobalInfoClause(self, ctx:MySqlParser.ShowGlobalInfoClauseContext):
        pass


    # Enter a parse tree produced by MySqlParser#showSchemaEntity.
    def enterShowSchemaEntity(self, ctx:MySqlParser.ShowSchemaEntityContext):
        pass

    # Exit a parse tree produced by MySqlParser#showSchemaEntity.
    def exitShowSchemaEntity(self, ctx:MySqlParser.ShowSchemaEntityContext):
        pass


    # Enter a parse tree produced by MySqlParser#showProfileType.
    def enterShowProfileType(self, ctx:MySqlParser.ShowProfileTypeContext):
        pass

    # Exit a parse tree produced by MySqlParser#showProfileType.
    def exitShowProfileType(self, ctx:MySqlParser.ShowProfileTypeContext):
        pass


    # Enter a parse tree produced by MySqlParser#binlogStatement.
    def enterBinlogStatement(self, ctx:MySqlParser.BinlogStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#binlogStatement.
    def exitBinlogStatement(self, ctx:MySqlParser.BinlogStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#cacheIndexStatement.
    def enterCacheIndexStatement(self, ctx:MySqlParser.CacheIndexStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#cacheIndexStatement.
    def exitCacheIndexStatement(self, ctx:MySqlParser.CacheIndexStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#flushStatement.
    def enterFlushStatement(self, ctx:MySqlParser.FlushStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#flushStatement.
    def exitFlushStatement(self, ctx:MySqlParser.FlushStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#killStatement.
    def enterKillStatement(self, ctx:MySqlParser.KillStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#killStatement.
    def exitKillStatement(self, ctx:MySqlParser.KillStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#loadIndexIntoCache.
    def enterLoadIndexIntoCache(self, ctx:MySqlParser.LoadIndexIntoCacheContext):
        pass

    # Exit a parse tree produced by MySqlParser#loadIndexIntoCache.
    def exitLoadIndexIntoCache(self, ctx:MySqlParser.LoadIndexIntoCacheContext):
        pass


    # Enter a parse tree produced by MySqlParser#resetStatement.
    def enterResetStatement(self, ctx:MySqlParser.ResetStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#resetStatement.
    def exitResetStatement(self, ctx:MySqlParser.ResetStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#shutdownStatement.
    def enterShutdownStatement(self, ctx:MySqlParser.ShutdownStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#shutdownStatement.
    def exitShutdownStatement(self, ctx:MySqlParser.ShutdownStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableIndexes.
    def enterTableIndexes(self, ctx:MySqlParser.TableIndexesContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableIndexes.
    def exitTableIndexes(self, ctx:MySqlParser.TableIndexesContext):
        pass


    # Enter a parse tree produced by MySqlParser#simpleFlushOption.
    def enterSimpleFlushOption(self, ctx:MySqlParser.SimpleFlushOptionContext):
        pass

    # Exit a parse tree produced by MySqlParser#simpleFlushOption.
    def exitSimpleFlushOption(self, ctx:MySqlParser.SimpleFlushOptionContext):
        pass


    # Enter a parse tree produced by MySqlParser#channelFlushOption.
    def enterChannelFlushOption(self, ctx:MySqlParser.ChannelFlushOptionContext):
        pass

    # Exit a parse tree produced by MySqlParser#channelFlushOption.
    def exitChannelFlushOption(self, ctx:MySqlParser.ChannelFlushOptionContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableFlushOption.
    def enterTableFlushOption(self, ctx:MySqlParser.TableFlushOptionContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableFlushOption.
    def exitTableFlushOption(self, ctx:MySqlParser.TableFlushOptionContext):
        pass


    # Enter a parse tree produced by MySqlParser#flushTableOption.
    def enterFlushTableOption(self, ctx:MySqlParser.FlushTableOptionContext):
        pass

    # Exit a parse tree produced by MySqlParser#flushTableOption.
    def exitFlushTableOption(self, ctx:MySqlParser.FlushTableOptionContext):
        pass


    # Enter a parse tree produced by MySqlParser#loadedTableIndexes.
    def enterLoadedTableIndexes(self, ctx:MySqlParser.LoadedTableIndexesContext):
        pass

    # Exit a parse tree produced by MySqlParser#loadedTableIndexes.
    def exitLoadedTableIndexes(self, ctx:MySqlParser.LoadedTableIndexesContext):
        pass


    # Enter a parse tree produced by MySqlParser#simpleDescribeStatement.
    def enterSimpleDescribeStatement(self, ctx:MySqlParser.SimpleDescribeStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#simpleDescribeStatement.
    def exitSimpleDescribeStatement(self, ctx:MySqlParser.SimpleDescribeStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#fullDescribeStatement.
    def enterFullDescribeStatement(self, ctx:MySqlParser.FullDescribeStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#fullDescribeStatement.
    def exitFullDescribeStatement(self, ctx:MySqlParser.FullDescribeStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#helpStatement.
    def enterHelpStatement(self, ctx:MySqlParser.HelpStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#helpStatement.
    def exitHelpStatement(self, ctx:MySqlParser.HelpStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#useStatement.
    def enterUseStatement(self, ctx:MySqlParser.UseStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#useStatement.
    def exitUseStatement(self, ctx:MySqlParser.UseStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#signalStatement.
    def enterSignalStatement(self, ctx:MySqlParser.SignalStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#signalStatement.
    def exitSignalStatement(self, ctx:MySqlParser.SignalStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#resignalStatement.
    def enterResignalStatement(self, ctx:MySqlParser.ResignalStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#resignalStatement.
    def exitResignalStatement(self, ctx:MySqlParser.ResignalStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#signalConditionInformation.
    def enterSignalConditionInformation(self, ctx:MySqlParser.SignalConditionInformationContext):
        pass

    # Exit a parse tree produced by MySqlParser#signalConditionInformation.
    def exitSignalConditionInformation(self, ctx:MySqlParser.SignalConditionInformationContext):
        pass


    # Enter a parse tree produced by MySqlParser#withStatement.
    def enterWithStatement(self, ctx:MySqlParser.WithStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#withStatement.
    def exitWithStatement(self, ctx:MySqlParser.WithStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableStatement.
    def enterTableStatement(self, ctx:MySqlParser.TableStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableStatement.
    def exitTableStatement(self, ctx:MySqlParser.TableStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#diagnosticsStatement.
    def enterDiagnosticsStatement(self, ctx:MySqlParser.DiagnosticsStatementContext):
        pass

    # Exit a parse tree produced by MySqlParser#diagnosticsStatement.
    def exitDiagnosticsStatement(self, ctx:MySqlParser.DiagnosticsStatementContext):
        pass


    # Enter a parse tree produced by MySqlParser#diagnosticsConditionInformationName.
    def enterDiagnosticsConditionInformationName(self, ctx:MySqlParser.DiagnosticsConditionInformationNameContext):
        pass

    # Exit a parse tree produced by MySqlParser#diagnosticsConditionInformationName.
    def exitDiagnosticsConditionInformationName(self, ctx:MySqlParser.DiagnosticsConditionInformationNameContext):
        pass


    # Enter a parse tree produced by MySqlParser#describeStatements.
    def enterDescribeStatements(self, ctx:MySqlParser.DescribeStatementsContext):
        pass

    # Exit a parse tree produced by MySqlParser#describeStatements.
    def exitDescribeStatements(self, ctx:MySqlParser.DescribeStatementsContext):
        pass


    # Enter a parse tree produced by MySqlParser#describeConnection.
    def enterDescribeConnection(self, ctx:MySqlParser.DescribeConnectionContext):
        pass

    # Exit a parse tree produced by MySqlParser#describeConnection.
    def exitDescribeConnection(self, ctx:MySqlParser.DescribeConnectionContext):
        pass


    # Enter a parse tree produced by MySqlParser#fullId.
    def enterFullId(self, ctx:MySqlParser.FullIdContext):
        pass

    # Exit a parse tree produced by MySqlParser#fullId.
    def exitFullId(self, ctx:MySqlParser.FullIdContext):
        pass


    # Enter a parse tree produced by MySqlParser#tableName.
    def enterTableName(self, ctx:MySqlParser.TableNameContext):
        pass

    # Exit a parse tree produced by MySqlParser#tableName.
    def exitTableName(self, ctx:MySqlParser.TableNameContext):
        pass


    # Enter a parse tree produced by MySqlParser#roleName.
    def enterRoleName(self, ctx:MySqlParser.RoleNameContext):
        pass

    # Exit a parse tree produced by MySqlParser#roleName.
    def exitRoleName(self, ctx:MySqlParser.RoleNameContext):
        pass


    # Enter a parse tree produced by MySqlParser#fullColumnName.
    def enterFullColumnName(self, ctx:MySqlParser.FullColumnNameContext):
        pass

    # Exit a parse tree produced by MySqlParser#fullColumnName.
    def exitFullColumnName(self, ctx:MySqlParser.FullColumnNameContext):
        pass


    # Enter a parse tree produced by MySqlParser#indexColumnName.
    def enterIndexColumnName(self, ctx:MySqlParser.IndexColumnNameContext):
        pass

    # Exit a parse tree produced by MySqlParser#indexColumnName.
    def exitIndexColumnName(self, ctx:MySqlParser.IndexColumnNameContext):
        pass


    # Enter a parse tree produced by MySqlParser#userName.
    def enterUserName(self, ctx:MySqlParser.UserNameContext):
        pass

    # Exit a parse tree produced by MySqlParser#userName.
    def exitUserName(self, ctx:MySqlParser.UserNameContext):
        pass


    # Enter a parse tree produced by MySqlParser#mysqlVariable.
    def enterMysqlVariable(self, ctx:MySqlParser.MysqlVariableContext):
        pass

    # Exit a parse tree produced by MySqlParser#mysqlVariable.
    def exitMysqlVariable(self, ctx:MySqlParser.MysqlVariableContext):
        pass


    # Enter a parse tree produced by MySqlParser#charsetName.
    def enterCharsetName(self, ctx:MySqlParser.CharsetNameContext):
        pass

    # Exit a parse tree produced by MySqlParser#charsetName.
    def exitCharsetName(self, ctx:MySqlParser.CharsetNameContext):
        pass


    # Enter a parse tree produced by MySqlParser#collationName.
    def enterCollationName(self, ctx:MySqlParser.CollationNameContext):
        pass

    # Exit a parse tree produced by MySqlParser#collationName.
    def exitCollationName(self, ctx:MySqlParser.CollationNameContext):
        pass


    # Enter a parse tree produced by MySqlParser#engineName.
    def enterEngineName(self, ctx:MySqlParser.EngineNameContext):
        pass

    # Exit a parse tree produced by MySqlParser#engineName.
    def exitEngineName(self, ctx:MySqlParser.EngineNameContext):
        pass


    # Enter a parse tree produced by MySqlParser#engineNameBase.
    def enterEngineNameBase(self, ctx:MySqlParser.EngineNameBaseContext):
        pass

    # Exit a parse tree produced by MySqlParser#engineNameBase.
    def exitEngineNameBase(self, ctx:MySqlParser.EngineNameBaseContext):
        pass


    # Enter a parse tree produced by MySqlParser#uuidSet.
    def enterUuidSet(self, ctx:MySqlParser.UuidSetContext):
        pass

    # Exit a parse tree produced by MySqlParser#uuidSet.
    def exitUuidSet(self, ctx:MySqlParser.UuidSetContext):
        pass


    # Enter a parse tree produced by MySqlParser#xid.
    def enterXid(self, ctx:MySqlParser.XidContext):
        pass

    # Exit a parse tree produced by MySqlParser#xid.
    def exitXid(self, ctx:MySqlParser.XidContext):
        pass


    # Enter a parse tree produced by MySqlParser#xuidStringId.
    def enterXuidStringId(self, ctx:MySqlParser.XuidStringIdContext):
        pass

    # Exit a parse tree produced by MySqlParser#xuidStringId.
    def exitXuidStringId(self, ctx:MySqlParser.XuidStringIdContext):
        pass


    # Enter a parse tree produced by MySqlParser#authPlugin.
    def enterAuthPlugin(self, ctx:MySqlParser.AuthPluginContext):
        pass

    # Exit a parse tree produced by MySqlParser#authPlugin.
    def exitAuthPlugin(self, ctx:MySqlParser.AuthPluginContext):
        pass


    # Enter a parse tree produced by MySqlParser#uid.
    def enterUid(self, ctx:MySqlParser.UidContext):
        pass

    # Exit a parse tree produced by MySqlParser#uid.
    def exitUid(self, ctx:MySqlParser.UidContext):
        pass


    # Enter a parse tree produced by MySqlParser#simpleId.
    def enterSimpleId(self, ctx:MySqlParser.SimpleIdContext):
        pass

    # Exit a parse tree produced by MySqlParser#simpleId.
    def exitSimpleId(self, ctx:MySqlParser.SimpleIdContext):
        pass


    # Enter a parse tree produced by MySqlParser#dottedId.
    def enterDottedId(self, ctx:MySqlParser.DottedIdContext):
        pass

    # Exit a parse tree produced by MySqlParser#dottedId.
    def exitDottedId(self, ctx:MySqlParser.DottedIdContext):
        pass


    # Enter a parse tree produced by MySqlParser#decimalLiteral.
    def enterDecimalLiteral(self, ctx:MySqlParser.DecimalLiteralContext):
        pass

    # Exit a parse tree produced by MySqlParser#decimalLiteral.
    def exitDecimalLiteral(self, ctx:MySqlParser.DecimalLiteralContext):
        pass


    # Enter a parse tree produced by MySqlParser#fileSizeLiteral.
    def enterFileSizeLiteral(self, ctx:MySqlParser.FileSizeLiteralContext):
        pass

    # Exit a parse tree produced by MySqlParser#fileSizeLiteral.
    def exitFileSizeLiteral(self, ctx:MySqlParser.FileSizeLiteralContext):
        pass


    # Enter a parse tree produced by MySqlParser#stringLiteral.
    def enterStringLiteral(self, ctx:MySqlParser.StringLiteralContext):
        pass

    # Exit a parse tree produced by MySqlParser#stringLiteral.
    def exitStringLiteral(self, ctx:MySqlParser.StringLiteralContext):
        pass


    # Enter a parse tree produced by MySqlParser#booleanLiteral.
    def enterBooleanLiteral(self, ctx:MySqlParser.BooleanLiteralContext):
        pass

    # Exit a parse tree produced by MySqlParser#booleanLiteral.
    def exitBooleanLiteral(self, ctx:MySqlParser.BooleanLiteralContext):
        pass


    # Enter a parse tree produced by MySqlParser#hexadecimalLiteral.
    def enterHexadecimalLiteral(self, ctx:MySqlParser.HexadecimalLiteralContext):
        pass

    # Exit a parse tree produced by MySqlParser#hexadecimalLiteral.
    def exitHexadecimalLiteral(self, ctx:MySqlParser.HexadecimalLiteralContext):
        pass


    # Enter a parse tree produced by MySqlParser#nullNotnull.
    def enterNullNotnull(self, ctx:MySqlParser.NullNotnullContext):
        pass

    # Exit a parse tree produced by MySqlParser#nullNotnull.
    def exitNullNotnull(self, ctx:MySqlParser.NullNotnullContext):
        pass


    # Enter a parse tree produced by MySqlParser#constant.
    def enterConstant(self, ctx:MySqlParser.ConstantContext):
        pass

    # Exit a parse tree produced by MySqlParser#constant.
    def exitConstant(self, ctx:MySqlParser.ConstantContext):
        pass


    # Enter a parse tree produced by MySqlParser#stringDataType.
    def enterStringDataType(self, ctx:MySqlParser.StringDataTypeContext):
        pass

    # Exit a parse tree produced by MySqlParser#stringDataType.
    def exitStringDataType(self, ctx:MySqlParser.StringDataTypeContext):
        pass


    # Enter a parse tree produced by MySqlParser#nationalVaryingStringDataType.
    def enterNationalVaryingStringDataType(self, ctx:MySqlParser.NationalVaryingStringDataTypeContext):
        pass

    # Exit a parse tree produced by MySqlParser#nationalVaryingStringDataType.
    def exitNationalVaryingStringDataType(self, ctx:MySqlParser.NationalVaryingStringDataTypeContext):
        pass


    # Enter a parse tree produced by MySqlParser#nationalStringDataType.
    def enterNationalStringDataType(self, ctx:MySqlParser.NationalStringDataTypeContext):
        pass

    # Exit a parse tree produced by MySqlParser#nationalStringDataType.
    def exitNationalStringDataType(self, ctx:MySqlParser.NationalStringDataTypeContext):
        pass


    # Enter a parse tree produced by MySqlParser#dimensionDataType.
    def enterDimensionDataType(self, ctx:MySqlParser.DimensionDataTypeContext):
        pass

    # Exit a parse tree produced by MySqlParser#dimensionDataType.
    def exitDimensionDataType(self, ctx:MySqlParser.DimensionDataTypeContext):
        pass


    # Enter a parse tree produced by MySqlParser#simpleDataType.
    def enterSimpleDataType(self, ctx:MySqlParser.SimpleDataTypeContext):
        pass

    # Exit a parse tree produced by MySqlParser#simpleDataType.
    def exitSimpleDataType(self, ctx:MySqlParser.SimpleDataTypeContext):
        pass


    # Enter a parse tree produced by MySqlParser#collectionDataType.
    def enterCollectionDataType(self, ctx:MySqlParser.CollectionDataTypeContext):
        pass

    # Exit a parse tree produced by MySqlParser#collectionDataType.
    def exitCollectionDataType(self, ctx:MySqlParser.CollectionDataTypeContext):
        pass


    # Enter a parse tree produced by MySqlParser#spatialDataType.
    def enterSpatialDataType(self, ctx:MySqlParser.SpatialDataTypeContext):
        pass

    # Exit a parse tree produced by MySqlParser#spatialDataType.
    def exitSpatialDataType(self, ctx:MySqlParser.SpatialDataTypeContext):
        pass


    # Enter a parse tree produced by MySqlParser#longVarcharDataType.
    def enterLongVarcharDataType(self, ctx:MySqlParser.LongVarcharDataTypeContext):
        pass

    # Exit a parse tree produced by MySqlParser#longVarcharDataType.
    def exitLongVarcharDataType(self, ctx:MySqlParser.LongVarcharDataTypeContext):
        pass


    # Enter a parse tree produced by MySqlParser#longVarbinaryDataType.
    def enterLongVarbinaryDataType(self, ctx:MySqlParser.LongVarbinaryDataTypeContext):
        pass

    # Exit a parse tree produced by MySqlParser#longVarbinaryDataType.
    def exitLongVarbinaryDataType(self, ctx:MySqlParser.LongVarbinaryDataTypeContext):
        pass


    # Enter a parse tree produced by MySqlParser#collectionOptions.
    def enterCollectionOptions(self, ctx:MySqlParser.CollectionOptionsContext):
        pass

    # Exit a parse tree produced by MySqlParser#collectionOptions.
    def exitCollectionOptions(self, ctx:MySqlParser.CollectionOptionsContext):
        pass


    # Enter a parse tree produced by MySqlParser#convertedDataType.
    def enterConvertedDataType(self, ctx:MySqlParser.ConvertedDataTypeContext):
        pass

    # Exit a parse tree produced by MySqlParser#convertedDataType.
    def exitConvertedDataType(self, ctx:MySqlParser.ConvertedDataTypeContext):
        pass


    # Enter a parse tree produced by MySqlParser#lengthOneDimension.
    def enterLengthOneDimension(self, ctx:MySqlParser.LengthOneDimensionContext):
        pass

    # Exit a parse tree produced by MySqlParser#lengthOneDimension.
    def exitLengthOneDimension(self, ctx:MySqlParser.LengthOneDimensionContext):
        pass


    # Enter a parse tree produced by MySqlParser#lengthTwoDimension.
    def enterLengthTwoDimension(self, ctx:MySqlParser.LengthTwoDimensionContext):
        pass

    # Exit a parse tree produced by MySqlParser#lengthTwoDimension.
    def exitLengthTwoDimension(self, ctx:MySqlParser.LengthTwoDimensionContext):
        pass


    # Enter a parse tree produced by MySqlParser#lengthTwoOptionalDimension.
    def enterLengthTwoOptionalDimension(self, ctx:MySqlParser.LengthTwoOptionalDimensionContext):
        pass

    # Exit a parse tree produced by MySqlParser#lengthTwoOptionalDimension.
    def exitLengthTwoOptionalDimension(self, ctx:MySqlParser.LengthTwoOptionalDimensionContext):
        pass


    # Enter a parse tree produced by MySqlParser#uidList.
    def enterUidList(self, ctx:MySqlParser.UidListContext):
        pass

    # Exit a parse tree produced by MySqlParser#uidList.
    def exitUidList(self, ctx:MySqlParser.UidListContext):
        pass


    # Enter a parse tree produced by MySqlParser#fullColumnNameList.
    def enterFullColumnNameList(self, ctx:MySqlParser.FullColumnNameListContext):
        pass

    # Exit a parse tree produced by MySqlParser#fullColumnNameList.
    def exitFullColumnNameList(self, ctx:MySqlParser.FullColumnNameListContext):
        pass


    # Enter a parse tree produced by MySqlParser#tables.
    def enterTables(self, ctx:MySqlParser.TablesContext):
        pass

    # Exit a parse tree produced by MySqlParser#tables.
    def exitTables(self, ctx:MySqlParser.TablesContext):
        pass


    # Enter a parse tree produced by MySqlParser#indexColumnNames.
    def enterIndexColumnNames(self, ctx:MySqlParser.IndexColumnNamesContext):
        pass

    # Exit a parse tree produced by MySqlParser#indexColumnNames.
    def exitIndexColumnNames(self, ctx:MySqlParser.IndexColumnNamesContext):
        pass


    # Enter a parse tree produced by MySqlParser#expressions.
    def enterExpressions(self, ctx:MySqlParser.ExpressionsContext):
        pass

    # Exit a parse tree produced by MySqlParser#expressions.
    def exitExpressions(self, ctx:MySqlParser.ExpressionsContext):
        pass


    # Enter a parse tree produced by MySqlParser#expressionsWithDefaults.
    def enterExpressionsWithDefaults(self, ctx:MySqlParser.ExpressionsWithDefaultsContext):
        pass

    # Exit a parse tree produced by MySqlParser#expressionsWithDefaults.
    def exitExpressionsWithDefaults(self, ctx:MySqlParser.ExpressionsWithDefaultsContext):
        pass


    # Enter a parse tree produced by MySqlParser#constants.
    def enterConstants(self, ctx:MySqlParser.ConstantsContext):
        pass

    # Exit a parse tree produced by MySqlParser#constants.
    def exitConstants(self, ctx:MySqlParser.ConstantsContext):
        pass


    # Enter a parse tree produced by MySqlParser#simpleStrings.
    def enterSimpleStrings(self, ctx:MySqlParser.SimpleStringsContext):
        pass

    # Exit a parse tree produced by MySqlParser#simpleStrings.
    def exitSimpleStrings(self, ctx:MySqlParser.SimpleStringsContext):
        pass


    # Enter a parse tree produced by MySqlParser#userVariables.
    def enterUserVariables(self, ctx:MySqlParser.UserVariablesContext):
        pass

    # Exit a parse tree produced by MySqlParser#userVariables.
    def exitUserVariables(self, ctx:MySqlParser.UserVariablesContext):
        pass


    # Enter a parse tree produced by MySqlParser#defaultValue.
    def enterDefaultValue(self, ctx:MySqlParser.DefaultValueContext):
        pass

    # Exit a parse tree produced by MySqlParser#defaultValue.
    def exitDefaultValue(self, ctx:MySqlParser.DefaultValueContext):
        pass


    # Enter a parse tree produced by MySqlParser#currentTimestamp.
    def enterCurrentTimestamp(self, ctx:MySqlParser.CurrentTimestampContext):
        pass

    # Exit a parse tree produced by MySqlParser#currentTimestamp.
    def exitCurrentTimestamp(self, ctx:MySqlParser.CurrentTimestampContext):
        pass


    # Enter a parse tree produced by MySqlParser#expressionOrDefault.
    def enterExpressionOrDefault(self, ctx:MySqlParser.ExpressionOrDefaultContext):
        pass

    # Exit a parse tree produced by MySqlParser#expressionOrDefault.
    def exitExpressionOrDefault(self, ctx:MySqlParser.ExpressionOrDefaultContext):
        pass


    # Enter a parse tree produced by MySqlParser#ifExists.
    def enterIfExists(self, ctx:MySqlParser.IfExistsContext):
        pass

    # Exit a parse tree produced by MySqlParser#ifExists.
    def exitIfExists(self, ctx:MySqlParser.IfExistsContext):
        pass


    # Enter a parse tree produced by MySqlParser#ifNotExists.
    def enterIfNotExists(self, ctx:MySqlParser.IfNotExistsContext):
        pass

    # Exit a parse tree produced by MySqlParser#ifNotExists.
    def exitIfNotExists(self, ctx:MySqlParser.IfNotExistsContext):
        pass


    # Enter a parse tree produced by MySqlParser#orReplace.
    def enterOrReplace(self, ctx:MySqlParser.OrReplaceContext):
        pass

    # Exit a parse tree produced by MySqlParser#orReplace.
    def exitOrReplace(self, ctx:MySqlParser.OrReplaceContext):
        pass


    # Enter a parse tree produced by MySqlParser#waitNowaitClause.
    def enterWaitNowaitClause(self, ctx:MySqlParser.WaitNowaitClauseContext):
        pass

    # Exit a parse tree produced by MySqlParser#waitNowaitClause.
    def exitWaitNowaitClause(self, ctx:MySqlParser.WaitNowaitClauseContext):
        pass


    # Enter a parse tree produced by MySqlParser#specificFunctionCall.
    def enterSpecificFunctionCall(self, ctx:MySqlParser.SpecificFunctionCallContext):
        pass

    # Exit a parse tree produced by MySqlParser#specificFunctionCall.
    def exitSpecificFunctionCall(self, ctx:MySqlParser.SpecificFunctionCallContext):
        pass


    # Enter a parse tree produced by MySqlParser#aggregateFunctionCall.
    def enterAggregateFunctionCall(self, ctx:MySqlParser.AggregateFunctionCallContext):
        pass

    # Exit a parse tree produced by MySqlParser#aggregateFunctionCall.
    def exitAggregateFunctionCall(self, ctx:MySqlParser.AggregateFunctionCallContext):
        pass


    # Enter a parse tree produced by MySqlParser#nonAggregateFunctionCall.
    def enterNonAggregateFunctionCall(self, ctx:MySqlParser.NonAggregateFunctionCallContext):
        pass

    # Exit a parse tree produced by MySqlParser#nonAggregateFunctionCall.
    def exitNonAggregateFunctionCall(self, ctx:MySqlParser.NonAggregateFunctionCallContext):
        pass


    # Enter a parse tree produced by MySqlParser#scalarFunctionCall.
    def enterScalarFunctionCall(self, ctx:MySqlParser.ScalarFunctionCallContext):
        pass

    # Exit a parse tree produced by MySqlParser#scalarFunctionCall.
    def exitScalarFunctionCall(self, ctx:MySqlParser.ScalarFunctionCallContext):
        pass


    # Enter a parse tree produced by MySqlParser#udfFunctionCall.
    def enterUdfFunctionCall(self, ctx:MySqlParser.UdfFunctionCallContext):
        pass

    # Exit a parse tree produced by MySqlParser#udfFunctionCall.
    def exitUdfFunctionCall(self, ctx:MySqlParser.UdfFunctionCallContext):
        pass


    # Enter a parse tree produced by MySqlParser#passwordFunctionCall.
    def enterPasswordFunctionCall(self, ctx:MySqlParser.PasswordFunctionCallContext):
        pass

    # Exit a parse tree produced by MySqlParser#passwordFunctionCall.
    def exitPasswordFunctionCall(self, ctx:MySqlParser.PasswordFunctionCallContext):
        pass


    # Enter a parse tree produced by MySqlParser#simpleFunctionCall.
    def enterSimpleFunctionCall(self, ctx:MySqlParser.SimpleFunctionCallContext):
        pass

    # Exit a parse tree produced by MySqlParser#simpleFunctionCall.
    def exitSimpleFunctionCall(self, ctx:MySqlParser.SimpleFunctionCallContext):
        pass


    # Enter a parse tree produced by MySqlParser#dataTypeFunctionCall.
    def enterDataTypeFunctionCall(self, ctx:MySqlParser.DataTypeFunctionCallContext):
        pass

    # Exit a parse tree produced by MySqlParser#dataTypeFunctionCall.
    def exitDataTypeFunctionCall(self, ctx:MySqlParser.DataTypeFunctionCallContext):
        pass


    # Enter a parse tree produced by MySqlParser#valuesFunctionCall.
    def enterValuesFunctionCall(self, ctx:MySqlParser.ValuesFunctionCallContext):
        pass

    # Exit a parse tree produced by MySqlParser#valuesFunctionCall.
    def exitValuesFunctionCall(self, ctx:MySqlParser.ValuesFunctionCallContext):
        pass


    # Enter a parse tree produced by MySqlParser#caseExpressionFunctionCall.
    def enterCaseExpressionFunctionCall(self, ctx:MySqlParser.CaseExpressionFunctionCallContext):
        pass

    # Exit a parse tree produced by MySqlParser#caseExpressionFunctionCall.
    def exitCaseExpressionFunctionCall(self, ctx:MySqlParser.CaseExpressionFunctionCallContext):
        pass


    # Enter a parse tree produced by MySqlParser#caseFunctionCall.
    def enterCaseFunctionCall(self, ctx:MySqlParser.CaseFunctionCallContext):
        pass

    # Exit a parse tree produced by MySqlParser#caseFunctionCall.
    def exitCaseFunctionCall(self, ctx:MySqlParser.CaseFunctionCallContext):
        pass


    # Enter a parse tree produced by MySqlParser#charFunctionCall.
    def enterCharFunctionCall(self, ctx:MySqlParser.CharFunctionCallContext):
        pass

    # Exit a parse tree produced by MySqlParser#charFunctionCall.
    def exitCharFunctionCall(self, ctx:MySqlParser.CharFunctionCallContext):
        pass


    # Enter a parse tree produced by MySqlParser#positionFunctionCall.
    def enterPositionFunctionCall(self, ctx:MySqlParser.PositionFunctionCallContext):
        pass

    # Exit a parse tree produced by MySqlParser#positionFunctionCall.
    def exitPositionFunctionCall(self, ctx:MySqlParser.PositionFunctionCallContext):
        pass


    # Enter a parse tree produced by MySqlParser#substrFunctionCall.
    def enterSubstrFunctionCall(self, ctx:MySqlParser.SubstrFunctionCallContext):
        pass

    # Exit a parse tree produced by MySqlParser#substrFunctionCall.
    def exitSubstrFunctionCall(self, ctx:MySqlParser.SubstrFunctionCallContext):
        pass


    # Enter a parse tree produced by MySqlParser#trimFunctionCall.
    def enterTrimFunctionCall(self, ctx:MySqlParser.TrimFunctionCallContext):
        pass

    # Exit a parse tree produced by MySqlParser#trimFunctionCall.
    def exitTrimFunctionCall(self, ctx:MySqlParser.TrimFunctionCallContext):
        pass


    # Enter a parse tree produced by MySqlParser#weightFunctionCall.
    def enterWeightFunctionCall(self, ctx:MySqlParser.WeightFunctionCallContext):
        pass

    # Exit a parse tree produced by MySqlParser#weightFunctionCall.
    def exitWeightFunctionCall(self, ctx:MySqlParser.WeightFunctionCallContext):
        pass


    # Enter a parse tree produced by MySqlParser#extractFunctionCall.
    def enterExtractFunctionCall(self, ctx:MySqlParser.ExtractFunctionCallContext):
        pass

    # Exit a parse tree produced by MySqlParser#extractFunctionCall.
    def exitExtractFunctionCall(self, ctx:MySqlParser.ExtractFunctionCallContext):
        pass


    # Enter a parse tree produced by MySqlParser#getFormatFunctionCall.
    def enterGetFormatFunctionCall(self, ctx:MySqlParser.GetFormatFunctionCallContext):
        pass

    # Exit a parse tree produced by MySqlParser#getFormatFunctionCall.
    def exitGetFormatFunctionCall(self, ctx:MySqlParser.GetFormatFunctionCallContext):
        pass


    # Enter a parse tree produced by MySqlParser#jsonValueFunctionCall.
    def enterJsonValueFunctionCall(self, ctx:MySqlParser.JsonValueFunctionCallContext):
        pass

    # Exit a parse tree produced by MySqlParser#jsonValueFunctionCall.
    def exitJsonValueFunctionCall(self, ctx:MySqlParser.JsonValueFunctionCallContext):
        pass


    # Enter a parse tree produced by MySqlParser#caseFuncAlternative.
    def enterCaseFuncAlternative(self, ctx:MySqlParser.CaseFuncAlternativeContext):
        pass

    # Exit a parse tree produced by MySqlParser#caseFuncAlternative.
    def exitCaseFuncAlternative(self, ctx:MySqlParser.CaseFuncAlternativeContext):
        pass


    # Enter a parse tree produced by MySqlParser#levelWeightList.
    def enterLevelWeightList(self, ctx:MySqlParser.LevelWeightListContext):
        pass

    # Exit a parse tree produced by MySqlParser#levelWeightList.
    def exitLevelWeightList(self, ctx:MySqlParser.LevelWeightListContext):
        pass


    # Enter a parse tree produced by MySqlParser#levelWeightRange.
    def enterLevelWeightRange(self, ctx:MySqlParser.LevelWeightRangeContext):
        pass

    # Exit a parse tree produced by MySqlParser#levelWeightRange.
    def exitLevelWeightRange(self, ctx:MySqlParser.LevelWeightRangeContext):
        pass


    # Enter a parse tree produced by MySqlParser#levelInWeightListElement.
    def enterLevelInWeightListElement(self, ctx:MySqlParser.LevelInWeightListElementContext):
        pass

    # Exit a parse tree produced by MySqlParser#levelInWeightListElement.
    def exitLevelInWeightListElement(self, ctx:MySqlParser.LevelInWeightListElementContext):
        pass


    # Enter a parse tree produced by MySqlParser#aggregateWindowedFunction.
    def enterAggregateWindowedFunction(self, ctx:MySqlParser.AggregateWindowedFunctionContext):
        pass

    # Exit a parse tree produced by MySqlParser#aggregateWindowedFunction.
    def exitAggregateWindowedFunction(self, ctx:MySqlParser.AggregateWindowedFunctionContext):
        pass


    # Enter a parse tree produced by MySqlParser#nonAggregateWindowedFunction.
    def enterNonAggregateWindowedFunction(self, ctx:MySqlParser.NonAggregateWindowedFunctionContext):
        pass

    # Exit a parse tree produced by MySqlParser#nonAggregateWindowedFunction.
    def exitNonAggregateWindowedFunction(self, ctx:MySqlParser.NonAggregateWindowedFunctionContext):
        pass


    # Enter a parse tree produced by MySqlParser#overClause.
    def enterOverClause(self, ctx:MySqlParser.OverClauseContext):
        pass

    # Exit a parse tree produced by MySqlParser#overClause.
    def exitOverClause(self, ctx:MySqlParser.OverClauseContext):
        pass


    # Enter a parse tree produced by MySqlParser#windowSpec.
    def enterWindowSpec(self, ctx:MySqlParser.WindowSpecContext):
        pass

    # Exit a parse tree produced by MySqlParser#windowSpec.
    def exitWindowSpec(self, ctx:MySqlParser.WindowSpecContext):
        pass


    # Enter a parse tree produced by MySqlParser#windowName.
    def enterWindowName(self, ctx:MySqlParser.WindowNameContext):
        pass

    # Exit a parse tree produced by MySqlParser#windowName.
    def exitWindowName(self, ctx:MySqlParser.WindowNameContext):
        pass


    # Enter a parse tree produced by MySqlParser#frameClause.
    def enterFrameClause(self, ctx:MySqlParser.FrameClauseContext):
        pass

    # Exit a parse tree produced by MySqlParser#frameClause.
    def exitFrameClause(self, ctx:MySqlParser.FrameClauseContext):
        pass


    # Enter a parse tree produced by MySqlParser#frameUnits.
    def enterFrameUnits(self, ctx:MySqlParser.FrameUnitsContext):
        pass

    # Exit a parse tree produced by MySqlParser#frameUnits.
    def exitFrameUnits(self, ctx:MySqlParser.FrameUnitsContext):
        pass


    # Enter a parse tree produced by MySqlParser#frameExtent.
    def enterFrameExtent(self, ctx:MySqlParser.FrameExtentContext):
        pass

    # Exit a parse tree produced by MySqlParser#frameExtent.
    def exitFrameExtent(self, ctx:MySqlParser.FrameExtentContext):
        pass


    # Enter a parse tree produced by MySqlParser#frameBetween.
    def enterFrameBetween(self, ctx:MySqlParser.FrameBetweenContext):
        pass

    # Exit a parse tree produced by MySqlParser#frameBetween.
    def exitFrameBetween(self, ctx:MySqlParser.FrameBetweenContext):
        pass


    # Enter a parse tree produced by MySqlParser#frameRange.
    def enterFrameRange(self, ctx:MySqlParser.FrameRangeContext):
        pass

    # Exit a parse tree produced by MySqlParser#frameRange.
    def exitFrameRange(self, ctx:MySqlParser.FrameRangeContext):
        pass


    # Enter a parse tree produced by MySqlParser#partitionClause.
    def enterPartitionClause(self, ctx:MySqlParser.PartitionClauseContext):
        pass

    # Exit a parse tree produced by MySqlParser#partitionClause.
    def exitPartitionClause(self, ctx:MySqlParser.PartitionClauseContext):
        pass


    # Enter a parse tree produced by MySqlParser#scalarFunctionName.
    def enterScalarFunctionName(self, ctx:MySqlParser.ScalarFunctionNameContext):
        pass

    # Exit a parse tree produced by MySqlParser#scalarFunctionName.
    def exitScalarFunctionName(self, ctx:MySqlParser.ScalarFunctionNameContext):
        pass


    # Enter a parse tree produced by MySqlParser#passwordFunctionClause.
    def enterPasswordFunctionClause(self, ctx:MySqlParser.PasswordFunctionClauseContext):
        pass

    # Exit a parse tree produced by MySqlParser#passwordFunctionClause.
    def exitPasswordFunctionClause(self, ctx:MySqlParser.PasswordFunctionClauseContext):
        pass


    # Enter a parse tree produced by MySqlParser#functionArgs.
    def enterFunctionArgs(self, ctx:MySqlParser.FunctionArgsContext):
        pass

    # Exit a parse tree produced by MySqlParser#functionArgs.
    def exitFunctionArgs(self, ctx:MySqlParser.FunctionArgsContext):
        pass


    # Enter a parse tree produced by MySqlParser#functionArg.
    def enterFunctionArg(self, ctx:MySqlParser.FunctionArgContext):
        pass

    # Exit a parse tree produced by MySqlParser#functionArg.
    def exitFunctionArg(self, ctx:MySqlParser.FunctionArgContext):
        pass


    # Enter a parse tree produced by MySqlParser#isExpression.
    def enterIsExpression(self, ctx:MySqlParser.IsExpressionContext):
        pass

    # Exit a parse tree produced by MySqlParser#isExpression.
    def exitIsExpression(self, ctx:MySqlParser.IsExpressionContext):
        pass


    # Enter a parse tree produced by MySqlParser#notExpression.
    def enterNotExpression(self, ctx:MySqlParser.NotExpressionContext):
        pass

    # Exit a parse tree produced by MySqlParser#notExpression.
    def exitNotExpression(self, ctx:MySqlParser.NotExpressionContext):
        pass


    # Enter a parse tree produced by MySqlParser#logicalExpression.
    def enterLogicalExpression(self, ctx:MySqlParser.LogicalExpressionContext):
        pass

    # Exit a parse tree produced by MySqlParser#logicalExpression.
    def exitLogicalExpression(self, ctx:MySqlParser.LogicalExpressionContext):
        pass


    # Enter a parse tree produced by MySqlParser#predicateExpression.
    def enterPredicateExpression(self, ctx:MySqlParser.PredicateExpressionContext):
        pass

    # Exit a parse tree produced by MySqlParser#predicateExpression.
    def exitPredicateExpression(self, ctx:MySqlParser.PredicateExpressionContext):
        pass


    # Enter a parse tree produced by MySqlParser#soundsLikePredicate.
    def enterSoundsLikePredicate(self, ctx:MySqlParser.SoundsLikePredicateContext):
        pass

    # Exit a parse tree produced by MySqlParser#soundsLikePredicate.
    def exitSoundsLikePredicate(self, ctx:MySqlParser.SoundsLikePredicateContext):
        pass


    # Enter a parse tree produced by MySqlParser#expressionAtomPredicate.
    def enterExpressionAtomPredicate(self, ctx:MySqlParser.ExpressionAtomPredicateContext):
        pass

    # Exit a parse tree produced by MySqlParser#expressionAtomPredicate.
    def exitExpressionAtomPredicate(self, ctx:MySqlParser.ExpressionAtomPredicateContext):
        pass


    # Enter a parse tree produced by MySqlParser#subqueryComparisonPredicate.
    def enterSubqueryComparisonPredicate(self, ctx:MySqlParser.SubqueryComparisonPredicateContext):
        pass

    # Exit a parse tree produced by MySqlParser#subqueryComparisonPredicate.
    def exitSubqueryComparisonPredicate(self, ctx:MySqlParser.SubqueryComparisonPredicateContext):
        pass


    # Enter a parse tree produced by MySqlParser#jsonMemberOfPredicate.
    def enterJsonMemberOfPredicate(self, ctx:MySqlParser.JsonMemberOfPredicateContext):
        pass

    # Exit a parse tree produced by MySqlParser#jsonMemberOfPredicate.
    def exitJsonMemberOfPredicate(self, ctx:MySqlParser.JsonMemberOfPredicateContext):
        pass


    # Enter a parse tree produced by MySqlParser#binaryComparisonPredicate.
    def enterBinaryComparisonPredicate(self, ctx:MySqlParser.BinaryComparisonPredicateContext):
        pass

    # Exit a parse tree produced by MySqlParser#binaryComparisonPredicate.
    def exitBinaryComparisonPredicate(self, ctx:MySqlParser.BinaryComparisonPredicateContext):
        pass


    # Enter a parse tree produced by MySqlParser#inPredicate.
    def enterInPredicate(self, ctx:MySqlParser.InPredicateContext):
        pass

    # Exit a parse tree produced by MySqlParser#inPredicate.
    def exitInPredicate(self, ctx:MySqlParser.InPredicateContext):
        pass


    # Enter a parse tree produced by MySqlParser#betweenPredicate.
    def enterBetweenPredicate(self, ctx:MySqlParser.BetweenPredicateContext):
        pass

    # Exit a parse tree produced by MySqlParser#betweenPredicate.
    def exitBetweenPredicate(self, ctx:MySqlParser.BetweenPredicateContext):
        pass


    # Enter a parse tree produced by MySqlParser#isNullPredicate.
    def enterIsNullPredicate(self, ctx:MySqlParser.IsNullPredicateContext):
        pass

    # Exit a parse tree produced by MySqlParser#isNullPredicate.
    def exitIsNullPredicate(self, ctx:MySqlParser.IsNullPredicateContext):
        pass


    # Enter a parse tree produced by MySqlParser#likePredicate.
    def enterLikePredicate(self, ctx:MySqlParser.LikePredicateContext):
        pass

    # Exit a parse tree produced by MySqlParser#likePredicate.
    def exitLikePredicate(self, ctx:MySqlParser.LikePredicateContext):
        pass


    # Enter a parse tree produced by MySqlParser#regexpPredicate.
    def enterRegexpPredicate(self, ctx:MySqlParser.RegexpPredicateContext):
        pass

    # Exit a parse tree produced by MySqlParser#regexpPredicate.
    def exitRegexpPredicate(self, ctx:MySqlParser.RegexpPredicateContext):
        pass


    # Enter a parse tree produced by MySqlParser#unaryExpressionAtom.
    def enterUnaryExpressionAtom(self, ctx:MySqlParser.UnaryExpressionAtomContext):
        pass

    # Exit a parse tree produced by MySqlParser#unaryExpressionAtom.
    def exitUnaryExpressionAtom(self, ctx:MySqlParser.UnaryExpressionAtomContext):
        pass


    # Enter a parse tree produced by MySqlParser#collateExpressionAtom.
    def enterCollateExpressionAtom(self, ctx:MySqlParser.CollateExpressionAtomContext):
        pass

    # Exit a parse tree produced by MySqlParser#collateExpressionAtom.
    def exitCollateExpressionAtom(self, ctx:MySqlParser.CollateExpressionAtomContext):
        pass


    # Enter a parse tree produced by MySqlParser#variableAssignExpressionAtom.
    def enterVariableAssignExpressionAtom(self, ctx:MySqlParser.VariableAssignExpressionAtomContext):
        pass

    # Exit a parse tree produced by MySqlParser#variableAssignExpressionAtom.
    def exitVariableAssignExpressionAtom(self, ctx:MySqlParser.VariableAssignExpressionAtomContext):
        pass


    # Enter a parse tree produced by MySqlParser#mysqlVariableExpressionAtom.
    def enterMysqlVariableExpressionAtom(self, ctx:MySqlParser.MysqlVariableExpressionAtomContext):
        pass

    # Exit a parse tree produced by MySqlParser#mysqlVariableExpressionAtom.
    def exitMysqlVariableExpressionAtom(self, ctx:MySqlParser.MysqlVariableExpressionAtomContext):
        pass


    # Enter a parse tree produced by MySqlParser#nestedExpressionAtom.
    def enterNestedExpressionAtom(self, ctx:MySqlParser.NestedExpressionAtomContext):
        pass

    # Exit a parse tree produced by MySqlParser#nestedExpressionAtom.
    def exitNestedExpressionAtom(self, ctx:MySqlParser.NestedExpressionAtomContext):
        pass


    # Enter a parse tree produced by MySqlParser#nestedRowExpressionAtom.
    def enterNestedRowExpressionAtom(self, ctx:MySqlParser.NestedRowExpressionAtomContext):
        pass

    # Exit a parse tree produced by MySqlParser#nestedRowExpressionAtom.
    def exitNestedRowExpressionAtom(self, ctx:MySqlParser.NestedRowExpressionAtomContext):
        pass


    # Enter a parse tree produced by MySqlParser#mathExpressionAtom.
    def enterMathExpressionAtom(self, ctx:MySqlParser.MathExpressionAtomContext):
        pass

    # Exit a parse tree produced by MySqlParser#mathExpressionAtom.
    def exitMathExpressionAtom(self, ctx:MySqlParser.MathExpressionAtomContext):
        pass


    # Enter a parse tree produced by MySqlParser#existsExpressionAtom.
    def enterExistsExpressionAtom(self, ctx:MySqlParser.ExistsExpressionAtomContext):
        pass

    # Exit a parse tree produced by MySqlParser#existsExpressionAtom.
    def exitExistsExpressionAtom(self, ctx:MySqlParser.ExistsExpressionAtomContext):
        pass


    # Enter a parse tree produced by MySqlParser#intervalExpressionAtom.
    def enterIntervalExpressionAtom(self, ctx:MySqlParser.IntervalExpressionAtomContext):
        pass

    # Exit a parse tree produced by MySqlParser#intervalExpressionAtom.
    def exitIntervalExpressionAtom(self, ctx:MySqlParser.IntervalExpressionAtomContext):
        pass


    # Enter a parse tree produced by MySqlParser#jsonExpressionAtom.
    def enterJsonExpressionAtom(self, ctx:MySqlParser.JsonExpressionAtomContext):
        pass

    # Exit a parse tree produced by MySqlParser#jsonExpressionAtom.
    def exitJsonExpressionAtom(self, ctx:MySqlParser.JsonExpressionAtomContext):
        pass


    # Enter a parse tree produced by MySqlParser#subqueryExpressionAtom.
    def enterSubqueryExpressionAtom(self, ctx:MySqlParser.SubqueryExpressionAtomContext):
        pass

    # Exit a parse tree produced by MySqlParser#subqueryExpressionAtom.
    def exitSubqueryExpressionAtom(self, ctx:MySqlParser.SubqueryExpressionAtomContext):
        pass


    # Enter a parse tree produced by MySqlParser#constantExpressionAtom.
    def enterConstantExpressionAtom(self, ctx:MySqlParser.ConstantExpressionAtomContext):
        pass

    # Exit a parse tree produced by MySqlParser#constantExpressionAtom.
    def exitConstantExpressionAtom(self, ctx:MySqlParser.ConstantExpressionAtomContext):
        pass


    # Enter a parse tree produced by MySqlParser#functionCallExpressionAtom.
    def enterFunctionCallExpressionAtom(self, ctx:MySqlParser.FunctionCallExpressionAtomContext):
        pass

    # Exit a parse tree produced by MySqlParser#functionCallExpressionAtom.
    def exitFunctionCallExpressionAtom(self, ctx:MySqlParser.FunctionCallExpressionAtomContext):
        pass


    # Enter a parse tree produced by MySqlParser#binaryExpressionAtom.
    def enterBinaryExpressionAtom(self, ctx:MySqlParser.BinaryExpressionAtomContext):
        pass

    # Exit a parse tree produced by MySqlParser#binaryExpressionAtom.
    def exitBinaryExpressionAtom(self, ctx:MySqlParser.BinaryExpressionAtomContext):
        pass


    # Enter a parse tree produced by MySqlParser#fullColumnNameExpressionAtom.
    def enterFullColumnNameExpressionAtom(self, ctx:MySqlParser.FullColumnNameExpressionAtomContext):
        pass

    # Exit a parse tree produced by MySqlParser#fullColumnNameExpressionAtom.
    def exitFullColumnNameExpressionAtom(self, ctx:MySqlParser.FullColumnNameExpressionAtomContext):
        pass


    # Enter a parse tree produced by MySqlParser#bitExpressionAtom.
    def enterBitExpressionAtom(self, ctx:MySqlParser.BitExpressionAtomContext):
        pass

    # Exit a parse tree produced by MySqlParser#bitExpressionAtom.
    def exitBitExpressionAtom(self, ctx:MySqlParser.BitExpressionAtomContext):
        pass


    # Enter a parse tree produced by MySqlParser#unaryOperator.
    def enterUnaryOperator(self, ctx:MySqlParser.UnaryOperatorContext):
        pass

    # Exit a parse tree produced by MySqlParser#unaryOperator.
    def exitUnaryOperator(self, ctx:MySqlParser.UnaryOperatorContext):
        pass


    # Enter a parse tree produced by MySqlParser#comparisonOperator.
    def enterComparisonOperator(self, ctx:MySqlParser.ComparisonOperatorContext):
        pass

    # Exit a parse tree produced by MySqlParser#comparisonOperator.
    def exitComparisonOperator(self, ctx:MySqlParser.ComparisonOperatorContext):
        pass


    # Enter a parse tree produced by MySqlParser#logicalOperator.
    def enterLogicalOperator(self, ctx:MySqlParser.LogicalOperatorContext):
        pass

    # Exit a parse tree produced by MySqlParser#logicalOperator.
    def exitLogicalOperator(self, ctx:MySqlParser.LogicalOperatorContext):
        pass


    # Enter a parse tree produced by MySqlParser#bitOperator.
    def enterBitOperator(self, ctx:MySqlParser.BitOperatorContext):
        pass

    # Exit a parse tree produced by MySqlParser#bitOperator.
    def exitBitOperator(self, ctx:MySqlParser.BitOperatorContext):
        pass


    # Enter a parse tree produced by MySqlParser#mathOperator.
    def enterMathOperator(self, ctx:MySqlParser.MathOperatorContext):
        pass

    # Exit a parse tree produced by MySqlParser#mathOperator.
    def exitMathOperator(self, ctx:MySqlParser.MathOperatorContext):
        pass


    # Enter a parse tree produced by MySqlParser#jsonOperator.
    def enterJsonOperator(self, ctx:MySqlParser.JsonOperatorContext):
        pass

    # Exit a parse tree produced by MySqlParser#jsonOperator.
    def exitJsonOperator(self, ctx:MySqlParser.JsonOperatorContext):
        pass


    # Enter a parse tree produced by MySqlParser#charsetNameBase.
    def enterCharsetNameBase(self, ctx:MySqlParser.CharsetNameBaseContext):
        pass

    # Exit a parse tree produced by MySqlParser#charsetNameBase.
    def exitCharsetNameBase(self, ctx:MySqlParser.CharsetNameBaseContext):
        pass


    # Enter a parse tree produced by MySqlParser#transactionLevelBase.
    def enterTransactionLevelBase(self, ctx:MySqlParser.TransactionLevelBaseContext):
        pass

    # Exit a parse tree produced by MySqlParser#transactionLevelBase.
    def exitTransactionLevelBase(self, ctx:MySqlParser.TransactionLevelBaseContext):
        pass


    # Enter a parse tree produced by MySqlParser#privilegesBase.
    def enterPrivilegesBase(self, ctx:MySqlParser.PrivilegesBaseContext):
        pass

    # Exit a parse tree produced by MySqlParser#privilegesBase.
    def exitPrivilegesBase(self, ctx:MySqlParser.PrivilegesBaseContext):
        pass


    # Enter a parse tree produced by MySqlParser#intervalTypeBase.
    def enterIntervalTypeBase(self, ctx:MySqlParser.IntervalTypeBaseContext):
        pass

    # Exit a parse tree produced by MySqlParser#intervalTypeBase.
    def exitIntervalTypeBase(self, ctx:MySqlParser.IntervalTypeBaseContext):
        pass


    # Enter a parse tree produced by MySqlParser#dataTypeBase.
    def enterDataTypeBase(self, ctx:MySqlParser.DataTypeBaseContext):
        pass

    # Exit a parse tree produced by MySqlParser#dataTypeBase.
    def exitDataTypeBase(self, ctx:MySqlParser.DataTypeBaseContext):
        pass


    # Enter a parse tree produced by MySqlParser#keywordsCanBeId.
    def enterKeywordsCanBeId(self, ctx:MySqlParser.KeywordsCanBeIdContext):
        pass

    # Exit a parse tree produced by MySqlParser#keywordsCanBeId.
    def exitKeywordsCanBeId(self, ctx:MySqlParser.KeywordsCanBeIdContext):
        pass


    # Enter a parse tree produced by MySqlParser#functionNameBase.
    def enterFunctionNameBase(self, ctx:MySqlParser.FunctionNameBaseContext):
        pass

    # Exit a parse tree produced by MySqlParser#functionNameBase.
    def exitFunctionNameBase(self, ctx:MySqlParser.FunctionNameBaseContext):
        pass



del MySqlParser